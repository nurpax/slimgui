m.def(
    "begin_plot",
    [](const char *title_id, ImVec2 size, ImPlotFlags_ flags) {
      return ImPlot::BeginPlot(title_id, size, flags);
    },
    "title_id"_a, "size"_a.sig("(-1,0)") = ImVec2(-1, 0),
    "flags"_a.sig("PlotFlags.NONE") = ImPlotFlags_None,
    "Starts a 2D plotting context. If this function returns `True`, "
    "`implot.end_plot()` MUST\n"
    "be called! You are encouraged to use the following convention:\n"
    "\n"
    "```\n"
    "if implot.begin_plot(...):\n"
    "    implot.plot_line(...)\n"
    "    ...\n"
    "    implot.end_plot()\n"
    "```\n"
    "\n"
    "Important notes:\n"
    "\n"
    "- `title_id` must be unique to the current ImGui ID scope. If you need to "
    "avoid ID\n"
    "  collisions or don't want to display a title in the plot, use double "
    "hashes\n"
    "  (e.g. `\"MyPlot##HiddenIdText\"` or `\"##NoTitle\"`).\n"
    "\n"
    "- `size` is the **frame** size of the plot widget, not the plot area. The "
    "default\n"
    "  size of plots (i.e. when `(0,0)`) can be modified in your "
    "`implot.Style`.\n");
m.def(
    "end_plot", []() { ImPlot::EndPlot(); },
    "Only call `implot.end_plot()` if `implot.begin_plot()` returns `True`! "
    "Typically called at the end of an if statement conditioned on "
    "`implot.begin_plot()`. See example above.\n");
m.def(
    "setup_axis",
    [](ImAxis_ axis, std::optional<const char *> label,
       ImPlotAxisFlags_ flags) {
      ImPlot::SetupAxis(axis, label ? label.value() : nullptr, flags);
    },
    "axis"_a, "label"_a.sig("None") = nb::none(),
    "flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None,
    "Enables an axis or sets the label and/or flags for an existing axis. "
    "Leave `label=None` for no label.\n");
m.def(
    "setup_axis_limits",
    [](ImAxis_ axis, double v_min, double v_max, ImPlotCond_ cond) {
      ImPlot::SetupAxisLimits(axis, v_min, v_max, cond);
    },
    "axis"_a, "v_min"_a, "v_max"_a, "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once,
    "Sets an axis range limits. If `Cond.ALWAYS` is used, the axes limits will "
    "be locked. Inversion with `v_min > v_max` is not supported; use "
    "`implot.setup_axis_limits` instead.\n");
m.def(
    "setup_axis_format",
    [](ImAxis_ axis, const char *fmt) { ImPlot::SetupAxisFormat(axis, fmt); },
    "axis"_a, "fmt"_a,
    "Sets the format of numeric axis labels via formater specifier "
    "(default=\"%g\"). Formated values will be double (i.e. use %f).  Note "
    "that the format string is specified in C printf syntax!\n");
m.def(
    "setup_axis_scale",
    [](ImAxis_ axis, ImPlotScale_ scale) {
      ImPlot::SetupAxisScale(axis, scale);
    },
    "axis"_a, "scale"_a, "Sets an axis' scale using built-in options.\n");
m.def(
    "setup_axis_limits_constraints",
    [](ImAxis_ axis, double v_min, double v_max) {
      ImPlot::SetupAxisLimitsConstraints(axis, v_min, v_max);
    },
    "axis"_a, "v_min"_a, "v_max"_a, "Sets an axis' limits constraints.\n");
m.def(
    "setup_axis_zoom_constraints",
    [](ImAxis_ axis, double z_min, double z_max) {
      ImPlot::SetupAxisZoomConstraints(axis, z_min, z_max);
    },
    "axis"_a, "z_min"_a, "z_max"_a, "Sets an axis' zoom constraints.\n");
