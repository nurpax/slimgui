---
url: /slimgui/recipes/widgets.md
---

# Widgets

## Simple button

![Simple button](./images/button_simple.png)

Add a simple button.  The `imgui.button` returns `True` if the button was clicked.

```python
def button_simple():
    if imgui.button("Test Button"):
        logging.info("button clicked")
```

## Colored buttons

![Colored buttons](./images/button_colors.png)

Add a button.  The button base, hover and active states are colored separately.

```python
def button_colors():
    for i in range(7):
        base_color = imgui.color_convert_hsv_to_rgb((i/7.0, 0.6, 0.6, 1))
        hover_color = imgui.color_convert_hsv_to_rgb((i/7.0, 0.7, 0.7, 1))
        active_color = imgui.color_convert_hsv_to_rgb((i/7.0, 0.8, 0.8, 1))

        if i > 0:
            imgui.same_line()

        imgui.push_id(i)
        imgui.push_style_color(imgui.Col.BUTTON, base_color)
        imgui.push_style_color(imgui.Col.BUTTON_HOVERED, hover_color)
        imgui.push_style_color(imgui.Col.BUTTON_ACTIVE, active_color)
        if imgui.button("Click"):
            logging.info("Colored button clicked")
        imgui.pop_style_color(3)
        imgui.pop_id()
```

## Multiline input with Enter to submit

![Multiline input with Enter to submit](./images/input_text_multiline_submit.png)

Configure `input_text_multiline()` for explicit submission and clear its contents after submission.

* `CTRL_ENTER_FOR_NEW_LINE`: Enter accepts the edit and deactivates the widget; Ctrl+Enter inserts
  a newline. Without this flag, the bindings are reversed. Shift+Enter always inserts a newline.
* `ENTER_RETURNS_TRUE`: the returned boolean indicates acceptance of the edit, rather than a text
  change. The returned string still updates while typing and must be stored on every call.

An active input widget maintains its own editing buffer. Assigning `""` to the Python string
while editing remains active does not reset that buffer. After Enter accepts the edit, the widget
is inactive and clearing the Python string takes effect. Call `set_keyboard_focus_here()` before
the input on the next frame to resume editing with the empty value.

Clicking elsewhere or tabbing away does not report submission. With
`io.config_mac_osx_behaviors` enabled, Cmd+Enter replaces Ctrl+Enter.

```python
def input_text_multiline_submit(state: MultilineInputState):
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
```
