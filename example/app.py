import logging
import os
from dataclasses import dataclass

import demo_window
import requests
import slimgui as imgui
from slimgui import InputTextFlags
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
    show_demo_window = True
    click_count: int = 0
    text: str = ""
    foo_enabled: bool = False
    saved_text: str = ""


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

    # Make title bar semi-transparent to test out the style colors array access.
    prev_col = imgui.get_style().colors[imgui.Col.TITLE_BG_ACTIVE]
    imgui.get_style().colors[imgui.Col.TITLE_BG_ACTIVE] = (*prev_col[:3], 0.75)

    while not window.should_close():
        window.begin_frame()

        for i in range(10):
            imgui.text("hello world!")

        res = imgui.button("click me")
        if res:
            state.click_count += 1

        imgui.text(f"state: {state.click_count}")

        io = imgui.get_io()
        io.ini_filename = None

        submit, state.text = imgui.input_text(
            "Prompt:", state.text, flags=InputTextFlags.ENTER_RETURNS_TRUE | InputTextFlags.AUTO_SELECT_ALL
        )
        if submit:
            state.saved_text = state.text
        imgui.text(state.saved_text)

        if (res := imgui.checkbox("Some setting", state.foo_enabled)).clicked:
            print('checkbox state changed')
            state.foo_enabled = res.value

        if state.show_demo_window:
            state.show_demo_window = demo_window.show_demo_window(state.show_demo_window)

        window.end_frame()
    window.close()

def main():
    run()


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s"
    )
    main()
