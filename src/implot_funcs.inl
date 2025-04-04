m.def(
    "begin_plot",
    [](const char *title_id, ImVec2 size, ImPlotFlags_ flags) {
      return ImPlot::BeginPlot(title_id, size, flags);
    },
    "title_id"_a, "size"_a.sig("(-1,0)") = ImVec2(-1, 0),
    "flags"_a.sig("PlotFlags.NONE") = ImPlotFlags_None);
m.def("end_plot", []() { ImPlot::EndPlot(); });
m.def(
    "setup_axis",
    [](ImAxis_ axis, std::optional<const char *> label,
       ImPlotAxisFlags_ flags) {
      ImPlot::SetupAxis(axis, label ? label.value() : nullptr, flags);
    },
    "axis"_a, "label"_a.sig("None") = nb::none(),
    "flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None);
m.def(
    "setup_axis_limits",
    [](ImAxis_ axis, double v_min, double v_max, ImPlotCond_ cond) {
      ImPlot::SetupAxisLimits(axis, v_min, v_max, cond);
    },
    "axis"_a, "v_min"_a, "v_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once);
m.def(
    "setup_axis_format",
    [](ImAxis_ axis, const char *fmt) { ImPlot::SetupAxisFormat(axis, fmt); },
    "axis"_a, "fmt"_a);
m.def(
    "setup_axis_scale",
    [](ImAxis_ axis, ImPlotScale_ scale) {
      ImPlot::SetupAxisScale(axis, scale);
    },
    "axis"_a, "scale"_a);
m.def(
    "setup_axis_limits_constraints",
    [](ImAxis_ axis, double v_min, double v_max) {
      ImPlot::SetupAxisLimitsConstraints(axis, v_min, v_max);
    },
    "axis"_a, "v_min"_a, "v_max"_a);
m.def(
    "setup_axis_zoom_constraints",
    [](ImAxis_ axis, double z_min, double z_max) {
      ImPlot::SetupAxisZoomConstraints(axis, z_min, z_max);
    },
    "axis"_a, "z_min"_a, "z_max"_a);
m.def(
    "setup_axes",
    [](std::optional<const char *> x_label, std::optional<const char *> y_label,
       ImPlotAxisFlags_ x_flags, ImPlotAxisFlags_ y_flags) {
      ImPlot::SetupAxes(x_label ? x_label.value() : nullptr,
                        y_label ? y_label.value() : nullptr, x_flags, y_flags);
    },
    "x_label"_a.none(), "y_label"_a.none(),
    "x_flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None,
    "y_flags"_a.sig("AxisFlags.NONE") = ImPlotAxisFlags_None);
m.def(
    "setup_axes_limits",
    [](double x_min, double x_max, double y_min, double y_max,
       ImPlotCond_ cond) {
      ImPlot::SetupAxesLimits(x_min, x_max, y_min, y_max, cond);
    },
    "x_min"_a, "x_max"_a, "y_min"_a, "y_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once);
m.def(
    "setup_legend",
    [](ImPlotLocation_ location, ImPlotLegendFlags_ flags) {
      ImPlot::SetupLegend(location, flags);
    },
    "location"_a, "flags"_a.sig("LegendFlags.NONE") = ImPlotLegendFlags_None);
m.def(
    "setup_mouse_text",
    [](ImPlotLocation_ location, ImPlotMouseTextFlags_ flags) {
      ImPlot::SetupMouseText(location, flags);
    },
    "location"_a,
    "flags"_a.sig("MouseTextFlags.NONE") = ImPlotMouseTextFlags_None);
m.def("setup_finish", []() { ImPlot::SetupFinish(); });
m.def(
    "set_next_axis_limits",
    [](ImAxis_ axis, double v_min, double v_max, ImPlotCond_ cond) {
      ImPlot::SetNextAxisLimits(axis, v_min, v_max, cond);
    },
    "axis"_a, "v_min"_a, "v_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once);
m.def(
    "set_next_axis_to_fit",
    [](ImAxis_ axis) { ImPlot::SetNextAxisToFit(axis); }, "axis"_a);
m.def(
    "set_next_axes_limits",
    [](double x_min, double x_max, double y_min, double y_max,
       ImPlotCond_ cond) {
      ImPlot::SetNextAxesLimits(x_min, x_max, y_min, y_max, cond);
    },
    "x_min"_a, "x_max"_a, "y_min"_a, "y_max"_a,
    "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once);
m.def("set_next_axes_to_fit", []() { ImPlot::SetNextAxesToFit(); });
m.def(
    "plot_text",
    [](const char *text, double x, double y, ImVec2 pix_offset,
       ImPlotTextFlags_ flags) {
      ImPlot::PlotText(text, x, y, pix_offset, flags);
    },
    "text"_a, "x"_a, "y"_a, "pix_offset"_a.sig("(0,0)") = ImVec2(0, 0),
    "flags"_a.sig("TextFlag.NONE") = ImPlotTextFlags_None);
m.def(
    "plot_dummy",
    [](const char *label_id, ImPlotDummyFlags_ flags) {
      ImPlot::PlotDummy(label_id, flags);
    },
    "label_id"_a, "flags"_a.sig("DummyFlag.NONE") = ImPlotDummyFlags_None);
m.def(
    "plot_image",
    [](const char *label_id, ImTextureID user_texture_id,
       ImPlotPoint bounds_min, ImPlotPoint bounds_max, ImVec2 uv0, ImVec2 uv1,
       ImVec4 tint_col, ImPlotImageFlags_ flags) {
      ImPlot::PlotImage(label_id, user_texture_id, bounds_min, bounds_max, uv0,
                        uv1, tint_col, flags);
    },
    "label_id"_a, "user_texture_id"_a, "bounds_min"_a, "bounds_max"_a,
    "uv0"_a.sig("(0,0)") = ImVec2(0, 0), "uv1"_a.sig("(1,1)") = ImVec2(1, 1),
    "tint_col"_a.sig("(1,1,1,1)") = ImVec4(1, 1, 1, 1),
    "flags"_a.sig("ImageFlag.NONE") = ImPlotImageFlags_None);
m.def("set_axis", [](ImAxis_ axis) { ImPlot::SetAxis(axis); }, "axis"_a);
m.def(
    "set_axes",
    [](ImAxis_ x_axis, ImAxis_ y_axis) { ImPlot::SetAxes(x_axis, y_axis); },
    "x_axis"_a, "y_axis"_a);
m.def(
    "pixels_to_plot",
    [](ImVec2 pix, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PixelsToPlot(pix, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "pix"_a, "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO));
m.def(
    "pixels_to_plot",
    [](float x, float y, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PixelsToPlot(x, y, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "x"_a, "y"_a,
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO));
m.def(
    "plot_to_pixels",
    [](ImPlotPoint plt, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PlotToPixels(plt, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "plt"_a, "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO));
m.def(
    "plot_to_pixels",
    [](double x, double y, std::variant<ImAxis_, int> x_axis,
       std::variant<ImAxis_, int> y_axis) {
      return ImPlot::PlotToPixels(x, y, variant_to_int(x_axis),
                                  variant_to_int(y_axis));
    },
    "x"_a, "y"_a,
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO));
m.def("get_plot_pos", []() { return ImPlot::GetPlotPos(); });
m.def("get_plot_size", []() { return ImPlot::GetPlotSize(); });
m.def(
    "get_plot_mouse_pos",
    [](std::variant<ImAxis_, int> x_axis, std::variant<ImAxis_, int> y_axis) {
      return ImPlot::GetPlotMousePos(variant_to_int(x_axis),
                                     variant_to_int(y_axis));
    },
    "x_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO),
    "y_axis"_a.sig("AUTO") = std::variant<ImAxis_, int>(IMPLOT_AUTO));
m.def("is_plot_hovered", []() { return ImPlot::IsPlotHovered(); });
m.def(
    "is_axis_hovered", [](ImAxis_ axis) { return ImPlot::IsAxisHovered(axis); },
    "axis"_a);
m.def("is_subplots_hovered", []() { return ImPlot::IsSubplotsHovered(); });
m.def("is_plot_selected", []() { return ImPlot::IsPlotSelected(); });
m.def("cancel_plot_selection", []() { ImPlot::CancelPlotSelection(); });
m.def(
    "hide_next_item",
    [](bool hidden, ImPlotCond_ cond) { ImPlot::HideNextItem(hidden, cond); },
    "hidden"_a.sig("True") = true, "cond"_a.sig("Cond.ONCE") = ImPlotCond_Once);
m.def(
    "begin_aligned_plots",
    [](const char *group_id, bool vertical) {
      return ImPlot::BeginAlignedPlots(group_id, vertical);
    },
    "group_id"_a, "vertical"_a.sig("True") = true);
m.def("end_aligned_plots", []() { ImPlot::EndAlignedPlots(); });
m.def(
    "begin_legend_popup",
    [](const char *label_id, ImGuiMouseButton_ mouse_button) {
      return ImPlot::BeginLegendPopup(label_id, mouse_button);
    },
    "label_id"_a,
    "mouse_button"_a.sig("slimgui_ext.imgui.MouseButton.RIGHT") =
        ImGuiMouseButton_Right);
m.def("end_legend_popup", []() { ImPlot::EndLegendPopup(); });
m.def(
    "is_legend_entry_hovered",
    [](const char *label_id) { return ImPlot::IsLegendEntryHovered(label_id); },
    "label_id"_a);
m.def("begin_drag_drop_target_plot",
      []() { return ImPlot::BeginDragDropTargetPlot(); });
m.def(
    "begin_drag_drop_target_axis",
    [](ImAxis_ axis) { return ImPlot::BeginDragDropTargetAxis(axis); },
    "axis"_a);
m.def("begin_drag_drop_target_legend",
      []() { return ImPlot::BeginDragDropTargetLegend(); });
m.def("end_drag_drop_target", []() { ImPlot::EndDragDropTarget(); });
m.def(
    "begin_drag_drop_source_plot",
    [](ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourcePlot(flags);
    },
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None);
m.def(
    "begin_drag_drop_source_axis",
    [](ImAxis_ axis, ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourceAxis(axis, flags);
    },
    "axis"_a,
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None);
m.def(
    "begin_drag_drop_source_item",
    [](const char *label_id, ImGuiDragDropFlags_ flags) {
      return ImPlot::BeginDragDropSourceItem(label_id, flags);
    },
    "label_id"_a,
    "flags"_a.sig("slimgui_ext.imgui.DragDropFlags.NONE") =
        ImGuiDragDropFlags_None);
m.def("end_drag_drop_source", []() { ImPlot::EndDragDropSource(); });
m.def(
    "style_colors_auto", [](ImPlotStyle *dst) { ImPlot::StyleColorsAuto(dst); },
    "dst"_a.sig("None") = nb::none());
m.def(
    "style_colors_classic",
    [](ImPlotStyle *dst) { ImPlot::StyleColorsClassic(dst); },
    "dst"_a.sig("None") = nb::none());
m.def(
    "style_colors_dark", [](ImPlotStyle *dst) { ImPlot::StyleColorsDark(dst); },
    "dst"_a.sig("None") = nb::none());
m.def(
    "style_colors_light",
    [](ImPlotStyle *dst) { ImPlot::StyleColorsLight(dst); },
    "dst"_a.sig("None") = nb::none());
m.def(
    "push_style_color",
    [](ImPlotCol_ idx, ImU32 col) { ImPlot::PushStyleColor(idx, col); },
    "idx"_a, "col"_a);
m.def(
    "push_style_color",
    [](ImPlotCol_ idx, ImVec4 col) { ImPlot::PushStyleColor(idx, col); },
    "idx"_a, "col"_a);
m.def(
    "pop_style_color", [](int count) { ImPlot::PopStyleColor(count); },
    "count"_a.sig("1") = 1);
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, float val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a);
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, int val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a);
m.def(
    "push_style_var",
    [](ImPlotStyleVar_ idx, ImVec2 val) { ImPlot::PushStyleVar(idx, val); },
    "idx"_a, "val"_a);
m.def(
    "pop_style_var", [](int count) { ImPlot::PopStyleVar(count); },
    "count"_a.sig("1") = 1);
m.def(
    "set_next_line_style",
    [](ImVec4 col, float weight) { ImPlot::SetNextLineStyle(col, weight); },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1), "weight"_a.sig("AUTO") = -1);
m.def(
    "set_next_fill_style",
    [](ImVec4 col, float alpha_mod) {
      ImPlot::SetNextFillStyle(col, alpha_mod);
    },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1),
    "alpha_mod"_a.sig("AUTO") = -1);
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
    "outline"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1));
m.def(
    "set_next_error_bar_style",
    [](ImVec4 col, float size, float weight) {
      ImPlot::SetNextErrorBarStyle(col, size, weight);
    },
    "col"_a.sig("AUTO_COL") = ImVec4(0, 0, 0, -1), "size"_a.sig("AUTO") = -1,
    "weight"_a.sig("AUTO") = -1);
m.def("get_last_item_color", []() { return ImPlot::GetLastItemColor(); });
m.def(
    "get_style_color_name",
    [](ImPlotCol_ idx) { return ImPlot::GetStyleColorName(idx); }, "idx"_a);
m.def(
    "get_marker_name",
    [](ImPlotMarker_ idx) { return ImPlot::GetMarkerName(idx); }, "idx"_a);
m.def("get_colormap_count", []() { return ImPlot::GetColormapCount(); });
m.def(
    "get_colormap_name",
    [](ImPlotColormap_ cmap) { return ImPlot::GetColormapName(cmap); },
    "cmap"_a);
m.def(
    "get_colormap_index",
    [](const char *name) { return ImPlot::GetColormapIndex(name); }, "name"_a);
m.def(
    "push_colormap", [](ImPlotColormap_ cmap) { ImPlot::PushColormap(cmap); },
    "cmap"_a);
m.def(
    "push_colormap", [](const char *name) { ImPlot::PushColormap(name); },
    "name"_a);
m.def(
    "pop_colormap", [](int count) { ImPlot::PopColormap(count); },
    "count"_a.sig("1") = 1);
m.def("next_colormap_color", []() { return ImPlot::NextColormapColor(); });
m.def(
    "get_colormap_size",
    [](std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::GetColormapSize(variant_to_int(cmap));
    },
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));
m.def(
    "get_colormap_color",
    [](int idx, std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::GetColormapColor(idx, variant_to_int(cmap));
    },
    "idx"_a,
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));
m.def(
    "sample_colormap",
    [](float t, std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::SampleColormap(t, variant_to_int(cmap));
    },
    "t"_a,
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));
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
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));
m.def(
    "colormap_button",
    [](const char *label, ImVec2 size,
       std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::ColormapButton(label, size, variant_to_int(cmap));
    },
    "label"_a, "size"_a.sig("(0,0)") = ImVec2(0, 0),
    "cmap"_a.sig("AUTO") = std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));
