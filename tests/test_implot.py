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
    implot.set_next_marker_style(-1) # both variants should work for this function
    implot.set_next_marker_style(implot.Marker.CIRCLE)

    implot.style_colors_classic()
    implot.style_colors_classic(implot.get_style())

    assert implot.get_style_color_name(implot.Col.MARKER_OUTLINE) == 'MarkerOutline'
    assert implot.get_marker_name(implot.Marker.DIAMOND) == 'Diamond'

    implot.push_style_var(implot.StyleVar.MARKER_SIZE, 10)
    implot.push_style_var(implot.StyleVar.MARKER_SIZE, 10.5)
    implot.pop_style_var(2)
