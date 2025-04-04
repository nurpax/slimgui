import time
import numpy as np
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
