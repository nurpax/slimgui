import pytest
from slimgui import imgui, implot
import numpy as np

# Define a fixture
@pytest.fixture
def context():
    imgui.set_nanobind_leak_warnings(True)
    ctx = imgui.create_context()
    implot_ctx = implot.create_context()
    imgui.get_io().ini_filename = None
    yield
    implot.destroy_context(implot_ctx)
    imgui.destroy_context(ctx)

@pytest.fixture
def null_renderer(context):
    from slimgui.integrations.null import NullRenderer
    renderer = NullRenderer()
    yield renderer

@pytest.fixture
def frame_scope(context, null_renderer):
    io = imgui.get_io()
    io.display_size = 640, 800
    null_renderer.refresh_font_texture()
    imgui.new_frame()

def test_setup_axis_ticks(frame_scope):
    if implot.begin_plot("##ticks", size=(-1, 40)):
        labels = ['S1', 'S2', 'S4', 'S4']
        xs = np.arange(4)
        implot.setup_axis_ticks(implot.Axis.X1, xs, labels)
        ys = np.random.RandomState(16).rand(4)
        implot.plot_bars("rand", ys)
        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

    # error checks
    if implot.begin_plot("##ticks2", size=(-1, 40)):
        labels = ['S1', 'S2', 'S4', 'S4', 'ONE TOO MANY']
        xs = np.arange(4)

        with pytest.raises(ValueError):
            implot.setup_axis_ticks(implot.Axis.X1, xs, labels)

        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

    # error checks
    if implot.begin_plot("##ticks3", size=(-1, 40)):
        labels = ['S1', 'S2', 'S4', 'S4']
        xs = np.arange(4)

        with pytest.raises(ValueError):
            implot.setup_axis_ticks(implot.Axis.X1, 0, 10, 5, labels) # test n_ticks != len(labels)

        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

def test_random_getter_setters(frame_scope):
    spec = implot.PlotSpec()
    spec.marker = -1  # both variants should work for this field
    spec.marker = implot.Marker.CIRCLE

    implot.style_colors_classic()
    implot.style_colors_classic(implot.get_style())

    assert implot.get_style_color_name(implot.Col.AXIS_TEXT) == 'AxisText'
    assert implot.get_marker_name(implot.Marker.DIAMOND) == 'Diamond'

    implot.push_style_var(implot.StyleVar.PLOT_BORDER_SIZE, 10)
    implot.push_style_var(implot.StyleVar.PLOT_BORDER_SIZE, 10.5)
    implot.pop_style_var(2)

def test_plot_spec_defaults_and_override(frame_scope):
    xs = np.arange(4, dtype=np.float64)
    ys = np.array([0.0, 1.0, 0.5, 1.5], dtype=np.float64)

    if implot.begin_plot("##plotspec", size=(-1, 80)):
        implot.plot_line("default-spec", xs, ys)  # spec defaults to None / ImPlotSpec()

        spec = implot.PlotSpec()
        spec.line_weight = 2.5
        spec.marker = implot.Marker.CIRCLE
        spec.marker_size = 6.0
        implot.plot_scatter("custom-spec", xs, ys, spec=spec)

        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"
