import time
import numpy as np
from numpy.typing import NDArray

from slimgui import imgui
from slimgui import implot

from slimgui.implot import LineFlags, PlotFlags, ScatterFlags

_surf_it = False

def show_demo_window(show_window: bool):
    global _surf_it
    main_viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos((main_viewport.work_pos[0] + 800, main_viewport.work_pos[1] + 40), imgui.Cond.FIRST_USE_EVER)
    imgui.set_next_window_size((640, 900), imgui.Cond.FIRST_USE_EVER)

    visible, show_window = imgui.begin("Implot tests", closable=show_window)
    if not visible:
        imgui.end()
        return show_window

    if imgui.collapsing_header('Basic line plots')[0]:
        _c, _surf_it = imgui.checkbox("Surf it!", _surf_it)

        if implot.begin_plot("Plot", flags=PlotFlags.NO_LEGEND):
            data_x = np.arange(0, 10, 0.25)
            data_y = np.sin(data_x)
            implot.plot_line("Sine Wave", data_y[::2]) # striding should work

            data_x = np.linspace(0, 3*np.pi, 200)
            data_y = np.sin(data_x)
            implot.plot_line("the wave", data_x, data_y) # striding should work

            if _surf_it:
                idx = int(time.time()*20)
                idx %= len(data_x)
                x, y = data_x[idx], data_y[idx]
                implot.plot_text("sine waves", x.item(), y.item())

            implot.end_plot()

    if imgui.collapsing_header('Line and scatter')[0]:
        if implot.begin_plot("Plot 2"):
            data_x = np.arange(0, 10, 0.25)
            data_y = np.sin(data_x)
            implot.plot_line("Sine Wave", data_y)

            # Generate a spiral pattern
            theta = np.linspace(0, 4 * np.pi, 50)
            r = np.linspace(0, 10, 50)
            xs = r * np.cos(theta)
            ys = r * np.sin(theta)
            implot.plot_scatter("Scatter ys", ys)
            implot.plot_scatter("Scatter xs, ys", xs, ys)

            implot.end_plot()

    if imgui.collapsing_header('Stairs##heading')[0]:
        if implot.begin_plot("Stairs"):
            x_steps = np.arange(0, 10, 1)
            y_steps = np.repeat(np.arange(1, 11), 2)[1:-1]
            implot.plot_stairs("Stairs", x_steps, y_steps)
            implot.end_plot()

        if implot.begin_plot("Shaded"):
            x_steps = np.arange(0, 10, 1)
            y_steps = np.repeat(np.arange(1, 11), 2)[1:-1]
            implot.plot_shaded("Shaded", x_steps, y_steps, yref=2.3)
            implot.end_plot()

    if imgui.collapsing_header('Bar charts##heading')[0]:
        if implot.begin_plot("Bar"):
            ys = np.random.RandomState(13).rand(10)
            implot.plot_bars("rand", ys)
            implot.end_plot()

        if implot.begin_plot("Bar 2 horizontal"):
            ys = np.random.RandomState(13).rand(10)
            implot.plot_bars("rand", ys, flags=implot.BarsFlags.HORIZONTAL)
            implot.end_plot()

    if imgui.collapsing_header('Bar chart ticks')[0]:
        if implot.begin_plot("##ticks"):
            labels = ['S1', 'S2', 'S4', 'S4']
            xs = np.arange(4)
            implot.setup_axis_ticks(implot.Axis.X1, xs, labels)
            ys = np.random.RandomState(16).rand(4)
            implot.plot_bars("rand", ys)
            implot.end_plot()

    if imgui.collapsing_header('Bar Groups')[0]:
        if implot.begin_plot("##groups"):
            labels = ['A', 'B', 'C']
            vals = np.random.RandomState(15).rand(3, 4)
            implot.setup_axes(None, None, implot.AxisFlags.NO_DECORATIONS, implot.AxisFlags.NO_DECORATIONS)
            implot.plot_bar_groups(labels, vals)
            # xs = np.arange(4)
            # ys = np.random.RandomState(16).rand(4)
            # implot.plot_bars("rand", ys)
            implot.end_plot()

    if imgui.collapsing_header('Error Bars')[0]:
        _error_bars()

    if imgui.collapsing_header('Draw list and misc')[0]:
        if implot.begin_plot("Plot 2"):
            data_x = np.arange(0, 10, 0.25)
            data_y = np.sin(data_x)
            implot.plot_line("Sine Wave", data_y)
            dl = implot.get_plot_draw_list()

            # Draw a circle
            implot.push_plot_clip_rect()
            cntr = implot.plot_to_pixels((6.5, 0.1))
            rmin = implot.plot_to_pixels((0.25, 0.75))
            rmax = implot.plot_to_pixels((0.75, 0.25))
            dl.add_circle_filled(cntr, 20, imgui.color_convert_float4_to_u32((1, 0.3, 0.5, 0.7)), 20)
            dl.add_rect(rmin, rmax, imgui.color_convert_float4_to_u32((1, 1, 0.7, 0.4)), thickness=2)
            implot.pop_plot_clip_rect()
            implot.end_plot()

    if imgui.collapsing_header('Styles')[0]:
        _styles()

    if imgui.collapsing_header('Heatmaps')[0]:
        _heatmaps()

    if imgui.collapsing_header('Annotations')[0]:
        _annotations()

    if imgui.collapsing_header('Subplots')[0]:
        _subplots()

    if imgui.collapsing_header('Histogram2d')[0]:
        _histogram2d()

    if imgui.collapsing_header('Built-in windows')[0]:
        imgui.text('Style selector')
        implot.show_style_selector("Style selector")
        imgui.text('Colormap selector')
        implot.show_colormap_selector("Colormap selector")
        imgui.text('Input map selector')
        implot.show_input_map_selector("Input map selector")
        imgui.text('Style editor')
        implot.show_style_editor()

    if imgui.collapsing_header('User guide')[0]:
        imgui.text('User guide follows ->')
        implot.show_user_guide()

    if imgui.collapsing_header('Drag Points')[0]:
        _drag_points()

    if imgui.collapsing_header('Drag Lines')[0]:
        _drag_lines()

    if imgui.collapsing_header('Drag Rects')[0]:
        _drag_rects()

    imgui.end()
    return show_window


