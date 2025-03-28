
from slimgui import imgui

refcol = (0.1, 0.2, 0.4, 1)
editing_col = (0.5, 0.5, 0.5, 1)
col3 = (0.1, 0.5, 0.5)

enable_clip_rect = False

style_mode = 0

def show():
    global editing_col, col3, enable_clip_rect

    expanded, _ = imgui.collapsing_header("Widgets 2")
    if not expanded:
        return

    _c, enable_clip_rect = imgui.checkbox("Enable cliprect", enable_clip_rect)
    mouse_pos = imgui.get_mouse_pos()
    if enable_clip_rect:
        p = mouse_pos
        imgui.push_clip_rect((p[0]+16, p[1]+16), (p[0]+128, p[1]+96), True)

    imgui.text("Random selection of widgets")
    _c, editing_col = imgui.color_picker4("##picker4", editing_col, imgui.ColorEditFlags.NO_SMALL_PREVIEW, refcol)
    imgui.text('Color btn'); imgui.same_line(); imgui.color_button("##color_button", editing_col)
    _c, col3 = imgui.color_picker3("##picker3", col3)

    # Text links & open URL
    imgui.text_link("Link##link"); imgui.same_line(); imgui.text_link_open_url("URL##url", "https://github.com/nurpax/slimgui")

    if enable_clip_rect:
        imgui.pop_clip_rect()

    _show_dark_light_select()


def _show_dark_light_select():
    global style_mode
    imgui.text("Dark/Light/Classic selection")
    changed, style_mode = imgui.radio_button("Dark", style_mode, 0)
    imgui.same_line()
    c, style_mode = imgui.radio_button("Light", style_mode, 1)
    changed |= c
    imgui.same_line()
    c, style_mode = imgui.radio_button("Classic", style_mode, 2)
    changed |= c

    if changed:
        if style_mode == 0:
            imgui.style_colors_dark()
        elif style_mode == 1:
            imgui.style_colors_light()
        elif style_mode == 2:
            imgui.style_colors_classic()
        else:
            assert False, "style_mode out of range"
