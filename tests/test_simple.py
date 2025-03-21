import pytest
import slimgui as imgui

# Define a fixture
@pytest.fixture
def imgui_context():
    ctx = imgui.create_context()
    imgui.get_io().ini_filename = None
    yield ctx
    imgui.destroy_context(ctx)

@pytest.fixture
def null_renderer(imgui_context):
    from slimgui.integrations.null import NullRenderer
    renderer = NullRenderer()
    yield renderer

@pytest.fixture
def frame_scope(imgui_context, null_renderer):
    io = imgui.get_io()
    io.display_size = 320, 200
    imgui.new_frame()

def test_current_context(imgui_context):
    assert imgui_context is not None
    assert imgui.get_current_context() is not None
    assert imgui_context == imgui.get_current_context()

def test_style_access(imgui_context):
    styles = imgui.get_style()
    for k, v in zip(imgui.Col, styles.colors):
        assert imgui.get_style().colors[k] == v
    assert styles.alpha == 1
    styles.alpha = 0.25
    assert styles.alpha == 0.25
    assert styles.window_padding == (8, 8)
    styles.window_padding = (2, 4)
    assert styles.window_padding == (2, 4)

def test_begin_base_window(frame_scope):
    visible, _ = imgui.begin("Window")
    imgui.end()

def test_input_widgets(frame_scope):
    imgui.set_next_window_pos((10, 10))
    imgui.set_next_window_size((100, 100))
    visible, _ = imgui.begin("Window")
    assert visible

    # The value shouldn't change when going through drag_float
    changed, v = imgui.drag_float("DragFloat", 0.5)
    assert not changed
    assert v == 0.5

    changed, v = imgui.drag_float2("DragFloat", (0.5, 1))
    assert not changed
    assert v == (0.5, 1)

    changed, v = imgui.drag_float3("DragFloat", (0.5, 1, 2))
    assert not changed
    assert v == (0.5, 1, 2)

    changed, v = imgui.drag_float4("DragFloat", (0.5, 1, 2, 4))
    assert not changed
    assert v == (0.5, 1, 2, 4)

    changed, t = imgui.input_text("##label", "this is text 🔥")
    assert not changed
    assert t == "this is text 🔥"

    imgui.end()
