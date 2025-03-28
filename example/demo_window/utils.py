
from slimgui import imgui

def help_marker(desc: str):
    imgui.text_disabled("(?)")
    if imgui.begin_item_tooltip():
        imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
        imgui.text(desc)
        imgui.pop_text_wrap_pos()
        imgui.end_tooltip()
