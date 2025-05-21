#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/make_iterator.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/variant.h>
#include <iterator>
#include <vector>
#include <array>

#include "imgui.h"
#include "implot.h"
#include "implot_internal.h"
#include "type_casts.h"
#include "type_casts_implot.h"

namespace nb = nanobind;
using namespace nb::literals;

typedef nb::ndarray<float, nb::ndim<1>, nb::device::cpu, nb::c_contig> ndarray_1d_f32_rw;
typedef nb::ndarray<const double, nb::ndim<1>, nb::device::cpu, nb::c_contig> ndarray_1d;
typedef nb::ndarray<const double, nb::ndim<2>, nb::device::cpu, nb::c_contig> ndarray_2d;

typedef nb::ndarray<bool, nb::shape<>, nb::device::cpu, nb::c_contig> ndarray_scalar_bool_rw;
typedef nb::ndarray<double, nb::shape<>, nb::device::cpu, nb::c_contig> ndarray_scalar_f64_rw;
typedef nb::ndarray<double, nb::shape<2>, nb::device::cpu, nb::c_contig> ndarray_vec2_f64_rw;
typedef nb::ndarray<double, nb::shape<2,2>, nb::device::cpu, nb::c_contig> ndarray_rect_f64_rw;

template <typename Func>
auto with_context(ImPlotContext* ctx, Func&& func) {
    ImPlotContext* prev = ImPlot::GetCurrentContext();
    ImPlot::SetCurrentContext(ctx);
    decltype(auto) result = func(); // Use decltype(auto) to preserve references
    ImPlot::SetCurrentContext(prev);
    return result;
}

