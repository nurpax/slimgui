import numpy as np
from slimgui import imgui
from slimgui import implot

from slimgui.implot import LineFlags, PlotFlags, ScatterFlags

def show_demo_window(show_window: bool):
    main_viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos((main_viewport.work_pos[0] + 800, main_viewport.work_pos[1] + 40), imgui.Cond.FIRST_USE_EVER)
    imgui.set_next_window_size((640, 1000), imgui.Cond.FIRST_USE_EVER)

    visible, show_window = imgui.begin("Implot tests", closable=show_window)
    if not visible:
        imgui.end()
        return show_window

    if imgui.collapsing_header('Basic line plots')[0]:
        if implot.begin_plot("Plot", flags=PlotFlags.NO_LEGEND):
            data_x = np.arange(0, 10, 0.25)
            data_y = np.sin(data_x)
            implot.plot_line("Sine Wave", data_y[::2]) # striding should work
            implot.plot_line("Sine Wave 2", data_x, np.abs(data_y))
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

    imgui.end()
    return show_window
