import pytest
from slimgui import imgui
import numpy as np

# Define a fixture
@pytest.fixture
def imgui_context():
    imgui.set_nanobind_leak_warnings(True)
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
    null_renderer.refresh_font_texture()
    imgui.new_frame()

def test_utility_funcs():
    assert imgui.get_style_color_name(imgui.Col.TITLE_BG_ACTIVE) == "TitleBgActive"

    assert imgui.color_convert_float4_to_u32((1, 1, 1, 1)) == 0xffffffff
    assert imgui.color_convert_float4_to_u32((1, 1, 1, 0)) == 0x00ffffff
    assert imgui.color_convert_float4_to_u32((0.5, 0.25, 0.125, 0)) == 0x00204080
    assert imgui.color_convert_u32_to_float4(0xffffffff) == (1, 1, 1, 1)
    assert imgui.color_convert_u32_to_float4(0xffff0000) == (0, 0, 1, 1)
    assert imgui.color_convert_u32_to_float4(0xff0000ff) == (1, 0, 0, 1)

def test_current_context(imgui_context):
    assert imgui_context is not None
    assert imgui.get_current_context() is not None
    assert imgui_context is imgui.get_current_context()

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

def test_set_current_context(imgui_context):
    assert imgui_context is not None
    assert imgui.get_current_context() is not None
    assert imgui_context is imgui.get_current_context()

    ctx2 = imgui.create_context()
    assert ctx2 is imgui.get_current_context()
    assert imgui_context is not imgui.get_current_context()
    c = imgui.get_current_context()
    assert c is not None
    assert imgui_context.context is not c.context
    imgui.set_current_context(imgui_context)
    assert imgui_context is imgui.get_current_context()
    c = imgui.get_current_context()
    assert c is not None
    assert imgui_context.context is c.context
    imgui.set_current_context(ctx2)
    imgui.destroy_context(None)
    assert imgui.get_current_context() is None
    imgui.set_current_context(imgui_context)
    assert imgui_context is imgui.get_current_context()


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

def test_draw_list(frame_scope):
    color = imgui.color_convert_float4_to_u32((0.5, 0.6, 0.1, 1.0))
    dl = imgui.get_window_draw_list()
    vertices = np.array([[3, 3], [4, 1], [5, 4], [2, 5], [1, 3]], dtype=np.float32)
    dl.add_concave_poly_filled(vertices, color)
    vertices[:, 0] += 50
    dl.add_concave_poly_filled(list(vertices), color)

    vert_wrong_shape = np.array([[3, 3, 0], [4, 1,0 ], [5, 4, 0], [2, 5, 0], [1, 3, 0]], dtype=np.float32)
    assert vert_wrong_shape.shape[1] == 3
    with pytest.raises(TypeError):
        dl.add_concave_poly_filled(vert_wrong_shape, color)
    vert = np.array([[3, 3], [4, 1], [5, 4], [2, 5], [1, 3]], dtype=np.float32)
    assert vert.shape[1] == 2
    dl.add_concave_poly_filled(vert, color) # should work
    dl.add_concave_poly_filled(vert.astype(np.int32), color) # should work too, autocast to float

def test_drag_drop(frame_scope):
    imgui.dummy((10,10))
    pl = imgui.get_drag_drop_payload()
    assert pl is None
    r = imgui.begin_drag_drop_target()
    assert not r # should return False because there's no previous draggable item

    if imgui.begin_drag_drop_source():
        imgui.end_drag_drop_source()

def test_drawlist_refcounts(imgui_context, frame_scope):
    # Note: this test relies on some internal properties.  You should not
    # need to access the internals like this.
    import sys

    ctx = imgui_context.context
    fg_dl = ctx.get_foreground_draw_list_internal()
    refcount1 = sys.getrefcount(fg_dl)
    assert refcount1 == 2
    fg_dl2 = ctx.get_foreground_draw_list_internal()
    assert fg_dl.ptr() == fg_dl2.ptr()
    # refcount increased, let's assume that's because fg_dl and fg_dl2 both point to the
    # same thing.
    assert sys.getrefcount(fg_dl) == refcount1 + 1
    assert fg_dl is fg_dl2

    bg_dl = ctx.get_background_draw_list_internal()
    assert sys.getrefcount(bg_dl) == 2
    assert fg_dl is not bg_dl


def test_drawlist_refcounts2(imgui_context, frame_scope):
    # Note: this test relies on some internal properties.  You should not
    # need to access the internals like this.
    import sys, gc

    ctx = imgui_context.context
    fg_dl = ctx.get_foreground_draw_list_internal()
    refcount1 = sys.getrefcount(fg_dl)
    assert refcount1 == 2  # fg_dl holds +1, call to sys.getrefcount with fg_dl another +1

    # Next use the DrawList wrapper API (the one that user's of this package
    # are expected to use).  The wrapping business should be reflected in fg_dl
    # refcounts.
    wrapped_fg_dl = imgui.get_foreground_draw_list()
    assert sys.getrefcount(fg_dl) == refcount1 + 1 # wrapper_fg_dl._dl for +1 refcount

    tmp = wrapped_fg_dl._dl
    assert sys.getrefcount(tmp) == refcount1 + 2  # wrapped_fg_dl +1, tmp +1
    del tmp

    assert fg_dl is wrapped_fg_dl._dl
    assert sys.getrefcount(fg_dl) == refcount1 + 1
    del wrapped_fg_dl
    assert sys.getrefcount(fg_dl) == refcount1 + 1 # fg_dl kept alive by the dl wrapper stored into context

    # But an imgui.new_frame() call should clear the references.
    imgui.end_frame()
    imgui.new_frame()
    gc.collect()
    assert sys.getrefcount(fg_dl) == refcount1 # fg_dl now kept alive only by fg_dl variable + getrefcount temporary, just like above
