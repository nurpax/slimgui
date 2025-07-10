import logging
import os
from dataclasses import dataclass
import numpy as np

import demo_window
import implot_demo_window
import requests

from slimgui import imgui
from slimgui import implot

from util import imgui_window


def download_and_cache(url, cache_dir='cache', filename=None) -> str:
    os.makedirs(cache_dir, exist_ok=True)

    if not filename:
        filename = os.path.basename(url)

    file_path = os.path.join(cache_dir, filename)

    if not os.path.isfile(file_path):
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)
    return file_path

@dataclass
class State:
    show_python_demo_window = True
    show_implot_demo_window = True
    show_python_implot_demo_window = True
    click_count: int = 0
    text: str = ""
    foo_enabled: bool = False
    saved_text: str = ""

def _make_texture():
    import OpenGL.GL as gl

    size = 128
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    x, y = np.meshgrid(x, y)

    radius = np.sqrt(x**2 + y**2)
    image = np.sin(radius * 5 * np.pi)
    image = (image * 0.5 + 0.5) * 255
    image = np.stack((image, image, image, image), axis=-1)
    image[:, :, 3] = 255
    image = image.astype(np.uint8)
    image = np.clip(image, 0, 255)
    image = np.array(image, dtype=np.uint8)

    h, w, _c = image.shape
    tex_id = gl.glGenTextures(1)

    gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)

    assert gl.glGetError() == gl.GL_NO_ERROR, "Error creating texture"
    return {
        "id": tex_id,
        "width": w,
        "height": h,
    }

def run():
    # Initialize state.
    state = State()

    use_ttf_font = True
    if use_ttf_font:
        with open(download_and_cache("https://github.com/jnmaloney/WebGui/raw/master/data/xkcd-script.ttf"), "rb") as f:
            font_bytes = f.read()
    else:
        font_bytes = None

    # GUI boilerplate.
    window = imgui_window.ImguiWindow(
        title="Prompt tool",
        close_on_esc=True,
        font_bytes=font_bytes,
        request_opengl_core_profile=True,
    )
    window.set_font_size(24)
    implot.create_context()

    texture = _make_texture()

    # Make title bar semi-transparent to test out the style colors array access.
    prev_col = imgui.get_style().colors[imgui.Col.TITLE_BG_ACTIVE]
    imgui.get_style().colors[imgui.Col.TITLE_BG_ACTIVE] = (*prev_col[:3], 0.75)

    while not window.should_close():
        window.begin_frame()

        for i in range(3):
            imgui.text("hello world!")

        res = imgui.button("click me")
        if res:
            state.click_count += 1

        imgui.text(f"state: {state.click_count}")

        io = imgui.get_io()
        io.ini_filename = None

        submit, state.text = imgui.input_text(
            "Prompt:", state.text, flags=imgui.InputTextFlags.ENTER_RETURNS_TRUE | imgui.InputTextFlags.AUTO_SELECT_ALL
        )
        if submit:
            state.saved_text = state.text
        imgui.text(state.saved_text)

        clicked, v = imgui.checkbox("Some setting", state.foo_enabled)
        if clicked:
            print('checkbox state changed')
            state.foo_enabled = v

        if state.show_python_demo_window:
            state.show_python_demo_window = demo_window.show_demo_window(state.show_python_demo_window, texture)

        if state.show_implot_demo_window:
            state.show_implot_demo_window = implot.show_demo_window(state.show_implot_demo_window)

        if state.show_python_implot_demo_window:
            state.show_python_implot_demo_window = implot_demo_window.show_demo_window(state.show_python_implot_demo_window)

        window.end_frame()
    window.close()

def main():
    run()


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s"
    )
    main()
