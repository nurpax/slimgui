from typing import Any, Callable

import glfw
from slimgui import imgui

from .opengl import OpenGLRenderer

class GlfwRenderer:
    def __init__(
        self,
        window,
        attach_callbacks: bool = True,
        mouse_wheel_multiplier: float = 1.0,
        prev_key_callback: None | Callable[[Any, int, int, int, int], None] = None,
        prev_char_callback: Callable[[Any, int], None] | None = None,
        prev_cursor_pos_callback: Callable[[Any, float, float], None] | None = None,
        prev_mouse_button_callback: Callable[[Any, int, int, int], None] | None = None,
        prev_scroll_callback: Callable[[Any, float, float], None] | None = None,
    ):
        self.renderer = OpenGLRenderer()
        self.window = window
        self.mouse_wheel_multiplier = mouse_wheel_multiplier

        self._prev_key_callback = prev_key_callback
        self._prev_char_callback = prev_char_callback
        self._prev_cursor_pos_callback = prev_cursor_pos_callback
        self._prev_mouse_button_callback = prev_mouse_button_callback
        self._prev_scroll_callback = prev_scroll_callback

        if attach_callbacks:
            glfw.set_key_callback(self.window, self.keyboard_callback)
            glfw.set_cursor_pos_callback(self.window, self.mouse_pos_callback)
            glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
            glfw.set_char_callback(self.window, self.char_callback)
            glfw.set_scroll_callback(self.window, self.scroll_callback)

        self.io = imgui.get_io()
        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_VTX_OFFSET
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_TEXTURES
        self.io.backend_flags |= imgui.BackendFlags.HAS_MOUSE_CURSORS

        plat_io = imgui.get_platform_io()
        plat_io.renderer_texture_max_height = self.renderer.max_texture_size
        plat_io.renderer_texture_max_width = self.renderer.max_texture_size

        self._cursors: dict[imgui.MouseCursor, glfw._GLFWcursor] = {}
        self._alloc_cursors()
        self._gui_time = None
        # FIXME nurpax
        # self.io.get_clipboard_text_fn = self._get_clipboard_text
        # self.io.set_clipboard_text_fn = self._set_clipboard_text

    def _alloc_cursors(self):
        self._cursors[imgui.MouseCursor.ARROW] = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        self._cursors[imgui.MouseCursor.TEXT_INPUT] = glfw.create_standard_cursor(glfw.IBEAM_CURSOR)
        self._cursors[imgui.MouseCursor.RESIZE_NS] = glfw.create_standard_cursor(glfw.VRESIZE_CURSOR)
        self._cursors[imgui.MouseCursor.RESIZE_EW] = glfw.create_standard_cursor(glfw.HRESIZE_CURSOR)
        self._cursors[imgui.MouseCursor.HAND] = glfw.create_standard_cursor(glfw.HAND_CURSOR)
        self._cursors[imgui.MouseCursor.RESIZE_ALL] = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        self._cursors[imgui.MouseCursor.RESIZE_NESW] = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        self._cursors[imgui.MouseCursor.RESIZE_NWSE] = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        self._cursors[imgui.MouseCursor.NOT_ALLOWED] = glfw.create_standard_cursor(glfw.ARROW_CURSOR)

    def _dealloc_cursors(self):
        for cursor in self._cursors.values():
            glfw.destroy_cursor(cursor)
        self._cursors.clear()

    def _update_mouse_cursor(self):
        imgui_cursor = imgui.get_mouse_cursor()
        if imgui_cursor == imgui.MouseCursor.NONE or self.io.mouse_draw_cursor:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        else:
            glfw.set_cursor(self.window, self._cursors.get(imgui_cursor, self._cursors[imgui.MouseCursor.ARROW]))
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def _update_mod_keys(self, window):
        # fmt: off
        self.io.add_key_event(imgui.Key.MOD_CTRL, glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)
        self.io.add_key_event(imgui.Key.MOD_SHIFT, glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)
        self.io.add_key_event(imgui.Key.MOD_ALT, glfw.get_key(window, glfw.KEY_LEFT_ALT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_ALT) == glfw.PRESS)
        self.io.add_key_event(imgui.Key.MOD_SUPER, glfw.get_key(window, glfw.KEY_LEFT_SUPER) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_SUPER) == glfw.PRESS)
        # fmt: on

    def _map_key(self, glfw_key: int) -> imgui.Key | None:
        from slimgui.imgui import Key

        if glfw_key >= glfw.KEY_A and glfw_key <= glfw.KEY_Z:
            return Key(Key.KEY_A + (glfw_key - glfw.KEY_A))
        if glfw_key >= glfw.KEY_0 and glfw_key <= glfw.KEY_9:
            return Key(Key.KEY_0 + (glfw_key - glfw.KEY_0))
        if glfw_key >= glfw.KEY_F1 and glfw_key <= glfw.KEY_F24:
            return Key(Key.KEY_F1 + (glfw_key - glfw.KEY_F1))
        if glfw_key >= glfw.KEY_KP_0 and glfw_key <= glfw.KEY_KP_EQUAL:
            return Key(Key.KEY_KEYPAD0 + (glfw_key - glfw.KEY_KP_0))
        return {
            glfw.KEY_TAB: Key.KEY_TAB,
            glfw.KEY_LEFT: Key.KEY_LEFT_ARROW,
            glfw.KEY_RIGHT: Key.KEY_RIGHT_ARROW,
            glfw.KEY_UP: Key.KEY_UP_ARROW,
            glfw.KEY_DOWN: Key.KEY_DOWN_ARROW,
            glfw.KEY_PAGE_UP: Key.KEY_PAGE_UP,
            glfw.KEY_PAGE_DOWN: Key.KEY_PAGE_DOWN,
            glfw.KEY_HOME: Key.KEY_HOME,
            glfw.KEY_END: Key.KEY_END,
            glfw.KEY_INSERT: Key.KEY_INSERT,
            glfw.KEY_DELETE: Key.KEY_DELETE,
            glfw.KEY_BACKSPACE: Key.KEY_BACKSPACE,
            glfw.KEY_SPACE: Key.KEY_SPACE,
            glfw.KEY_ENTER: Key.KEY_ENTER,
            glfw.KEY_ESCAPE: Key.KEY_ESCAPE,
            glfw.KEY_APOSTROPHE: Key.KEY_APOSTROPHE,
            glfw.KEY_COMMA: Key.KEY_COMMA,
            glfw.KEY_MINUS: Key.KEY_MINUS,
            glfw.KEY_PERIOD: Key.KEY_PERIOD,
            glfw.KEY_SLASH: Key.KEY_SLASH,
            glfw.KEY_SEMICOLON: Key.KEY_SEMICOLON,
            glfw.KEY_EQUAL: Key.KEY_EQUAL,
            glfw.KEY_LEFT_BRACKET: Key.KEY_LEFT_BRACKET,
            glfw.KEY_BACKSLASH: Key.KEY_BACKSLASH,
            glfw.KEY_WORLD_1: Key.KEY_OEM102,
            glfw.KEY_WORLD_2: Key.KEY_OEM102,
            glfw.KEY_RIGHT_BRACKET: Key.KEY_RIGHT_BRACKET,
            glfw.KEY_GRAVE_ACCENT: Key.KEY_GRAVE_ACCENT,
            glfw.KEY_CAPS_LOCK: Key.KEY_CAPS_LOCK,
            glfw.KEY_SCROLL_LOCK: Key.KEY_SCROLL_LOCK,
            glfw.KEY_NUM_LOCK: Key.KEY_NUM_LOCK,
            glfw.KEY_PRINT_SCREEN: Key.KEY_PRINT_SCREEN,
            glfw.KEY_PAUSE: Key.KEY_PAUSE,
            glfw.KEY_LEFT_SHIFT: Key.KEY_LEFT_SHIFT,
            glfw.KEY_LEFT_CONTROL: Key.KEY_LEFT_CTRL,
            glfw.KEY_LEFT_ALT: Key.KEY_LEFT_ALT,
            glfw.KEY_LEFT_SUPER: Key.KEY_LEFT_SUPER,
            glfw.KEY_RIGHT_SHIFT: Key.KEY_RIGHT_SHIFT,
            glfw.KEY_RIGHT_CONTROL: Key.KEY_RIGHT_CTRL,
            glfw.KEY_RIGHT_ALT: Key.KEY_RIGHT_ALT,
            glfw.KEY_RIGHT_SUPER: Key.KEY_RIGHT_SUPER,
            glfw.KEY_MENU: Key.KEY_MENU,
        }.get(glfw_key)

    def keyboard_callback(self, window, key, scancode, action, mods):
        if self._prev_key_callback is not None:
            self._prev_key_callback(window, key, scancode, action, mods)
        if action not in [glfw.PRESS, glfw.RELEASE]:
            return
        self._update_mod_keys(window)
        k = self._map_key(key)
        if k is not None:
            self.io.add_key_event(k, action == glfw.PRESS)

    def char_callback(self, window, char):
        if self._prev_char_callback is not None:
            self._prev_char_callback(window, char)
        self.io.add_input_character(char)

    def mouse_pos_callback(self, window, x, y):
        if self._prev_cursor_pos_callback is not None:
            self._prev_cursor_pos_callback(window, x, y)
        self.io.add_mouse_pos_event(x, y)

    def mouse_button_callback(self, window, btn, action, mods):
        if self._prev_mouse_button_callback is not None:
            self._prev_mouse_button_callback(window, btn, action, mods)
        self._update_mod_keys(window)
        self.io.add_mouse_button_event(btn, action != 0)

    def scroll_callback(self, window, x_offset, y_offset):
        if self._prev_scroll_callback is not None:
            self._prev_scroll_callback(window, x_offset, y_offset)
        x_offset *= self.mouse_wheel_multiplier
        y_offset *= self.mouse_wheel_multiplier
        self.io.add_mouse_wheel_event(x_offset, y_offset)

    def new_frame(self):
        # See https://github.com/ocornut/imgui/issues/5081

        w, h = glfw.get_window_size(self.window)
        disp_w, disp_h = glfw.get_framebuffer_size(self.window)
        self.io.display_size = w, h
        if w > 0 and h > 0:
            self.io.display_framebuffer_scale = float(disp_w) / float(w), float(disp_h) / float(h)

        current_time = glfw.get_time()
        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1.0 / 60.0
        if self.io.delta_time <= 0.0:
            self.io.delta_time = 1.0 / 1000.0
        self._gui_time = current_time

        # Mouse cursor style changes
        self._update_mouse_cursor()

    def shutdown(self):
        self.renderer.shutdown()
        self._dealloc_cursors()

    def render(self, draw_data: imgui.DrawData):
        self.renderer.render(draw_data)
