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
    ImplotFunc('ImPlot_PlotImage', 'plot_image'),

    # Utils
    ImplotFunc('ImPlot_SetAxis', 'set_axis'),
    ImplotFunc('ImPlot_SetAxes', 'set_axes'),
    ImplotFunc('ImPlot_PixelsToPlot_Vec2', 'pixels_to_plot'),
    ImplotFunc('ImPlot_PixelsToPlot_Float', 'pixels_to_plot'),
    ImplotFunc('ImPlot_PlotToPixels_PlotPoInt', 'plot_to_pixels'),
    ImplotFunc('ImPlot_PlotToPixels_double', 'plot_to_pixels'),

    ImplotFunc('ImPlot_GetPlotPos', 'get_plot_pos'),
    ImplotFunc('ImPlot_GetPlotSize', 'get_plot_size'),
    ImplotFunc('ImPlot_GetPlotMousePos', 'get_plot_mouse_pos'),
    #ImplotFunc('ImPlot_GetPlotLimits', 'get_plot_limits'), <- TODO implotrect type
    ImplotFunc('ImPlot_IsPlotHovered', 'is_plot_hovered'),
    ImplotFunc('ImPlot_IsAxisHovered', 'is_axis_hovered'),
    ImplotFunc('ImPlot_IsSubplotsHovered', 'is_subplots_hovered'),
    ImplotFunc('ImPlot_IsPlotSelected', 'is_plot_selected'),
    #ImplotFunc('ImPlot_GetPlotSelection', 'get_plot_selection'), <- TODO implotrect type
    ImplotFunc('ImPlot_CancelPlotSelection', 'cancel_plot_selection'),
    ImplotFunc('ImPlot_HideNextItem', 'hide_next_item'),
    ImplotFunc('ImPlot_BeginAlignedPlots', 'begin_aligned_plots'),
    ImplotFunc('ImPlot_EndAlignedPlots', 'end_aligned_plots'),

    # [SECTION] Legend Utils
    ImplotFunc('ImPlot_BeginLegendPopup', 'begin_legend_popup'),
    ImplotFunc('ImPlot_EndLegendPopup', 'end_legend_popup'),
    ImplotFunc('ImPlot_IsLegendEntryHovered', 'is_legend_entry_hovered'),

    # [SECTION] Drag and Drop
    ImplotFunc('ImPlot_BeginDragDropTargetPlot', 'begin_drag_drop_target_plot'),
    ImplotFunc('ImPlot_BeginDragDropTargetAxis', 'begin_drag_drop_target_axis'),
    ImplotFunc('ImPlot_BeginDragDropTargetLegend', 'begin_drag_drop_target_legend'),
    ImplotFunc('ImPlot_EndDragDropTarget', 'end_drag_drop_target'),
    ImplotFunc('ImPlot_BeginDragDropSourcePlot', 'begin_drag_drop_source_plot'),
    ImplotFunc('ImPlot_BeginDragDropSourceAxis', 'begin_drag_drop_source_axis'),
    ImplotFunc('ImPlot_BeginDragDropSourceItem', 'begin_drag_drop_source_item'),
    ImplotFunc('ImPlot_EndDragDropSource', 'end_drag_drop_source'),

    # Styles
    ImplotFunc('ImPlot_StyleColorsAuto', 'style_colors_auto'),
    ImplotFunc('ImPlot_StyleColorsClassic', 'style_colors_classic'),
    ImplotFunc('ImPlot_StyleColorsDark', 'style_colors_dark'),
    ImplotFunc('ImPlot_StyleColorsLight', 'style_colors_light'),

    ImplotFunc('ImPlot_PushStyleColor_U32', 'push_style_color'),
    ImplotFunc('ImPlot_PushStyleColor_Vec4', 'push_style_color'),
    ImplotFunc('ImPlot_PopStyleColor', 'pop_style_color'),

    ImplotFunc('ImPlot_PushStyleVar_Float', 'push_style_var'),
    ImplotFunc('ImPlot_PushStyleVar_Int', 'push_style_var'),
    ImplotFunc('ImPlot_PushStyleVar_Vec2', 'push_style_var'),
    ImplotFunc('ImPlot_PopStyleVar', 'pop_style_var'),

    ImplotFunc('ImPlot_SetNextLineStyle', 'set_next_line_style'),
    ImplotFunc('ImPlot_SetNextFillStyle', 'set_next_fill_style'),
    ImplotFunc('ImPlot_SetNextMarkerStyle', 'set_next_marker_style'),
    ImplotFunc('ImPlot_SetNextErrorBarStyle', 'set_next_error_bar_style'),

    ImplotFunc('ImPlot_GetLastItemColor', 'get_last_item_color'),
    ImplotFunc('ImPlot_GetStyleColorName', 'get_style_color_name'),
    ImplotFunc('ImPlot_GetMarkerName', 'get_marker_name'),

    # PROTO SECTION
    ImplotFunc('ImPlot_GetColormapCount', 'get_colormap_count'),
    ImplotFunc('ImPlot_GetColormapName', 'get_colormap_name'),
    ImplotFunc('ImPlot_GetColormapIndex', 'get_colormap_index'),

    ImplotFunc('ImPlot_PushColormap_PlotColormap', 'push_colormap'),
    ImplotFunc('ImPlot_PushColormap_Str', 'push_colormap'),
    ImplotFunc('ImPlot_PopColormap', 'pop_colormap'),

    ImplotFunc('ImPlot_NextColormapColor', 'next_colormap_color'),
    ImplotFunc('ImPlot_GetColormapSize', 'get_colormap_size'),
    ImplotFunc('ImPlot_GetColormapColor', 'get_colormap_color'),
    ImplotFunc('ImPlot_SampleColormap', 'sample_colormap'),
    ImplotFunc('ImPlot_ColormapScale', 'colormap_scale'),

    # ImplotFunc('ImPlot_ColormapSlider', 'colormap_slider'), <-- TODO do manually, needs to return tuple[bool, tuple[float, float..]
    ImplotFunc('ImPlot_ColormapButton', 'colormap_button'),
    ImplotFunc('ImPlot_BustColorCache', 'bust_color_cache'),

    # [SECTION] Input Mapping
    # GetInputMap <- implemented in C++ side
    ImplotFunc('ImPlot_MapInputDefault', 'map_input_default'),
    ImplotFunc('ImPlot_MapInputReverse', 'map_input_reverse'),

    # [SECTION] Miscellaneous
    # IMPLOT_API ImDrawList* GetPlotDrawList(); <-- implemented manually due to references
    ImplotFunc('ImPlot_ItemIcon_Vec4', 'item_icon'),
    ImplotFunc('ImPlot_ItemIcon_U32', 'item_icon'),
    ImplotFunc('ImPlot_ColormapIcon', 'colormap_icon'),

    ImplotFunc('ImPlot_PushPlotClipRect', 'push_plot_clip_rect'),
    ImplotFunc('ImPlot_PopPlotClipRect', 'pop_plot_clip_rect'),

    ImplotFunc('ImPlot_ShowStyleSelector', 'show_style_selector'),
    ImplotFunc('ImPlot_ShowColormapSelector', 'show_colormap_selector'),
    ImplotFunc('ImPlot_ShowInputMapSelector', 'show_input_map_selector'),
    ImplotFunc('ImPlot_ShowStyleEditor', 'show_style_editor'),
    ImplotFunc('ImPlot_ShowUserGuide', 'show_user_guide'),
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
        if self.cpp_type.startswith('std::optional<'):
            return f'{self.name} ? {self.name}.value() : nullptr'
        if 'std::variant<' in self.cpp_type:
            return f'variant_to_int({self.name})' # Note: variant_to_int defined in the file that includes the funcs inl file
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
                    # Revert cimplot "return value to pOut" transform back to original struct return type.
                    fn_def = ov
                    args = fn_def["argsT"]
                    if len(args) > 0 and args[0]['name'] == 'pOut' and args[0]['type'].endswith('*'):
                        fn_def['ret'] = args[0]['type']
                        fn_def['argsT'] = args[1:]

        known_enums = dict(gen_utils.enum_list_implot + gen_utils.enum_list_imgui)

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
                            if default == 'nullptr':
                                args['cpp_type'] = 'std::optional<const char*>'
                                args['py_type'] = 'str | None'
                                args['cpp_default'] = 'nb::none()'
                                args['py_default'] = 'None'
                            else:
                                args['cpp_default'] = default
                                args['py_default'] = default.replace('"', "'")
                        else:
                            if arg_flags & ArgFlags.OPTIONAL:
                                args['cpp_type'] = 'std::optional<const char*>'
                                args['py_type'] = 'str | None'
                        out_args.append(FuncArg(**args))
                    case 'const char* const[]':
                        assert default == 'nullptr'
                        assert False
                        logging.warning('unimplemented const char* const[]')
                        out_args.append(FuncArg(arg_name, cpp_type='const char* const[]', py_type='list[str]'))
                    case ptrtype if ptrtype in {'ImPlotStyle*', 'ImPlotInputMap*'}:
                        pname = { 'ImPlotStyle*': 'Style', 'ImPlotInputMap*': 'InputMap' }[ptrtype]
                        args = { 'name': arg_name, 'cpp_type': ptrtype, 'py_type': pname }
                        if default is not None:
                            assert default == 'nullptr'
                            args['cpp_default'] = 'nb::none()'
                            args['py_default'] = 'None'
                        out_args.append(FuncArg(**args))
                    case 'const ImVec2':
                        if default is not None:
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec2', py_type='tuple[float, float]', cpp_default=default, py_default=default.replace('ImVec2', '')))
                        else:
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec2', py_type='tuple[float, float]'))
                    case 'const ImPlotPoint':
                        if default is not None:
                            out_args.append(FuncArg(arg_name, cpp_type='ImPlotPoint', py_type='tuple[float, float]', cpp_default=default, py_default=default.replace('ImPlotPoint', '')))
                        else:
                            out_args.append(FuncArg(arg_name, cpp_type='ImPlotPoint', py_type='tuple[float, float]'))
                    case 'const ImVec4':
                        if default is not None:
                            py_default = default.replace('ImVec4', '')
                            if py_default == '(0,0,0,-1)':
                                py_default = 'AUTO_COL'
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec4', py_type='tuple[float, float, float, float]', cpp_default=default, py_default=py_default))
                        else:
                            out_args.append(FuncArg(arg_name, cpp_type='ImVec4', py_type='tuple[float, float, float, float]'))
                    case 'float':
                        args = { 'name': arg_name, 'cpp_type': 'float', 'py_type': 'float' }
                        if default is not None:
                            args['cpp_default'] = default
                            py_default = default.replace('.f', '')
                            if py_default == '-1':
                                py_default = 'AUTO'
                            args['py_default'] = py_default
                        out_args.append(FuncArg(**args))
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
                    case 'ImU32':
                        args = { 'name': arg_name, 'cpp_type': 'ImU32', 'py_type': 'int' }
                        args['cpp_default'] = default
                        args['py_default'] = default
                        out_args.append(FuncArg(**args))
                    case 'ImTextureID':
                        args = { 'name': arg_name, 'cpp_type': 'ImTextureID', 'py_type': 'int' }
                        assert default is None
                        out_args.append(FuncArg(**args))
                    case 'bool':
                        args = { 'name': arg_name, 'cpp_type': 'bool', 'py_type': 'bool' }
                        args['cpp_default'] = default
                        args['py_default'] = default.capitalize()
                        out_args.append(FuncArg(**args))
                    case maybe_enum if f'{maybe_enum}_' in known_enums:
                        enum_cpp_type = f'{maybe_enum}_'
                        enum_py_type = known_enums[enum_cpp_type]
                        enum_mod_prefix = ''
                        if 'ImGui' in enum_cpp_type:
                            enum_mod_prefix = 'slimgui_ext.imgui.'
                        py_default = None
                        cpp_default = None
                        if default is not None:
                            if default == '0':
                                py_default = f'{enum_py_type}.NONE'
                                cpp_default = f'{enum_cpp_type}None'
                            elif default in ['-1', 'IMPLOT_AUTO']:
                                py_default = 'AUTO'
                                cpp_default = f'std::variant<{enum_cpp_type}, int>(IMPLOT_AUTO)'
                                enum_cpp_type = f'std::variant<{enum_cpp_type}, int>'
                            elif default.startswith(enum_cpp_type):
                                py_default = gen_utils.translate_enum_name(default)
                                cpp_default = default
                            elif default == '1' and enum_cpp_type.startswith('ImGuiMouseButton'):
                                py_default = f'{enum_py_type}.RIGHT'
                                cpp_default = f'{enum_cpp_type}Right'
                            else:
                                assert False, 'unknown default'
                        if py_default is not None:
                            py_default = enum_mod_prefix + py_default
                        out_args.append(FuncArg(arg_name, cpp_type=enum_cpp_type, py_type=enum_py_type, cpp_default=cpp_default, py_default=py_default))
                    case _:
                        print(f"{f.cim_ov_name}: {a['type']}")
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