void implot_bindings(nb::module_& m) {
    #include "implot_enums.inl"

    m.attr("AUTO") = -1;
    m.attr("AUTO_COL") = ImVec4(0, 0, 0, -1);

    // ColorsArray is just a way of providing mutable list access to
    // the Colors array in ImGuiStyle.
    struct ColorsArray {
        ImVec4* data;
        ColorsArray(ImVec4* colors) : data(colors) {}
    };
    nb::class_<ColorsArray>(m, "ColorsArray")
        .def("__getitem__", [](const ColorsArray& self, ImPlotCol_ index) {
            return self.data[index];
        })
        .def("__setitem__", [](ColorsArray& self, ImPlotCol_ index, ImVec4 value) {
            self.data[index] = value;
        })
        .def("__iter__", [](const ColorsArray& self) {
            // TODO weird why 'slimgui_ext.' is required here.  Some missing setup in this class binding?
            return nb::make_iterator(nb::type<ImVec4>(), "slimgui_ext.implot.ColorsArrayIterator", self.data, self.data + (size_t)ImPlotCol_COUNT);
        }, nb::keep_alive<0, 1>())
        .def("__len__", [](const ColorsArray& self) {
            return (size_t)ImPlotCol_COUNT;
        });

    nb::class_<ImPlotStyle>(m, "Style", "Plot style structure")
        .def_rw("line_weight", &ImPlotStyle::LineWeight)
        .def_rw("marker", &ImPlotStyle::Marker)
        .def_rw("marker_size", &ImPlotStyle::MarkerSize)
        .def_rw("marker_weight", &ImPlotStyle::MarkerWeight)
        .def_rw("fill_alpha", &ImPlotStyle::FillAlpha)
        .def_rw("error_bar_size", &ImPlotStyle::ErrorBarSize)
        .def_rw("error_bar_weight", &ImPlotStyle::ErrorBarWeight)
        .def_rw("digital_bit_height", &ImPlotStyle::DigitalBitHeight)
        .def_rw("digital_bit_gap", &ImPlotStyle::DigitalBitGap)
        .def_rw("plot_border_size", &ImPlotStyle::PlotBorderSize)
        .def_rw("minor_alpha", &ImPlotStyle::MinorAlpha)
        .def_rw("major_tick_len", &ImPlotStyle::MajorTickLen)
        .def_rw("minor_tick_len", &ImPlotStyle::MinorTickLen)
        .def_rw("major_tick_size", &ImPlotStyle::MajorTickSize)
        .def_rw("minor_tick_size", &ImPlotStyle::MinorTickSize)
        .def_rw("major_grid_size", &ImPlotStyle::MajorGridSize)
        .def_rw("minor_grid_size", &ImPlotStyle::MinorGridSize)
        .def_rw("plot_padding", &ImPlotStyle::PlotPadding)
        .def_rw("label_padding", &ImPlotStyle::LabelPadding)
        .def_rw("legend_padding", &ImPlotStyle::LegendPadding)
        .def_rw("legend_inner_padding", &ImPlotStyle::LegendInnerPadding)
        .def_rw("legend_spacing", &ImPlotStyle::LegendSpacing)
        .def_rw("mouse_pos_padding", &ImPlotStyle::MousePosPadding)
        .def_rw("annotation_padding", &ImPlotStyle::AnnotationPadding)
        .def_rw("fit_padding", &ImPlotStyle::FitPadding)
        .def_rw("plot_default_size", &ImPlotStyle::PlotDefaultSize)
        .def_rw("plot_min_size", &ImPlotStyle::PlotMinSize)
        .def_prop_ro("colors", [](ImPlotStyle* style) -> ColorsArray { return ColorsArray(style->Colors); }, nb::rv_policy::reference_internal)
        .def_rw("colormap", &ImPlotStyle::Colormap)
        .def_rw("use_local_time", &ImPlotStyle::UseLocalTime)
        .def_rw("use_iso8601", &ImPlotStyle::UseISO8601)
        .def_rw("use_24hour_clock", &ImPlotStyle::Use24HourClock);

    nb::class_<ImPlotInputMap>(m, "InputMap", "Input mapping structure. Default values listed. See also `implot.map_input_default()`, `implot.map_input_reverse()`.");

    nb::class_<ImPlotContext>(m, "Context", "ImPlot context (opaque struct, see implot_internal.h)")
    .def("get_plot_draw_list_internal", [](ImPlotContext* ctx) -> ImDrawList* {
        return with_context(ctx, []() { return ImPlot::GetPlotDrawList(); });
    }, nb::rv_policy::reference_internal)
    .def("get_style_internal", [](ImPlotContext* ctx) -> ImPlotStyle* {
        return with_context(ctx, []() { auto& r = ImPlot::GetStyle(); return &r; });
    }, nb::rv_policy::reference_internal)
    .def("get_input_map_internal", [](ImPlotContext* ctx) -> ImPlotInputMap* {
        return with_context(ctx, []() { auto& r = ImPlot::GetInputMap(); return &r; });
    }, nb::rv_policy::reference_internal);

    m.def("create_context_internal", &ImPlot::CreateContext, nb::rv_policy::reference);
    m.def("set_current_context_internal", &ImPlot::SetCurrentContext, nb::rv_policy::reference);
    m.def("destroy_context_internal", &ImPlot::DestroyContext);

    m.def("show_demo_window", [](bool closable) {
        bool open = true;
        ImPlot::ShowDemoWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false, "Shows the ImPlot demo window.");

    m.def("show_metrics_window", [](bool closable) {
        bool open = true;
        ImPlot::ShowMetricsWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false, "Shows ImPlot metrics/debug information window.");

    // SetupAxisTicks overloads
    m.def("setup_axis_ticks", [](ImAxis axis, ndarray_1d& values, std::optional<std::vector<const char*>> labels, bool keep_default) {
        const char** labels_ptr = nullptr;
        size_t len = values.shape(0);
        if (labels) {
            if (labels->size() != len) {
                throw std::length_error("`labels` must be same the length as `values`.");
            }
            labels_ptr = (const char**)labels->data();
        }
        ImPlot::SetupAxisTicks(axis, (const double*)values.data(), len, labels_ptr, keep_default);
    }, "axis"_a, "values"_a, "labels"_a = nb::none(), "keep_default"_a = false,
    "Sets an axis' ticks and optionally the labels. To keep the default ticks, set `keep_default=True`.");

    m.def("setup_axis_ticks", [](ImAxis axis, double v_min, double v_max, int n_ticks, std::optional<std::vector<const char*>> labels, bool keep_default) {
        const char** labels_ptr = nullptr;
        if (labels) {
            if (labels->size() != n_ticks) {
                throw std::length_error("`labels` length must equal `n_ticks`.");
            }
            labels_ptr = (const char**)labels->data();
        }
        ImPlot::SetupAxisTicks(axis, v_min, v_max, n_ticks, labels_ptr, keep_default);
    }, "axis"_a, "v_min"_a, "v_max"_a, "n_ticks"_a, "labels"_a = nb::none(), "keep_default"_a = false,
    "Sets an axis' ticks and optionally the labels. To keep the default ticks, set `keep_default=True`.");


    // Subplots
    m.def("begin_subplots", [](const char* title_id, int rows, int cols, ImVec2 size, ImPlotSubplotFlags_ flags, std::optional<ndarray_1d_f32_rw>& row_ratios, std::optional<ndarray_1d_f32_rw>& col_ratios) {
        float* row_ratios_ptr = nullptr;
        float* col_ratios_ptr = nullptr;
        if (row_ratios) {
            if (row_ratios->shape(0) != rows) {
                throw std::length_error("`row_ratios` must be same the length as `rows`.");
            }
            row_ratios_ptr = row_ratios->data();
        }
        if (col_ratios) {
            if (col_ratios->shape(0) != cols) {
                throw std::length_error("`col_ratios` must be same the length as `cols`.");
            }
            col_ratios_ptr = col_ratios->data();
        }
        return ImPlot::BeginSubplots(title_id, rows, cols, size, flags, row_ratios_ptr, col_ratios_ptr);
    }, "title_id"_a, "rows"_a, "cols"_a, "size"_a, "flags"_a.sig("SubplotFlags.NONE") = ImPlotSubplotFlags_None, "row_ratios"_a = nb::none(), "col_ratios"_a = nb::none(),
    "See https://nurpax.github.io/slimgui/apiref_implot.html#subplots for details.");
    m.def("end_subplots", &ImPlot::EndSubplots);

    // PlotLine functions
    const char* line_docstring = "Plots a standard 2D line plot. The x values are spaced evenly along the x axis, starting at `xstart` and spaced by `xscale`. The y values are taken from the `values` array.";
    m.def("plot_line", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotLineFlags_ flags) {
        ImPlot::PlotLine(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("LineFlags.NONE") = ImPlotLineFlags_None, line_docstring);
    const char* line_docstring2 = "Plots a standard 2D line plot. The x values are taken from the `xs` array, and the y values are taken from the `ys` array.";
    m.def("plot_line", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotLineFlags_ flags) {
        ImPlot::PlotLine(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("LineFlags.NONE") = ImPlotLineFlags_None, line_docstring2);

    // PlotScatter functions
    const char* scatter_docstring = "Plots a standard 2D scatter plot. Default marker is `Marker.CIRCLE`.";
    m.def("plot_scatter", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotScatterFlags_ flags) {
        ImPlot::PlotScatter(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("ScatterFlags.NONE") = ImPlotScatterFlags_None, scatter_docstring);
    m.def("plot_scatter", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotScatterFlags_ flags) {
        ImPlot::PlotScatter(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("ScatterFlags.NONE") = ImPlotScatterFlags_None, scatter_docstring);

    // PlotStairs functions
    const char stairs_docstring[] = "Plots a stairstep graph. The y value is continued constantly to the right from every x position, i.e. the interval `[x[i], x[i+1])` has the value `y[i]`";
    m.def("plot_stairs", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotStairsFlags_ flags) {
        ImPlot::PlotStairs(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("StairsFlags.NONE") = ImPlotStairsFlags_None, stairs_docstring);
    m.def("plot_stairs", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotStairsFlags_ flags) {
        ImPlot::PlotStairs(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("StairsFlags.NONE") = ImPlotStairsFlags_None, stairs_docstring);

    // PlotShaded functions
    const char shaded_docstring[] = "Plots a shaded (filled) region between two lines, or a line and a horizontal reference. Set `yref` to +/-INFINITY for infinite fill extents.";
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& values, double yref, double xscale, double xstart, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)values.data(), values.shape(0), yref, xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "yref"_a = 0, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None, shaded_docstring);
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double yref, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), yref, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "yref"_a = 0, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None, shaded_docstring);
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys1, ndarray_1d& ys2, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)xs.data(), (const double*)ys1.data(), (const double*)ys2.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys1"_a, "ys2"_a, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None, shaded_docstring);

    // Plots a bar graph. Vertical by default. #bar_size and #shift are in plot units.
    const char bars_docstring[] = "Plots a bar graph. Vertical by default. `bar_size` and `shift` are in plot units.";
    m.def("plot_bars", [](const char* label_id, ndarray_1d& values, double bar_size, double shift, ImPlotBarsFlags_ flags) {
        ImPlot::PlotBars(label_id, (const double*)values.data(), values.shape(0), bar_size, shift, flags);
    }, "label_id"_a, "values"_a, "bar_size"_a = 0.67, "shift"_a = 0.0, "flags"_a.sig("BarsFlags.NONE") = ImPlotBarsFlags_None, bars_docstring);
    m.def("plot_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double bar_size, ImPlotBarsFlags_ flags) {
        ImPlot::PlotBars(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), bar_size, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "bar_size"_a, "flags"_a.sig("BarsFlags.NONE") = ImPlotBarsFlags_None, bars_docstring);

    // Plots a group of bars. #values is a row-major matrix with #item_count rows and #group_count cols. #label_ids should have #item_count elements.
    const char bar_groups_docstring[] = "Plots a group of bars. `values` is a matrix with a shape `(item_count, group_count)`. `label_ids` should have `item_count` elements.";
    m.def("plot_bar_groups", [](std::vector<const char*> label_ids, ndarray_2d& values, double group_size, double shift, ImPlotBarGroupsFlags_ flags) {
        int item_count = values.shape(0);
        int group_count = values.shape(1);
        if (label_ids.size() != item_count) {
            throw std::length_error("`label_ids` must be same the length as `values.shape(0)`");
        }
        ImPlot::PlotBarGroups(label_ids.data(), (const double*)values.data(), item_count, group_count, group_size, shift, flags);
    }, "label_ids"_a, "values"_a, "group_size"_a = 0.67, "shift"_a = 0.0, "flags"_a.sig("BarGroupsFlags.NONE") = ImPlotBarGroupsFlags_None, bar_groups_docstring);

    // Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.
    const char error_bars_docstring[] = "Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.";
    m.def("plot_error_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ndarray_1d& err, ImPlotErrorBarsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0) || count != err.shape(0)) {
            throw std::length_error("`xs`, `ys` and `err` must all be same length");
        }
        ImPlot::PlotErrorBars(label_id, (const double*)xs.data(), (const double*)ys.data(), (const double*)err.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "err"_a, "flags"_a.sig("ErrorBarsFlags.NONE") = ImPlotErrorBarsFlags_None, error_bars_docstring);
    m.def("plot_error_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ndarray_1d& neg, ndarray_1d& pos, ImPlotErrorBarsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0) || count != neg.shape(0) || count != pos.shape(0)) {
            throw std::length_error("`xs`, `ys`, `neg`, and `pos` must all be same length");
        }
        ImPlot::PlotErrorBars(label_id, (const double*)xs.data(), (const double*)ys.data(), (const double*)neg.data(), (const double*)pos.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "neg"_a, "pos"_a, "flags"_a.sig("ErrorBarsFlags.NONE") = ImPlotErrorBarsFlags_None, error_bars_docstring);

    const char plot_stems_docstring[] = "Plots stems. Vertical by default.";
    m.def("plot_stems", [](const char* label_id, ndarray_1d& values, double ref, double scale, double start, ImPlotStemsFlags_ flags) {
        ImPlot::PlotStems(label_id, (const double*)values.data(), values.shape(0), ref, scale, start, flags);
    }, "label_id"_a, "values"_a, "ref"_a = 0.0, "scale"_a = 1.0, "start"_a = 0.0, "flags"_a.sig("StemsFlags.NONE") = ImPlotStemsFlags_None);
    m.def("plot_stems", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double ref, ImPlotStemsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0)) {
            throw std::length_error("`xs` and `ys` must be the same length");
        }
        ImPlot::PlotStems(label_id, (const double*)xs.data(), (const double*)ys.data(), count, ref, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "ref"_a = 0.0, "flags"_a.sig("StemsFlags.NONE") = ImPlotStemsFlags_None, plot_stems_docstring);

    const char inf_lines_docstring[] = "Plots infinite vertical or horizontal lines (e.g. for references or asymptotes).";
    m.def("plot_inf_lines", [](const char* label_id, ndarray_1d& values, ImPlotInfLinesFlags_ flags) {
        ImPlot::PlotInfLines(label_id, (const double*)values.data(), values.shape(0), flags);
    }, "label_id"_a, "values"_a, "flags"_a.sig("InfLinesFlags.NONE") = ImPlotInfLinesFlags_None, inf_lines_docstring);

    // Plots a 2D heatmap chart. Values are expected to be in row-major order by default. Leave #scale_min and scale_max both at 0 for automatic color scaling, or set them to a predefined range. #label_fmt can be set to nullptr for no labels.
    const char heatmap_docstring[] = "Plots a 2D heatmap chart. `values` is expected to have shape (rows, cols). Leave `scale_min` and `scale_max` both at 0 for automatic color scaling, or set them to a predefined range. `label_fmt` can be set to `None` for no labels.";
    m.def("plot_heatmap", [](const char* label_id, ndarray_2d& values, double scale_min, double scale_max, std::optional<const char*> label_fmt, ImPlotPoint bounds_min, ImPlotPoint bounds_max, ImPlotHeatmapFlags_ flags) {
        ImPlot::PlotHeatmap(label_id, (const double*)values.data(), values.shape(0), values.shape(1), scale_min, scale_max, label_fmt ? label_fmt.value() : nullptr, bounds_min, bounds_max, flags);
    }, "label_id"_a, "values"_a, "scale_min"_a = 0, "scale_max"_a = 0.0, "label_fmt"_a.none() = "%.1f", "bounds_min"_a = ImPlotPoint(0,0), "bounds_max"_a = ImPlotPoint(1,1), "flags"_a.sig("HeatmapFlags.NONE") = ImPlotHeatmapFlags_None, 
    heatmap_docstring);


    const char histogram_docstring[] = "Plots a horizontal histogram. `bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `values` will be used as the range.  Otherwise, outlier values outside of the range are not binned. The largest bin count or density is returned.";
    m.def("plot_histogram", [](const char* label_id, const ndarray_1d& values, std::variant<int, ImPlotBin_> bins, double bar_scale, std::optional<std::tuple<double, double>> range, ImPlotHistogramFlags_ flags) {
        ImPlotRange r = ImPlotRange();
        if (range) {
            r.Min = std::get<0>(*range);
            r.Max = std::get<1>(*range);
        }
        return ImPlot::PlotHistogram(label_id, values.data(), values.shape(0), variant_to_int(bins), bar_scale, r, flags);
    }, "label_id"_a, "values"_a, "bins"_a = ImPlotBin_Sturges, "bar_scale"_a = 1.0, "range"_a.none() = nb::none(), "flags"_a.sig("HistogramFlags.NONE") = ImPlotHistogramFlags_None, histogram_docstring);

    const char histogram2d_docstring[] = "Plots two dimensional, bivariate histogram as a heatmap. `x_bins` and `y_bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `xs` an `ys` will be used as the ranges. Otherwise, outlier values outside of range are not binned. The largest bin count or density is returned.";
    m.def("plot_histogram2d", [](const char* label_id, const ndarray_1d& xs, const ndarray_1d& ys, std::variant<int, ImPlotBin_> x_bins, std::variant<int, ImPlotBin_> y_bins, std::optional<std::tuple<std::tuple<double, double>, std::tuple<double, double>>> range, ImPlotHistogramFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0)) {
            throw std::length_error("`xs` and `ys` must be the same length");
        }
        ImPlotRect ranges = ImPlotRect();
        if (range) {
            auto rx = std::get<0>(*range);
            auto ry = std::get<1>(*range);
            ranges.X.Min = std::get<0>(rx);
            ranges.X.Max = std::get<1>(rx);
            ranges.Y.Min = std::get<0>(ry);
            ranges.Y.Max = std::get<1>(ry);
        }
        return ImPlot::PlotHistogram2D(label_id, xs.data(), ys.data(), count, variant_to_int(x_bins), variant_to_int(y_bins), ranges, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "x_bins"_a = ImPlotBin_Sturges, "y_bins"_a = ImPlotBin_Sturges, "range"_a.none() = nb::none(), "flags"_a.sig("HistogramFlags.NONE") = ImPlotHistogramFlags_None, histogram2d_docstring);

    // Plots digital data. Digital plots do not respond to y drag or zoom, and are always referenced to the bottom of the plot.
    const char plot_digital_docstring[] = "Plots digital data. Digital plots do not respond to y drag or zoom, and are always referenced to the bottom of the plot.";
    m.def("plot_digital", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotDigitalFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0)) {
            throw std::length_error("`xs` and `ys` must be the same length");
        }
        ImPlot::PlotDigital(label_id, (const double*)xs.data(), (const double*)ys.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("DigitalFlags.NONE") = ImPlotDigitalFlags_None, plot_digital_docstring);

#define NP_ARRAY_ARGS_DOC "The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details."
    // Shows a draggable point at x,y. #col defaults to ImGuiCol_Text.
    m.def("drag_point", [](int id, ndarray_vec2_f64_rw& point, ImVec4 col, float size, ImPlotDragToolFlags_ flags, std::optional<ndarray_scalar_bool_rw> out_clicked, std::optional<ndarray_scalar_bool_rw> out_hovered, std::optional<ndarray_scalar_bool_rw> out_held) {
        bool* clicked = out_clicked ? out_clicked->data() : nullptr;
        bool* hovered = out_hovered ? out_hovered->data() : nullptr;
        bool* held = out_held ? out_held->data() : nullptr;
        double* xy = point.data();
        return ImPlot::DragPoint(id, xy, xy + 1, col, size, flags, clicked, hovered, held);
    }, "id"_a, "point"_a, "col"_a, "size"_a = 4.0, "flags"_a.sig("DragToolFlags.NONE") = ImPlotDragToolFlags_None, "out_clicked"_a = nb::none(), "out_hovered"_a = nb::none(), "out_held"_a = nb::none(),
    "Shows a draggable point at `point`.  The updated drag position will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.\n"
    "`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.\n"
    "Returns `True` if the point was dragged.\n\n"
    NP_ARRAY_ARGS_DOC);

    m.def("drag_line_x", [](int id, ndarray_scalar_f64_rw& x, ImVec4 col, float thickness, ImPlotDragToolFlags_ flags, std::optional<ndarray_scalar_bool_rw> out_clicked, std::optional<ndarray_scalar_bool_rw> out_hovered, std::optional<ndarray_scalar_bool_rw> out_held) {
        bool* clicked = out_clicked ? out_clicked->data() : nullptr;
        bool* hovered = out_hovered ? out_hovered->data() : nullptr;
        bool* held = out_held ? out_held->data() : nullptr;
        return ImPlot::DragLineX(id, x.data(), col, thickness, flags, clicked, hovered, held);
    }, "id"_a, "x"_a, "col"_a, "thickness"_a = 1, "flags"_a.sig("DragToolFlags.NONE") = ImPlotDragToolFlags_None, "out_clicked"_a = nb::none(), "out_hovered"_a = nb::none(), "out_held"_a = nb::none(),
    "Shows a draggable vertical guide line at an x-value. The updated drag position will be written to the `x` array.  Color `col` defaults to `imgui.Col.TEXT`.\n"
    "`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.\n"
    "Returns `True` if the line was dragged.\n\n"
    NP_ARRAY_ARGS_DOC);

    m.def("drag_line_y", [](int id, ndarray_scalar_f64_rw& y, ImVec4 col, float thickness, ImPlotDragToolFlags_ flags, std::optional<ndarray_scalar_bool_rw> out_clicked, std::optional<ndarray_scalar_bool_rw> out_hovered, std::optional<ndarray_scalar_bool_rw> out_held) {
        bool* clicked = out_clicked ? out_clicked->data() : nullptr;
        bool* hovered = out_hovered ? out_hovered->data() : nullptr;
        bool* held = out_held ? out_held->data() : nullptr;
        return ImPlot::DragLineY(id, y.data(), col, thickness, flags, clicked, hovered, held);
    }, "id"_a, "y"_a, "col"_a, "thickness"_a = 1, "flags"_a.sig("DragToolFlags.NONE") = ImPlotDragToolFlags_None, "out_clicked"_a = nb::none(), "out_hovered"_a = nb::none(), "out_held"_a = nb::none(),
    "Shows a draggable horizontal guide line at a y-value. The updated drag position will be written to the `y` array.  Color `col` defaults to `imgui.Col.TEXT`.\n"
    "`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the line is clicked, hovered, or held, respectively.\n"
    "Returns `True` if the line was dragged.\n\n"
    NP_ARRAY_ARGS_DOC);

    m.def("drag_rect", [](int id, ndarray_rect_f64_rw& rect, ImVec4 col, ImPlotDragToolFlags_ flags, std::optional<ndarray_scalar_bool_rw> out_clicked, std::optional<ndarray_scalar_bool_rw> out_hovered, std::optional<ndarray_scalar_bool_rw> out_held) {
        bool* clicked = out_clicked ? out_clicked->data() : nullptr;
        bool* hovered = out_hovered ? out_hovered->data() : nullptr;
        bool* held = out_held ? out_held->data() : nullptr;
        double* r = rect.data();
        return ImPlot::DragRect(id, r, r + 1, r + 2, r + 3, col, flags, clicked, hovered, held);
    }, "id"_a, "rect"_a, "col"_a, "flags"_a.sig("DragToolFlags.NONE") = ImPlotDragToolFlags_None, "out_clicked"_a = nb::none(), "out_hovered"_a = nb::none(), "out_held"_a = nb::none(),
    "Shows a draggable rectangle at `[[x0, y0], [x1, y1]` coordinates, loaded from `rect`.  The updated drag rectangle will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.\n"
    "`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.\n"
    "Returns `True` if the rectangle was dragged.\n\n"
    NP_ARRAY_ARGS_DOC);

    // Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.
    const char annotation_docstring[] = "Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.";
    m.def("annotation", [](double x, double y, ImVec4 col, ImVec2 pix_offset, bool clamp, bool round) { ImPlot::Annotation(x, y, col, pix_offset, clamp, round); }, "x"_a, "y"_a, "col"_a, "pix_offset"_a, "clamp"_a, "round"_a = false, annotation_docstring);
    m.def("annotation", [](double x, double y, ImVec4 col, ImVec2 pix_offset, bool clamp, const char* text) { ImPlot::Annotation(x, y, col, pix_offset, clamp, "%s", text); }, "x"_a, "y"_a, "col"_a, "pix_offset"_a, "clamp"_a, "text"_a, annotation_docstring);

    const char tag_x_docstring[] = "Shows a x-axis tag at the specified coordinate value.";
    m.def("tag_x", [](double x, ImVec4 col, bool round) { ImPlot::TagX(x, col, round); }, "x"_a, "col"_a, "round"_a = false, tag_x_docstring);
    m.def("tag_x", [](double x, ImVec4 col, const char* text) { ImPlot::TagX(x, col, "%s", text); }, "x"_a, "col"_a, "text"_a);

    const char tag_y_docstring[] = "Shows a y-axis tag at the specified coordinate value.";
    m.def("tag_y", [](double y, ImVec4 col, bool round) { ImPlot::TagY(y, col, round); }, "y"_a, "col"_a, "round"_a = false, tag_y_docstring);
    m.def("tag_y", [](double y, ImVec4 col, const char* text) { ImPlot::TagY(y, col, "%s", text); }, "y"_a, "col"_a, "text"_a, tag_y_docstring);

#include "implot_funcs.inl"
}