m.def(
    "setup_axes",
    [](std::optional<const char *> x_label, std::optional<const char *> y_label,
       ImPlotAxisFlags_ x_flags, ImPlotAxisFlags_ y_flags) {
      ImPlot::SetupAxes(x_label ? x_label.value() : nullptr,
                        y_label ? y_label.value() : nullptr, x_flags, y_flags);
    },
    "x_label"_a.none(), "y_label"_a.none(),
    "x_flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None,
    "y_flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None,
    "Sets the label and/or flags for primary X and Y axes (shorthand for two "
    "calls to `implot.setup_Axis()`).\n");
m.def(
    "setup_axes_limits",
    [](double x_min, double x_max, double y_min, double y_max,
       ImPlotCond_ cond) {
      ImPlot::SetupAxesLimits(x_min, x_max, y_min, y_max, cond);
    },
    "x_min"_a, "x_max"_a, "y_min"_a, "y_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once,
    "Sets the primary X and Y axes range limits. If `Cond.ALWAYS` is used, the "
    "axes limits will be locked (shorthand for two calls to "
    "`implot.setup_axis_limits()`).\n");
m.def(
    "setup_legend",
    [](ImPlotLocation_ location, ImPlotLegendFlags_ flags) {
      ImPlot::SetupLegend(location, flags);
    },
    "location"_a, "flags"_a.sig("LegendFlags.NONE") = ImPlotLegendFlags_None,
    "Sets up the plot legend. This can also be called immediately after "
    "`implot.begin_subplots()` when using `SubplotFlags.SHARE_ITEMS`.\n");
m.def(
    "setup_mouse_text",
    [](ImPlotLocation_ location, ImPlotMouseTextFlags_ flags) {
      ImPlot::SetupMouseText(location, flags);
    },
    "location"_a,
    "flags"_a.sig("MouseTextFlags.NONE") = ImPlotMouseTextFlags_None,
    "Set the location of the current plot's mouse position text (default = "
    "South|East).\n");
m.def(
    "setup_finish", []() { ImPlot::SetupFinish(); },
    "Explicitly finalize plot setup. Once you call this, you cannot make "
    "anymore Setup calls for the current plot!\n"
    "\n"
    "Note that calling this function is OPTIONAL; it will be called by the "
    "first subsequent setup-locking API call.\n");
m.def(
    "set_next_axis_limits",
    [](ImAxis_ axis, double v_min, double v_max, ImPlotCond_ cond) {
      ImPlot::SetNextAxisLimits(axis, v_min, v_max, cond);
    },
    "axis"_a, "v_min"_a, "v_max"_a, "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once,
    "Sets an upcoming axis range limits. If ImPlotCond_Always is used, the "
    "axes limits will be locked.\n");
m.def(
    "set_next_axis_to_fit",
    [](ImAxis_ axis) { ImPlot::SetNextAxisToFit(axis); }, "axis"_a,
    "Set an upcoming axis to auto fit to its data.\n");
m.def(
    "set_next_axes_limits",
    [](double x_min, double x_max, double y_min, double y_max,
       ImPlotCond_ cond) {
      ImPlot::SetNextAxesLimits(x_min, x_max, y_min, y_max, cond);
    },
    "x_min"_a, "x_max"_a, "y_min"_a, "y_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once,
    "Sets the upcoming primary X and Y axes range limits. If `Cond.ALWAYS` is "
    "used, the axes limits will be locked (shorthand for two calls to "
    "`implot.setup_axis_limits()`).\n");
m.def(
    "set_next_axes_to_fit", []() { ImPlot::SetNextAxesToFit(); },
    "Sets all upcoming axes to auto fit to their data.\n");
m.def(
    "plot_text",
    [](const char *text, double x, double y, ImVec2 pix_offset,
       ImPlotTextFlags_ flags) {
      ImPlot::PlotText(text, x, y, pix_offset, flags);
    },
    "text"_a, "x"_a, "y"_a, "pix_offset"_a.sig("(0,0)") = ImVec2(0, 0),
    "flags"_a.sig("TextFlag.NONE") = ImPlotTextFlags_None,
    "Plots a centered text label at point x,y with an optional pixel offset. "
    "Text color can be changed with `implot.push_style_color(Col.INLAY_TEXT, "
    "...)`.\n");
