
from slimgui import imgui

from .base import BaseRenderer

DUMMY_ID = 42

class NullRenderer(BaseRenderer):
    """Integration that does nothing.  For running unit tests."""
    def __init__(self):
        super().__init__()

    def refresh_font_texture(self):
        io = imgui.get_io()
        width, height, pixels = io.fonts.get_tex_data_as_rgba32()
        io.fonts.texture_id = DUMMY_ID

    def render(self, draw_data):
        io = imgui.get_io()
        display_width, display_height = io.display_size

    def shutdown(self):
        pass
