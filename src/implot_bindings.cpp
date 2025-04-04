#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
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

typedef nb::ndarray<const float, nb::ndim<1>, nb::device::cpu, nb::c_contig> ndarray_1d_f32;
typedef nb::ndarray<const double, nb::ndim<1>, nb::device::cpu, nb::c_contig> ndarray_1d;
typedef nb::ndarray<const double, nb::ndim<2>, nb::device::cpu, nb::c_contig> ndarray_2d;

template <typename Enum, typename Int = int>
int variant_to_int(const std::variant<Enum, Int>& var) {
    if (auto p = std::get_if<Enum>(&var)) {
        return static_cast<int>(*p);
    }
    return std::get<Int>(var);
}

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

    nb::class_<ImPlotStyle>(m, "Style");
    nb::class_<ImPlotInputMap>(m, "InputMap");

    nb::class_<ImPlotContext>(m, "Context")
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
    }, "closable"_a = false);

    m.def("show_metrics_window", [](bool closable) {
        bool open = true;
        ImPlot::ShowMetricsWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);

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
    }, "axis"_a, "values"_a, "labels"_a = nb::none(), "keep_default"_a = false);

    m.def("setup_axis_ticks", [](ImAxis axis, double v_min, double v_max, int n_ticks, std::optional<std::vector<const char*>> labels, bool keep_default) {
        const char** labels_ptr = nullptr;
        if (labels) {
            if (labels->size() != n_ticks) {
                throw std::length_error("`labels` length must equal `n_ticks`.");
            }
            labels_ptr = (const char**)labels->data();
        }
        ImPlot::SetupAxisTicks(axis, v_min, v_max, n_ticks, labels_ptr, keep_default);
    }, "axis"_a, "v_min"_a, "v_max"_a, "n_ticks"_a, "labels"_a = nb::none(), "keep_default"_a = false);

    // TODO how to model row/col ratio return?  BeginSubplots writes to the source arrays.
    // // Subplots
    // m.def("begin_subplots", [](const char* title_id, int rows, int cols, ImVec2 size, ImPlotSubplotFlags_ flags, std::optional<ndarray_1d_f32>& row_ratios, std::optional<ndarray_1d_f32>& col_ratios) {
    //     const float* row_ratios_ptr = nullptr;
    //     const float* col_ratios_ptr = nullptr;
    //     if (row_ratios) {
    //         if (row_ratios->shape(0) != rows) {
    //             throw std::length_error("`row_ratios` must be same the length as `rows`.");
    //         }
    //         row_ratios_ptr = (const float*)row_ratios->data();
    //     }
    //     if (col_ratios) {
    //         if (col_ratios->shape(0) != cols) {
    //             throw std::length_error("`col_ratios` must be same the length as `cols`.");
    //         }
    //         col_ratios_ptr = (const float*)col_ratios->data();
    //     }
    //     return ImPlot::BeginSubplots(title_id, rows, cols, size, flags, row_ratios_ptr, col_ratios_ptr);
    // }, "title_id"_a, "rows"_a, "cols"_a, "size"_a, "flags"_a.sig("SubplotFlags.NONE") = ImPlotSubplotFlags_None);
    // m.def("end_subplots", &ImPlot::EndSubplots);

    // PlotLine functions
    m.def("plot_line", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotLineFlags_ flags) {
        ImPlot::PlotLine(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("LineFlags.NONE") = ImPlotLineFlags_None);
    m.def("plot_line", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotLineFlags_ flags) {
        ImPlot::PlotLine(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("LineFlags.NONE") = ImPlotLineFlags_None);

    // PlotScatter functions
    m.def("plot_scatter", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotScatterFlags_ flags) {
        ImPlot::PlotScatter(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("ScatterFlags.NONE") = ImPlotScatterFlags_None);
    m.def("plot_scatter", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotScatterFlags_ flags) {
        ImPlot::PlotScatter(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("ScatterFlags.NONE") = ImPlotScatterFlags_None);

    // PlotStairs functions
    m.def("plot_stairs", [](const char* label_id, ndarray_1d& values, double xscale, double xstart, ImPlotStairsFlags_ flags) {
        ImPlot::PlotStairs(label_id, (const double*)values.data(), values.shape(0), xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("StairsFlags.NONE") = ImPlotStairsFlags_None);
    m.def("plot_stairs", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotStairsFlags_ flags) {
        ImPlot::PlotStairs(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("StairsFlags.NONE") = ImPlotStairsFlags_None);

    // PlotShaded functions
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& values, double yref, double xscale, double xstart, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)values.data(), values.shape(0), yref, xscale, xstart, flags);
    }, "label_id"_a, "values"_a, "yref"_a = 0, "xscale"_a = 1.0, "xstart"_a = 0.0, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None);
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double yref, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), yref, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "yref"_a = 0, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None);
    m.def("plot_shaded", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys1, ndarray_1d& ys2, ImPlotShadedFlags_ flags) {
        ImPlot::PlotShaded(label_id, (const double*)xs.data(), (const double*)ys1.data(), (const double*)ys2.data(), xs.shape(0), flags);
    }, "label_id"_a, "xs"_a, "ys1"_a, "ys2"_a, "flags"_a.sig("ShadedFlags.NONE") = ImPlotShadedFlags_None);

    // Plots a bar graph. Vertical by default. #bar_size and #shift are in plot units.
    m.def("plot_bars", [](const char* label_id, ndarray_1d& values, double bar_size, double shift, ImPlotBarsFlags_ flags) {
        ImPlot::PlotBars(label_id, (const double*)values.data(), values.shape(0), bar_size, shift, flags);
    }, "label_id"_a, "values"_a, "bar_size"_a = 0.67, "shift"_a = 0.0, "flags"_a.sig("BarFlags.NONE") = ImPlotBarsFlags_None);
    m.def("plot_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double bar_size, ImPlotBarsFlags_ flags) {
        ImPlot::PlotBars(label_id, (const double*)xs.data(), (const double*)ys.data(), xs.shape(0), bar_size, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "bar_size"_a, "flags"_a.sig("BarFlags.NONE") = ImPlotBarsFlags_None);

    // Plots a group of bars. #values is a row-major matrix with #item_count rows and #group_count cols. #label_ids should have #item_count elements.
    m.def("plot_bar_groups", [](std::vector<const char*> label_ids, ndarray_2d& values, double group_size, double shift, ImPlotBarGroupsFlags_ flags) {
        int item_count = values.shape(0);
        int group_count = values.shape(1);
        if (label_ids.size() != item_count) {
            throw std::length_error("`label_ids` must be same the length as `values.shape(0)`");
        }
        ImPlot::PlotBarGroups(label_ids.data(), (const double*)values.data(), item_count, group_count, group_size, shift, flags);
    }, "label_ids"_a, "values"_a, "group_size"_a = 0.67, "shift"_a = 0.0, "flags"_a.sig("BarGroupsFlags.NONE") = ImPlotBarGroupsFlags_None);

    // Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.
    m.def("plot_error_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ndarray_1d& err, ImPlotErrorBarsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0) || count != err.shape(0)) {
            throw std::length_error("`xs`, `ys` and `err` must all be same length");
        }
        ImPlot::PlotErrorBars(label_id, (const double*)xs.data(), (const double*)ys.data(), (const double*)err.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "err"_a, "flags"_a.sig("ErrorBarsFlags.NONE") = ImPlotErrorBarsFlags_None);
    m.def("plot_error_bars", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ndarray_1d& neg, ndarray_1d& pos, ImPlotErrorBarsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0) || count != neg.shape(0) || count != pos.shape(0)) {
            throw std::length_error("`xs`, `ys`, `neg`, and `pos` must all be same length");
        }
        ImPlot::PlotErrorBars(label_id, (const double*)xs.data(), (const double*)ys.data(), (const double*)neg.data(), (const double*)pos.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "neg"_a, "pos"_a, "flags"_a.sig("ErrorBarsFlags.NONE") = ImPlotErrorBarsFlags_None);

    // Plots stems. Vertical by default.
    m.def("plot_stems", [](const char* label_id, ndarray_1d& values, double ref, double scale, double start, ImPlotStemsFlags_ flags) {
        ImPlot::PlotStems(label_id, (const double*)values.data(), values.shape(0), ref, scale, start, flags);
    }, "label_id"_a, "values"_a, "ref"_a = 0.0, "scale"_a = 1.0, "start"_a = 0.0, "flags"_a.sig("StemsFlags.NONE") = ImPlotStemsFlags_None);
    m.def("plot_stems", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, double ref, ImPlotStemsFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0)) {
            throw std::length_error("`xs` and `ys` must be the same length");
        }
        ImPlot::PlotStems(label_id, (const double*)xs.data(), (const double*)ys.data(), count, ref, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "ref"_a = 0.0, "flags"_a.sig("StemsFlags.NONE") = ImPlotStemsFlags_None);

    // Plots infinite vertical or horizontal lines (e.g. for references or asymptotes).
    m.def("plot_inf_lines", [](const char* label_id, ndarray_1d& values, ImPlotInfLinesFlags_ flags) {
        ImPlot::PlotInfLines(label_id, (const double*)values.data(), values.shape(0), flags);
    }, "label_id"_a, "values"_a, "flags"_a.sig("InfLinesFlags.NONE") = ImPlotInfLinesFlags_None);

    // Plots a 2D heatmap chart. Values are expected to be in row-major order by default. Leave #scale_min and scale_max both at 0 for automatic color scaling, or set them to a predefined range. #label_fmt can be set to nullptr for no labels.
    m.def("plot_heatmap", [](const char* label_id, ndarray_2d& values, double scale_min, double scale_max, std::optional<const char*> label_fmt, ImPlotPoint bounds_min, ImPlotPoint bounds_max, ImPlotHeatmapFlags_ flags) {
        ImPlot::PlotHeatmap(label_id, (const double*)values.data(), values.shape(0), values.shape(1), scale_min, scale_max, label_fmt ? label_fmt.value() : nullptr, bounds_min, bounds_max, flags);
    }, "label_id"_a, "values"_a, "scale_min"_a = 0, "scale_max"_a = 0.0, "label_fmt"_a.none() = "%.1f", "bounds_min"_a = ImPlotPoint(0,0), "bounds_max"_a = ImPlotPoint(1,1), "flags"_a.sig("HeatmapFlags.NONE") = ImPlotHeatmapFlags_None);


    // TODO range typecaster
    // // Plots a horizontal histogram. #bins can be a positive integer or an ImPlotBin_ method. If #range is left unspecified, the min/max of #values will be used as the range.
    // // Otherwise, outlier values outside of the range are not binned. The largest bin count or density is returned.
    // IMPLOT_TMP double PlotHistogram(const char* label_id, const T* values, int count, int bins=ImPlotBin_Sturges, double bar_scale=1.0, ImPlotRange range=ImPlotRange(), ImPlotHistogramFlags flags=0);

    // // Plots two dimensional, bivariate histogram as a heatmap. #x_bins and #y_bins can be a positive integer or an ImPlotBin. If #range is left unspecified, the min/max of
    // // #xs an #ys will be used as the ranges. Otherwise, outlier values outside of range are not binned. The largest bin count or density is returned.
    // IMPLOT_TMP double PlotHistogram2D(const char* label_id, const T* xs, const T* ys, int count, int x_bins=ImPlotBin_Sturges, int y_bins=ImPlotBin_Sturges, ImPlotRect range=ImPlotRect(), ImPlotHistogramFlags flags=0);

    // Plots digital data. Digital plots do not respond to y drag or zoom, and are always referenced to the bottom of the plot.
    m.def("plot_digital", [](const char* label_id, ndarray_1d& xs, ndarray_1d& ys, ImPlotDigitalFlags_ flags) {
        int count = xs.shape(0);
        if (count != ys.shape(0)) {
            throw std::length_error("`xs` and `ys` must be the same length");
        }
        ImPlot::PlotDigital(label_id, (const double*)xs.data(), (const double*)ys.data(), count, flags);
    }, "label_id"_a, "xs"_a, "ys"_a, "flags"_a.sig("DigitalFlags.NONE") = ImPlotDigitalFlags_None);

    // Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.
    m.def("annotation", [](double x, double y, ImVec4 col, ImVec2 pix_offset, bool clamp, bool round) { ImPlot::Annotation(x, y, col, pix_offset, clamp, round); }, "x"_a, "y"_a, "col"_a, "pix_offset"_a, "clamp"_a, "round"_a = false);
    m.def("annotation", [](double x, double y, ImVec4 col, ImVec2 pix_offset, bool clamp, const char* text) { ImPlot::Annotation(x, y, col, pix_offset, clamp, "%s", text); }, "x"_a, "y"_a, "col"_a, "pix_offset"_a, "clamp"_a, "text"_a);

    m.def("tag_x", [](double x, ImVec4 col, bool round) { ImPlot::TagX(x, col, round); }, "x"_a, "col"_a, "round"_a = false);
    m.def("tag_x", [](double x, ImVec4 col, const char* text) { ImPlot::TagX(x, col, "%s", text); }, "x"_a, "col"_a, "text"_a);

    m.def("tag_y", [](double y, ImVec4 col, bool round) { ImPlot::TagY(y, col, round); }, "y"_a, "col"_a, "round"_a = false);
    m.def("tag_y", [](double y, ImVec4 col, const char* text) { ImPlot::TagY(y, col, "%s", text); }, "y"_a, "col"_a, "text"_a);

#include "implot_funcs.inl"
}
