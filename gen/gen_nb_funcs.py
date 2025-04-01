from dataclasses import dataclass
import io
import json
import os
import subprocess
import click
import logging

import gen_utils

# Note: using cimplot C names
_implot_func_list = [
    ('ImPlot_BeginPlot', 'begin_plot'),
    ('ImPlot_EndPlot', 'end_plot'),

    # BeginSubplots
    # EndSubplots
    ('ImPlot_SetupAxis', 'setup_axis'),
    ('ImPlot_SetupAxisLimits', 'setup_axis_limits'),
    ('ImPlot_SetupAxisFormat_Str', 'setup_axis_format'),
    # ImPlot_SetupAxisFormat_PlotFormatter <- not needed?
    # ImPlot_SetupAxisTicks_doublePtr <- TODO
    #('ImPlot_SetupAxisTicks_double', 'setup_axis_ticks'), # needs const char* const[]

    ('ImPlot_SetupAxisScale_PlotScale', 'setup_axis_scale'),
    # ('ImPlot_SetupAxisScale_PlotTransform', 'setup_axis_scale'), <- needs callback support
    ('ImPlot_SetupAxisLimitsConstraints', 'setup_axis_limits_constraints'),
    ('ImPlot_SetupAxisZoomConstraints', 'setup_axis_zoom_constraints'),

    ('ImPlot_SetupAxes', 'setup_axes'),
    ('ImPlot_SetupAxesLimits', 'setup_axes_limits'),

    ('ImPlot_SetupLegend', 'setup_legend'),
    ('ImPlot_SetupMouseText', 'setup_mouse_text'),

    ('ImPlot_SetupFinish', 'setup_finish'),

    ('ImPlot_SetNextAxisLimits', 'set_next_axis_limits'),
    # IMPLOT_API void SetNextAxisLinks(ImAxis axis, double* link_min, double* link_max); <- weird pointer api for python
    ('ImPlot_SetNextAxisToFit', 'set_next_axis_to_fit'),
    ('ImPlot_SetNextAxesLimits', 'set_next_axes_limits'),
    ('ImPlot_SetNextAxesToFit', 'set_next_axes_to_fit'),

    ('ImPlot_PlotText', 'plot_text'),
    ('ImPlot_PlotDummy', 'plot_dummy'),

    # PROTO SECTION
    ('ImPlot_GetColormapSize', 'get_colormap_size'),
]

@dataclass
class FuncArg:
    name: str
    cpp_type: str
    py_type: str
    cpp_default: str | None = None
    py_default: str | None = None

    def unwrap_cpp_arg_value(self) -> str:
        if self.cpp_type == 'std::optional<std::string>':
            return f'{self.name} ? {self.name}.value().c_str() : nullptr'
        if 'std::variant<' in self.cpp_type:
            return f'std::get<int>({self.name})'
        return self.name

