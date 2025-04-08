import pytest
from slimgui import imgui, BoolRef, IntRef, FloatRef, StrRef, Vec2Ref, Vec3Ref, Vec4Ref, IntVec2Ref, IntVec3Ref, IntVec4Ref
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
    _visible = imgui.begin("Window")
    imgui.end()

def test_input_widgets(frame_scope):
    imgui.set_next_window_pos((10, 10))
    imgui.set_next_window_size((100, 100))
    visible = imgui.begin("Window")
    assert visible

    # The value shouldn't change when going through drag_float
    vref = FloatRef(0.5)
    changed = imgui.drag_float("DragFloat", vref)
    assert not changed
    assert vref == 0.5

    v2ref = Vec2Ref(0.5, 1)
    changed = imgui.drag_float2("DragFloat", v2ref)
    assert not changed
    assert v2ref.value == (0.5, 1)

    v3ref = Vec3Ref(0.5, 1, 2)
    changed = imgui.drag_float3("DragFloat", v3ref)
    assert not changed
    assert v3ref == (0.5, 1, 2)

    v4ref = Vec4Ref(0.5, 1, 2, 4)
    changed = imgui.drag_float4("DragFloat", v4ref)
    assert not changed
    assert v4ref == (0.5, 1, 2, 4)

    str_ref = StrRef("this is text 🔥")
    imgui.input_text("##label", str_ref)
    assert not changed
    assert str_ref == "this is text 🔥"

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

def test_reftypes():
    '''Sanity checks for RefType constructors.'''
    br = BoolRef(True)
    assert br.value
    assert br
    br_not = BoolRef(False)
    assert not br_not.value
    assert not br_not

    assert IntRef(42) == 42
    assert IntRef(42).value == 42

    assert FloatRef(0.5) == 0.5
    assert FloatRef(0.25).value == 0.25
    assert FloatRef(0.25) != 0.5

    assert Vec2Ref(1.5, 2).value == (1.5, 2)
    assert Vec2Ref((1.5, 2)) == (1.5, 2)
    assert Vec3Ref(1.5, 2, 3) == (1.5, 2, 3)
    assert Vec3Ref((4, 5, 6)) == (4, 5, 6,)
    with pytest.raises(TypeError):
        Vec3Ref(1, 2, 3, 4) # pyright: ignore
    with pytest.raises(TypeError):
        Vec3Ref('break it') # pyright: ignore
    assert Vec4Ref(1.5, 2, 3, 4).value == (1.5, 2, 3, 4)
    assert Vec4Ref((4, 5, 6, 7.5)) == (4, 5, 6, 7.5)

    assert IntVec2Ref(1, 2).value == (1, 2)
    assert IntVec2Ref((4, 5)) == (4, 5)
    with pytest.raises(TypeError):
        IntVec2Ref(1, 2, 3) # pyright: ignore
    with pytest.raises(TypeError):
        IntVec2Ref('break it') # pyright: ignore
    assert IntVec3Ref(1, 2, 3) == (1, 2, 3)
    assert IntVec3Ref((4, 5, 6)) == (4, 5, 6)
    with pytest.raises(TypeError):
        IntVec3Ref(1, 2, 3, 4) # pyright: ignore
    with pytest.raises(TypeError):
        IntVec3Ref('break it') # pyright: ignore
    assert IntVec4Ref(1, 2, 3, 4).value == (1, 2, 3, 4)
    assert IntVec4Ref((4, 5, 6, 7)) == (4, 5, 6, 7)
    with pytest.raises(TypeError):
        IntVec4Ref(1, 2, 3) # pyright: ignore
    with pytest.raises(TypeError):
        IntVec4Ref('break it') # pyright: ignore
