
from slimgui import imgui
import numpy as np
from dataclasses import dataclass

edit_color: tuple = (0.5, 0.6, 0.1, 1.0)
tex = None

@dataclass
class CustomState:
    sz: float = 36.0
    thickness: float = 3.0
    ngon_sides: int = 6
    circle_segments_override: bool = False
    circle_segments_override_v: int = 12
    curve_segments_override: bool = False
    curve_segments_override_v: int = 8
    colf: tuple[float, float, float, float] = (1.0, 1.0, 0.4, 1.0)

# Global state instance
_custom = CustomState()

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


def _path_concave_shape(draw_list: imgui.DrawList, x: float, y: float, sz: float):
    pos_norms = [
        (0, 0), (0.3, 0), (0.3, 0.7), (0.7, 0.7), (0.7, 0), (1, 0), (1, 1), (0, 1)
    ]
    for p in pos_norms:
        draw_list.path_line_to((x + 0.5 + int(sz*p[0]), y + 0.5 + int(sz*p[1])))


def custom_rendering() -> bool:
    """Demonstrate using the low-level ImDrawList to draw custom shapes."""
    visible, show_window = imgui.begin("Example: Custom rendering##py_custom", closable=True)
    if not visible:
        imgui.end()
        return show_window

    if imgui.begin_tab_bar("##TabBar"):
        if imgui.begin_tab_item("Primitives")[0]:
            imgui.push_item_width(-imgui.get_font_size() * 15)
            draw_list = imgui.get_window_draw_list()

            # Draw gradients
            imgui.text("Gradients")
            gradient_size = (imgui.calc_item_width(), imgui.get_frame_height())

            # First gradient (black->white)
            p0 = imgui.get_cursor_screen_pos()
            p1 = (p0[0] + gradient_size[0], p0[1] + gradient_size[1])
            col_a = imgui.get_color_u32((0, 0, 0, 1))
            col_b = imgui.get_color_u32((1, 1, 1, 1))
            draw_list.add_rect_filled_multi_color(p0, p1, col_a, col_b, col_b, col_a)
            imgui.invisible_button("##gradient1", gradient_size)

            # Second gradient (green->red)
            p0 = imgui.get_cursor_screen_pos()
            p1 = (p0[0] + gradient_size[0], p0[1] + gradient_size[1])
            col_a = imgui.get_color_u32((0, 1, 0, 1))
            col_b = imgui.get_color_u32((1, 0, 0, 1))
            draw_list.add_rect_filled_multi_color(p0, p1, col_a, col_b, col_b, col_a)
            imgui.invisible_button("##gradient2", gradient_size)

            # Draw a bunch of primitives
            imgui.text("All primitives")

            # Update static variables
            _, _custom.sz = imgui.drag_float("Size", _custom.sz, 0.2, 2.0, 100.0, "%.0f")
            _, _custom.thickness = imgui.drag_float("Thickness", _custom.thickness, 0.05, 1.0, 8.0, "%.02f")
            _, _custom.ngon_sides = imgui.slider_int("N-gon sides", _custom.ngon_sides, 3, 12)

            _, _custom.circle_segments_override = imgui.checkbox("##circlesegmentoverride", _custom.circle_segments_override)
            imgui.same_line(0.0, imgui.get_style().item_inner_spacing[0])
            changed, _custom.circle_segments_override_v = imgui.slider_int(
                "Circle segments override", _custom.circle_segments_override_v, 3, 40
            )
            _custom.circle_segments_override |= changed

            _, _custom.curve_segments_override = imgui.checkbox("##curvessegmentoverride", _custom.curve_segments_override)
            imgui.same_line(0.0, imgui.get_style().item_inner_spacing[0])
            changed, _custom.curve_segments_override_v = imgui.slider_int(
                "Curves segments override", _custom.curve_segments_override_v, 3, 40
            )
            _custom.curve_segments_override |= changed

            _, _custom.colf = imgui.color_edit4("Color", _custom.colf)

            p = imgui.get_cursor_screen_pos()
            col = imgui.color_convert_float4_to_u32(_custom.colf)
            spacing = 10.0
            corners_tl_br = imgui.DrawFlags.ROUND_CORNERS_TOP_LEFT | imgui.DrawFlags.ROUND_CORNERS_BOTTOM_RIGHT
            rounding = _custom.sz / 5.0
            circle_segments = _custom.circle_segments_override_v if _custom.circle_segments_override else 0
            curve_segments = _custom.curve_segments_override_v if _custom.curve_segments_override else 0

            # Control points for curves
            sz = _custom.sz
            cp3 = [(0.0, sz * 0.6),
                   (sz * 0.5, -sz * 0.4),
                   (sz, sz)]

            cp4 = [(0.0, 0.0),
                   (sz * 1.3, sz * 0.3),
                   (sz - sz * 1.3, sz - sz * 0.3),
                   (sz, sz)]

            x = p[0] + 4.0
            y = p[1] + 4.0

            # Draw shapes with outline
            for n in range(2):
                # First line uses a thickness of 1.0f, second line uses the configurable thickness
                th = 1.0 if n == 0 else _custom.thickness

                # N-gon
                draw_list.add_ngon((x + sz*0.5, y + sz*0.5), sz*0.5, col, _custom.ngon_sides, th)
                x += sz + spacing

                # Circle
                draw_list.add_circle((x + sz*0.5, y + sz*0.5), sz*0.5, col, circle_segments, th)
                x += sz + spacing

                # Ellipse
                draw_list.add_ellipse((x + sz*0.5, y + sz*0.5), (sz*0.5, sz*0.3), col, -0.3, circle_segments, th)
                x += sz + spacing

                # Square
                draw_list.add_rect((x, y), (x + sz, y + sz), col, 0.0, thickness=th)
                x += sz + spacing

                # Square with all rounded corners
                draw_list.add_rect((x, y), (x + sz, y + sz), col, rounding, thickness=th)
                x += sz + spacing

                # Square with two rounded corners
                draw_list.add_rect((x, y), (x + sz, y + sz), col, rounding, corners_tl_br, th)
                x += sz + spacing

                # Triangle
                draw_list.add_triangle((x+sz*0.5,y), (x+sz, y+sz-0.5), (x, y+sz-0.5), col, th)
                x += sz + spacing

                _path_concave_shape(draw_list, x, y, sz)
                draw_list.path_stroke(col, imgui.DrawFlags.CLOSED, th)
                x += sz + spacing

                # Lines
                draw_list.add_line((x, y), (x + sz, y), col, th)  # Horizontal
                x += sz + spacing

                draw_list.add_line((x, y), (x, y + sz), col, th)  # Vertical
                x += spacing

                draw_list.add_line((x, y), (x + sz, y + sz), col, th)  # Diagonal
                x += sz + spacing

                # Arc
                draw_list.path_arc_to((x + sz*0.5, y + sz*0.5), sz*0.5, 3.141592, 3.141592 * -0.5)
                draw_list.path_stroke(col, imgui.DrawFlags.NONE, th)
                x += sz + spacing

                # Bezier curves
                # Quadratic Bezier (3 control points)
                draw_list.add_bezier_quadratic(
                    (x + cp3[0][0], y + cp3[0][1]),
                    (x + cp3[1][0], y + cp3[1][1]),
                    (x + cp3[2][0], y + cp3[2][1]),
                    col, th, curve_segments)
                x += sz + spacing

                # Cubic Bezier (4 control points)
                draw_list.add_bezier_cubic(
                    (x + cp4[0][0], y + cp4[0][1]),
                    (x + cp4[1][0], y + cp4[1][1]),
                    (x + cp4[2][0], y + cp4[2][1]),
                    (x + cp4[3][0], y + cp4[3][1]),
                    col, th, curve_segments)

                x = p[0] + 4.0
                y += sz + spacing

            # Draw filled shapes
            # N-gon
            draw_list.add_ngon_filled((x + sz * 0.5, y + sz * 0.5), sz * 0.5, col, _custom.ngon_sides)
            x += sz + spacing

            # Circle
            draw_list.add_circle_filled((x + sz * 0.5, y + sz * 0.5), sz * 0.5, col, circle_segments)
            x += sz + spacing

            # Ellipse
            draw_list.add_ellipse_filled((x + sz * 0.5, y + sz * 0.5), (sz * 0.5, sz * 0.3), col, -0.3, circle_segments)
            x += sz + spacing

            # Square
            draw_list.add_rect_filled((x, y), (x + sz, y + sz), col)
            x += sz + spacing

            # Square with all rounded corners
            draw_list.add_rect_filled((x, y), (x + sz, y + sz), col, 10.0)
            x += sz + spacing

            # Square with two rounded corners
            draw_list.add_rect_filled((x, y), (x + sz, y + sz), col, 10.0, corners_tl_br)
            x += sz + spacing

            # Triangle
            draw_list.add_triangle_filled((x+sz*0.5,y), (x+sz, y+sz-0.5), (x, y+sz-0.5), col)
            x += sz + spacing

            _path_concave_shape(draw_list, x, y, sz)
            draw_list.path_fill_concave(col)
            x += sz + spacing

            # Lines
            draw_list.add_rect_filled((x, y), (x + sz, y + _custom.thickness), col)  # Horizontal
            x += sz + spacing

            draw_list.add_rect_filled((x, y), (x + _custom.thickness, y + sz), col)  # Vertical
            x += spacing * 2.0

            draw_list.add_rect_filled((x, y), (x + 1, y + 1), col)  # Pixel
            x += sz

            # Path filled arc
            draw_list.path_arc_to((x + sz * 0.5, y + sz * 0.5), sz * 0.5, 3.141592 * -0.5, 3.141592)
            draw_list.path_fill_convex(col)
            x += sz + spacing

            # Quadratic bezier path
            draw_list.path_line_to((x + cp3[0][0], y + cp3[0][1]))
            draw_list.path_bezier_quadratic_curve_to(
                (x + cp3[1][0], y + cp3[1][1]),
                (x + cp3[2][0], y + cp3[2][1]),
                curve_segments
            )
            draw_list.path_fill_convex(col)
            x += sz + spacing

            # Multi-colored rectangle
            draw_list.add_rect_filled_multi_color(
                (x, y), (x + sz, y + sz),
                imgui.color_convert_float4_to_u32((0, 0, 0, 1)),
                imgui.color_convert_float4_to_u32((1, 0, 0, 1)),
                imgui.color_convert_float4_to_u32((1, 1, 0, 1)),
                imgui.color_convert_float4_to_u32((0, 1, 0, 1))
            )
            x += sz + spacing

            imgui.dummy(((sz + spacing) * 13.2, (sz + spacing) * 3.0))
            imgui.pop_item_width()
            imgui.end_tab_item()

        imgui.end_tab_bar()

    imgui.end()
    return show_window
