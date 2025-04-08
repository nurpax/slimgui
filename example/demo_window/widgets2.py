
from slimgui import imgui, BoolRef, IntRef, Vec3Ref, Vec4Ref

refcol = (0.1, 0.2, 0.4, 1)
editing_col = Vec4Ref(0.5, 0.5, 0.5, 1)
col3 = Vec3Ref(0.1, 0.5, 0.5)

enable_clip_rect_ref = BoolRef(False)
style_mode_ref = IntRef(0)

def show():
    if not imgui.collapsing_header("Widgets 2"):
        return

    imgui.checkbox("Enable cliprect", enable_clip_rect_ref)
    mouse_pos = imgui.get_mouse_pos()
    if bool(enable_clip_rect_ref):
        p = mouse_pos
        imgui.push_clip_rect((p[0]+16, p[1]+16), (p[0]+128, p[1]+96), True)

    imgui.text("Random selection of widgets")
    imgui.color_picker4("##picker4", editing_col, imgui.ColorEditFlags.NO_SMALL_PREVIEW, refcol)
    imgui.text('Color btn'); imgui.same_line(); imgui.color_button("##color_button", editing_col.value)
    imgui.color_picker3("##picker3", col3)

    # Text links & open URL
    imgui.text_link("Link##link"); imgui.same_line(); imgui.text_link_open_url("URL##url", "https://github.com/nurpax/slimgui")

    if bool(enable_clip_rect_ref):
        imgui.pop_clip_rect()

    _show_dark_light_select()


def _show_dark_light_select():
    global style_mode_ref
    imgui.text("Dark/Light/Classic selection")
    changed = imgui.radio_button("Dark", style_mode_ref, 0)
    imgui.same_line()
    changed |= imgui.radio_button("Light", style_mode_ref, 1)
    imgui.same_line()
    changed |= imgui.radio_button("Classic", style_mode_ref, 2)

    if changed:
        if int(style_mode_ref) == 0:
            imgui.style_colors_dark()
        elif int(style_mode_ref) == 1:
            imgui.style_colors_light()
        elif int(style_mode_ref) == 2:
            imgui.style_colors_classic()
        else:
            assert False, "style_mode out of range"
