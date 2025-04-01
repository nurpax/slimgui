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

namespace nb = nanobind;
using namespace nb::literals;

typedef nb::ndarray<const double, nb::ndim<1>, nb::device::cpu, nb::c_contig> ndarray_1d;
typedef nb::ndarray<const double, nb::ndim<2>, nb::device::cpu, nb::c_contig> ndarray_2d;

void implot_bindings(nb::module_& m) {
    #include "implot_enums.inl"

    m.attr("IMPLOT_AUTO") = -1;

    nb::class_<ImPlotContext>(m, "Context");
    m.def("create_context_internal", &ImPlot::CreateContext, nb::rv_policy::reference);
    m.def("set_current_context_internal", &ImPlot::SetCurrentContext, nb::rv_policy::reference);
    m.def("destroy_context_internal", &ImPlot::DestroyContext);

    m.def("show_demo_window", [](bool closable) {
        bool open = true;
        ImPlot::ShowDemoWindow(closable ? &open : nullptr);
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
            throw std::length_error("`label_ids` must be same the length as `values.shape(0)`.");
        }
        ImPlot::PlotBarGroups(label_ids.data(), (const double*)values.data(), item_count, group_count, group_size, shift, flags);
    }, "label_ids"_a, "values"_a, "group_size"_a = 0.67, "shift"_a = 0.0, "flags"_a.sig("BarGroupsFlags.NONE") = ImPlotBarGroupsFlags_None);


#include "implot_funcs.inl"
}
