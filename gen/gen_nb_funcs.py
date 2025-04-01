from dataclasses import dataclass, field
from enum import IntFlag
import io
import json
import os
import subprocess
from typing import Any
import click
import logging

import gen_utils

class ArgFlags(IntFlag):
    NONE = 0
    OPTIONAL = 1 << 0

@dataclass
class ImplotFunc:
    cim_ov_name: str
    py_name: str
    arg_flags: dict[str, ArgFlags] = field(default_factory=dict)

# Note: using cimplot C names
_implot_func_list: list[ImplotFunc] = [
    ImplotFunc('ImPlot_BeginPlot', 'begin_plot'),
    ImplotFunc('ImPlot_EndPlot', 'end_plot'),

    # BeginSubplots
    # EndSubplots
    ImplotFunc('ImPlot_SetupAxis', 'setup_axis'),
    ImplotFunc('ImPlot_SetupAxisLimits', 'setup_axis_limits'),
    ImplotFunc('ImPlot_SetupAxisFormat_Str', 'setup_axis_format'),
    # ImPlot_SetupAxisFormat_PlotFormatter <- not needed?
    # ImPlot_SetupAxisTicks_doublePtr - done, implemented by hand
    # ImPlot_SetupAxisTicks_double    - done, implemented by hand

    ImplotFunc('ImPlot_SetupAxisScale_PlotScale', 'setup_axis_scale'),
    # ('ImPlot_SetupAxisScale_PlotTransform', 'setup_axis_scale'), <- needs callback support
    ImplotFunc('ImPlot_SetupAxisLimitsConstraints', 'setup_axis_limits_constraints'),
    ImplotFunc('ImPlot_SetupAxisZoomConstraints', 'setup_axis_zoom_constraints'),

    ImplotFunc('ImPlot_SetupAxes', 'setup_axes', arg_flags={ 'x_label': ArgFlags.OPTIONAL, 'y_label': ArgFlags.OPTIONAL }),
    ImplotFunc('ImPlot_SetupAxesLimits', 'setup_axes_limits'),

    ImplotFunc('ImPlot_SetupLegend', 'setup_legend'),
    ImplotFunc('ImPlot_SetupMouseText', 'setup_mouse_text'),

    ImplotFunc('ImPlot_SetupFinish', 'setup_finish'),

    ImplotFunc('ImPlot_SetNextAxisLimits', 'set_next_axis_limits'),
    # IMPLOT_API void SetNextAxisLinks(ImAxis axis, double* link_min, double* link_max); <- weird pointer api for python
    ImplotFunc('ImPlot_SetNextAxisToFit', 'set_next_axis_to_fit'),
    ImplotFunc('ImPlot_SetNextAxesLimits', 'set_next_axes_limits'),
    ImplotFunc('ImPlot_SetNextAxesToFit', 'set_next_axes_to_fit'),

    ImplotFunc('ImPlot_PlotText', 'plot_text'),
    ImplotFunc('ImPlot_PlotDummy', 'plot_dummy'),

    # PROTO SECTION
    ImplotFunc('ImPlot_GetColormapSize', 'get_colormap_size'),
]

@dataclass
class FuncArg:
    name: str
    cpp_type: str
    py_type: str
    cpp_default: str | None = None
    py_default: str | None = None
    flags: ArgFlags = ArgFlags.NONE

    def unwrap_cpp_arg_value(self) -> str:
        if self.cpp_type == 'std::optional<const char*>':
            return f'{self.name} ? {self.name}.value() : nullptr'
        if 'std::variant<' in self.cpp_type:
            return f'std::get<int>({self.name})'
        return self.name

class GenContext:
    def __init__(self, cimgui_defs_dir: str, func_list: list[ImplotFunc]):
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
            fn_def = defs[f.cim_ov_name]
            logging.info(f'==== {f.cim_ov_name} ====')
            out_args: list[FuncArg] = []
            for a in fn_def["argsT"]:
                arg_name = a['name']
                arg_flags = f.arg_flags.get(arg_name, ArgFlags.NONE)
                if arg_flags & ArgFlags.OPTIONAL:
                    assert arg_name not in fn_def['defaults'], "OPTIONAL is only used for args that can take a nullptr, but don\'t have a default"
                default = fn_def['defaults'].get(arg_name)
                #  # IMPLOT_API ImVec2 PlotToPixels(double x, double y, ImAxis x_axis = IMPLOT_AUTO, ImAxis y_axis = IMPLOT_AUTO);
                match a['type']:
                    case 'const char*':
                        args = { 'name': arg_name, 'cpp_type': 'const char*', 'py_type': 'str', 'flags': arg_flags }
                        if default is not None:
                            assert default == 'nullptr'
                            args['cpp_type'] = 'std::optional<const char*>'
                            args['py_type'] = 'str | None'
                            args['cpp_default'] = 'nb::none()'
                            args['py_default'] = 'None'
                        else:
                            args['cpp_type'] = 'const char*'
                            args['py_type'] = 'str'
                            if arg_flags & ArgFlags.OPTIONAL:
                                args['cpp_type'] = 'std::optional<const char*>'
                                args['py_type'] = 'str | None'
                        out_args.append(FuncArg(**args))
                    case 'const char* const[]':
                        assert default == 'nullptr'
                        assert False
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
            self.write(f'm.def("{f.py_name}", [](')
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
                    arg_str = f'"{arg.name}"_a'
                    if arg.flags & ArgFlags.OPTIONAL:
                        arg_str += '.none()'
                    self.write(arg_str)
            self.write(');\n')


@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir: str):
    logging.basicConfig(level=logging.INFO)
    ctx = GenContext(cimgui_defs_dir, _implot_func_list)
    ctx.generate_funcs()
    print(ctx.source())


if __name__ == "__main__":
    main()
