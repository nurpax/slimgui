import pytest
from slimgui import imgui, implot
import numpy as np
import sys
import gc

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

def test_plot_spec_array_backed_fields(frame_scope):
    xs = np.arange(4, dtype=np.float64)
    ys = np.array([0.0, 1.0, 0.5, 1.5], dtype=np.float64)
    colors = np.array([0xFF0000FF, 0xFF00FF00, 0xFFFF0000, 0xFFFFFFFF], dtype=np.uint32)
    marker_sizes = np.array([4.0, 6.0, 8.0, 10.0], dtype=np.float64)

    spec = implot.PlotSpec(line_colors=colors, marker_sizes=marker_sizes)
    assert spec.line_colors is colors
    assert spec.marker_sizes is marker_sizes

    colors[1] = 0xFF112233
    marker_sizes[2] = 12.0

    if implot.begin_plot("##plotspec-arrays", size=(-1, 80)):
        spec.marker = implot.Marker.CIRCLE
        implot.plot_line("line-colors", xs, ys, spec=spec)
        implot.plot_scatter("marker-sizes", xs, ys, spec=spec)
        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

def test_plot_spec_array_field_refcounts(frame_scope):
    colors = np.array([0xFF0000FF, 0xFF00FF00, 0xFFFF0000, 0xFFFFFFFF], dtype=np.uint32)
    spec = implot.PlotSpec()

    gc.collect()
    refcount = sys.getrefcount(colors)
    spec.line_colors = colors
    gc.collect()
    assert sys.getrefcount(colors) == refcount + 1

    if implot.begin_plot("##plotspec-refcounts", size=(-1, 80)):
        xs = np.arange(4, dtype=np.float64)
        ys = np.array([0.0, 1.0, 0.5, 1.5], dtype=np.float64)
        implot.plot_line("line-colors", xs, ys, spec=spec)
        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

    gc.collect()
    assert sys.getrefcount(colors) == refcount + 1

    spec.line_colors = None
    gc.collect()
    assert sys.getrefcount(colors) == refcount

def test_plot_spec_array_field_shape_validation(frame_scope):
    xs = np.arange(4, dtype=np.float64)
    ys = np.array([0.0, 1.0, 0.5, 1.5], dtype=np.float64)
    invalid_colors = np.zeros((2, 2), dtype=np.uint32)
    spec = implot.PlotSpec(line_colors=invalid_colors)

    if implot.begin_plot("##plotspec-shape", size=(-1, 80)):
        with pytest.raises(TypeError):
            implot.plot_line("invalid-shape", xs, ys, spec=spec)
        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"

def test_plot_spec_array_field_length_validation(frame_scope):
    xs = np.arange(4, dtype=np.float64)
    ys = np.array([0.0, 1.0, 0.5, 1.5], dtype=np.float64)
    short_colors = np.array([0xFF0000FF, 0xFF00FF00], dtype=np.uint32)
    spec = implot.PlotSpec(line_colors=short_colors)

    if implot.begin_plot("##plotspec-length", size=(-1, 80)):
        with pytest.raises(ValueError):
            implot.plot_line("invalid-length", xs, ys, spec=spec)
        implot.end_plot()
    else:
        assert False, "assert that begin_plot actually ran"