m.def(
    "bust_color_cache",
    [](std::optional<const char *> plot_title_id) {
      ImPlot::BustColorCache(plot_title_id ? plot_title_id.value() : nullptr);
    },
    "plot_title_id"_a.sig("None") = nb::none());
m.def(
    "map_input_default",
    [](ImPlotInputMap *dst) { ImPlot::MapInputDefault(dst); },
    "dst"_a.sig("None") = nb::none());
m.def(
    "map_input_reverse",
    [](ImPlotInputMap *dst) { ImPlot::MapInputReverse(dst); },
    "dst"_a.sig("None") = nb::none());
m.def("item_icon", [](ImVec4 col) { ImPlot::ItemIcon(col); }, "col"_a);
m.def("item_icon", [](ImU32 col) { ImPlot::ItemIcon(col); }, "col"_a);
m.def(
    "colormap_icon", [](ImPlotColormap_ cmap) { ImPlot::ColormapIcon(cmap); },
    "cmap"_a);
m.def(
    "push_plot_clip_rect",
    [](float expand) { ImPlot::PushPlotClipRect(expand); },
    "expand"_a.sig("0") = 0);
m.def("pop_plot_clip_rect", []() { ImPlot::PopPlotClipRect(); });
m.def(
    "show_style_selector",
    [](const char *label) { return ImPlot::ShowStyleSelector(label); },
    "label"_a);
m.def(
    "show_colormap_selector",
    [](const char *label) { return ImPlot::ShowColormapSelector(label); },
    "label"_a);
m.def(
    "show_input_map_selector",
    [](const char *label) { return ImPlot::ShowInputMapSelector(label); },
    "label"_a);
m.def(
    "show_style_editor", [](ImPlotStyle *ref) { ImPlot::ShowStyleEditor(ref); },
    "ref"_a.sig("None") = nb::none());
m.def("show_user_guide", []() { ImPlot::ShowUserGuide(); });