class GenContext:
    def __init__(self, cimgui_defs_dir: str, func_list: list[tuple[str, str]]):
        self._out = io.StringIO()
        self._defs_dir = cimgui_defs_dir
        self._func_list = func_list

    def write(self, text: str):
        self._out.write(text)

    def source(self, clang_format=True) -> str:
        source_text = self._out.getvalue()
        if not clang_format:
            return source_text
        process = subprocess.Popen(
            ["clang-format"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        formatted_code, errors = process.communicate(input=source_text)
        if process.returncode != 0:
            raise Exception(f"Error formatting code: {errors}")
        return formatted_code

    def generate_funcs(self):
        with open(os.path.join(self._defs_dir, "definitions.json"), "rt", encoding="utf-8") as f:
            defs = {}
            doc = json.load(f)
            for d in doc.values():
                for ov in d:
                    defs[ov['ov_cimguiname']] = ov

        known_enums = dict(gen_utils.enum_list_implot)

        for f in self._func_list:
            func_cim_name, func_py_name = f
            fn_def = defs[func_cim_name]
            logging.info(f'==== {func_cim_name} ====')
            out_args: list[FuncArg] = []
            for a in fn_def["argsT"]:
                arg_name = a['name']
                default = fn_def['defaults'].get(arg_name)
                #  # IMPLOT_API ImVec2 PlotToPixels(double x, double y, ImAxis x_axis = IMPLOT_AUTO, ImAxis y_axis = IMPLOT_AUTO);
                match a['type']:
                    case 'const char*':
                        if default is not None:
                            assert default == 'nullptr'
                            out_args.append(FuncArg(arg_name, cpp_type='std::optional<std::string>', py_type='str | None', cpp_default='nb::none()', py_default='None'))
                        else:
                            out_args.append(FuncArg(arg_name, cpp_type='const char*', py_type='str'))
                    case 'const char* const[]':
                        assert default == 'nullptr'
                        # TODO
                        logging.warning('unimplemented const char* const[]')
                        out_args.append(FuncArg(arg_name, cpp_type='const char* const[]', py_type='list[str]'))
                    case 'const ImVec2':
                        if default is not None:
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec2', py_type='tuple[float, float]', cpp_default=default, py_default=default.replace('ImVec2', '')))
                        else:
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec2', py_type='tuple[float, float]'))
                    case 'double':
                        args = { 'name': arg_name, 'cpp_type': 'double', 'py_type': 'float' }
                        if default is not None:
                            args['cpp_default'] = default
                            args['py_default'] = default.replace('.f', '')
                        out_args.append(FuncArg(**args))
                    case 'int':
                        args = { 'name': arg_name, 'cpp_type': 'int', 'py_type': 'int' }
                        args['cpp_default'] = default
                        args['py_default'] = default
                        out_args.append(FuncArg(**args))
                    case 'bool':
                        args = { 'name': arg_name, 'cpp_type': 'bool', 'py_type': 'bool' }
                        args['cpp_default'] = default
                        args['py_default'] = default.capitalize()
                        out_args.append(FuncArg(**args))
                    case maybe_enum if f'{maybe_enum}_' in known_enums:
                        enum_cpp_type = f'{maybe_enum}_'
                        enum_py_type = known_enums[enum_cpp_type]
                        py_default = None
                        cpp_default = None
                        if default is not None:
                            if default == '0':
                                py_default = f'{enum_py_type}.NONE'
                                cpp_default = f'{enum_cpp_type}None'
                            elif default in ['-1', 'IMPLOT_AUTO']:
                                py_default = 'IMPLOT_AUTO'
                                cpp_default = 'std::variant<ImPlotColormap_, int>(IMPLOT_AUTO)'
                                enum_cpp_type = 'std::variant<ImPlotColormap_, int>'
                            elif default.startswith(enum_cpp_type):
                                py_default = gen_utils.translate_enum_name(default)
                                cpp_default = default
                            else:
                                assert False, 'unknown default'
                        out_args.append(FuncArg(arg_name, cpp_type=enum_cpp_type, py_type=enum_py_type, cpp_default=cpp_default, py_default=py_default))
                    case _:
                        print(a['type'])
                        assert False

            # Start a nanobind def
            self.write(f'm.def("{func_py_name}", [](')
            for i, arg in enumerate(out_args):
                if i > 0:
                    self.write(', ')
                self.write(f'{arg.cpp_type} {arg.name}')
            self.write(') {\n')

            # Generate the API function call inside the lambda wrapper
            func_cpp_name = f'ImPlot::{fn_def["funcname"]}'
            if fn_def['ret'] == 'void':
                self.write(f'    {func_cpp_name}(')
            else:
                self.write(f'    return {func_cpp_name}(')
            for i, arg in enumerate(out_args):
                if i > 0:
                    self.write(', ')
                self.write(f'{arg.unwrap_cpp_arg_value()}')
            self.write(');\n')
            self.write('}')

            # Write the nanobind def arg listing
            if len(out_args) > 0:
                self.write(', ')
            for i, arg in enumerate(out_args):
                if i > 0:
                    self.write(', ')
                if arg.cpp_default is not None:
                    self.write(f'"{arg.name}"_a.sig("{arg.py_default}") = {arg.cpp_default}')
                else:
                    self.write(f'"{arg.name}"_a')
            self.write(');\n')


@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir: str):
    logging.basicConfig(level=logging.INFO)
    enum_list = _implot_func_list
    ctx = GenContext(cimgui_defs_dir, enum_list)
    ctx.generate_funcs()
    print(ctx.source())


if __name__ == "__main__":
    main()
