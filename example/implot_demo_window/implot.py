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

    imgui.end()
    return show_window