m.def(
    "plot_dummy",
    [](const char *label_id, ImPlotDummyFlags_ flags) {
      ImPlot::PlotDummy(label_id, flags);
    },
    "label_id"_a, "flags"_a.sig("DummyFlag.NONE") = ImPlotDummyFlags_None,
    "Plots a dummy item (i.e. adds a legend entry colored by `Col.LINE`).\n");
m.def(
    "plot_image",
    [](const char *label_id, ImTextureRef tex_ref, ImPlotPoint bounds_min,
       ImPlotPoint bounds_max, ImVec2 uv0, ImVec2 uv1, ImVec4 tint_col,
       ImPlotImageFlags_ flags) {
      ImPlot::PlotImage(label_id, tex_ref, bounds_min, bounds_max, uv0, uv1,
                        tint_col, flags);
    },
    "label_id"_a, "tex_ref"_a, "bounds_min"_a, "bounds_max"_a,
    "uv0"_a.sig("(0,0)") = ImVec2(0, 0), "uv1"_a.sig("(1,1)") = ImVec2(1, 1),
    "tint_col"_a.sig("(1,1,1,1)") = ImVec4(1, 1, 1, 1),
    "flags"_a.sig("ImageFlag.NONE") = ImPlotImageFlags_None,
    "Plots an axis-aligned image. `bounds_min`/`bounds_max` are in plot "
    "coordinates (y-up) and `uv0`/`uv1` are in texture coordinates "
    "(y-down).\n");
m.def(
    "set_axis", [](ImAxis_ axis) { ImPlot::SetAxis(axis); }, "axis"_a,
    "Select which axis/axes will be used for subsequent plot elements.\n");
m.def(
    "set_axes",
    [](ImAxis_ x_axis, ImAxis_ y_axis) { ImPlot::SetAxes(x_axis, y_axis); },
    "x_axis"_a, "y_axis"_a,
    "Select which axis/axes will be used for subsequent plot elements.\n");