def _error_bars():
    xs = np.array([1, 2, 3, 4, 5], dtype=np.float32)
    bar = np.array([1, 2, 5, 3, 4], dtype=np.float32)
    lin1 = np.array([8, 8, 9, 7, 8], dtype=np.float32)
    lin2 = np.array([6, 7, 6, 9, 6], dtype=np.float32)
    err1 = np.array([0.2, 0.4, 0.2, 0.6, 0.4], dtype=np.float32)
    err2 = np.array([0.4, 0.2, 0.4, 0.8, 0.6], dtype=np.float32)
    err3 = np.array([0.09, 0.14, 0.09, 0.12, 0.16], dtype=np.float32)
    err4 = np.array([0.02, 0.08, 0.15, 0.05, 0.2], dtype=np.float32)

    if implot.begin_plot('##ErrorBars'):
        implot.setup_axes_limits(0, 6, 0, 10)
        implot.plot_bars("Bar", xs, bar, 0.5)
        implot.plot_error_bars("Bar", xs, bar, err1)
        implot.set_next_error_bar_style(implot.get_colormap_color(1), 0)

        implot.plot_error_bars("Line", xs, lin1, err1, err2)
        implot.set_next_marker_style(implot.Marker.SQUARE)
        implot.plot_line("Line", xs, lin1)
        implot.push_style_color(implot.Col.ERROR_BAR, implot.get_colormap_color(2))
        implot.plot_error_bars("Scatter", xs, lin2, err2)
        implot.plot_error_bars("Scatter", xs, lin2, err3, err4, implot.ErrorBarsFlags.HORIZONTAL)
        implot.pop_style_color()
        implot.plot_scatter("Scatter", xs, lin2)
        implot.end_plot()


