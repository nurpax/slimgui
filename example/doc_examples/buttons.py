
from slimgui import imgui

import logging

from .meta import example

@example(category="widgets", title="Simple button")
def button_simple():
    """
    Add a simple button.  The `imgui.button` returns `True` if the button was clicked.
    """
    if imgui.button("Test Button"):
        logging.info("button clicked")


@example(category="widgets", title="Colored buttons")
def button_colors():
    """
    Add a button.  The button base, hover and active states are colored separately.
    """
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
