import numpy as np

from slimgui import implot

from .meta import example


@example(category="ImPlot", title="Line plot from x/y arrays")
def plot_line_basic():
    """
    Plot a line from explicit `x` and `y` NumPy arrays.

    This is the most direct `implot.plot_line()` calling pattern: prepare one array for x-coordinates
    and one array for y-values, then submit both arrays inside a `begin_plot()` / `end_plot()` block.
    Use this form when your x-axis is not just an implicit sample index and you want full control over
    the horizontal values shown in the plot.
    """
    xs = np.linspace(0.0, 10.0, 200)
    ys = np.sin(xs)

    if implot.begin_plot("Line Plot"):
        implot.plot_line("sin(x)", xs, ys)
        implot.end_plot()


@example(category="ImPlot", title="Line plot from values only")
def plot_line_values_only():
    """
    Plot a line from a single value array and let ImPlot infer the x-axis from the sample index.

    This overload is useful when you only have y-values and want evenly spaced samples without creating
    a separate x-array yourself. It is a compact way to plot a waveform or time series when the natural
    x-coordinate is just "point 0, point 1, point 2, ...".
    """
    ys = np.sin(np.linspace(0.0, 3.0 * np.pi, 200))

    if implot.begin_plot("Values Only"):
        implot.plot_line("wave", ys)
        implot.end_plot()


@example(category="ImPlot", title="Bar plot from values")
def plot_bars_basic():
    """
    Plot bars from a one-dimensional NumPy array.

    `implot.plot_bars()` can consume a single array of values and place each bar at the corresponding
    sample index. This is the simplest form for categorical or small summary data when you do not need
    custom x-positions for the bars.
    """
    ys = np.array([0.3, 0.8, 0.55, 0.9, 0.45], dtype=np.float32)

    if implot.begin_plot("Bars"):
        implot.plot_bars("bars", ys)
        implot.end_plot()


@example(category="ImPlot", title="Grouped bar plot")
def plot_bar_groups_basic():
    """
    Plot grouped bars from a two-dimensional NumPy array.

    `implot.plot_bar_groups()` expects tabular data where each row represents one labeled series and
    each column represents one group position. The call to `setup_axes()` removes axis decorations here
    so the grouped structure is easier to focus on in the example screenshot.
    """
    values = np.array(
        [
            [0.2, 0.4, 0.7, 0.5],
            [0.6, 0.3, 0.5, 0.8],
            [0.4, 0.7, 0.2, 0.6],
        ],
        dtype=np.float32,
    )

    if implot.begin_plot("Grouped Bars"):
        implot.setup_axes(
            None,
            None,
            implot.AxisFlags.NO_DECORATIONS,
            implot.AxisFlags.NO_DECORATIONS,
        )
        implot.plot_bar_groups(["A", "B", "C"], values)
        implot.end_plot()


@example(category="ImPlot", title="Scatter plot from x/y arrays")
def plot_scatter_basic():
    """
    Plot scatter points from x/y NumPy arrays.

    Scatter plots use the same explicit x/y array pattern as line plots, but render disconnected points
    instead of a continuous curve. This example builds a simple spiral from polar coordinates to show that
    the points do not need to lie on a regular grid or be evenly spaced.
    """
    theta = np.linspace(0.0, 4.0 * np.pi, 80)
    radius = np.linspace(0.2, 1.0, 80)
    xs = radius * np.cos(theta)
    ys = radius * np.sin(theta)

    if implot.begin_plot("Scatter"):
        implot.plot_scatter("spiral", xs, ys)
        implot.end_plot()