_style_idx = 0
def _styles():
    global _style_idx
    style = implot.get_style()
    style_names = ["Auto", "Classic", "Dark", "Light"]
    for i, name in enumerate(style_names):
        if i != 0:
            imgui.same_line()
        if imgui.radio_button(name, _style_idx == i):
            _style_idx = i
            match _style_idx:
                case 0:
                    implot.style_colors_auto()
                case 1:
                    implot.style_colors_classic()
                case 2:
                    implot.style_colors_dark(style)
                case 3:
                    implot.style_colors_light(style)


def _heatmaps():
    values1 = np.array([
        [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]
    ], dtype=np.float64)
    scale_min = 0.0
    scale_max = 6.3
    xlabels = ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
    ylabels = ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]

    axes_flags = implot.AxisFlags.LOCK | implot.AxisFlags.NO_GRID_LINES | implot.AxisFlags.NO_TICK_MARKS

    implot.push_colormap(implot.Colormap.VIRIDIS)

    if implot.begin_plot("##Heatmap1", size=(225, 225), flags=implot.PlotFlags.NO_LEGEND | implot.PlotFlags.NO_MOUSE_TEXT):
        implot.setup_axes(None, None, axes_flags, axes_flags)
        implot.setup_axis_ticks(implot.Axis.X1, 0 + 1.0 / 14.0, 1 - 1.0 / 14.0, 7, xlabels)
        implot.setup_axis_ticks(implot.Axis.Y1, 1 - 1.0 / 14.0, 0 + 1.0 / 14.0, 7, ylabels)
        implot.plot_heatmap("heat", values1, scale_min, scale_max, label_fmt="%g", bounds_min=(0, 0), bounds_max=(1, 1))
        implot.end_plot()

    imgui.same_line()
    implot.colormap_scale("##HeatScale", scale_min, scale_max, (60, 225))
    imgui.same_line()

    values2 = np.random.RandomState(int(time.time()*100) % (1<<31)).rand(80, 80)
    if implot.begin_plot("##Heatmap2", size=(225, 225)):
        implot.setup_axes(None, None, implot.AxisFlags.NO_DECORATIONS, implot.AxisFlags.NO_DECORATIONS)
        implot.setup_axes_limits(-1, 1, -1, 1)
        implot.plot_heatmap("heat1", values2, 0, 1, label_fmt=None)
        implot.plot_heatmap("heat2", values2, 0, 1, label_fmt=None, bounds_min=(-1, -1), bounds_max=(0, 0))
        implot.end_plot()

    implot.pop_colormap()


_clamp = False
def _annotations():
    global _clamp
    _, _clamp = imgui.checkbox("Clamp", _clamp)

    if implot.begin_plot("##Annotations"):
        implot.setup_axes_limits(0, 2, 0, 1)

        p = np.array([0.25, 0.25, 0.75, 0.75, 0.25])

        # ImPlot::PlotScatter("##Points",&p[0],&p[1],4);
        implot.plot_scatter("##Points", p[:-1], p[1:])

        col = implot.get_last_item_color()

        implot.annotation(0.25, 0.25, col, (-15, 15), _clamp, "BL")
        implot.annotation(0.75, 0.25, col, (15, 15), _clamp, "BR")
        implot.annotation(0.75, 0.75, col, (15, -15), _clamp, "TR")
        implot.annotation(0.25, 0.75, col, (-15, -15), _clamp, "TL")
        implot.annotation(0.5, 0.5, col, (0, 0), _clamp, "Center")
        implot.annotation(1.25, 0.75, (0, 1, 0, 1), (0, 0), _clamp)

        bx = np.array([1.2, 1.5, 1.8], dtype=np.float32)
        by = np.array([0.25, 0.5, 0.75], dtype=np.float32)
        implot.plot_bars("##Bars", bx, by, bar_size=0.2)

        for i in range(3):
            implot.annotation(bx[i], by[i], (0, 0, 0, 0), (0, -5), _clamp, f"B[{i}]={by[i]:.2f}")

        # ImPlot::EndPlot();
        implot.end_plot()


_enable_ratios = False
_row_ratios: NDArray[np.float32] = np.array([0.3, 0.7], dtype=np.float32)
_col_ratios: NDArray[np.float32] = np.ones(3, dtype=np.float32) / 3.0

