import os

import glfw
import OpenGL.GL as gl
import requests
from slimgui import imgui
from slimgui.integrations.glfw import GlfwRenderer

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
        return imgui.get_io().fonts.add_font_from_memory_ttf(font_data, 24)

_esc_pressed = False
def _key_callback(_window, key, _scan, action, _mods):
    global _esc_pressed
    if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
        _esc_pressed = True

def main():
    # GLFW init.
    glfw.init()

    # OpenGL context version, required for operation on macOS.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.VISIBLE, True)

    glfw_window = glfw.create_window(width=1200, height=1200, title="Standalone GLFW Window", monitor=None, share=None)
    glfw.make_context_current(glfw_window)

    # Imgui init.
    imgui.create_context()
    io = imgui.get_io()
    io.config_flags |= imgui.ConfigFlags.NAV_ENABLE_KEYBOARD
    renderer = GlfwRenderer(glfw_window, prev_key_callback=_key_callback)

    font = _load_font()

    # Application main loop.
    count = 0
    while not (glfw.window_should_close(glfw_window) or _esc_pressed):
        glfw.poll_events()

        # Start new imgui frame.
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        renderer.new_frame()
        imgui.new_frame()
        imgui.push_font(font, 0)  # or push_font(font, font.legacy_size)

        # Your application code goes here..
        imgui.set_next_window_size((400, 400), imgui.Cond.FIRST_USE_EVER)
        imgui.begin('Application Window')
        if imgui.button("Click me!"):
            count += 1
        imgui.same_line()
        imgui.text(f"Clicked {count} times")
        imgui.end()
        # ..end of your application code.

        # ImGui frame rendering.
        imgui.pop_font()
        imgui.render()
        renderer.render(imgui.get_draw_data())

        # Swap buffers.
        glfw.swap_buffers(glfw_window)

    renderer.shutdown()
    imgui.destroy_context(None)

if __name__ == "__main__":
    main()
