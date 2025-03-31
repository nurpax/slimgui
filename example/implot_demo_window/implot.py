from slimgui import imgui
from slimgui import implot

def show_demo_window(show_window: bool):
    main_viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos((main_viewport.work_pos[0] + 640, main_viewport.work_pos[1] + 120), imgui.Cond.FIRST_USE_EVER)
    imgui.set_next_window_size((500, 680), imgui.Cond.FIRST_USE_EVER)

    visible, show_window = imgui.begin("Implot tests", closable=show_window)
    if not visible:
        imgui.end()
        return show_window

    imgui.end()
    return show_window