def _subplots():
    global _enable_ratios, _col_ratios, _row_ratios
    # List of 4-float tuple colors
    colors = [
        (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0.5, 0, 1), (0.5, 0, 0.5, 1), (0.5, 0.5, 0.5, 1), (0.2, 0.2, 0.2, 1)
    ]
    def _lineplot(ij, idx):
        if implot.begin_plot(f"Line ({ij})##{idx}", flags=PlotFlags.NO_LEGEND):
            implot.push_style_color(implot.Col.LINE, (colors[idx]))
            implot.push_style_var(implot.StyleVar.LINE_WEIGHT, 3.0)
            data_x = np.linspace(0, 3*np.pi, 200)
            data_y = np.sin(data_x)
            implot.plot_line("the wave", data_x, data_y) # striding should work
            implot.pop_style_var()
            implot.pop_style_color()
            implot.end_plot()

    cols = 3
    rows = 2
    _, _enable_ratios = imgui.checkbox("Enable row/column ratios", _enable_ratios)
    if _enable_ratios:
        r = _row_ratios
        c = _col_ratios
    else:
        r = None
        c = None

    # If the user adjusts row/column sizing in the subplot and row_ratios/col_ratios are specified,
    # the new values will be written to the numpy arrays.
    if implot.begin_subplots("Subplots", rows, cols, (-1, 500), row_ratios=r, col_ratios=c):
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                _lineplot(f'{i+1},{j+1}', idx)
        implot.end_subplots()


_count = 50000
_xybins = (100, 100)
_hist_flags = 0
_dist1 = None
_dist2 = None

def _histogram2d():
    global _count, _xybins, _hist_flags, _dist1, _dist2

    _, _count = imgui.slider_int("Count", _count, 100, 100000)
    _, _xybins = imgui.slider_int2("Bins", _xybins, 1, 500)
    imgui.same_line()
    _, _hist_flags = imgui.checkbox_flags("Density", _hist_flags, int(implot.HistogramFlags.DENSITY))

    # Generate random data for two normal distributions
    recompute = _dist1 is None or _dist2 is None
    recompute |= _dist1 is not None and _dist1.shape[0] != _count
    if recompute:
        _dist1 = np.random.normal(1, 2, _count)
        _dist2 = np.random.normal(1, 1, _count)

    implot.push_colormap("Hot")

    max_count = 0
    if implot.begin_plot("##Hist2D", size=(imgui.get_content_region_avail()[0] - 100 - imgui.get_style().item_spacing[0], 0)):
        flags = implot.AxisFlags.AUTO_FIT | implot.AxisFlags.FOREGROUND
        implot.setup_axes(None, None, flags, flags)
        implot.setup_axes_limits(-6, 6, -6, 6)

        assert _dist1 is not None and _dist2 is not None
        max_count = implot.plot_histogram2d(
            "Hist2D",
            _dist1,
            _dist2,
            _xybins[0],
            _xybins[1],
            range=((-6, 6), (-6, 6)),
            flags=implot.HistogramFlags(_hist_flags)
        )
        implot.end_plot()

    imgui.same_line()
    implot.colormap_scale(
        "Density" if _hist_flags & implot.HistogramFlags.DENSITY else "Count", 0, max_count, size=(100, 0)
    )
    implot.pop_colormap()


# Persistent state for _drag_points
_drag_points_state = {
    "flags": 0,
    "P": np.array([[0.05, 0.05], [0.2, 0.4], [0.8, 0.6], [0.95, 0.95]], dtype=np.float64),
    "clicked": [np.array(False, dtype=np.bool_) for _ in range(4)],
    "hovered": [np.array(False, dtype=np.bool_) for _ in range(4)],
    "held": [np.array(False, dtype=np.bool_) for _ in range(4)],
}

