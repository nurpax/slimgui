from typing import Any, Callable

import glfw
import slimgui as imgui

from .opengl import ProgrammablePipelineRenderer

class GlfwRenderer(ProgrammablePipelineRenderer):
    def __init__(
        self,
        window,
        attach_callbacks: bool = True,
        prev_key_callback: None | Callable[[Any, int, int, int, int], None] = None,
        prev_char_callback: Callable[[Any, int], None] | None = None,
        prev_cursor_pos_callback: Callable[[Any, float, float], None] | None = None,
        prev_mouse_button_callback: Callable[[Any, int, int, int], None] | None = None,
        prev_scroll_callback: Callable[[Any, float, float], None] | None = None,
        prev_window_size_callback: Callable[[Any, int, int], None] | None = None,
    ):
        super(GlfwRenderer, self).__init__()
        self.window = window

        self._prev_key_callback = prev_key_callback
        self._prev_char_callback = prev_char_callback
        self._prev_cursor_pos_callback = prev_cursor_pos_callback
        self._prev_mouse_button_callback = prev_mouse_button_callback
        self._prev_scroll_callback = prev_scroll_callback
        self._prev_window_size_callback = prev_window_size_callback

        if attach_callbacks:
            glfw.set_key_callback(self.window, self.keyboard_callback)
            glfw.set_cursor_pos_callback(self.window, self.mouse_pos_callback)
            glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
            glfw.set_window_size_callback(self.window, self.resize_callback)
            glfw.set_char_callback(self.window, self.char_callback)
            glfw.set_scroll_callback(self.window, self.scroll_callback)

        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self._gui_time = None
        # FIXME nurpax
        # self.io.get_clipboard_text_fn = self._get_clipboard_text
        # self.io.set_clipboard_text_fn = self._set_clipboard_text

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def _update_mod_keys(self, window):
        io = imgui.get_io()
        # fmt: off
        io.add_key_event(imgui.Key.MOD_CTRL, glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)
        io.add_key_event(imgui.Key.MOD_SHIFT, glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)
        io.add_key_event(imgui.Key.MOD_ALT, glfw.get_key(window, glfw.KEY_LEFT_ALT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_ALT) == glfw.PRESS)
        io.add_key_event(imgui.Key.MOD_SUPER, glfw.get_key(window, glfw.KEY_LEFT_SUPER) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_SUPER) == glfw.PRESS)
        # fmt: on

    def _map_key(self, glfw_key: int) -> imgui.Key | None:
        from slimgui import Key

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
            glfw.KEY_KP_ENTER: Key.KEY_KEYPAD_ENTER,
            glfw.KEY_A: Key.KEY_A,
            glfw.KEY_C: Key.KEY_C,
            glfw.KEY_V: Key.KEY_V,
            glfw.KEY_X: Key.KEY_X,
            glfw.KEY_Y: Key.KEY_Y,
            glfw.KEY_Z: Key.KEY_Z,
        }.get(glfw_key)

    def keyboard_callback(self, window, key, scancode, action, mods):
        if self._prev_key_callback is not None:
            self._prev_key_callback(window, key, scancode, action, mods)
        if action not in [glfw.PRESS, glfw.RELEASE]:
            return
        io = imgui.get_io()
        self._update_mod_keys(window)
        k = self._map_key(key)
        if k is not None:
            io.add_key_event(k, action == glfw.PRESS)

    def char_callback(self, window, char):
        if self._prev_char_callback is not None:
            self._prev_char_callback(window, char)
        io = imgui.get_io()
        io.add_input_character(char)

    def resize_callback(self, window, width, height):
        if self._prev_window_size_callback is not None:
            self._prev_window_size_callback(window, width, height)
        self.io.display_size = width, height

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
        self.io.add_mouse_wheel_event(x_offset, y_offset)

    def new_frame(self):
        io = imgui.get_io()

        window_size = glfw.get_window_size(self.window)
        display_w, display_h = glfw.get_framebuffer_size(self.window)

        io.display_size = window_size

        w, h = window_size
        if w != 0 and h != 0:
            io.display_fb_scale = (display_w / w, display_h / h)

        current_time = glfw.get_time()
        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1.0 / 60.0
        if io.delta_time <= 0.0:
            io.delta_time = 1.0 / 1000.0
        self._gui_time = current_time
