from dataclasses import dataclass

from slimgui import imgui

from .meta import example


@dataclass
class MultilineInputState:
    text: str = "Write a message here.\nPress Enter to submit it."
    last_submission: str | None = None
    focus_input: bool = False


@example(category="widgets", title="Multiline input with Enter to submit", state_constructor=MultilineInputState,
         window_size=(750, 440))
def input_text_multiline_submit(state: MultilineInputState):
    """
    Configure `input_text_multiline()` for explicit submission and clear its contents after submission.

    - `CTRL_ENTER_FOR_NEW_LINE`: Enter accepts the edit and deactivates the widget; Ctrl+Enter inserts
      a newline. Without this flag, the bindings are reversed. Shift+Enter always inserts a newline.
    - `ENTER_RETURNS_TRUE`: the returned boolean indicates acceptance of the edit, rather than a text
      change. The returned string still updates while typing and must be stored on every call.

    An active input widget maintains its own editing buffer. Assigning `""` to the Python string
    while editing remains active does not reset that buffer. After Enter accepts the edit, the widget
    is inactive and clearing the Python string takes effect. Call `set_keyboard_focus_here()` before
    the input on the next frame to resume editing with the empty value.

    Clicking elsewhere or tabbing away does not report submission. With
    `io.config_mac_osx_behaviors` enabled, Cmd+Enter replaces Ctrl+Enter.
    """
    newline_modifier = "Cmd" if imgui.get_io().config_mac_osx_behaviors else "Ctrl"
    imgui.text(f"Enter to submit; {newline_modifier}+Enter or Shift+Enter for a new line.")
    if state.focus_input:
        imgui.set_keyboard_focus_here()
        state.focus_input = False

    flags = imgui.InputTextFlags.ENTER_RETURNS_TRUE | imgui.InputTextFlags.CTRL_ENTER_FOR_NEW_LINE
    submitted, state.text = imgui.input_text_multiline(
        "##message", state.text, size=(-1, imgui.get_text_line_height() * 6), flags=flags
    )
    if submitted:
        state.last_submission = state.text
        state.text = ""
        state.focus_input = True

    imgui.separator()
    imgui.text("Last submission:")
    if state.last_submission is None:
        imgui.text_disabled("No message submitted yet.")
    else:
        imgui.text_wrapped(state.last_submission)