def _drag_points():
    state = _drag_points_state

    # UI for flags
    flags = state["flags"]
    _, flags = imgui.checkbox_flags("NoCursors", flags, int(implot.DragToolFlags.NO_CURSORS))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoFit", flags, int(implot.DragToolFlags.NO_FIT))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoInput", flags, int(implot.DragToolFlags.NO_INPUTS))
    state["flags"] = flags

    ax_flags = implot.AxisFlags.NO_TICK_LABELS | implot.AxisFlags.NO_TICK_MARKS

    P = state["P"]
    hovered = state["hovered"]
    held = state["held"]

    if implot.begin_plot("##Bezier", size=(-1, 0), flags=implot.PlotFlags.CANVAS_ONLY):
        implot.setup_axes(None, None, ax_flags, ax_flags)
        implot.setup_axes_limits(0, 1, 0, 1)
        colors = [
            (0, 0.9, 0, 1),
            (1, 0.5, 1, 1),
            (0, 0.5, 1, 1),
            (0, 0.9, 0, 1),
        ]
        for i in range(4):
            implot.drag_point(
                i, P[i], col=colors[i], size=4, flags=implot.DragToolFlags(flags),
                out_hovered=state["hovered"][i],
                out_held=state["held"][i]
            )

        # Compute Bezier curve
        B = np.zeros((100, 2), dtype=np.float64)
        for i in range(100):
            t = i / 99.0
            u = 1 - t
            w1 = u * u * u
            w2 = 3 * u * u * t
            w3 = 3 * u * t * t
            w4 = t * t * t
            B[i, 0] = w1 * P[0, 0] + w2 * P[1, 0] + w3 * P[2, 0] + w4 * P[3, 0]
            B[i, 1] = w1 * P[0, 1] + w2 * P[1, 1] + w3 * P[2, 1] + w4 * P[3, 1]

        implot.set_next_line_style((1, 0.5, 1, 1), 2.0 if hovered[1] or held[1] else 1.0)
        implot.plot_line("##h1", P[:2, 0], P[:2, 1])
        implot.set_next_line_style((0, 0.5, 1, 1), 2.0 if hovered[2] or held[2] else 1.0)
        implot.plot_line("##h2", P[2:, 0], P[2:, 1])
        implot.set_next_line_style((0, 0.9, 0, 1), 3.0 if hovered[0] or held[0] or hovered[3] or held[3] else 2.0)
        implot.plot_line("##bez", B[:, 0], B[:, 1])
        implot.end_plot()


# Persistent state for _drag_lines
_drag_lines_state = {
    "x1": np.array(0.2, dtype=np.float64),
    "x2": np.array(0.8, dtype=np.float64),
    "y1": np.array(0.25, dtype=np.float64),
    "y2": np.array(0.75, dtype=np.float64),
    "f": np.array(0.1, dtype=np.float64),
    "flags": 0,
    "clicked": np.array(False, dtype=np.bool_),
    "hovered": np.array(False, dtype=np.bool_),
    "held": np.array(False, dtype=np.bool_),
}

def _drag_lines():
    import numpy as np
    state = _drag_lines_state

    # UI for flags
    _, flags = imgui.checkbox_flags("NoCursors", state["flags"], int(implot.DragToolFlags.NO_CURSORS))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoFit", flags, int(implot.DragToolFlags.NO_FIT))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoInput", flags, int(implot.DragToolFlags.NO_INPUTS))
    state["flags"] = flags

    if implot.begin_plot("##lines", size=(-1, 0)):
        implot.setup_axes_limits(0, 1, 0, 1)

        # Drag lines
        white = (1, 1, 1, 1)
        implot.drag_line_x(0, state["x1"], white, 1, implot.DragToolFlags(flags))
        implot.drag_line_x(1, state["x2"], white, 1, implot.DragToolFlags(flags))
        implot.drag_line_y(2, state["y1"], white, 1, implot.DragToolFlags(flags))
        implot.drag_line_y(3, state["y2"], white, 1, implot.DragToolFlags(flags))

        # Generate data points
        xs = np.zeros(1000, dtype=np.float64)
        ys = np.zeros(1000, dtype=np.float64)
        for i in range(1000):
            xs[i] = (state["x2"][...] + state["x1"][...])/2 + abs(state["x2"][...] - state["x1"][...])*(i/1000.0 - 0.5)
            ys[i] = (state["y1"][...] + state["y2"][...])/2 + abs(state["y2"][...] - state["y1"][...])/2 * np.sin(state["f"][...] * i/10)

        # Frequency control line
        implot.drag_line_y(120482, state["f"], (1, 0.5, 1, 1), 1, implot.DragToolFlags(flags),
                          out_clicked=state["clicked"],
                          out_hovered=state["hovered"],
                          out_held=state["held"])

        # Plot the interactive data
        implot.set_next_line_style(implot.AUTO_COL, 2.0 if state["hovered"][...] or state["held"][...] else 1.0)
        implot.plot_line("Interactive Data", xs, ys)
        implot.end_plot()

    imgui.text(f"x1: {state['x1']:.3f}, x2: {state['x2']:.3f}, y1: {state['y1']:.3f}, y2: {state['y2']:.3f}, f: {state['f']:.3f}")


