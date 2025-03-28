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
    "get_colormap_size",
    [](std::variant<ImPlotColormap_, int> cmap) {
      return ImPlot::GetColormapSize(std::get<int>(cmap));
    },
    "cmap"_a.sig("IMPLOT_AUTO") =
        std::variant<ImPlotColormap_, int>(IMPLOT_AUTO));

