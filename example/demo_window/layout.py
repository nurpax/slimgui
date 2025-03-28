from slimgui import imgui
from slimgui.imgui import WindowFlags, ChildFlags

from .types import State

# //-----------------------------------------------------------------------------
# // [SECTION] Example App: Simple Layout / ShowExampleAppLayout()
# //-----------------------------------------------------------------------------

_selected = 0

def show_example_app_layout(st: State):
    global _selected
    imgui.set_next_window_size((500, 440), imgui.Cond.FIRST_USE_EVER)
    visible, st.show_app_layout = imgui.begin("Example: Simple layout", st.show_app_layout, WindowFlags.MENU_BAR)
    if visible:
        if imgui.begin_menu_bar():
            if imgui.begin_menu("File"):
                if imgui.menu_item("Close", "Ctrl+W")[0]:
                    st.show_app_layout = False
                imgui.end_menu()
            imgui.end_menu_bar()

        # Left
        imgui.begin_child("left pane", (150, 0), ChildFlags.BORDERS | ChildFlags.RESIZE_X)
        for i in range(100):
            if imgui.selectable(f'MyObject{i}', _selected == i)[0]:
                _selected = i
        imgui.end_child()
        imgui.same_line()

        # Right
        imgui.begin_group()
        imgui.begin_child("item view", (0, -imgui.get_frame_height_with_spacing()))
        imgui.text(f'MyObject: {_selected}')
        imgui.separator()
        if imgui.begin_tab_bar("##Tabs"):
            if imgui.begin_tab_item("Description")[0]:
                imgui.text_wrapped("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
                imgui.end_tab_item()
            if imgui.begin_tab_item("Details")[0]:
                imgui.text("ID: 0123456789")
                imgui.end_tab_item()
            imgui.end_tab_bar()
        imgui.end_child()
        if imgui.button("Revert"):
            pass
        imgui.same_line()
        if imgui.button("Save"):
            pass
        imgui.end_group()
        imgui.end()
