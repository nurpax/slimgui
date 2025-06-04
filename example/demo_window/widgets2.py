import pickle
from typing import Literal
from slimgui import imgui
from .utils import help_marker
refcol = (0.1, 0.2, 0.4, 1)
editing_col = (0.5, 0.5, 0.5, 1)
col3 = (0.1, 0.5, 0.5)

enable_clip_rect = False

style_mode = 0

def show():
    global editing_col, col3, enable_clip_rect

    _drag_and_drop()

    _show_shortcut_demo()

    _show_input_state_demo()

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

_col1 = (1, 0, 0.2 )
_col2 = (0.4, 0.7, 0.0, 0.5)

def _drag_and_drop():
    global _col1, _col2
    if not imgui.collapsing_header("Drag and Drop")[0]:
        return

    if imgui.tree_node("Drag and drop in standard widgets"):
        help_marker("You can drag from the color squares.")
        _, _col1 = imgui.color_edit3("color 1", _col1)
        _, _col2 = imgui.color_edit4("color 2", _col2)
        imgui.tree_pop()

    _drag_and_drop_copy_swap_items()

# Define modes
_mode: Literal['copy', 'move', 'swap'] = 'copy'
_names = [
    "Bobby", "Beatrice", "Betty",
    "Brianna", "Barry", "Bernard",
    "Bibi", "Blaine", "Bryn"
]
def _drag_and_drop_copy_swap_items():
    global _mode, _names

    if not imgui.tree_node("Drag and drop to copy/swap items"):
        return

    # Radio buttons for mode selection
    if imgui.radio_button("Copy", _mode == 'copy'):
        _mode = 'copy'
    imgui.same_line()
    if imgui.radio_button("Move", _mode == 'move'):
        _mode = 'move'
    imgui.same_line()
    if imgui.radio_button("Swap", _mode == 'swap'):
        _mode = 'swap'

    # Render buttons and handle drag-and-drop
    for n in range(len(_names)):
        imgui.push_id(n)
        if (n % 3) != 0:
            imgui.same_line()

        imgui.button(_names[n], size=(60, 60))

        # Drag source
        if imgui.begin_drag_drop_source():
            data = pickle.dumps(n) # encode arbitrary drag'n'drop payload to Python 'bytes'
            imgui.set_drag_drop_payload("DND_DEMO_CELL", data)
            if _mode == 'copy':
                imgui.text(f"Copy {_names[n]}")
            elif _mode == 'move':
                imgui.text(f"Move {_names[n]}")
            elif _mode == 'swap':
                imgui.text(f"Swap {_names[n]}")
            imgui.end_drag_drop_source()

        # Drag target
        if imgui.begin_drag_drop_target():
            if (payload := imgui.accept_drag_drop_payload("DND_DEMO_CELL")) is not None:
                payload_n = pickle.loads(payload.data())
                if _mode == 'copy':
                    _names[n] = _names[payload_n]
                elif _mode == 'move':
                    _names[n] = _names[payload_n]
                    _names[payload_n] = ""
                elif _mode == 'swap':
                    _names[n], _names[payload_n] = _names[payload_n], _names[n]
            imgui.end_drag_drop_target()
        imgui.pop_id()
    imgui.tree_pop()


_shortcut_pressed = 0
_shortcut_blockpos = 0
def _show_shortcut_demo():
    global _shortcut_pressed, _shortcut_blockpos
    expanded, _ = imgui.collapsing_header("Shortcuts")
    if not expanded:
        return

    imgui.text('Use arrow keys UP/DOWN to incr/decr number')
    if imgui.shortcut(imgui.Key.KEY_UP_ARROW):
        _shortcut_pressed += 1
    elif imgui.shortcut(imgui.Key.KEY_DOWN_ARROW):
        _shortcut_pressed -= 1
    imgui.text_colored((0.7, 0.6, 0.2, 1), f'Shortcut counter: {_shortcut_pressed}')
    imgui.text('Use CTRL+LEFT/RIGHT to move the block around'); imgui.same_line()
    help_marker("CTRL == COMMAND on Mac")

    imgui.set_next_item_shortcut(imgui.Key.KEY_LEFT_ARROW | imgui.Key.MOD_CTRL, flags=imgui.InputFlags.REPEAT)
    if imgui.button('Move LEFT'):
        _shortcut_blockpos -= 1

    imgui.same_line()

    imgui.set_next_item_shortcut(imgui.Key.KEY_RIGHT_ARROW | imgui.Key.MOD_CTRL, flags=imgui.InputFlags.REPEAT)
    if imgui.button('Move RIGHT'):
        _shortcut_blockpos += 1

    _shortcut_blockpos = max(0, min(_shortcut_blockpos, 14))
    pos_x, pos_y = imgui.get_cursor_screen_pos()
    imgui.set_cursor_screen_pos((pos_x + _shortcut_blockpos * 32, pos_y))
    imgui.color_button('block', (1, 0.3, 0.1, 1), size=(32, 32))


def _show_input_state_demo():
    expanded, _ = imgui.collapsing_header("Mouse & Keyboard State APIs")
    if not expanded:
        return

    io = imgui.get_io()
    imgui.text(f"mouse_pos: {io.mouse_pos}")
    imgui.text(f"mouse_down: {io.mouse_down}")
    imgui.text(f"mouse_wheel: {io.mouse_wheel}")
    imgui.text(f"mouse_wheel_h: {io.mouse_wheel_h}")
    imgui.text(f"mouse_source: {io.mouse_source}")
    imgui.text(f"key_ctrl: {io.key_ctrl}")
    imgui.text(f"key_shift: {io.key_shift}")
    imgui.text(f"key_alt: {io.key_alt}")
    imgui.text(f"key_super: {io.key_super}")

