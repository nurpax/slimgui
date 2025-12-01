# TODO
#
# left side:  example window that showcases whatever feature that's being showcased
# right side: example docstring (markdown) + listview with all the samples
# should have keyboard shortcut for up/down to flip through examples

import inspect
import logging
import os
from pathlib import Path
from typing import Callable

import glfw
import OpenGL.GL as gl
import requests
from slimgui import imgui, implot
from slimgui.integrations.glfw import GlfwRenderer
from slimgui.imgui import WindowFlags

import doc_examples

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
    font_data = Path(_download_cached(doc_examples.font_url)).read_bytes()
    return imgui.get_io().fonts.add_font_from_memory_ttf(font_data, 24)

_esc_pressed = False
def _key_callback(_window, key, _scan, action, _mods):
    global _esc_pressed
    if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
        _esc_pressed = True

class ExampleAppLog:
    def __init__(self):
        self.lines: list[str] = []
        self.auto_scroll: bool = True

    def clear(self):
        """Clear all log entries"""
        self.lines.clear()

    def add_log(self, text: str):
        """Add a log entry. Can contain newlines which will be split into separate lines."""
        # Split on newlines and add each line separately
        for line in text.splitlines():
            self.lines.append(line)

    def draw(self, title: str = "Log", open: bool | None = None) -> bool | None:
        """
        Draw the log window.

        Args:
            title: Window title
            p_open: Optional pointer to open state (for close button)

        Returns:
            New open state if p_open was provided, otherwise None
        """
        if open is not None:
            expanded, open = imgui.begin(title, open)
        else:
            expanded = imgui.begin(title)

        if not expanded:
            imgui.end()
            return open

        clear = imgui.button("Clear")
        imgui.same_line()
        copy = imgui.button("Copy")
        imgui.separator()

        # Scrollable text area
        if imgui.begin_child("scrolling", child_flags=imgui.ChildFlags.BORDERS, window_flags=WindowFlags.HORIZONTAL_SCROLLBAR):
            if clear:
                self.clear()
            if copy:
                imgui.log_to_clipboard()

            # Display all lines
            imgui.push_style_var(imgui.StyleVar.ITEM_SPACING, (0, 0))

            imgui.push_font(None, 18)
            for line in self.lines:
                imgui.text(line)
            imgui.pop_font()

            imgui.pop_style_var()

            # Auto-scroll to bottom if we were already at the bottom
            if self.auto_scroll and imgui.get_scroll_y() >= imgui.get_scroll_max_y():
                imgui.set_scroll_here_y(1.0)

        imgui.end_child()
        imgui.end()
        return open

class ImGuiLogHandler(logging.Handler):
    def __init__(self, log_widget: ExampleAppLog):
        super().__init__()
        self.log_widget = log_widget

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_widget.add_log(msg)
        except Exception:
            self.handleError(record)

class Example:
    def __init__(self, callable: Callable, name: str):
        self.callable = callable
        self.name = name
        self.category: str = getattr(callable, "_example_category", "<unknown>")
        self.help = inspect.getdoc(callable)
        self.state_ctor = getattr(callable, "_example_state_ctor")
        self.state = self.state_ctor()

