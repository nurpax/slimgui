"""
Very much beta quality Pyglet example.  Probably buggy but should be a useful starting point.

Display scale (display_size, display_fb_scale) are probably a bit wonky.  Not sure how it
should be implemented on Pyglet.

Provided as-is.  Will make superficial attempts to keep it up to date but no promises.
"""

import os
import pyglet
from pyglet.window import key, mouse
import requests

from slimgui import imgui

from slimgui.integrations.glfw import OpenGLRenderer

#------------------------------------------------------------------------

REVERSE_KEY_MAP = {
    key.TAB: imgui.Key.KEY_TAB,
    key.LEFT: imgui.Key.KEY_LEFT_ARROW,
    key.RIGHT: imgui.Key.KEY_RIGHT_ARROW,
    key.UP: imgui.Key.KEY_UP_ARROW,
    key.DOWN: imgui.Key.KEY_DOWN_ARROW,
    key.PAGEUP: imgui.Key.KEY_PAGE_UP,
    key.PAGEDOWN: imgui.Key.KEY_PAGE_DOWN,
    key.HOME: imgui.Key.KEY_HOME,
    key.END: imgui.Key.KEY_END,
    key.INSERT: imgui.Key.KEY_INSERT,
    key.DELETE: imgui.Key.KEY_DELETE,
    key.BACKSPACE: imgui.Key.KEY_BACKSPACE,
    key.SPACE: imgui.Key.KEY_SPACE,
    key.RETURN: imgui.Key.KEY_ENTER,
    key.ESCAPE: imgui.Key.KEY_ESCAPE,
    key.NUM_ENTER: imgui.Key.KEY_KEYPAD_ENTER,
    key.A: imgui.Key.KEY_A,
    key.C: imgui.Key.KEY_C,
    key.V: imgui.Key.KEY_V,
    key.X: imgui.Key.KEY_X,
    key.Y: imgui.Key.KEY_Y,
    key.Z: imgui.Key.KEY_Z,
}

class PygletRenderer:
    def __init__(self, window):
        self.renderer = OpenGLRenderer()
        self.window = window

        self.io = imgui.get_io()

        window_size = window.get_size()
        self.io.display_size = window_size
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_VTX_OFFSET
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_TEXTURES

        self._window = window
        window.push_handlers(
            self.on_mouse_motion,
            self.on_key_press,
            self.on_key_release,
            self.on_text,
            self.on_mouse_drag,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_resize,
        )

    def _on_mods_change(self, mods, key_pressed = 0):
        self.io.add_key_event(imgui.Key.MOD_CTRL, (mods & key.MOD_CTRL) != 0 or key_pressed in (key.LCTRL, key.RCTRL))
        self.io.add_key_event(imgui.Key.MOD_SUPER, (mods & key.MOD_COMMAND) != 0 or key_pressed in (key.LCOMMAND, key.RCOMMAND))
        self.io.add_key_event(imgui.Key.MOD_ALT, (mods & key.MOD_ALT) != 0 or key_pressed in (key.LALT, key.RALT))
        self.io.add_key_event(imgui.Key.MOD_SHIFT, (mods & key.MOD_SHIFT) != 0 or key_pressed in (key.LSHIFT, key.RSHIFT))

    def on_mouse_motion(self, x, y, dx, dy):
        self.io.add_mouse_pos_event(x, self.io.display_size[1] - y)

    def on_key_press(self, key_pressed, mods):
        if key_pressed in REVERSE_KEY_MAP:
            self.io.add_key_event(REVERSE_KEY_MAP[key_pressed], True)
        self._on_mods_change(mods, key_pressed)

    def on_key_release(self, key_released, mods):
        if key_released in REVERSE_KEY_MAP:
            self.io.add_key_event(REVERSE_KEY_MAP[key_released], False)
        self._on_mods_change(mods)

    def on_text(self, text):
        for char in text:
            self.io.add_input_character(ord(char))

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.io.add_mouse_pos_event(x, self.io.display_size[1] - y)
        if button == mouse.LEFT:
            self.io.add_mouse_button_event(0, True)
        if button == mouse.MIDDLE:
            self.io.add_mouse_button_event(1, True)
        if button == mouse.RIGHT:
            self.io.add_mouse_button_event(2, True)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.io.add_mouse_button_event(0, True)
        if button == mouse.MIDDLE:
            self.io.add_mouse_button_event(1, True)
        if button == mouse.RIGHT:
            self.io.add_mouse_button_event(2, True)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.io.add_mouse_button_event(0, False)
        if button == mouse.MIDDLE:
            self.io.add_mouse_button_event(1, False)
        if button == mouse.RIGHT:
            self.io.add_mouse_button_event(2, False)

    def on_mouse_scroll(self, x, y, mods, scroll):
        self.io.add_mouse_wheel_event(0, scroll)

    def on_resize(self, width, height):
        self.io.display_size = width, height

    def new_frame(self):
        current_time = pyglet.clock.tick()

        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        if self.io.delta_time <= 0.0:
            self.io.delta_time = 1./ 1000.

        self._gui_time = current_time

    def shutdown(self):
        self.renderer.shutdown()

    def render(self, draw_data: imgui.DrawData):
        self.renderer.render(draw_data)

#------------------------------------------------------------------------

def _download_cached(url, cache_dir="slimgui_examples") -> str:
    os.makedirs(os.path.expanduser(f"~/.cache/{cache_dir}"), exist_ok=True)
    filename = os.path.basename(url)
    cache_path = os.path.expanduser(f"~/.cache/{cache_dir}/{filename}")
    if not os.path.exists(cache_path):
        r = requests.get(url)
        r.raise_for_status()
        with open(cache_path, 'wb') as f:
            f.write(r.content)
    return cache_path

def _load_font():
    with open(_download_cached('https://github.com/jnmaloney/WebGui/raw/master/data/xkcd-script.ttf'), 'rb') as f:
        font_data = f.read()
        return imgui.get_io().fonts.add_font_from_memory_ttf(font_data)

#------------------------------------------------------------------------

def main():
    window = pyglet.window.Window(width=1600, height=1200, resizable=True, caption="Pyglet example")

    imgui.create_context()
    io = imgui.get_io()
    io.config_flags |= imgui.ConfigFlags.NAV_ENABLE_KEYBOARD
    renderer = PygletRenderer(window)

    font = _load_font()

    count = 0
    input_text = ''
    def draw(_dt):
        nonlocal count, input_text

        imgui.new_frame()
        imgui.push_font(font, 30)

        # Your application code goes here..
        imgui.set_next_window_size((400, 400), imgui.Cond.FIRST_USE_EVER)
        imgui.begin('Application Window')
        if imgui.button("Click me!"):
            count += 1
        imgui.same_line()
        imgui.text(f"Clicked {count} times")

        submit, input_text = imgui.input_text("Prompt:", input_text, flags=imgui.InputTextFlags.ENTER_RETURNS_TRUE | imgui.InputTextFlags.AUTO_SELECT_ALL)
        if submit:
            print(f'"{input_text}"', 'submitted')

        imgui.end()
        # ..end of your application code.

        imgui.pop_font()
        window.clear()
        imgui.render()
        renderer.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1 / 60.0)
    pyglet.app.run()
    renderer.shutdown()
    imgui.destroy_context(None)


#------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------
