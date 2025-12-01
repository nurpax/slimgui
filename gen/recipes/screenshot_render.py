from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import glfw
import OpenGL.GL as gl
import requests
from PIL import Image
from slimgui import imgui, implot
from slimgui.integrations.glfw import GlfwRenderer

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recipes.examples import Example, load_examples
else:
    from .examples import Example, load_examples


_esc_pressed = False


def _download_cached(url, cache_dir="slimgui_examples") -> str:
    os.makedirs(os.path.expanduser(f"~/.cache/{cache_dir}"), exist_ok=True)
    filename = os.path.basename(url)
    cache_path = os.path.expanduser(f"~/.cache/{cache_dir}/{filename}")
    if not os.path.exists(cache_path):
        r = requests.get(url)
        r.raise_for_status()
        with open(cache_path, "wb") as f:
            f.write(r.content)
    return cache_path


def _load_font(font_url: str, font_size: int):
    with open(_download_cached(font_url), "rb") as f:
        font_data = f.read()
        return imgui.get_io().fonts.add_font_from_memory_ttf(font_data, font_size)


def _key_callback(_window, key, _scan, action, _mods):
    global _esc_pressed
    if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
        _esc_pressed = True


def _find_example(examples: list[Example], name: str) -> Example:
    matches = [example for example in examples if example.name == name]
    if not matches:
        available = ", ".join(ex.name for ex in examples)
        raise ValueError(f"Unknown example '{name}'. Available: {available}")
    return matches[0]


def _render_example(
    example: Example,
    state: object,
    window_size: tuple[int, int],
    window_pos: tuple[int, int],
) -> tuple[float, float, float, float]:
    imgui.set_next_window_pos(window_pos, imgui.Cond.ALWAYS)
    imgui.set_next_window_size(window_size, imgui.Cond.ALWAYS)
    imgui.begin(_titleize(example.name))
    if state is not None:
        example.callable(state)
    else:
        example.callable()
    win_pos = imgui.get_window_pos()
    win_size = imgui.get_window_size()
    imgui.end()
    return win_pos[0], win_pos[1], win_size[0], win_size[1]


def _titleize(name: str) -> str:
    return name.replace("_", " ").strip().title()


def save_screenshot(
    filename: str,
    width: int,
    height: int,
    crop: tuple[int, int, int, int] | None = None,
):
    gl.glReadBuffer(gl.GL_FRONT)
    gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)

    pixels = gl.glReadPixels(0, 0, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), pixels)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if crop is not None:
        image = image.crop(crop)
    image.save(filename)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a screenshot for a recipe example.")
    parser.add_argument("--example", help="Example function name to render.")
    parser.add_argument("--list", action="store_true", help="List available examples and exit.")
    parser.add_argument("--output", type=Path, default=None, help="Output image path.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "docs" / "recipes",
        help="Output directory for screenshots.",
    )
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--font-size", type=int, default=24)
    parser.add_argument("--visible", action="store_true", help="Show the GLFW window.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    repo_root = Path(__file__).resolve().parents[2]
    doc_examples, examples = load_examples(repo_root)
    if args.list:
        for example in examples:
            print(example.name)
        return 0

    if not args.example:
        parser.error("--example is required unless --list is used.")

    example = _find_example(examples, args.example)

    output_path = args.output
    if output_path is None:
        output_path = args.output_dir / f"{example.name}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # GLFW init.
    glfw.init()

    if args.visible:
        parser.error("Screenshot rendering only supports headless mode (omit --visible).")
    headless = True

    # OpenGL context version, required for operation on macOS.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.VISIBLE, not headless)

    window_margin = 20
    window_size = example.window_size
    requested_width = max(args.width, window_size[0] + window_margin * 2)
    requested_height = max(args.height, window_size[1] + window_margin * 2)

    glfw_window = glfw.create_window(
        width=requested_width,
        height=requested_height,
        title="Recipe Render",
        monitor=None,
        share=None,
    )
    glfw.make_context_current(glfw_window)

    # Imgui init.
    imgui_context = imgui.create_context()
    implot_context = implot.create_context()
    io = imgui.get_io()
    io.ini_filename = None
    io.config_flags |= imgui.ConfigFlags.NAV_ENABLE_KEYBOARD
    renderer = GlfwRenderer(glfw_window, prev_key_callback=_key_callback)

    font = _load_font(doc_examples.font_url, args.font_size)
    state_ctor = example.state_ctor
    assert state_ctor is not None
    example_state = state_ctor()
    warmup_frames = 2

    # Application main loop.
    while not (glfw.window_should_close(glfw_window) or _esc_pressed):
        glfw.poll_events()

        # Start new imgui frame.
        fb_width, fb_height = glfw.get_framebuffer_size(glfw_window)

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        renderer.new_frame()

        if headless:
            io.display_size = fb_width, fb_height
            io.display_framebuffer_scale = 1, 1

        imgui.new_frame()
        imgui.push_font(font, 0)

        window_rect = _render_example(example, example_state, window_size, (window_margin, window_margin))

        # ImGui frame rendering.
        imgui.pop_font()
        imgui.render()
        renderer.render(imgui.get_draw_data())

        # Swap buffers.
        glfw.swap_buffers(glfw_window)

        warmup_frames -= 1
        if warmup_frames > 0:
            continue

        # Adjust crop rect for border outline and save a screenshot.
        win_x, win_y, win_w, win_h = window_rect
        left = int(win_x)-1
        top = int(win_y)-1
        right = int(win_x + win_w)+2
        bottom = int(win_y + win_h)+2
        save_screenshot(str(output_path), fb_width, fb_height, crop=(left, top, right, bottom))
        break

    renderer.shutdown()
    implot.destroy_context(implot_context)
    imgui.destroy_context(imgui_context)

    logging.info("Saved screenshot to %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
