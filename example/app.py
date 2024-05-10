from dataclasses import dataclass
import logging
import os

import slimgui as imgui
from slimgui import InputTextFlags

from util import imgui_window

import demo


@dataclass
class State:
    click_count: int = 0
    text: str = ""
    saved_text: str = ""


def run():
    # Initialize state.
    state = State()

    # GUI boilerplate.
    window = imgui_window.ImguiWindow(title="Prompt tool", close_on_esc=True)
    while not window.should_close():
        window.begin_frame()

        for i in range(10):
            imgui.text("hello world!")

        res = imgui.button("click me")
        if res:
            state.click_count += 1

        imgui.text(f"state: {state.click_count}")

        submit, state.text = imgui.input_text(
            "Prompt:", state.text, flags=InputTextFlags.ENTER_RETURNS_TRUE | InputTextFlags.AUTO_SELECT_ALL
        )
        if submit:
            state.saved_text = state.text
        imgui.text(state.saved_text)

        demo.show_demo_window(True)

        window.end_frame()
    window.close()


def main():
    run()


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s"
    )
    main()