# Persistent state for _drag_rects
_drag_rects_state = {
    "rect": np.array([[0.0025, 0], [0.0045, 0.5]], dtype=np.float64),  # [[x0, y0], [x1, y1]]
    "flags": 0,
    "clicked": np.array(False, dtype=np.bool_),
    "hovered": np.array(False, dtype=np.bool_),
    "held": np.array(False, dtype=np.bool_),
}

def _drag_rects():
    state = _drag_rects_state

    # UI for flags
    _, flags = imgui.checkbox_flags("NoCursors", state["flags"], int(implot.DragToolFlags.NO_CURSORS))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoFit", flags, int(implot.DragToolFlags.NO_FIT))
    imgui.same_line()
    _, flags = imgui.checkbox_flags("NoInput", flags, int(implot.DragToolFlags.NO_INPUTS))
    state["flags"] = flags

    # Generate signal data
    sampling_freq = 44100
    freq = 500
    t = np.arange(512) / sampling_freq
    arg = 2 * np.pi * freq * t
    y_data1 = np.sin(arg)
    y_data2 = y_data1 * -0.6 + np.sin(2 * arg) * 0.4
    y_data3 = y_data2 * -0.6 + np.sin(3 * arg) * 0.4

    if implot.begin_plot("##Main", size=(-1, 150)):
        implot.setup_axes(None, None, implot.AxisFlags.NO_TICK_LABELS, implot.AxisFlags.NO_TICK_LABELS)
        implot.setup_axes_limits(0, 0.01, -1, 1)
        implot.plot_line("Signal 1", t, y_data1)
        implot.plot_line("Signal 2", t, y_data2)
        implot.plot_line("Signal 3", t, y_data3)
        implot.drag_rect(
            0,
            state["rect"],
            (1, 0, 1, 1),
            implot.DragToolFlags(flags),
            out_clicked=state["clicked"],
            out_hovered=state["hovered"],
            out_held=state["held"]
        )
        implot.end_plot()

    # Set background color based on state
    bg_col = (0.5, 0, 0.5, 1) if state["held"] else ((0.25, 0, 0.25, 1) if state["hovered"] else implot.get_style().colors[implot.Col.PLOT_BG])
    implot.push_style_color(implot.Col.PLOT_BG, bg_col)
    if implot.begin_plot("##rect", size=(-1, 150), flags=implot.PlotFlags.CANVAS_ONLY):
        implot.setup_axes(None, None, implot.AxisFlags.NO_DECORATIONS, implot.AxisFlags.NO_DECORATIONS)
        implot.setup_axes_limits(state["rect"][0, 0], state["rect"][1, 0], state["rect"][0, 1], state["rect"][1, 1], implot.Cond.ALWAYS)
        implot.plot_line("Signal 1", t, y_data1)
        implot.plot_line("Signal 2", t, y_data2)
        implot.plot_line("Signal 3", t, y_data3)
        implot.end_plot()
    implot.pop_style_color()
    imgui.text(f"Rect is {'not ' if not state['clicked'] else ''}clicked, {'not ' if not state['hovered'] else ''}hovered, {'not ' if not state['held'] else ''}held")
