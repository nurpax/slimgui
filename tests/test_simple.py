import pytest
import slimgui as imgui

# Define a fixture
@pytest.fixture
def imgui_context():
    ctx = imgui.create_context()
    yield ctx
    imgui.destroy_context(ctx)

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
