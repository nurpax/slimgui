
from slimgui import imgui
import numpy as np

edit_color: tuple = (0.5, 0.6, 0.1, 1.0)
tex = None

def show(tex_id: int):
    global edit_color

    expanded, _ = imgui.collapsing_header("DrawLists")
    if not expanded:
        return

    _c, edit_color = imgui.color_edit4("Color", edit_color)
    _render_shapes(tex_id)


def _render_shapes(tex_id: int):
    px, py = imgui.get_cursor_screen_pos()
    dl = imgui.get_window_draw_list()
    color = imgui.color_convert_float4_to_u32(edit_color)
    color2 = imgui.color_convert_float4_to_u32((0.5, 0.6, 0.5, 1.0))
    color3 = imgui.color_convert_float4_to_u32((0.2, 0.4, 0.8, 1))
    dl.add_line((px + 10, py + 10), (px + 50, py + 50), color, 1)
    dl.add_rect((px + 60, py + 10), (px + 100, py + 50), color, rounding=5)
    dl.add_quad_filled((px + 110, py + 10), (px + 150, py + 10), (px + 150, py + 50), (px + 110, py + 50), color2)
    dl.add_ellipse_filled((px + 180, py + 30), (20, 10), color2, num_segments=9, rot=imgui.get_time() * 0.5)
    dl.add_triangle_filled((px + 200, py + 10), (px + 240, py + 10), (px + 220, py + 50), color)
    dl.add_text((px + 250, py + 17), color, "hello")
    dl.add_bezier_quadratic((px + 300, py + 15), (px + 340, py + 15), (px + 340, py + 40), color3, thickness=2)
    dl.add_polyline([(px + 350, py + 10), (px + 370, py + 10), (px + 370, py + 50), (px + 350, py + 50)], color3, flags=imgui.DrawFlags.CLOSED, thickness=2)
    arr = np.array([(px + 350, py + 10), (px + 370, py + 10), (px + 370, py + 50), (px + 350, py + 50)], dtype=np.float32)
    dl.add_polyline(arr + np.array([25, 0], dtype=np.float32), color3, flags=imgui.DrawFlags.CLOSED, thickness=2)

    vertices = np.array([[1, 1], [4, 1], [5, 4], [2, 5], [1, 3]], dtype=np.float32)
    vertices = vertices * 10
    vertices[:, 0] += px
    vertices[:, 1] += py + 50
    dl.add_convex_poly_filled(list(vertices), color2)

    vertices = np.array([[3, 3], [4, 1], [5, 4], [2, 5], [1, 3]], dtype=np.float32)
    vertices = vertices * 10
    vertices[:, 0] += px + 50
    vertices[:, 1] += py + 50
    dl.add_concave_poly_filled(vertices.astype(np.int32), color2) # cast to int, that should work too
    vertices[:, 0] += 50
    dl.add_concave_poly_filled(list(vertices), color)

    xx = px + 10
    yy = py + 100
    dl.add_image(tex_id, (xx, yy), (xx + 128, yy + 128), col=0xff70ff30)

    xx += 130
    dl.add_image_rounded(tex_id, (xx, yy), (xx + 128, yy + 128), (0,0), (1, 1), 0xffffffff, rounding=10)
