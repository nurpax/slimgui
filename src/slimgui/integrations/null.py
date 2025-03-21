
import slimgui as imgui

from .base import BaseOpenGLRenderer

DUMMY_ID = 42

class NullRenderer(BaseOpenGLRenderer):
    """Integration that does nothing.  For running unit tests."""
    def __init__(self):
        super().__init__()

    def refresh_font_texture(self):
        width, height, pixels = self.io.fonts.get_tex_data_as_rgba32()
        self.io.fonts.texture_id = DUMMY_ID

    def render(self, draw_data):
        display_width, display_height = self.io.display_size
