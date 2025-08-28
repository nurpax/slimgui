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


# -----------------------------------------------------------------------------
# [SECTION] Example App: Constrained Resize
# -----------------------------------------------------------------------------

FVec2 = tuple[float, float]

def _to_fixed_16(n: float) -> int:
    return round(n * 65536)

def _from_fixed_16(n: int) -> float:
    return n / 65536.0

def aspect_ratio_constraint_16_9(_pos:  FVec2, _current_size: FVec2, desired_size: FVec2, _user_int: int) -> FVec2:
    aspect_ratio = 16.0 / 9
    new_desired_y = int(desired_size[0] / aspect_ratio)
    return (desired_size[0], new_desired_y)

def aspect_ratio_constraint(_pos:  FVec2, _current_size: FVec2, desired_size: FVec2, int_user_data: int) -> FVec2:
    aspect_ratio = _from_fixed_16(int_user_data)
    new_desired_y = int(desired_size[0] / aspect_ratio)
    return (desired_size[0], new_desired_y)

def square_constraint(_pos: FVec2, _current_size: FVec2, desired_size: FVec2, _int_user_data: int) -> FVec2:
    size = max(desired_size[0], desired_size[1])
    return (size, size)

def step_constraint(_pos: FVec2, _current_size: FVec2, desired_size: FVec2, int_user_data: int):
    step = _from_fixed_16(int_user_data)
    new_size_x = int(desired_size[0] / step + 0.5) * step
    new_size_y = int(desired_size[1] / step + 0.5) * step
    return (new_size_x, new_size_y)

# Test descriptions
_test_desc = [
    "Between 100x100 and 500x500",
    "At least 100x100",
    "Resize vertical + lock current width",
    "Resize horizontal + lock current height",
    "Width Between 400 and 500",
    "Height at least 400",
    "Custom: Aspect Ratio 16:9",
    "Custom: Always Square",
    "Custom: Fixed Steps (100)"
]

# State for the demo window
_auto_resize = False
_window_padding = True
_constraint_type = 6  # Aspect Ratio
_display_lines = 10

def show_example_app_constrained_resize() -> bool:
    """Demonstrate creating a window with custom resize constraints."""
    global _auto_resize, _window_padding, _constraint_type, _display_lines

    # Constants
    aspect_ratio = 16.0 / 9.0
    fixed_step = 100.0
    float_max = imgui.FLT_MAX

    # Submit constraint
    if _constraint_type == 0:
        # Between 100x100 and 500x500
        imgui.set_next_window_size_constraints((100, 100), (500, 500))
    elif _constraint_type == 1:
        # Width > 100, Height > 100
        imgui.set_next_window_size_constraints((100, 100), (float_max, float_max))
    elif _constraint_type == 2:
        # Resize vertical + lock current width
        imgui.set_next_window_size_constraints((-1, 0), (-1, float_max))
    elif _constraint_type == 3:
        # Resize horizontal + lock current height
        imgui.set_next_window_size_constraints((0, -1), (float_max, -1))
    elif _constraint_type == 4:
        # Width Between 400 and 500
        imgui.set_next_window_size_constraints((400, -1), (500, -1))
    elif _constraint_type == 5:
        # Height at least 400
        imgui.set_next_window_size_constraints((-1, 400), (-1, float_max))
    elif _constraint_type == 6:
        # Aspect ratio
        imgui.set_next_window_size_constraints((0, 0), (float_max, float_max), aspect_ratio_constraint, _to_fixed_16(aspect_ratio))
    elif _constraint_type == 7:
        # Always Square
        imgui.set_next_window_size_constraints((0, 0), (float_max, float_max), square_constraint)
    elif _constraint_type == 8:
        # Fixed Step
        imgui.set_next_window_size_constraints((0, 0), (float_max, float_max), step_constraint, _to_fixed_16(fixed_step))

    # Submit window
    if not _window_padding:
        imgui.push_style_var(imgui.StyleVar.WINDOW_PADDING, (0.0, 0.0))

    window_flags = imgui.WindowFlags.ALWAYS_AUTO_RESIZE if _auto_resize else imgui.WindowFlags.NONE
    visible, show_window = imgui.begin("Example: Constrained Resize##python", flags=window_flags)

    if not _window_padding:
        imgui.pop_style_var()

    if visible:
        if imgui.get_io().key_shift:
            # Display a dummy viewport (in your real app you would likely use ImageButton() to display a texture)
            avail_size = imgui.get_content_region_avail()
            pos = imgui.get_cursor_screen_pos()
            imgui.color_button("viewport", (0.5, 0.2, 0.5, 1.0), imgui.ColorEditFlags.NO_TOOLTIP | imgui.ColorEditFlags.NO_DRAG_DROP, size=avail_size)
            imgui.set_cursor_screen_pos((pos[0] + 10, pos[1] + 10))
            imgui.text(f"{avail_size[0]:.2f} x {avail_size[1]:.2f}")
        else:
            imgui.text("(Hold SHIFT to display a dummy viewport)")
            if imgui.button("Set 200x200"):
                imgui.set_window_size((200, 200))
            imgui.same_line()
            if imgui.button("Set 500x500"):
                imgui.set_window_size((500, 500))
            imgui.same_line()
            if imgui.button("Set 800x200"):
                imgui.set_window_size((800, 200))

            imgui.set_next_item_width(imgui.get_font_size() * 20)
            _, _constraint_type = imgui.combo("Constraint", _constraint_type, _test_desc)

            imgui.set_next_item_width(imgui.get_font_size() * 20)
            _, _display_lines = imgui.drag_int("Lines", _display_lines, 0.2, 1, 100)

            _, _auto_resize = imgui.checkbox("Auto-resize", _auto_resize)
            _, _window_padding = imgui.checkbox("Window padding", _window_padding)

            for i in range(_display_lines):
                imgui.text(f"{' ' * (i * 4)}Hello, sailor! Making this line long enough for the example.")

    imgui.end()
    return show_window
