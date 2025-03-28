
import glfw
import OpenGL.GL as gl

from slimgui import imgui
from slimgui.integrations.glfw import GlfwRenderer

# ----------------------------------------------------------------------------

class GlfwWindow:  # pylint: disable=too-many-public-methods
    def __init__(
        self, *, title="GlfwWindow", window_width=1920, window_height=1080, deferred_show=True, request_opengl_core_profile=False
    ):
        self._glfw_window = None
        self._drawing_frame = False
        self._frame_start_time = None
        self._frame_delta = 0
        self._vsync = None
        self._skip_frames = 0
        self._deferred_show = True
        self._drag_and_drop_paths = None
        self._core_profile = False

        # Create window.
        glfw.init()
        if request_opengl_core_profile:
            self._core_profile = True
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.VISIBLE, False)
        self._glfw_window = glfw.create_window(
            width=window_width, height=window_height, title=title, monitor=None, share=None
        )
        self.make_context_current()

        # Adjust window.
        self.set_vsync(False)
        self.set_window_size(window_width, window_height)
        if not deferred_show:
            self._show_now()

    def close(self):
        if self._drawing_frame:
            self.end_frame()
        if self._glfw_window is not None:
            glfw.destroy_window(self._glfw_window)
            self._glfw_window = None
        # glfw.terminate() # Commented out to play it nice with other glfw clients.

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    @property
    def window_width(self):
        return self.content_width

    @property
    def window_height(self):
        return self.content_height + self.title_bar_height

    @property
    def content_width(self):
        width, _height = glfw.get_window_size(self._glfw_window)
        return width

    @property
    def content_height(self):
        _width, height = glfw.get_window_size(self._glfw_window)
        return height

    @property
    def title_bar_height(self):
        _left, top, _right, _bottom = glfw.get_window_frame_size(self._glfw_window)
        return top

    @property
    def monitor_width(self):
        _, _, width, _height = glfw.get_monitor_workarea(glfw.get_primary_monitor())
        return width

    @property
    def monitor_height(self):
        _, _, _width, height = glfw.get_monitor_workarea(glfw.get_primary_monitor())
        return height

    @property
    def frame_delta(self):
        return self._frame_delta

    def set_title(self, title):
        glfw.set_window_title(self._glfw_window, title)

    def set_window_size(self, width, height):
        width = min(width, self.monitor_width)
        height = min(height, self.monitor_height)
        glfw.set_window_size(self._glfw_window, width, max(height - self.title_bar_height, 0))
        if width == self.monitor_width and height == self.monitor_height:
            self.maximize()

    def set_content_size(self, width, height):
        self.set_window_size(width, height + self.title_bar_height)

    def maximize(self):
        glfw.maximize_window(self._glfw_window)

    def set_position(self, x, y):
        glfw.set_window_pos(self._glfw_window, x, y + self.title_bar_height)

    def center(self):
        self.set_position(
            (self.monitor_width - self.window_width) // 2, (self.monitor_height - self.window_height) // 2
        )

    def _show_now(self):
        if self._deferred_show:
            glfw.show_window(self._glfw_window)
            self._deferred_show = False

    def set_vsync(self, vsync):
        vsync = bool(vsync)
        if vsync != self._vsync:
            glfw.swap_interval(1 if vsync else 0)
            self._vsync = vsync

    def draw_frame(self):  # To be overridden by subclass.
        self.begin_frame()
        # Rendering code goes here.
        self.end_frame()

    def make_context_current(self):
        if self._glfw_window is not None:
            glfw.make_context_current(self._glfw_window)

    def begin_frame(self):
        # End previous frame.
        if self._drawing_frame:
            self.end_frame()

        # Process events.
        glfw.poll_events()

        # Begin frame.
        self._drawing_frame = True
        self.make_context_current()

        # Initialize GL state.
        if not self._core_profile:
            gl.glViewport(0, 0, self.content_width, self.content_height)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glTranslate(-1, 1, 0)
            gl.glScale(2 / max(self.content_width, 1), -2 / max(self.content_height, 1), 1)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA)  # Pre-multiplied alpha.

        # Clear.
        gl.glClearColor(0.1, 0.2, 0.4, 1)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

    def end_frame(self):
        assert self._drawing_frame
        self._drawing_frame = False

        # Update window.
        self._show_now()
        glfw.swap_buffers(self._glfw_window)

# ----------------------------------------------------------------------------


class ImguiWindow(GlfwWindow):
    def __init__(self, *, title="ImguiWindow", font_bytes: bytes | None=None, font_sizes=range(14, 24), close_on_esc=False, ini_filename: str | None=None, mouse_wheel_multiplier: float = 1, **glfw_kwargs):
        font_sizes = {int(size) for size in font_sizes}
        super().__init__(title=title, **glfw_kwargs)

        # Init fields.
        self._imgui_context = None
        self._imgui_renderer = None
        self._imgui_fonts  = None
        self._cur_font_size = max(font_sizes)
        self._close_on_esc = close_on_esc
        self._esc_pressed = False

        # Init ImGui.
        self._imgui_context = imgui.create_context()
        io = imgui.get_io()
        io.ini_filename = ini_filename
        # TODO pass these in?
        io.config_flags |= imgui.ConfigFlags.NAV_ENABLE_KEYBOARD

        self._imgui_renderer = GlfwRenderer(
            self._glfw_window,
            mouse_wheel_multiplier=mouse_wheel_multiplier,
            prev_key_callback=self._glfw_key_callback,
        )

        if font_bytes is not None:
            self._imgui_fonts = {size: imgui.get_io().fonts.add_font_from_memory_ttf(font_bytes, size) for size in font_sizes}
        self._imgui_renderer.refresh_font_texture()

    def close(self):
        self.make_context_current()
        self._imgui_fonts = None
        if self._imgui_renderer is not None:
            self._imgui_renderer.shutdown()
            self._imgui_renderer = None
        if self._imgui_context is not None:
            imgui.destroy_context(self._imgui_context)  # Commented out to avoid creating imgui.ini at the end.
            self._imgui_context = None
        super().close()

    def _glfw_key_callback(self, _window, key, _scan, action, _mods):
        if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
            self._esc_pressed = True

    def should_close(self) -> bool:
        return glfw.window_should_close(self._glfw_window) or (self._close_on_esc and self._esc_pressed)

    @property
    def font_size(self):
        return self._cur_font_size

    @property
    def spacing(self):
        return round(self._cur_font_size * 0.4)

    def set_font_size(self, target):  # Applied on next frame.
        assert self._imgui_fonts is not None
        self._cur_font_size = min((abs(key - target), key) for key in self._imgui_fonts.keys())[1]

    def begin_frame(self):
        assert self._imgui_renderer is not None
        super().begin_frame()

        self._imgui_renderer.new_frame()
        imgui.new_frame()
        if self._imgui_fonts is not None:
            imgui.push_font(self._imgui_fonts[self._cur_font_size])

    def end_frame(self):
        assert self._imgui_renderer is not None
        if self._imgui_fonts is not None:
            imgui.pop_font()
        imgui.render()
        self._imgui_renderer.render(imgui.get_draw_data())
        super().end_frame()
