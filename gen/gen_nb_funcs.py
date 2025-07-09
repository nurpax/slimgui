from dataclasses import dataclass, field
from enum import IntFlag
import inspect
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
    docstring: str | None = None

# Note: using cimplot C names
_implot_func_list: list[ImplotFunc] = [
    ImplotFunc('ImPlot_BeginPlot', 'begin_plot', docstring='''Starts a 2D plotting context. If this function returns `True`, `implot.end_plot()` MUST
be called! You are encouraged to use the following convention:

```
if implot.begin_plot(...):
    implot.plot_line(...)
    ...
    implot.end_plot()
```

Important notes:

- `title_id` must be unique to the current ImGui ID scope. If you need to avoid ID
  collisions or don't want to display a title in the plot, use double hashes
  (e.g. `"MyPlot##HiddenIdText"` or `"##NoTitle"`).

- `size` is the **frame** size of the plot widget, not the plot area. The default
  size of plots (i.e. when `(0,0)`) can be modified in your `implot.Style`.
'''),
    ImplotFunc('ImPlot_EndPlot', 'end_plot', docstring='Only call `implot.end_plot()` if `implot.begin_plot()` returns `True`! Typically called at the end of an if statement conditioned on `implot.begin_plot()`. See example above.'),

    # BeginSubplots
    # EndSubplots
    ImplotFunc('ImPlot_SetupAxis', 'setup_axis', docstring='Enables an axis or sets the label and/or flags for an existing axis. Leave `label=None` for no label.'),
    ImplotFunc('ImPlot_SetupAxisLimits', 'setup_axis_limits', docstring='Sets an axis range limits. If `Cond.ALWAYS` is used, the axes limits will be locked. Inversion with `v_min > v_max` is not supported; use `implot.setup_axis_limits` instead.'),
    ImplotFunc('ImPlot_SetupAxisFormat_Str', 'setup_axis_format', docstring='Sets the format of numeric axis labels via formater specifier (default="%g"). Formated values will be double (i.e. use %f).  Note that the format string is specified in C printf syntax!'),
    # ImPlot_SetupAxisFormat_PlotFormatter <- not needed?
    # ImPlot_SetupAxisTicks_doublePtr - done, implemented by hand
    # ImPlot_SetupAxisTicks_double    - done, implemented by hand

    ImplotFunc('ImPlot_SetupAxisScale_PlotScale', 'setup_axis_scale', docstring='Sets an axis\' scale using built-in options.'),
    # ('ImPlot_SetupAxisScale_PlotTransform', 'setup_axis_scale'), <- needs callback support
    ImplotFunc('ImPlot_SetupAxisLimitsConstraints', 'setup_axis_limits_constraints', docstring="Sets an axis' limits constraints."),
    ImplotFunc('ImPlot_SetupAxisZoomConstraints', 'setup_axis_zoom_constraints', docstring="Sets an axis' zoom constraints."),

    ImplotFunc('ImPlot_SetupAxes', 'setup_axes', arg_flags={ 'x_label': ArgFlags.OPTIONAL, 'y_label': ArgFlags.OPTIONAL },
               docstring="Sets the label and/or flags for primary X and Y axes (shorthand for two calls to `implot.setup_Axis()`)."),
    ImplotFunc('ImPlot_SetupAxesLimits', 'setup_axes_limits',
               docstring="Sets the primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`)."),

    ImplotFunc('ImPlot_SetupLegend', 'setup_legend',
               docstring="Sets up the plot legend. This can also be called immediately after `implot.begin_subplots()` when using `SubplotFlags.SHARE_ITEMS`."),
    ImplotFunc('ImPlot_SetupMouseText', 'setup_mouse_text',
               docstring="Set the location of the current plot's mouse position text (default = South|East)."),

    ImplotFunc('ImPlot_SetupFinish', 'setup_finish',
               docstring='''Explicitly finalize plot setup. Once you call this, you cannot make anymore Setup calls for the current plot!

               Note that calling this function is OPTIONAL; it will be called by the first subsequent setup-locking API call.'''),

    ImplotFunc('ImPlot_SetNextAxisLimits', 'set_next_axis_limits',
               docstring="Sets an upcoming axis range limits. If ImPlotCond_Always is used, the axes limits will be locked."),
    # IMPLOT_API void SetNextAxisLinks(ImAxis axis, double* link_min, double* link_max); <- weird pointer api for python
    ImplotFunc('ImPlot_SetNextAxisToFit', 'set_next_axis_to_fit',
               docstring="Set an upcoming axis to auto fit to its data."),
    ImplotFunc('ImPlot_SetNextAxesLimits', 'set_next_axes_limits',
               docstring="Sets the upcoming primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`)."),
    ImplotFunc('ImPlot_SetNextAxesToFit', 'set_next_axes_to_fit',
               docstring="Sets all upcoming axes to auto fit to their data."),

    ImplotFunc('ImPlot_PlotText', 'plot_text',
               docstring="Plots a centered text label at point x,y with an optional pixel offset. Text color can be changed with `implot.push_style_color(Col.INLAY_TEXT, ...)`."),
    ImplotFunc('ImPlot_PlotDummy', 'plot_dummy',
               docstring="Plots a dummy item (i.e. adds a legend entry colored by `Col.LINE`)."),
    ImplotFunc('ImPlot_PlotImage', 'plot_image',
               docstring="Plots an axis-aligned image. `bounds_min`/`bounds_max` are in plot coordinates (y-up) and `uv0`/`uv1` are in texture coordinates (y-down)."),

    # Utils
    ImplotFunc('ImPlot_SetAxis', 'set_axis', docstring="Select which axis/axes will be used for subsequent plot elements."),
    ImplotFunc('ImPlot_SetAxes', 'set_axes', docstring="Select which axis/axes will be used for subsequent plot elements."),
    ImplotFunc('ImPlot_PixelsToPlot_Vec2', 'pixels_to_plot', docstring="Convert pixels to a position in the current plot's coordinate system. Passing `implot.AUTO` uses the current axes."),
    ImplotFunc('ImPlot_PixelsToPlot_Float', 'pixels_to_plot', docstring="Convert pixels to a position in the current plot's coordinate system. Passing `implot.AUTO` uses the current axes."),
    ImplotFunc('ImPlot_PlotToPixels_PlotPoInt', 'plot_to_pixels', docstring="Convert a position in the current plot's coordinate system to pixels. Passing `implot.AUTO` uses the current axes."),
    ImplotFunc('ImPlot_PlotToPixels_double', 'plot_to_pixels', docstring="Convert a position in the current plot's coordinate system to pixels. Passing `implot.AUTO` uses the current axes."),

    ImplotFunc('ImPlot_GetPlotPos', 'get_plot_pos', docstring="Get the current Plot position (top-left) in pixels."),
    ImplotFunc('ImPlot_GetPlotSize', 'get_plot_size', docstring="Get the curent Plot size in pixels."),
    ImplotFunc('ImPlot_GetPlotMousePos', 'get_plot_mouse_pos', docstring="Returns the mouse position in x,y coordinates of the current plot. Passing `implot.AUTO` uses the current axes."),
    #ImplotFunc('ImPlot_GetPlotLimits', 'get_plot_limits'), <- TODO implotrect type
    ImplotFunc('ImPlot_IsPlotHovered', 'is_plot_hovered', docstring="Returns `True` if the plot area in the current plot is hovered."),
    ImplotFunc('ImPlot_IsAxisHovered', 'is_axis_hovered', docstring="Returns `True` if the axis label area in the current plot is hovered."),
    ImplotFunc('ImPlot_IsSubplotsHovered', 'is_subplots_hovered', docstring="Returns `True` if the bounding frame of a subplot is hovered."),
    ImplotFunc('ImPlot_IsPlotSelected', 'is_plot_selected', docstring="Returns `True` if the current plot is being box selected."),
    #ImplotFunc('ImPlot_GetPlotSelection', 'get_plot_selection'), <- TODO implotrect type
    ImplotFunc('ImPlot_CancelPlotSelection', 'cancel_plot_selection', docstring="Cancels a the current plot box selection."),
    ImplotFunc('ImPlot_HideNextItem', 'hide_next_item', 
               docstring='''Hides or shows the next plot item (i.e. as if it were toggled from the legend).

               Use `Cond.ALWAYS` if you need to forcefully set this every frame.'''),
    ImplotFunc('ImPlot_BeginAlignedPlots', 'begin_aligned_plots',
               docstring='''Align axis padding over multiple plots in a single row or column. `group_id` must
               be unique. If this function returns `True`, `implot.end_aligned_plots()` must be called.'''),
    ImplotFunc('ImPlot_EndAlignedPlots', 'end_aligned_plots', docstring="Only call `implot.end_aligned_plots()` if `implot.begin_aligned_plots()` returns `True`!"),

    # [SECTION] Legend Utils
    ImplotFunc('ImPlot_BeginLegendPopup', 'begin_legend_popup', docstring="Begin a popup for a legend entry."),
    ImplotFunc('ImPlot_EndLegendPopup', 'end_legend_popup', docstring="End a popup for a legend entry."),
    ImplotFunc('ImPlot_IsLegendEntryHovered', 'is_legend_entry_hovered', docstring="Returns `True` if a plot item legend entry is hovered."),

    # [SECTION] Drag and Drop
    ImplotFunc('ImPlot_BeginDragDropTargetPlot', 'begin_drag_drop_target_plot',
               docstring="Turns the current plot's plotting area into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!"),
    ImplotFunc('ImPlot_BeginDragDropTargetAxis', 'begin_drag_drop_target_axis',
               docstring="Turns the current plot's X-axis into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!"),
    ImplotFunc('ImPlot_BeginDragDropTargetLegend', 'begin_drag_drop_target_legend',
               docstring="Turns the current plot's legend into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!"),
    ImplotFunc('ImPlot_EndDragDropTarget', 'end_drag_drop_target', 
               docstring="Ends a drag and drop target (currently just an alias for `imgui.end_drag_drop_target()`)."),
    ImplotFunc('ImPlot_BeginDragDropSourcePlot', 'begin_drag_drop_source_plot',
               docstring="Turns the current plot's plotting area into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!"),
    ImplotFunc('ImPlot_BeginDragDropSourceAxis', 'begin_drag_drop_source_axis',
               docstring="Turns the current plot's X-axis into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!"),
    ImplotFunc('ImPlot_BeginDragDropSourceItem', 'begin_drag_drop_source_item',
               docstring="Turns an item in the current plot's legend into drag and drop source. Don't forget to call `implot.end_drag_drop_source()`!"),
    ImplotFunc('ImPlot_EndDragDropSource', 'end_drag_drop_source',
               docstring="Ends a drag and drop source (currently just an alias for `imgui.end_drag_drop_source()`)."),

    # Styles
    ImplotFunc('ImPlot_StyleColorsAuto', 'style_colors_auto', docstring="Style plot colors for current ImGui style (default)."),
    ImplotFunc('ImPlot_StyleColorsClassic', 'style_colors_classic', docstring="Style plot colors for ImGui \"Classic\"."),
    ImplotFunc('ImPlot_StyleColorsDark', 'style_colors_dark', docstring="Style plot colors for ImGui \"Dark\"."),
    ImplotFunc('ImPlot_StyleColorsLight', 'style_colors_light', docstring="Style plot colors for ImGui \"Light\"."),

    ImplotFunc('ImPlot_PushStyleColor_U32', 'push_style_color', docstring="Temporarily modify a style color. Don't forget to call `implot.pop_style_color()`!"),
    ImplotFunc('ImPlot_PushStyleColor_Vec4', 'push_style_color', docstring="Temporarily modify a style color. Don't forget to call `implot.pop_style_color()`!"),
    ImplotFunc('ImPlot_PopStyleColor', 'pop_style_color', docstring="Undo temporary style color modification(s). Undo multiple pushes at once by increasing count."),

    ImplotFunc('ImPlot_PushStyleVar_Int', 'push_style_var', docstring="Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!"),
    ImplotFunc('ImPlot_PushStyleVar_Float', 'push_style_var', docstring="Temporarily modify a style variable of float type. Don't forget to call `implot.pop_style_var()`!"),
    ImplotFunc('ImPlot_PushStyleVar_Vec2', 'push_style_var',  docstring="Temporarily modify a style variable of float 2-tuple. Don't forget to call `implot.pop_style_var()`!"),
    ImplotFunc('ImPlot_PopStyleVar', 'pop_style_var', docstring="Undo temporary style variable modification(s). Undo multiple pushes at once by increasing count."),

    ImplotFunc('ImPlot_SetNextLineStyle', 'set_next_line_style', docstring="Set the line color and weight for the next item only."),
    ImplotFunc('ImPlot_SetNextFillStyle', 'set_next_fill_style', docstring="Set the fill color for the next item only."),
    ImplotFunc('ImPlot_SetNextMarkerStyle', 'set_next_marker_style', docstring="Set the marker style for the next item only."),
    ImplotFunc('ImPlot_SetNextErrorBarStyle', 'set_next_error_bar_style', docstring="Set the error bar style for the next item only."),

    ImplotFunc('ImPlot_GetLastItemColor', 'get_last_item_color', docstring="Gets the last item primary color (i.e. its legend icon color)"),
    ImplotFunc('ImPlot_GetStyleColorName', 'get_style_color_name', docstring="Returns the string name for an `implot.Col`."),
    ImplotFunc('ImPlot_GetMarkerName', 'get_marker_name', docstring="Returns the string name for an ImPlotMarker."),

    # PROTO SECTION
    ImplotFunc('ImPlot_GetColormapCount', 'get_colormap_count', docstring="Returns the number of available colormaps (i.e. the built-in + user-added count)."),
    ImplotFunc('ImPlot_GetColormapName', 'get_colormap_name', docstring="Returns a string name for a colormap given an index. Returns `None` if index is invalid."),
    ImplotFunc('ImPlot_GetColormapIndex', 'get_colormap_index', docstring="Returns an index number for a colormap given a valid string name. Returns -1 if name is invalid."),

    ImplotFunc('ImPlot_PushColormap_PlotColormap', 'push_colormap', docstring="Temporarily switch to one of the built-in (i.e. ImPlotColormap_XXX) or user-added colormaps (i.e. a return value of `implot.add_colormap()`). Don't forget to call `implot.pop_colormap()`!"),
    ImplotFunc('ImPlot_PushColormap_Str', 'push_colormap', docstring="Push a colormap by string name. Use built-in names such as \"Default\", \"Deep\", \"Jet\", etc. or a string you provided to `implot.add_colormap(). Don't forget to call `implot.pop_colormap()`!"),
    ImplotFunc('ImPlot_PopColormap', 'pop_colormap', docstring="Undo temporary colormap modification(s). Undo multiple pushes at once by increasing count."),

    ImplotFunc('ImPlot_NextColormapColor', 'next_colormap_color',
               docstring='''Returns the next color from the current colormap and advances the colormap for the current plot.

               Can also be used with no return value to skip colors if desired. You need to call this between `implot.begin_plot()`/`implot.end_plot()`!'''),
    ImplotFunc('ImPlot_GetColormapSize', 'get_colormap_size', docstring="Returns the size of a colormap."),
    ImplotFunc('ImPlot_GetColormapColor', 'get_colormap_color', docstring="Returns a color from a colormap given an index >= 0 (modulo will be performed)."),
    ImplotFunc('ImPlot_SampleColormap', 'sample_colormap', docstring="Sample a color from the current colormap given t between 0 and 1."),
    ImplotFunc('ImPlot_ColormapScale', 'colormap_scale', docstring="Shows a vertical color scale with linear spaced ticks using the specified color map. Use double hashes to hide label (e.g. \"##NoLabel\"). If `scale_min > scale_max`, the scale to color mapping will be reversed."),

    # ImplotFunc('ImPlot_ColormapSlider', 'colormap_slider'), <-- TODO do manually, needs to return tuple[bool, tuple[float, float..]
    ImplotFunc('ImPlot_ColormapButton', 'colormap_button', docstring="Shows a button with a colormap gradient brackground."),
    ImplotFunc('ImPlot_BustColorCache', 'bust_color_cache', 
               docstring='''When items in a plot sample their color from a colormap, the color is cached and does not change
               unless explicitly overriden. Therefore, if you change the colormap after the item has already been plotted,
               item colors will NOT update. If you need item colors to resample the new colormap, then use this
               function to bust the cached colors. If #plot_title_id is nullptr, then every item in EVERY existing plot
               will be cache busted. Otherwise only the plot specified by #plot_title_id will be busted. For the
               latter, this function must be called in the same ImGui ID scope that the plot is in. You should rarely if ever
               need this function, but it is available for applications that require runtime colormap swaps (e.g. Heatmaps demo).'''),

    # [SECTION] Input Mapping
    # GetInputMap <- implemented in C++ side
    ImplotFunc('ImPlot_MapInputDefault', 'map_input_default', docstring="Default input mapping: pan = LMB drag, box select = RMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll."),
    ImplotFunc('ImPlot_MapInputReverse', 'map_input_reverse', docstring="Reverse input mapping: pan = RMB drag, box select = LMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll."),

    # [SECTION] Miscellaneous
    # IMPLOT_API ImDrawList* GetPlotDrawList(); <-- implemented manually due to references
    ImplotFunc('ImPlot_ItemIcon_Vec4', 'item_icon', docstring="Render icons similar to those that appear in legends (nifty for data lists)."),
    ImplotFunc('ImPlot_ItemIcon_U32', 'item_icon', docstring="Render icons similar to those that appear in legends (nifty for data lists)."),
    ImplotFunc('ImPlot_ColormapIcon', 'colormap_icon', docstring="Render icons similar to those that appear in legends (nifty for data lists)."),

    ImplotFunc('ImPlot_PushPlotClipRect', 'push_plot_clip_rect', docstring="Push clip rect for rendering to current plot area. The rect can be expanded or contracted by #expand pixels. Call between `implot.begin_plot()`/`implot.end_plot()`."),
    ImplotFunc('ImPlot_PopPlotClipRect', 'pop_plot_clip_rect', docstring="Pop plot clip rect. Call between `implot.begin_plot()`/`implot.end_plot()`."),

    ImplotFunc('ImPlot_ShowStyleSelector', 'show_style_selector', docstring="Shows ImPlot style selector dropdown menu."),
    ImplotFunc('ImPlot_ShowColormapSelector', 'show_colormap_selector', docstring="Shows ImPlot colormap selector dropdown menu."),
    ImplotFunc('ImPlot_ShowInputMapSelector', 'show_input_map_selector', docstring="Shows ImPlot input map selector dropdown menu."),
    ImplotFunc('ImPlot_ShowStyleEditor', 'show_style_editor', docstring="Shows ImPlot style editor block (not a window)."),
    ImplotFunc('ImPlot_ShowUserGuide', 'show_user_guide', docstring="Add basic help/info block for end users (not a window)."),
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
                    case 'ImTextureRef':
                        args = { 'name': arg_name, 'cpp_type': 'ImTextureRef', 'py_type': 'TextureRef' }
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
            if f.docstring is not None:
                doc = inspect.cleandoc(f.docstring)
                doc_str_lines = [f'\"{s.replace('"', '\\"')}\\n\"' for s in doc.split('\n')]
                self.write(f', {'\n'.join(doc_str_lines)});\n')
            else:
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