class ExamplesState:
    def __init__(self):
        callables = []
        for name, obj in inspect.getmembers(doc_examples, lambda obj: inspect.isfunction(obj) or inspect.isclass(obj)):
            if not name.startswith('_') and hasattr(obj, '__code__') and hasattr(obj, '_is_example'):
                callables.append((obj.__code__.co_firstlineno, name, obj))
        callables.sort(key=lambda x: x[0])

        examples_by_category: dict[str, list[Example]] = {}
        examples = [Example(callable=x[2], name=x[1]) for x in callables]
        for ex in examples:
            examples_by_category.setdefault(ex.category, []).append(ex)
        self.examples_by_category = examples_by_category
        self._selected_example = (next(iter(self.examples_by_category.keys())), 0)

        self.log = ExampleAppLog()
        self.setup_logging()

    def setup_logging(self):
        handler = ImGuiLogHandler(self.log)
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG)

    def render(self):
        y_pos = 40
        imgui.set_next_window_size((680, 680), imgui.Cond.FIRST_USE_EVER)
        imgui.set_next_window_pos((20, y_pos), imgui.Cond.FIRST_USE_EVER)
        imgui.begin("Select Example")
        imgui.begin_child(
            "##example-list-pane",
            (220, 0),
            child_flags=imgui.ChildFlags.BORDERS | imgui.ChildFlags.RESIZE_X,
        )
        list_size = imgui.get_content_region_avail()
        if imgui.begin_list_box("##example_select", list_size):
            for categ_idx, (category, examples) in enumerate(self.examples_by_category.items()):
                flags = imgui.TreeNodeFlags.NONE if categ_idx != 0 else imgui.TreeNodeFlags.DEFAULT_OPEN
                if imgui.tree_node(category, flags):
                    for idx, example in enumerate(examples):
                        _clicked, selected = imgui.selectable(example.name, (category, idx) == self._selected_example)
                        if selected:
                            self._selected_example = (category, idx)
                        if imgui.begin_popup_context_item(f"##example-menu-{category}-{idx}"):
                            if imgui.menu_item("Copy function name")[0]:
                                imgui.set_clipboard_text(example.name)
                                self.log.add_log(f"copied example name: {example.name}")
                            imgui.end_popup()
                    imgui.tree_pop()
            imgui.end_list_box()
        imgui.end_child()

        sel_category, sel_example = self._selected_example
        cur_example = self.examples_by_category[sel_category][sel_example]

        imgui.same_line()
        imgui.begin_child("##details", child_flags=imgui.ChildFlags.BORDERS)
        if descr := cur_example.help:
            imgui.text_wrapped(descr)
        imgui.end_child()

        imgui.end()

        imgui.set_next_window_size((650, 260), imgui.Cond.FIRST_USE_EVER)
        imgui.set_next_window_pos((720, y_pos + 420), imgui.Cond.FIRST_USE_EVER)
        self.log.draw()

        # Render example last so that it gains focus.
        imgui.set_next_window_size((650, 400), imgui.Cond.FIRST_USE_EVER)
        imgui.set_next_window_pos((720, y_pos), imgui.Cond.FIRST_USE_EVER)
        imgui.begin("Show Example")
        if cur_example.state is not None:
            cur_example.callable(cur_example.state)
        else:
            cur_example.callable()
        imgui.end()



def main():
    # GLFW init.
    glfw.init()

    # OpenGL context version, required for operation on macOS.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.VISIBLE, True)

    glfw_window = glfw.create_window(width=1400, height=800, title="Standalone GLFW Window", monitor=None, share=None)
    glfw.make_context_current(glfw_window)

    # Imgui init.
    imgui_context = imgui.create_context()
    implot_context = implot.create_context()
    io = imgui.get_io()
    io.config_flags |= imgui.ConfigFlags.NAV_ENABLE_KEYBOARD
    io.ini_filename = None
    renderer = GlfwRenderer(glfw_window, prev_key_callback=_key_callback)

    font = _load_font()

    examples = ExamplesState()

    # Application main loop.
    while not (glfw.window_should_close(glfw_window) or _esc_pressed):
        glfw.poll_events()

        # Start new imgui frame.
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        renderer.new_frame()
        imgui.new_frame()
        imgui.push_font(font, 22)

        examples.render()

        # ImGui frame rendering.
        imgui.pop_font()
        imgui.render()
        renderer.render(imgui.get_draw_data())

        # Swap buffers.
        glfw.swap_buffers(glfw_window)

    renderer.shutdown()
    implot.destroy_context(implot_context)
    imgui.destroy_context(imgui_context)

if __name__ == "__main__":
    main()