m.def(
    "pixels_to_plot",
    [](ImVec2 pix, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PixelsToPlot(pix, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "pix"_a, "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "Convert pixels to a position in the current plot's coordinate system. "
    "Passing `implot.AUTO` uses the current axes.\n");
m.def(
    "pixels_to_plot",
    [](float x, float y, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PixelsToPlot(x, y, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "x"_a, "y"_a,
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "Convert pixels to a position in the current plot's coordinate system. "
    "Passing `implot.AUTO` uses the current axes.\n");
m.def(
    "plot_to_pixels",
    [](ImPlotPoint plt, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PlotToPixels(plt, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "plt"_a, "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "Convert a position in the current plot's coordinate system to pixels. "
    "Passing `implot.AUTO` uses the current axes.\n");
m.def(
    "plot_to_pixels",
    [](double x, double y, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PlotToPixels(x, y, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "x"_a, "y"_a,
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "Convert a position in the current plot's coordinate system to pixels. "
    "Passing `implot.AUTO` uses the current axes.\n");
m.def(
    "get_plot_pos", []() { return ImPlot::GetPlotPos(); },
    "Get the current Plot position (top-left) in pixels.\n");
m.def(
    "get_plot_size", []() { return ImPlot::GetPlotSize(); },
    "Get the curent Plot size in pixels.\n");
m.def(
    "get_plot_mouse_pos",
    [](std::variant<ImAxis_, int> x_axis, std::variant<ImAxis_, int> y_axis) {
      return ImPlot::GetPlotMousePos(variant_to_int(x_axis),
                                     variant_to_int(y_axis));
    },
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "Returns the mouse position in x,y coordinates of the current plot. "
    "Passing `implot.AUTO` uses the current axes.\n");
m.def(
    "is_plot_hovered", []() { return ImPlot::IsPlotHovered(); },
    "Returns `True` if the plot area in the current plot is hovered.\n");
m.def(
    "is_axis_hovered", [](ImAxis_ axis) { return ImPlot::IsAxisHovered(axis); },
    "axis"_a,
    "Returns `True` if the axis label area in the current plot is hovered.\n");
m.def(
    "is_subplots_hovered", []() { return ImPlot::IsSubplotsHovered(); },
    "Returns `True` if the bounding frame of a subplot is hovered.\n");
m.def(
    "is_plot_selected", []() { return ImPlot::IsPlotSelected(); },
    "Returns `True` if the current plot is being box selected.\n");
m.def(
    "cancel_plot_selection", []() { ImPlot::CancelPlotSelection(); },
    "Cancels a the current plot box selection.\n");
m.def(
    "hide_next_item",
    [](bool hidden, ImPlotCond_ cond) { ImPlot::HideNextItem(hidden, cond); },
    "hidden"_a.sig("True") = true, "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once,
    "Hides or shows the next plot item (i.e. as if it were toggled from the "
    "legend).\n"
    "\n"
    "Use `Cond.ALWAYS` if you need to forcefully set this every frame.\n");
m.def(
    "begin_aligned_plots",
    [](const char *group_id, bool vertical) {
      return ImPlot::BeginAlignedPlots(group_id, vertical);
    },
    "group_id"_a, "vertical"_a.sig("True") = true,
    "Align axis padding over multiple plots in a single row or column. "
    "`group_id` must\n"
    "be unique. If this function returns `True`, `implot.end_aligned_plots()` "
    "must be called.\n");
m.def(
    "end_aligned_plots", []() { ImPlot::EndAlignedPlots(); },
    "Only call `implot.end_aligned_plots()` if `implot.begin_aligned_plots()` "
    "returns `True`!\n");
m.def(
    "begin_legend_popup",
    [](const char *label_id, ImGuiMouseButton_ mouse_button) {
      return ImPlot::BeginLegendPopup(label_id, mouse_button);
    },
    "label_id"_a,
    "mouse_button"_a.sig("slimgui_ext.imgui.MouseButton.RIGHT") =
        ImGuiMouseButton_Right,
    "Begin a popup for a legend entry.\n");
m.def(
    "end_legend_popup", []() { ImPlot::EndLegendPopup(); },
    "End a popup for a legend entry.\n");
m.def(
    "is_legend_entry_hovered",
    [](const char *label_id) { return ImPlot::IsLegendEntryHovered(label_id); },
    "label_id"_a, "Returns `True` if a plot item legend entry is hovered.\n");
m.def(
    "begin_drag_drop_target_plot",
    []() { return ImPlot::BeginDragDropTargetPlot(); },
    "Turns the current plot's plotting area into a drag and drop target. Don't "
    "forget to call `implot.end_drag_drop_target()`!\n");
m.def(
    "begin_drag_drop_target_axis",
    [](ImAxis_ axis) { return ImPlot::BeginDragDropTargetAxis(axis); },
    "axis"_a,
    "Turns the current plot's X-axis into a drag and drop target. Don't forget "
    "to call `implot.end_drag_drop_target()`!\n");
m.def(
    "begin_drag_drop_target_legend",
    []() { return ImPlot::BeginDragDropTargetLegend(); },
    "Turns the current plot's legend into a drag and drop target. Don't forget "
    "to call `implot.end_drag_drop_target()`!\n");
m.def(
    "end_drag_drop_target", []() { ImPlot::EndDragDropTarget(); },
    "Ends a drag and drop target (currently just an alias for "
    "`imgui.end_drag_drop_target()`).\n");
m.def(
    "begin_drag_drop_source_plot",
    [](ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourcePlot(flags);
    },
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None,
    "Turns the current plot's plotting area into a drag and drop source. You "
    "must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!\n");
m.def(
    "begin_drag_drop_source_axis",
    [](ImAxis_ axis, ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourceAxis(axis, flags);
    },
    "axis"_a,
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None,
    "Turns the current plot's X-axis into a drag and drop source. You must "
    "hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!\n");
m.def(
    "begin_drag_drop_source_item",
    [](const char *label_id, ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourceItem(label_id, flags);
    },
    "label_id"_a,
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None,
    "Turns an item in the current plot's legend into drag and drop source. "
    "Don't forget to call `implot.end_drag_drop_source()`!\n");
m.def(
    "end_drag_drop_source", []() { ImPlot::EndDragDropSource(); },
    "Ends a drag and drop source (currently just an alias for "
    "`imgui.end_drag_drop_source()`).\n");
m.def(
    "style_colors_auto", [](ImPlotStyle *dst) { ImPlot::StyleColorsAuto(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Style plot colors for current ImGui style (default).\n");
m.def(
    "style_colors_classic",
    [](ImPlotStyle *dst) { ImPlot::StyleColorsClassic(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Style plot colors for ImGui \"Classic\".\n");
m.def(
    "style_colors_dark", [](ImPlotStyle *dst) { ImPlot::StyleColorsDark(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Style plot colors for ImGui \"Dark\".\n");
m.def(
    "style_colors_light",
    [](ImPlotStyle *dst) { ImPlot::StyleColorsLight(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Style plot colors for ImGui \"Light\".\n");
m.def(
    "push_style_color",
    [](ImPlotCol_ idx, ImU32 col) { ImPlot::PushStyleColor(idx, col); },
    "idx"_a, "col"_a,
    "Temporarily modify a style color. Don't forget to call "
    "`implot.pop_style_color()`!\n");
m.def(
    "push_style_color",
    [](ImPlotCol_ idx, ImVec4 col) { ImPlot::PushStyleColor(idx, col); },
    "idx"_a, "col"_a,
    "Temporarily modify a style color. Don't forget to call "
    "`implot.pop_style_color()`!\n");
m.def(
    "pop_style_color", [](int count) { ImPlot::PopStyleColor(count); },
    "count"_a.sig("1") = 1,
    "Undo temporary style color modification(s). Undo multiple pushes at once "
    "by increasing count.\n");
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, int val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a,
    "Temporarily modify a style variable of int type. Don't forget to call "
    "`implot.pop_style_var()`!\n");
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, float val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a,
    "Temporarily modify a style variable of float type. Don't forget to call "
    "`implot.pop_style_var()`!\n");
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, ImVec2 val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a,
    "Temporarily modify a style variable of float 2-tuple. Don't forget to "
    "call `implot.pop_style_var()`!\n");
m.def(
    "pop_style_var", [](int count) { ImPlot::PopStyleVar(count); },
    "count"_a.sig("1") = 1,
    "Undo temporary style variable modification(s). Undo multiple pushes at "
    "once by increasing count.\n");
m.def(
    "set_next_line_style",
    [](ImVec4 col, float weight) { ImPlot::SetNextLineStyle(col, weight); },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1), "weight"_a.sig("AUTO") = -1,
    "Set the line color and weight for the next item only.\n");
m.def(
    "set_next_fill_style",
    [](ImVec4 col, float alpha_mod) {
      ImPlot::SetNextFillStyle(col, alpha_mod);
    },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1),
    "alpha_mod"_a.sig("AUTO") = -1,
    "Set the fill color for the next item only.\n");
m.def(
    "set_next_marker_style",
    [](std::variant<ImPlotMarker_, int> marker, float size, ImVec4 fill,
       float weight, ImVec4 outline) {
      ImPlot::SetNextMarkerStyle(variant_to_int(marker), size, fill, weight,
                                 outline);
    },
    "marker"_a.sig("AUTO") = std::variant<ImPlotMarker_, int>(IMPLOT_AUTO),
    "size"_a.sig("AUTO") = -1, "fill"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1),
    "weight"_a.sig("AUTO") = -1,
    "outline"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1),
    "Set the marker style for the next item only.\n");
m.def(
    "set_next_error_bar_style",
    [](ImVec4 col, float size, float weight) {
      ImPlot::SetNextErrorBarStyle(col, size, weight);
    },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1), "size"_a.sig("AUTO") = -1,
    "weight"_a.sig("AUTO") = -1,
    "Set the error bar style for the next item only.\n");
m.def(
    "get_last_item_color", []() { return ImPlot::GetLastItemColor(); },
    "Gets the last item primary color (i.e. its legend icon color)\n");
m.def(
    "get_style_color_name",
    [](ImPlotCol_ idx) { return ImPlot::GetStyleColorName(idx); }, "idx"_a,
    "Returns the string name for an `implot.Col`.\n");
m.def(
    "get_marker_name",
    [](ImPlotMarker_ idx) { return ImPlot::GetMarkerName(idx); }, "idx"_a,
    "Returns the string name for an ImPlotMarker.\n");
m.def(
    "get_colormap_count", []() { return ImPlot::GetColormapCount(); },
    "Returns the number of available colormaps (i.e. the built-in + user-added "
    "count).\n");
m.def(
    "get_colormap_name",
    [](ImPlotColormap_ cmap) { return ImPlot::GetColormapName(cmap); },
    "cmap"_a,
    "Returns a string name for a colormap given an index. Returns `None` if "
    "index is invalid.\n");
m.def(
    "get_colormap_index",
    [](const char *name) { return ImPlot::GetColormapIndex(name); }, "name"_a,
    "Returns an index number for a colormap given a valid string name. Returns "
    "-1 if name is invalid.\n");
m.def(
    "push_colormap", [](ImPlotColormap_ cmap) { ImPlot::PushColormap(cmap); },
    "cmap"_a,
    "Temporarily switch to one of the built-in (i.e. ImPlotColormap_XXX) or "
    "user-added colormaps (i.e. a return value of `implot.add_colormap()`). "
    "Don't forget to call `implot.pop_colormap()`!\n");
m.def(
    "push_colormap", [](const char *name) { ImPlot::PushColormap(name); },
    "name"_a,
    "Push a colormap by string name. Use built-in names such as \"Default\", "
    "\"Deep\", \"Jet\", etc. or a string you provided to "
    "`implot.add_colormap(). Don't forget to call `implot.pop_colormap()`!\n");
m.def(
    "pop_colormap", [](int count) { ImPlot::PopColormap(count); },
    "count"_a.sig("1") = 1,
    "Undo temporary colormap modification(s). Undo multiple pushes at once by "
    "increasing count.\n");
m.def(
    "next_colormap_color", []() { return ImPlot::NextColormapColor(); },
    "Returns the next color from the current colormap and advances the "
    "colormap for the current plot.\n"
    "\n"
    "Can also be used with no return value to skip colors if desired. You need "
    "to call this between `implot.begin_plot()`/`implot.end_plot()`!\n");
m.def(
    "get_colormap_size",
    [](std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::GetColormapSize(variant_to_int(cmap));
    },
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO),
    "Returns the size of a colormap.\n");
m.def(
    "get_colormap_color",
    [](int idx, std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::GetColormapColor(idx, variant_to_int(cmap));
    },
    "idx"_a,
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO),
    "Returns a color from a colormap given an index >= 0 (modulo will be "
    "performed).\n");
m.def(
    "sample_colormap",
    [](float t, std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::SampleColormap(t, variant_to_int(cmap));
    },
    "t"_a,
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO),
    "Sample a color from the current colormap given t between 0 and 1.\n");
m.def(
    "colormap_scale",
    [](const char *label, double scale_min, double scale_max, ImVec2 size,
       const char *format, ImPlotColormapScaleFlags_ flags,
       std::variant<ImPlotColormap_, int> cmap) {
      ImPlot::ColormapScale(label, scale_min, scale_max, size, format, flags,
                            variant_to_int(cmap));
    },
    "label"_a, "scale_min"_a, "scale_max"_a,
    "size"_a.sig("(0,0)") = ImVec2(0, 0), "format"_a.sig("'%g'") = "%g",
    "flags"_a.sig("ColormapScaleFlags.NONE") = ImPlotColormapScaleFlags_None,
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO),
    "Shows a vertical color scale with linear spaced ticks using the specified "
    "color map. Use double hashes to hide label (e.g. \"##NoLabel\"). If "
    "`scale_min > scale_max`, the scale to color mapping will be reversed.\n");
m.def(
    "colormap_button",
    [](const char *label, ImVec2 size,
       std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::ColormapButton(label, size, variant_to_int(cmap));
    },
    "label"_a, "size"_a.sig("(0,0)") = ImVec2(0, 0),
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO),
    "Shows a button with a colormap gradient brackground.\n");
m.def(
    "bust_color_cache",
    [](std::optional<const char *> plot_title_id) {
      ImPlot::BustColorCache(plot_title_id ? plot_title_id.value() : nullptr);
    },
    "plot_title_id"_a.sig("None") = nb::none(),
    "When items in a plot sample their color from a colormap, the color is "
    "cached and does not change\n"
    "unless explicitly overriden. Therefore, if you change the colormap after "
    "the item has already been plotted,\n"
    "item colors will NOT update. If you need item colors to resample the new "
    "colormap, then use this\n"
    "function to bust the cached colors. If #plot_title_id is nullptr, then "
    "every item in EVERY existing plot\n"
    "will be cache busted. Otherwise only the plot specified by #plot_title_id "
    "will be busted. For the\n"
    "latter, this function must be called in the same ImGui ID scope that the "
    "plot is in. You should rarely if ever\n"
    "need this function, but it is available for applications that require "
    "runtime colormap swaps (e.g. Heatmaps demo).\n");
m.def(
    "map_input_default",
    [](ImPlotInputMap *dst) { ImPlot::MapInputDefault(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Default input mapping: pan = LMB drag, box select = RMB drag, fit = LMB "
    "double click, context menu = RMB click, zoom = scroll.\n");
m.def(
    "map_input_reverse",
    [](ImPlotInputMap *dst) { ImPlot::MapInputReverse(dst); },
    "dst"_a.sig("None") = nb::none(),
    "Reverse input mapping: pan = RMB drag, box select = LMB drag, fit = LMB "
    "double click, context menu = RMB click, zoom = scroll.\n");
m.def(
    "item_icon", [](ImVec4 col) { ImPlot::ItemIcon(col); }, "col"_a,
    "Render icons similar to those that appear in legends (nifty for data "
    "lists).\n");
m.def(
    "item_icon", [](ImU32 col) { ImPlot::ItemIcon(col); }, "col"_a,
    "Render icons similar to those that appear in legends (nifty for data "
    "lists).\n");
m.def(
    "colormap_icon", [](ImPlotColormap_ cmap) { ImPlot::ColormapIcon(cmap); },
    "cmap"_a,
    "Render icons similar to those that appear in legends (nifty for data "
    "lists).\n");
m.def(
    "push_plot_clip_rect",
    [](float expand) { ImPlot::PushPlotClipRect(expand); },
    "expand"_a.sig("0") = 0,
    "Push clip rect for rendering to current plot area. The rect can be "
    "expanded or contracted by #expand pixels. Call between "
    "`implot.begin_plot()`/`implot.end_plot()`.\n");
m.def(
    "pop_plot_clip_rect", []() { ImPlot::PopPlotClipRect(); },
    "Pop plot clip rect. Call between "
    "`implot.begin_plot()`/`implot.end_plot()`.\n");
m.def(
    "show_style_selector",
    [](const char *label) { return ImPlot::ShowStyleSelector(label); },
    "label"_a, "Shows ImPlot style selector dropdown menu.\n");
m.def(
    "show_colormap_selector",
    [](const char *label) { return ImPlot::ShowColormapSelector(label); },
    "label"_a, "Shows ImPlot colormap selector dropdown menu.\n");
m.def(
    "show_input_map_selector",
    [](const char *label) { return ImPlot::ShowInputMapSelector(label); },
    "label"_a, "Shows ImPlot input map selector dropdown menu.\n");
m.def(
    "show_style_editor", [](ImPlotStyle *ref) { ImPlot::ShowStyleEditor(ref); },
    "ref"_a.sig("None") = nb::none(),
    "Shows ImPlot style editor block (not a window).\n");
m.def(
    "show_user_guide", []() { ImPlot::ShowUserGuide(); },
    "Add basic help/info block for end users (not a window).\n");

