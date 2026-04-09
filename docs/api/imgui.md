---
title: 'slimgui - ImGui API reference'
subtitle: 'Python bindings for Dear ImGui'
---

# ImGui API reference

Slimgui is built against Dear ImGui version 1.92.4.

API reference documentation is primarily adapted from Dear ImGui main header [imgui.h](https://github.com/ocornut/imgui/blob/master/imgui.h),
with minor modifications to adapt symbol naming to Pythonic snake case.

See [Typing](/guide/typing) for an explanation of the public `imgui` module,
wrapper types such as `slimgui.imgui.DrawList`, and how they relate to the
underlying `slimgui.slimgui_ext.*` bindings.

## Context creation and access

Each context creates its own `FontAtlas` by default. You may instance one yourself and pass it to `create_context()` to share a font atlas between contexts.

### Functions
::: api-signature
```python
def create_context(
    shared_font_atlas: slimgui.slimgui_ext.imgui.FontAtlas | None = None,
) -> slimgui.imgui.WrappedContext:
    """
    Create an ImGui `Context`.  The newly created context is also set current.
    """
```
:::

::: api-signature
```python
def destroy_context(
    ctx: slimgui.imgui.WrappedContext | None,
):
    """
    Destroy ImGui `Context`.  `None` = destroy current context.
    """
```
:::

::: api-signature
```python
def get_current_context() -> slimgui.imgui.WrappedContext | None:
    """
    Get the current ImGui context.
    """
```
:::

::: api-signature
```python
def set_current_context(
    ctx: slimgui.imgui.WrappedContext,
) -> None:
    """
    Set the current ImGui context.
    """
```
:::

## Main

### Functions
::: api-signature
```python
def get_io() -> slimgui.slimgui_ext.imgui.IO:
    """
    Access the ImGui `IO` structure (mouse/keyboard/gamepad inputs, time, various configuration options/flags).
    """
```
:::

::: api-signature
```python
def get_style() -> slimgui.slimgui_ext.imgui.Style:
    """
    Access the `Style` structure (colors, sizes). Always use `push_style_color()`, `push_style_var()` to modify style mid-frame!
    """
```
:::

::: api-signature
```python
def get_platform_io() -> slimgui.slimgui_ext.imgui.PlatformIO:
    """
    Access the ImGui `PlatformIO` structure.
    """
```
:::

::: api-signature
```python
def new_frame():
    """
    ImGui::NewFrame() call but with some Python binding specific book keeping.
    """
```
:::

::: api-signature
```python
def end_frame() -> None:
    """
    Ends the Dear ImGui frame. automatically called by `render()`. If you don't need to render data (skipping rendering) you may call `end_frame()` without `render()`... but you'll have wasted CPU already! If you don't need to render, better to not create any windows and not call `new_frame()` at all!
    """
```
:::

::: api-signature
```python
def render() -> None:
    """
    Ends the Dear ImGui frame, finalize the draw data. You can then get call `get_draw_data()`.
    """
```
:::

::: api-signature
```python
def get_draw_data() -> DrawData:
    """
    Valid after `render()` and until the next call to `new_frame()`. Call ImGui_ImplXXXX_RenderDrawData() function in your Renderer Backend to render.
    """
```
:::

## Demo, Debug, Information

### Error recovery and debug options

Please see [https://github.com/ocornut/imgui/wiki/Error-Handling](https://github.com/ocornut/imgui/wiki/Error-Handling) for information.

Currently only the `IO.config_*` boolean options are exposed from Slimgui. `IM_ASSERT` is configured by default to raise a Python exception, but note that it is not always recoverable — your Python application may be in a bad state afterward.

### Functions
::: api-signature
```python
def show_demo_window(
    closable: bool = False,
) -> bool:
    """
    Create Demo window. demonstrate most ImGui features. call this to learn about the library! try to make it always available in your application!
    """
```
:::

::: api-signature
```python
def show_metrics_window(
    closable: bool = False,
) -> bool:
    """
    Create Metrics/Debugger window. display Dear ImGui internals: windows, draw commands, various internal state, etc.
    """
```
:::

::: api-signature
```python
def show_debug_log_window(
    closable: bool = False,
) -> bool:
    """
    Create Debug Log window. display a simplified log of important dear imgui events.
    """
```
:::

::: api-signature
```python
def show_id_stack_tool_window(
    closable: bool = False,
) -> bool:
    """
    Create Stack Tool window. hover items with mouse to query information about the source of their unique ID.
    """
```
:::

::: api-signature
```python
def show_about_window(
    closable: bool = False,
) -> bool:
    """
    Create About window. display Dear ImGui version, credits and build/system information.
    """
```
:::

::: api-signature
```python
def show_style_editor() -> None:
    """
    Add style editor block (not a window). you can pass in a reference ImGuiStyle structure to compare to, revert to and save to (else it uses the default style)
    """
```
:::

::: api-signature
```python
def show_style_selector(
    label: str,
) -> bool:
    """
    Add style selector block (not a window), essentially a combo listing the default styles.
    """
```
:::

::: api-signature
```python
def show_font_selector(
    label: str,
) -> None:
    """
    Add font selector block (not a window), essentially a combo listing the loaded fonts.
    """
```
:::

::: api-signature
```python
def show_user_guide() -> None:
    """
    Add basic help/info block (not a window): how to manipulate ImGui as an end-user (mouse/keyboard controls).
    """
```
:::

::: api-signature
```python
def get_version() -> str:
    """
    Get the compiled version string e.g. "1.80 WIP" (essentially the value for IMGUI_VERSION from the compiled version of imgui.cpp)
    """
```
:::

### Logging

::: api-signature
```python
def log_to_tty(
    auto_open_depth: int = -1,
) -> None:
    """
    Start logging to tty (stdout)
    """
```
:::

::: api-signature
```python
def log_to_file(
    auto_open_depth: int = -1,
    filename: str | None = None,
) -> None:
    """
    Start logging to file
    """
```
:::

::: api-signature
```python
def log_to_clipboard(
    auto_open_depth: int = -1,
) -> None:
    """
    Start logging to OS clipboard
    """
```
:::

::: api-signature
```python
def log_finish() -> None:
    """
    Stop logging (close file, etc.)
    """
```
:::

::: api-signature
```python
def log_buttons() -> None:
    """
    Helper to display buttons for logging to tty/file/clipboard
    """
```
:::

::: api-signature
```python
def log_text(
    text: str,
) -> None:
    """
    Pass text data straight to log (without being displayed)
    """
```
:::

::: api-signature
```python
def set_nanobind_leak_warnings(
    enable: bool,
) -> None:
```
:::

## Styles

Note: functions shown below intentionally do not accept `None` as the destination style.  Python wrappers with same name exist in the `slimgui` module that can be called with `None` that then modifies the current context's style.

### Functions
::: api-signature
```python
def style_colors_dark(
    dst: slimgui.slimgui_ext.imgui.Style | None = None,
) -> None:
    """
    Write dark mode styles into the destination style.  Set directly to context's style if dst is None.
    """
```
:::

::: api-signature
```python
def style_colors_light(
    dst: slimgui.slimgui_ext.imgui.Style | None = None,
) -> None:
    """
    Write light mode styles into the destination style.  Set directly to context's style if dst is None.
    """
```
:::

::: api-signature
```python
def style_colors_classic(
    dst: slimgui.slimgui_ext.imgui.Style | None = None,
) -> None:
    """
    Write classic mode styles into the destination style.  Set directly to context's style if dst is None.
    """
```
:::

## Windows

- `begin()` = push window to the stack and start appending to it. `end()` = pop window from the stack.
- Passing `closable = True` shows a window-closing widget in the upper-right corner of the window,
  which clicking will set the boolean to false when clicked.
- You may append multiple times to the same window during the same frame by calling `begin()`/`end()` pairs multiple times. Some information such as `flags` or `closable` will only be considered by the first call to `begin()`.
- `begin()` returns `False` to indicate the window is collapsed or fully clipped, so you may early out and omit submitting
  anything to the window. Always call a matching `end()` for each `begin()` call, regardless of its return value!

  Important: due to legacy reason, `begin()`/`end()` and `begin_child()`/`end_child()` are inconsistent with all other functions such as `begin_menu()`/`end_menu()`, `begin_popup()`/`end_popup()`, etc. where the `end_xxx()` call should only be called if the corresponding
   `begin_xxx()` function returned `True`. `begin()` and `begin_child()` are the only odd ones out. Will be fixed in a future update.
- Note that the bottom of window stack always contains a window called "Debug".

### Functions
::: api-signature
```python
def begin(
    name: str,
    closable: bool = False,
    flags: WindowFlags = WindowFlags.NONE,
) -> tuple[bool, bool]:
    """
    When the `closable` argument is set to `True`, the created window will display a close button.  The second bool of the return value will be `False` if the close button was pressed.  The intended usage is as follows:
    ```python
    win_open = True  # open/closed state

    visible, win_open = imgui.begin(..., closable=win_open)
    if visible:
        # render window contents here..
    imgui.end()
    ```
    """
```
:::

::: api-signature
```python
def end() -> None:
    """
    Every `begin()` call must be paired with a corresponding `end()` call, regardless of the return value of `begin()` return value.
    """
```
:::

## Child Windows

- Use child windows to begin into a self-contained independent scrolling/clipping regions within a host window. Child windows can embed their own child.
- Manual sizing (each axis can use a different setting e.g. `(0, 400)`):
  == 0: use remaining parent window size for this axis.
   > 0: use specified size for this axis.
   < 0: right/bottom-align to specified distance from available content boundaries.
- Specifying `ChildFlags.AUTO_RESIZE_X` or `ChildFlags.AUTO_RESIZE_Y` makes the sizing automatic based on child contents.
  Combining both `ChildFlags.AUTO_RESIZE_X` _and_ `ChildFlags.AUTO_RESIZE_Y` defeats purpose of a scrolling region and is NOT recommended.
- `begin_child()` returns false to indicate the window is collapsed or fully clipped, so you may early out and omit submitting
  anything to the window. Always call a matching `end_child()` for each `begin_child()` call, regardless of its return value.

Important: due to legacy reason, `begin()`/`end()` and `begin_child()`/`end_child()` are inconsistent with all other functions such as `begin_menu()`/`end_menu()`, `begin_popup()`/`end_popup()`, etc. where the `end_xxx()` call should only be called if the corresponding `begin_xxx()` function returned true. `begin()` and `begin_child()` are the only odd ones out. Will be fixed in a future update.

### Functions
::: api-signature
```python
def begin_child(
    str_id: str,
    size: tuple[float, float] = (0.0, 0.0),
    child_flags: ChildFlags = ChildFlags.NONE,
    window_flags: WindowFlags = WindowFlags.NONE,
) -> bool:
```
:::

::: api-signature
```python
def end_child() -> None:
```
:::

## Window Utilities

- 'current window' = the window we are appending into while inside a `begin()`/`end()` block. 'next window' = next window we will `begin()` into.

### Functions
::: api-signature
```python
def is_window_appearing() -> bool:
```
:::

::: api-signature
```python
def is_window_collapsed() -> bool:
```
:::

::: api-signature
```python
def is_window_focused(
    flags: FocusedFlags = FocusedFlags.NONE,
) -> bool:
    """
    Is current window focused? or its root/child, depending on flags. see flags for options.
    """
```
:::

::: api-signature
```python
def is_window_hovered(
    flags: HoveredFlags = HoveredFlags.NONE,
) -> bool:
    """
    Is current window hovered and hoverable (e.g. not blocked by a popup/modal)? See `HoveredFlags` for options. IMPORTANT: If you are trying to check whether your mouse should be dispatched to Dear ImGui or to your underlying app, you should not use this function! Use the 'io.WantCaptureMouse' boolean for that! Refer to FAQ entry "How can I tell whether to dispatch mouse/keyboard to Dear ImGui or my application?" for details.
    """
```
:::

::: api-signature
```python
def get_window_draw_list() -> slimgui.imgui.DrawList:
    """
    Get draw list associated to the current window, to append your own drawing primitives.
    """
```
:::

::: api-signature
```python
def get_window_pos() -> tuple[float, float]:
    """
    Get current window position in screen space (IT IS UNLIKELY YOU EVER NEED TO USE THIS. Consider always using `get_cursor_screen_pos()` and `get_content_region_avail()` instead)
    """
```
:::

::: api-signature
```python
def get_window_size() -> tuple[float, float]:
    """
    Get current window size (IT IS UNLIKELY YOU EVER NEED TO USE THIS. Consider always using `get_cursor_screen_pos()` and `get_content_region_avail()` instead)
    """
```
:::

::: api-signature
```python
def get_window_width() -> float:
    """
    Get current window width (IT IS UNLIKELY YOU EVER NEED TO USE THIS). Shortcut for `get_window_size()`.x.
    """
```
:::

::: api-signature
```python
def get_window_height() -> float:
    """
    Get current window height (IT IS UNLIKELY YOU EVER NEED TO USE THIS). Shortcut for `get_window_size()`.y.
    """
```
:::

## Window Manipulation

- Prefer using `set_next_xxx` functions (before `begin`) rather than `set_xxx` functions (after `begin`).

### Functions
::: api-signature
```python
def set_next_window_pos(
    pos: tuple[float, float],
    cond: Cond = Cond.NONE,
    pivot: tuple[float, float] = (0.0, 0.0),
) -> None:
    """
    Set next window position. call before `begin()`. use pivot=(0.5f,0.5f) to center on given point, etc.
    """
```
:::

::: api-signature
```python
def set_next_window_size(
    size: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    Set next window size. set axis to 0.0f to force an auto-fit on this axis. call before `begin()`
    """
```
:::

::: api-signature
```python
def set_next_window_size_constraints(
    size_min: tuple[float, float],
    size_max: tuple[float, float],
    cb: Optional[Callable[[tuple[float, float], tuple[float, float], tuple[float, float], int], tuple[float, float]]] = None,
    user_data_id: int = 0,
) -> None:
    """
    Set next window size limits.  Use 0.0 or FLT_MAX if you don't want limits.  Use -1 for both min and max of same axis to preserve current size (which itself is a constraint).  Use callback to apply non-trivial programmatic constraints.

    This function still has some rough corners.  It only accepts an integer `user_data` argument.  If you need to pass a float through it, you could for example convert to fixed point and convert back to float in the constraint function.  Or you can capture any such values as a function closure.

    Use of constrain callbacks:
    ```python
    def aspect_ratio_constraint_16_9(_pos:  FVec2, _current_size: FVec2, desired_size: FVec2, _int_user_data: int) -> FVec2:
        aspect_ratio = 16.0 / 9
        new_desired_y = int(desired_size[0] / aspect_ratio)
        return (desired_size[0], new_desired_y)

    # usage:

    imgui.set_next_window_size_constraints((0, 0), (FLT_MAX, FLT_MAX), aspect_ratio_constraint_16_9)
    ```
    """
```
:::

::: api-signature
```python
def set_next_window_content_size(
    size: tuple[float, float],
) -> None:
    """
    Set next window content size (~ scrollable client area, which enforce the range of scrollbars). Not including window decorations (title bar, menu bar, etc.) nor WindowPadding. set an axis to 0.0f to leave it automatic. call before `begin()`
    """
```
:::

::: api-signature
```python
def set_next_window_collapsed(
    collapsed: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    Set next window collapsed state. call before `begin()`
    """
```
:::

::: api-signature
```python
def set_next_window_focus() -> None:
    """
    Set next window to be focused / top-most. call before `begin()`
    """
```
:::

::: api-signature
```python
def set_next_window_scroll(
    scroll: tuple[float, float],
) -> None:
    """
    Set next window scrolling value (use < 0.0f to not affect a given axis).
    """
```
:::

::: api-signature
```python
def set_next_window_bg_alpha(
    alpha: float,
) -> None:
    """
    Set next window background color alpha. helper to easily override the Alpha component of `Col.WINDOW_BG`/ChildBg/PopupBg. you may also use `WindowFlags.NO_BACKGROUND`.
    """
```
:::

::: api-signature
```python
def set_window_pos(
    pos: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window position - call within `begin()`/`end()`. prefer using `set_next_window_pos()`, as this may incur tearing and side-effects.
    """
```
:::

::: api-signature
```python
def set_window_pos(
    name: str,
    pos: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window position - call within `begin()`/`end()`. prefer using `set_next_window_pos()`, as this may incur tearing and side-effects.
    """
```
:::

::: api-signature
```python
def set_window_size(
    size: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window size - call within `begin()`/`end()`. set to ImVec2(0, 0) to force an auto-fit. prefer using `set_next_window_size()`, as this may incur tearing and minor side-effects.
    """
```
:::

::: api-signature
```python
def set_window_size(
    name: str,
    size: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window size - call within `begin()`/`end()`. set to ImVec2(0, 0) to force an auto-fit. prefer using `set_next_window_size()`, as this may incur tearing and minor side-effects.
    """
```
:::

::: api-signature
```python
def set_window_collapsed(
    collapsed: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window collapsed state. prefer using `set_next_window_collapsed()`.
    """
```
:::

::: api-signature
```python
def set_window_collapsed(
    name: str,
    collapsed: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window collapsed state. prefer using `set_next_window_collapsed()`.
    """
```
:::

::: api-signature
```python
def set_window_focus() -> None:
    """
    (not recommended) set current window to be focused / top-most. prefer using `set_next_window_focus()`.
    """
```
:::

::: api-signature
```python
def set_window_focus(
    name: str,
) -> None:
    """
    (not recommended) set current window to be focused / top-most. prefer using `set_next_window_focus()`.
    """
```
:::

::: api-signature
```python
def set_window_pos(
    pos: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window position - call within `begin()`/`end()`. prefer using `set_next_window_pos()`, as this may incur tearing and side-effects.
    """
```
:::

::: api-signature
```python
def set_window_pos(
    name: str,
    pos: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window position - call within `begin()`/`end()`. prefer using `set_next_window_pos()`, as this may incur tearing and side-effects.
    """
```
:::

::: api-signature
```python
def set_window_size(
    size: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window size - call within `begin()`/`end()`. set to ImVec2(0, 0) to force an auto-fit. prefer using `set_next_window_size()`, as this may incur tearing and minor side-effects.
    """
```
:::

::: api-signature
```python
def set_window_size(
    name: str,
    size: tuple[float, float],
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window size - call within `begin()`/`end()`. set to ImVec2(0, 0) to force an auto-fit. prefer using `set_next_window_size()`, as this may incur tearing and minor side-effects.
    """
```
:::

::: api-signature
```python
def set_window_collapsed(
    collapsed: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window collapsed state. prefer using `set_next_window_collapsed()`.
    """
```
:::

::: api-signature
```python
def set_window_collapsed(
    name: str,
    collapsed: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    (not recommended) set current window collapsed state. prefer using `set_next_window_collapsed()`.
    """
```
:::

::: api-signature
```python
def set_window_focus() -> None:
    """
    (not recommended) set current window to be focused / top-most. prefer using `set_next_window_focus()`.
    """
```
:::

::: api-signature
```python
def set_window_focus(
    name: str,
) -> None:
    """
    (not recommended) set current window to be focused / top-most. prefer using `set_next_window_focus()`.
    """
```
:::

## Windows Scrolling

- Any change of scroll will be applied at the beginning of next frame in the first call to `begin()`.
- You may instead use `set_next_window_scroll()` prior to calling `begin()` to avoid this delay, as an alternative to using `set_scroll_x()`/`set_scroll_y()`.

### Functions
::: api-signature
```python
def set_next_window_scroll(
    scroll: tuple[float, float],
) -> None:
    """
    Set next window scrolling value (use < 0.0f to not affect a given axis).
    """
```
:::

::: api-signature
```python
def get_scroll_x() -> float:
    """
    Get scrolling amount [0 .. `get_scroll_max_x()`]
    """
```
:::

::: api-signature
```python
def get_scroll_y() -> float:
    """
    Get scrolling amount [0 .. `get_scroll_max_y()`]
    """
```
:::

::: api-signature
```python
def set_scroll_x(
    scroll_x: float,
) -> None:
    """
    Set scrolling amount [0 .. `get_scroll_max_x()`]
    """
```
:::

::: api-signature
```python
def set_scroll_y(
    scroll_y: float,
) -> None:
    """
    Set scrolling amount [0 .. `get_scroll_max_y()`]
    """
```
:::

::: api-signature
```python
def get_scroll_max_x() -> float:
    """
    Get maximum scrolling amount ~~ ContentSize.x - WindowSize.x - DecorationsSize.x
    """
```
:::

::: api-signature
```python
def get_scroll_max_y() -> float:
    """
    Get maximum scrolling amount ~~ ContentSize.y - WindowSize.y - DecorationsSize.y
    """
```
:::

::: api-signature
```python
def set_scroll_here_x(
    center_x_ratio: float = 0.5,
) -> None:
    """
    Adjust scrolling amount to make current cursor position visible. center_x_ratio=0.0: left, 0.5: center, 1.0: right. When using to make a "default/current item" visible, consider using `set_item_default_focus()` instead.
    """
```
:::

::: api-signature
```python
def set_scroll_here_y(
    center_y_ratio: float = 0.5,
) -> None:
    """
    Adjust scrolling amount to make current cursor position visible. center_y_ratio=0.0: top, 0.5: center, 1.0: bottom. When using to make a "default/current item" visible, consider using `set_item_default_focus()` instead.
    """
```
:::

::: api-signature
```python
def set_scroll_from_pos_x(
    local_x: float,
    center_x_ratio: float = 0.5,
) -> None:
    """
    Adjust scrolling amount to make given position visible. Generally `get_cursor_start_pos()` + offset to compute a valid position.
    """
```
:::

::: api-signature
```python
def set_scroll_from_pos_y(
    local_y: float,
    center_y_ratio: float = 0.5,
) -> None:
    """
    Adjust scrolling amount to make given position visible. Generally `get_cursor_start_pos()` + offset to compute a valid position.
    """
```
:::

## Parameter stacks (shared)

### Functions
::: api-signature
```python
def push_font(
    font: Font | None,
    font_size_base: float,
) -> None:
    """
    Use `None` as a shortcut to keep current font.  Use 0.0 for `font_size_base` to keep the current font size.
    """
```
:::

::: api-signature
```python
def pop_font() -> None:
```
:::

::: api-signature
```python
def push_style_color(
    idx: Col,
    col: int,
) -> None:
    """
    Modify a style color. always use this if you modify the style after `new_frame()`.
    """
```
:::

::: api-signature
```python
def push_style_color(
    idx: Col,
    col: tuple[float, float, float, float],
) -> None:
    """
    Modify a style color. always use this if you modify the style after `new_frame()`.
    """
```
:::

::: api-signature
```python
def push_style_color(
    idx: Col,
    col: tuple[float, float, float],
) -> None:
    """
    Modify a style color. always use this if you modify the style after `new_frame()`.
    """
```
:::

::: api-signature
```python
def pop_style_color(
    count: int = 1,
) -> None:
```
:::

::: api-signature
```python
def push_style_var(
    idx: StyleVar,
    val: float,
) -> None:
    """
    Modify a style float variable. always use this if you modify the style after `new_frame()`!
    """
```
:::

::: api-signature
```python
def push_style_var(
    idx: StyleVar,
    val: tuple[float, float],
) -> None:
    """
    Modify a style float variable. always use this if you modify the style after `new_frame()`!
    """
```
:::

::: api-signature
```python
def push_style_var_x(
    idx: StyleVar,
    val_x: float,
) -> None:
    """
    Modify X component of a style ImVec2 variable. "
    """
```
:::

::: api-signature
```python
def push_style_var_y(
    idx: StyleVar,
    val_y: float,
) -> None:
    """
    Modify Y component of a style ImVec2 variable. "
    """
```
:::

::: api-signature
```python
def pop_style_var(
    count: int = 1,
) -> None:
```
:::

::: api-signature
```python
def push_item_flag(
    option: ItemFlags,
    enabled: bool,
) -> None:
    """
    Modify specified shared item flag, e.g. `push_item_flag(ItemFlags.NO_TAB_STOP, true)`
    """
```
:::

::: api-signature
```python
def pop_item_flag() -> None:
```
:::

::: api-signature
```python
def get_item_flags() -> int:
    """
    Get generic flags of the last item.
    """
```
:::

## Parameter stacks (current window)

### Functions
::: api-signature
```python
def push_item_width(
    item_width: float,
) -> None:
    """
    Push width of items for common large "item+label" widgets. >0.0f: width in pixels, <0.0f align xx pixels to the right of window (so -FLT_MIN always align width to the right side).
    """
```
:::

::: api-signature
```python
def pop_item_width() -> None:
```
:::

::: api-signature
```python
def set_next_item_width(
    item_width: float,
) -> None:
    """
    Set width of the _next_ common large "item+label" widget. >0.0f: width in pixels, <0.0f align xx pixels to the right of window (so -FLT_MIN always align width to the right side)
    """
```
:::

::: api-signature
```python
def calc_item_width() -> float:
    """
    Width of item given pushed settings and current cursor position. NOT necessarily the width of last item unlike most 'Item' functions.
    """
```
:::

::: api-signature
```python
def push_text_wrap_pos(
    wrap_local_pos_x: float = 0.0,
) -> None:
```
:::

::: api-signature
```python
def pop_text_wrap_pos() -> None:
```
:::

## Style read access

- Use `show_style_editor()` function to interactively see/edit the colors.

### Functions
::: api-signature
```python
def get_font() -> slimgui.slimgui_ext.imgui.Font:
    """
    Get the current font.
    """
```
:::

::: api-signature
```python
def get_font_size() -> float:
    """
    Get current font size (= height in pixels) of current font, with global scale factors applied.

    - Use `style.font_size_base` to get value before global scale factors.
    - recap: `imgui.get_font_size() == style.font_size_base * (style.font_scale_main * style.font_scale_dpi * other_scaling_factors)`
    """
```
:::

Get current font size (= height in pixels) of current font, with global scale factors applied.

- Use `style.font_size_base` to get value before global scale factors.
- recap: `imgui.get_font_size() == style.font_size_base * (style.font_scale_main * style.font_scale_dpi * other_scaling_factors)`

::: api-signature
```python
def get_font_tex_uv_white_pixel() -> tuple[float, float]:
    """
    Get UV coordinate for a white pixel, useful to draw custom shapes via the ImDrawList API
    """
```
:::

::: api-signature
```python
def get_color_u32(
    idx: Col,
    alpha_mul: float = 1.0,
) -> int:
    """
    Retrieve given style color with style alpha applied and optional extra alpha multiplier, packed as a 32-bit value suitable for ImDrawList
    """
```
:::

::: api-signature
```python
def get_color_u32(
    col: tuple[float, float, float, float],
) -> int:
    """
    Retrieve given style color with style alpha applied and optional extra alpha multiplier, packed as a 32-bit value suitable for ImDrawList
    """
```
:::

::: api-signature
```python
def get_color_u32(
    col: int,
    alpha_mul: float = 1.0,
) -> int:
    """
    Retrieve given style color with style alpha applied and optional extra alpha multiplier, packed as a 32-bit value suitable for ImDrawList
    """
```
:::

::: api-signature
```python
def get_style_color_vec4(
    col: Col,
) -> tuple[float, float, float, float]:
    """
    Retrieve style color as stored in ImGuiStyle structure. use to feed back into `push_style_color()`, otherwise use `get_color_u32()` to get style color with style alpha baked in.
    """
```
:::

## Layout cursor positioning

- By "cursor" we mean the current output position.
- The typical widget behavior is to output themselves at the current cursor position, then move the cursor one line down.
- You can call `same_line()` between widgets to undo the last carriage return and output at the right of the preceding widget.
- YOU CAN DO 99% OF WHAT YOU NEED WITH ONLY `get_cursor_screen_pos()` and `get_content_region_avail()`.
- Attention! We currently have inconsistencies between window-local and absolute positions we will aim to fix with future API:
  - Absolute coordinate: `get_cursor_screen_pos()`, `set_cursor_screen_pos()`, all `DrawList` functions. -> this is the preferred way forward.
  - Window-local coordinates: `same_line(offset)`, `get_cursor_pos()`, `set_cursor_pos()`, `get_cursor_start_pos()`, `push_text_wrap_pos()`
  - Window-local coordinates: `get_content_region_max()`, `get_window_content_region_min()`, `get_window_content_region_max()` --> all obsoleted. YOU DON'T NEED THEM.
- `get_cursor_screen_pos()` = `get_cursor_pos()` + `get_window_pos()`. `get_window_pos()` is almost only ever useful to convert from window-local to absolute coordinates. Try not to use it.

### Functions
::: api-signature
```python
def get_cursor_screen_pos() -> tuple[float, float]:
    """
    Cursor position, absolute coordinates. THIS IS YOUR BEST FRIEND (prefer using this rather than `get_cursor_pos()`, also more useful to work with ImDrawList API).
    """
```
:::

::: api-signature
```python
def set_cursor_screen_pos(
    pos: tuple[float, float],
) -> None:
    """
    Cursor position, absolute coordinates. THIS IS YOUR BEST FRIEND.
    """
```
:::

::: api-signature
```python
def get_content_region_avail() -> tuple[float, float]:
    """
    Available space from current position. THIS IS YOUR BEST FRIEND.
    """
```
:::

::: api-signature
```python
def get_cursor_pos() -> tuple[float, float]:
    """
    [window-local] cursor position in window-local coordinates. This is not your best friend.
    """
```
:::

::: api-signature
```python
def get_cursor_pos_x() -> float:
    """
    [window-local] "
    """
```
:::

::: api-signature
```python
def get_cursor_pos_y() -> float:
    """
    [window-local] "
    """
```
:::

::: api-signature
```python
def set_cursor_pos(
    local_pos: tuple[float, float],
) -> None:
    """
    [window-local] "
    """
```
:::

::: api-signature
```python
def set_cursor_pos_x(
    local_x: float,
) -> None:
    """
    [window-local] "
    """
```
:::

::: api-signature
```python
def set_cursor_pos_y(
    local_y: float,
) -> None:
    """
    [window-local] "
    """
```
:::

::: api-signature
```python
def get_cursor_start_pos() -> tuple[float, float]:
    """
    [window-local] initial cursor position, in window-local coordinates. Call `get_cursor_screen_pos()` after `begin()` to get the absolute coordinates version.
    """
```
:::

## Other layout functions

### Functions
::: api-signature
```python
def separator() -> None:
    """
    Separator, generally horizontal. inside a menu bar or in horizontal layout mode, this becomes a vertical separator.
    """
```
:::

::: api-signature
```python
def same_line(
    offset_from_start_x: float = 0.0,
    spacing: float = -1.0,
) -> None:
    """
    Call between widgets or groups to layout them horizontally. X position given in window coordinates.
    """
```
:::

::: api-signature
```python
def new_line() -> None:
    """
    Undo a `same_line()` or force a new line when in a horizontal-layout context.
    """
```
:::

::: api-signature
```python
def spacing() -> None:
    """
    Add vertical spacing.
    """
```
:::

::: api-signature
```python
def dummy(
    size: tuple[float, float],
) -> None:
    """
    Add a dummy item of given size. unlike `invisible_button()`, `dummy()` won't take the mouse click or be navigable into.
    """
```
:::

::: api-signature
```python
def indent(
    indent_w: float = 0.0,
) -> None:
    """
    Move content position toward the right, by indent_w, or style.IndentSpacing if indent_w <= 0
    """
```
:::

::: api-signature
```python
def unindent(
    indent_w: float = 0.0,
) -> None:
    """
    Move content position back to the left, by indent_w, or style.IndentSpacing if indent_w <= 0
    """
```
:::

::: api-signature
```python
def begin_group() -> None:
    """
    Lock horizontal starting position
    """
```
:::

::: api-signature
```python
def end_group() -> None:
    """
    Unlock horizontal starting position + capture the whole group bounding box into one "item" (so you can use `is_item_hovered()` or layout primitives such as `same_line()` on whole group, etc.)
    """
```
:::

::: api-signature
```python
def align_text_to_frame_padding() -> None:
    """
    Vertically align upcoming text baseline to FramePadding.y so that it will align properly to regularly framed items (call if you have text on a line before a framed item)
    """
```
:::

::: api-signature
```python
def get_text_line_height() -> float:
    """
    ~ FontSize
    """
```
:::

::: api-signature
```python
def get_text_line_height_with_spacing() -> float:
    """
    ~ FontSize + style.ItemSpacing.y (distance in pixels between 2 consecutive lines of text)
    """
```
:::

::: api-signature
```python
def get_frame_height() -> float:
    """
    ~ FontSize + style.FramePadding.y * 2
    """
```
:::

::: api-signature
```python
def get_frame_height_with_spacing() -> float:
    """
    ~ FontSize + style.FramePadding.y * 2 + style.ItemSpacing.y (distance in pixels between 2 consecutive lines of framed widgets)
    """
```
:::

## ID stack/scopes

Read the FAQ (docs/FAQ.md or http://dearimgui.com/faq) for more details about how ID are handled in dear imgui.

Those questions are answered and impacted by understanding of the ID stack system:

  - "Q: Why is my widget not reacting when I click on it?"
  - "Q: How can I have widgets with an empty label?"
  - "Q: How can I have multiple widgets with the same label?"

Short version: ID are hashes of the entire ID stack. If you are creating widgets in a loop you most likely want to push a unique identifier (e.g. object pointer, loop index) to uniquely differentiate them.

You can also use the `"Label##foobar"` syntax within widget label to distinguish them from each others.

In this header file we use the `label`/`name` terminology to denote a string that will be displayed + used as an ID, whereas `str_id` denote a string that is only used as an ID and not normally displayed.

### Functions
::: api-signature
```python
def push_id(
    str_id: str,
) -> None:
    """
    Push string into the ID stack (will hash string).
    """
```
:::

::: api-signature
```python
def push_id(
    int_id: int,
) -> None:
    """
    Push string into the ID stack (will hash string).
    """
```
:::

::: api-signature
```python
def pop_id() -> None:
    """
    Pop from the ID stack.
    """
```
:::

::: api-signature
```python
def get_id(
    str_id: str,
) -> None:
    """
    Calculate unique ID (hash of whole ID stack + given parameter). e.g. if you want to query into ImGuiStorage yourself
    """
```
:::

::: api-signature
```python
def get_id(
    int_id: int,
) -> None:
    """
    Calculate unique ID (hash of whole ID stack + given parameter). e.g. if you want to query into ImGuiStorage yourself
    """
```
:::

## Widgets: Text

### Functions
::: api-signature
```python
def text(
    text: str,
) -> None:
    """
    Formatted text
    """
```
:::

::: api-signature
```python
def text_colored(
    col: tuple[float, float, float, float],
    text: str,
) -> None:
```
:::

::: api-signature
```python
def text_disabled(
    text: str,
) -> None:
```
:::

::: api-signature
```python
def text_wrapped(
    text: str,
) -> None:
```
:::

::: api-signature
```python
def label_text(
    label: str,
    text: str,
) -> None:
    """
    Display text+label aligned the same way as value+label widgets
    """
```
:::

::: api-signature
```python
def bullet_text(
    text: str,
) -> None:
    """
    Shortcut for `bullet()`+`text()`
    """
```
:::

::: api-signature
```python
def separator_text(
    text: str,
) -> None:
    """
    Currently: formatted text with a horizontal line
    """
```
:::

## Widgets: Main

- Most widgets return `True` when the value has been changed or when pressed/selected.
- You may also use one of the many `is_item_xxx` functions (e.g. `is_item_active()`, `is_item_hovered()`, etc.) to query widget state.

### Functions
::: api-signature
```python
def button(
    label: str,
    size: tuple[float, float] = (0.0, 0.0),
) -> bool:
    """
    Button
    """
```
:::

::: api-signature
```python
def small_button(
    label: str,
) -> bool:
    """
    Button with (FramePadding.y == 0) to easily embed within text
    """
```
:::

::: api-signature
```python
def invisible_button(
    str_id: str,
    size: tuple[float, float],
    flags: ButtonFlags = ButtonFlags.NONE,
) -> bool:
    """
    Flexible button behavior without the visuals, frequently useful to build custom behaviors using the public api (along with `is_item_active`, `is_item_hovered`, etc.)
    """
```
:::

::: api-signature
```python
def arrow_button(
    str_id: str,
    dir: Dir,
) -> bool:
    """
    Square button with an arrow shape
    """
```
:::

::: api-signature
```python
def checkbox(
    label: str,
    v: bool,
) -> tuple[bool, bool]:
```
:::

::: api-signature
```python
def checkbox_flags(
    label: str,
    flags: int,
    flags_value: int,
) -> tuple[bool, int]:
```
:::

::: api-signature
```python
def radio_button(
    label: str,
    active: bool,
) -> bool:
```
:::

::: api-signature
```python
def radio_button(
    label: str,
    v: int,
    v_button: int,
) -> tuple[bool, int]:
```
:::

::: api-signature
```python
def progress_bar(
    fraction: float,
    size_arg: tuple[float, float] = (-FLT_MIN, 0),
    overlay: str | None = None,
) -> None:
```
:::

::: api-signature
```python
def bullet() -> None:
    """
    Draw a small circle + keep the cursor on the same line. advance cursor x position by `get_tree_node_to_label_spacing()`, same distance that `tree_node()` uses
    """
```
:::

::: api-signature
```python
def text_link(
    label: str,
) -> None:
    """
    Hyperlink text button, return true when clicked
    """
```
:::

::: api-signature
```python
def text_link_open_url(
    label: str,
    url: str | None = None,
) -> None:
    """
    Hyperlink text button, automatically open file/url when clicked
    """
```
:::

## Widgets: Images

- Read about texture IDs and TextureRef in ImGui docs: [Image Loading and Displaying Examples](https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples)
  - In general, you shouldn't need to worry about `TextureRef` -- all image functions also accept an integer texture ID.
- `uv0` and `uv1` are texture coordinates. Read about them from the same link above.
  - `image()` pads adds `StyleVar.IMAGE_BORDER_SIZE` on each side, `image_button()` adds `StyleVar.FRAME_PADDING` on each side.
  - `image_button()` draws a background based on regular `button()` color and optionally an inner background if specified.

### Functions
::: api-signature
```python
def image(
    tex_ref: TextureRef | int,
    image_size: tuple[float, float],
    uv0: tuple[float, float] = (0.0, 0.0),
    uv1: tuple[float, float] = (1.0, 1.0),
) -> None:
```
:::

::: api-signature
```python
def image_with_bg(
    tex_ref: TextureRef | int,
    image_size: tuple[float, float],
    uv0: tuple[float, float] = (0.0, 0.0),
    uv1: tuple[float, float] = (1.0, 1.0),
    bg_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
) -> None:
```
:::

::: api-signature
```python
def image_button(
    str_id: str,
    tex_ref: TextureRef | int,
    image_size: tuple[float, float],
    uv0: tuple[float, float] = (0.0, 0.0),
    uv1: tuple[float, float] = (1.0, 1.0),
    bg_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
) -> bool:
```
:::

## Widgets: Combo Box (Dropdown)

- The `begin_combo()`/`end_combo()` API allows you to manage your contents and selection state however you want it, by creating e.g. `selectable()` items.
- The old `combo()` API are helpers over `begin_combo()`/`end_combo()` which are kept available for convenience purposes. This is analogous to how `list_box` is created.

### Functions
::: api-signature
```python
def begin_combo(
    label: str,
    preview_value: str,
    flags: ComboFlags = ComboFlags.NONE,
) -> bool:
```
:::

::: api-signature
```python
def end_combo() -> None:
    """
    Only call `end_combo()` if `begin_combo()` returns true!
    """
```
:::

::: api-signature
```python
def combo(
    label: str,
    current_item: int,
    items: Sequence[str],
    popup_max_height_in_items: int = -1,
) -> tuple[bool, int]:
```
:::
## Widgets: Drag Sliders

- CTRL+Click on any drag box to turn them into an input box. Manually input values aren't clamped by default and can go off-bounds. Use `SliderFlags.ALWAYS_CLAMP` to always clamp.
- Adjust format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision e.g. `"%.3f"` -> `1.234`; `"%5.2f secs"` -> `01.23 secs`; `"Biscuit: %.0f"` -> `Biscuit: 1`; etc.
- Format string may also be set to `None` or use the default format (`"%f"` or `"%d"`).
- Speed is per-pixel of mouse movement (`v_speed=0.2`: mouse needs to move by 5 pixels to increase value by 1). For keyboard/gamepad navigation, minimum speed is `max(v_speed, minimum_step_at_given_precision)`.
- Use `v_min < v_max` to clamp edits to given limits. Note that CTRL+Click manual input can override those limits if `SliderFlags.ALWAYS_CLAMP` is not used.
- Use `v_max = FLT_MAX` / `INT_MAX` etc. to avoid clamping to a maximum, same with `v_min = -FLT_MAX` / `INT_MIN` to avoid clamping to a minimum.
- We use the same sets of flags for `drag_xxx()` and `slider_xxx()` functions as the features are the same and it makes it easier to swap them.

### Functions
::: api-signature
```python
def drag_float(
    label: str,
    v: float,
    v_speed: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 0.0,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, float]:
    """
    If v_min >= v_max we have no bound
    """
```
:::

::: api-signature
```python
def drag_float2(
    label: str,
    v: tuple[float, float],
    v_speed: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 0.0,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float]]:
```
:::

::: api-signature
```python
def drag_float3(
    label: str,
    v: tuple[float, float, float],
    v_speed: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 0.0,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float, float]]:
```
:::

::: api-signature
```python
def drag_float4(
    label: str,
    v: tuple[float, float, float, float],
    v_speed: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 0.0,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float, float, float]]:
```
:::

::: api-signature
```python
def drag_float_range2(
    label: str,
    v_current_min: float,
    v_current_max: float,
    v_speed: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 0.0,
    format: str = '%.3f',
    format_max: str | None = None,
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, float, float]:
```
:::

::: api-signature
```python
def drag_int(
    label: str,
    v: int,
    v_speed: float = 1.0,
    v_min: int = 0,
    v_max: int = 0,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, int]:
    """
    If v_min >= v_max we have no bound
    """
```
:::

::: api-signature
```python
def drag_int2(
    label: str,
    v: tuple[int, int],
    v_speed: float = 1.0,
    v_min: int = 0,
    v_max: int = 0,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int]]:
```
:::

::: api-signature
```python
def drag_int3(
    label: str,
    v: tuple[int, int, int],
    v_speed: float = 1.0,
    v_min: int = 0,
    v_max: int = 0,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int, int]]:
```
:::

::: api-signature
```python
def drag_int4(
    label: str,
    v: tuple[int, int, int, int],
    v_speed: float = 1.0,
    v_min: int = 0,
    v_max: int = 0,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int, int, int]]:
```
:::

::: api-signature
```python
def drag_int_range2(
    label: str,
    v_current_min: int,
    v_current_max: int,
    v_speed: float = 1.0,
    v_min: int = 0,
    v_max: int = 0,
    format: str = '%d',
    format_max: str | None = None,
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, int, int]:
```
:::

## Widgets: Regular Sliders

- CTRL+Click on any slider to turn it into an input box. Manually input values aren't clamped by default and can go off-bounds. Use `SliderFlags.ALWAYS_CLAMP` to always clamp.
- Adjust the format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision, e.g., `"%.3f"` -> `1.234`; `"%5.2f secs"` -> `01.23 secs`; `"Biscuit: %.0f"` -> `Biscuit: 1`; etc.
- The format string may also be set to `None` or use the default format (`"%f"` or `"%d"`).

### Functions
::: api-signature
```python
def slider_float(
    label: str,
    v: float,
    v_min: float,
    v_max: float,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, float]:
    """
    Adjust format to decorate the value with a prefix or a suffix for in-slider labels or unit display.
    """
```
:::

::: api-signature
```python
def slider_float2(
    label: str,
    v: tuple[float, float],
    v_min: float,
    v_max: float,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float]]:
```
:::

::: api-signature
```python
def slider_float3(
    label: str,
    v: tuple[float, float, float],
    v_min: float,
    v_max: float,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float, float]]:
```
:::

::: api-signature
```python
def slider_float4(
    label: str,
    v: tuple[float, float, float, float],
    v_min: float,
    v_max: float,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[float, float, float, float]]:
```
:::

::: api-signature
```python
def slider_angle(
    label: str,
    v: float,
    v_degrees_min: float = -360.0,
    v_degrees_max: float = 360.0,
    format: str = '%.0f deg',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, float]:
```
:::

::: api-signature
```python
def slider_int(
    label: str,
    v: int,
    v_min: int,
    v_max: int,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, int]:
```
:::

::: api-signature
```python
def slider_int2(
    label: str,
    v: tuple[int, int],
    v_min: int,
    v_max: int,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int]]:
```
:::

::: api-signature
```python
def slider_int3(
    label: str,
    v: tuple[int, int, int],
    v_min: int,
    v_max: int,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int, int]]:
```
:::

::: api-signature
```python
def slider_int4(
    label: str,
    v: tuple[int, int, int, int],
    v_min: int,
    v_max: int,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, tuple[int, int, int, int]]:
```
:::

::: api-signature
```python
def vslider_float(
    label: str,
    size: tuple[float, float],
    v: float,
    v_min: float,
    v_max: float,
    format: str = '%.3f',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, float]:
```
:::

::: api-signature
```python
def vslider_int(
    label: str,
    size: tuple[float, float],
    v: int,
    v_min: int,
    v_max: int,
    format: str = '%d',
    flags: SliderFlags = SliderFlags.NONE,
) -> tuple[bool, int]:
```
:::

## Widgets: Input with Keyboard

- Most of the `InputTextFlags` flags are only useful for `input_text()` and not for `input_float_*`, `input_float_*`, `input_int_*`, etc.

### Functions
::: api-signature
```python
def input_text(
    label: str,
    text: str,
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, str]:
```
:::

::: api-signature
```python
def input_text_multiline(
    label: str,
    text: str,
    size: tuple[float, float] = (0.0, 0.0),
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, str]:
```
:::

::: api-signature
```python
def input_text_with_hint(
    label: str,
    hint: str,
    text: str,
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, str]:
```
:::

::: api-signature
```python
def input_float(
    label: str,
    v: float,
    step: float = 0.0,
    step_fast: float = 0.0,
    format: str = '%.3f',
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, float]:
```
:::

::: api-signature
```python
def input_float2(
    label: str,
    v: tuple[float, float],
    format: str = '%.3f',
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[float, float]]:
```
:::

::: api-signature
```python
def input_float3(
    label: str,
    v: tuple[float, float, float],
    format: str = '%.3f',
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[float, float, float]]:
```
:::

::: api-signature
```python
def input_float4(
    label: str,
    v: tuple[float, float, float, float],
    format: str = '%.3f',
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[float, float, float, float]]:
```
:::

::: api-signature
```python
def input_int(
    label: str,
    v: int,
    step: int = 1,
    step_fast: int = 100,
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, int]:
```
:::

::: api-signature
```python
def input_int2(
    label: str,
    v: tuple[int, int],
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[int, int]]:
```
:::

::: api-signature
```python
def input_int3(
    label: str,
    v: tuple[int, int, int],
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[int, int, int]]:
```
:::

::: api-signature
```python
def input_int4(
    label: str,
    v: tuple[int, int, int, int],
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, tuple[int, int, int, int]]:
```
:::

::: api-signature
```python
def input_double(
    label: str,
    v: float,
    step: float = 0.0,
    step_fast: float = 0.0,
    format: str = '%.6f',
    flags: InputTextFlags = InputTextFlags.NONE,
) -> tuple[bool, float]:
```
:::

## Widgets: Color Editor/Picker

Tip: the `color_edit_*` functions have a little color square that can be left-clicked to open a picker, and right-clicked to open an option menu.

### Functions
::: api-signature
```python
def color_edit3(
    label: str,
    col: tuple[float, float, float],
    flags: ColorEditFlags = ColorEditFlags.NONE,
) -> tuple[bool, tuple[float, float, float]]:
```
:::

::: api-signature
```python
def color_edit4(
    label: str,
    col: tuple[float, float, float, float],
    flags: ColorEditFlags = ColorEditFlags.NONE,
) -> tuple[bool, tuple[float, float, float, float]]:
```
:::

::: api-signature
```python
def color_picker3(
    label: str,
    col: tuple[float, float, float],
    flags: ColorEditFlags = ColorEditFlags.NONE,
) -> tuple[bool, tuple[float, float, float]]:
```
:::

::: api-signature
```python
def color_picker4(
    label: str,
    col: tuple[float, float, float, float],
    flags: ColorEditFlags = ColorEditFlags.NONE,
    ref_col: tuple[float, float, float, float] | None = None,
) -> tuple[bool, tuple[float, float, float, float]]:
```
:::

::: api-signature
```python
def color_button(
    desc_id: str,
    col: tuple[float, float, float, float],
    flags: ColorEditFlags = ColorEditFlags.NONE,
    size: tuple[float, float] = (0.0, 0.0),
) -> bool:
    """
    Display a color square/button, hover for details, return true when pressed.
    """
```
:::

::: api-signature
```python
def set_color_edit_options(
    flags: ColorEditFlags,
) -> None:
    """
    Initialize current options (generally on application startup) if you want to select a default format, picker type, etc. User will be able to change many settings, unless you pass the _NoOptions flag to your calls.
    """
```
:::

## Widgets: Trees

- `tree_node` functions return `True` when the node is open, in which case you need to also call `tree_pop()` when you are finished displaying the tree node contents.

### Functions
::: api-signature
```python
def tree_node(
    label: str,
    flags: TreeNodeFlags = TreeNodeFlags.NONE,
) -> bool:
```
:::

::: api-signature
```python
def tree_node(
    str_id: str,
    text: str,
    flags: TreeNodeFlags = TreeNodeFlags.NONE,
) -> bool:
```
:::

::: api-signature
```python
def tree_push(
    str_id: str,
) -> None:
    """
    ~ `indent()`+`push_id()`. Already called by `tree_node()` when returning true, but you can call `tree_push`/`tree_pop` yourself if desired.
    """
```
:::

::: api-signature
```python
def tree_pop() -> None:
    """
    ~ `unindent()`+`pop_id()`
    """
```
:::

::: api-signature
```python
def get_tree_node_to_label_spacing() -> float:
    """
    Horizontal distance preceding label when using `tree_node`*() or `bullet()` == (g.FontSize + style.FramePadding.x*2) for a regular unframed `tree_node`
    """
```
:::

::: api-signature
```python
def collapsing_header(
    label: str,
    visible: bool | None = None,
    flags: TreeNodeFlags = TreeNodeFlags.NONE,
) -> tuple[bool, bool | None]:
    """
    If returning 'true' the header is open. doesn't indent nor push on ID stack. user doesn't have to call `tree_pop()`.
    """
```
:::

::: api-signature
```python
def set_next_item_open(
    is_open: bool,
    cond: Cond = Cond.NONE,
) -> None:
    """
    Set next `tree_node`/`collapsing_header` open state.
    """
```
:::

## Widgets: Selectables

- A selectable highlights when hovered, and can display another color when selected.
- Neighbors selectable extend their highlight bounds in order to leave no gap between them. This is so a series of selected `selectable` appear contiguous.

### Functions
::: api-signature
```python
def selectable(
    label: str,
    selected: bool = False,
    flags: SelectableFlags = SelectableFlags.NONE,
    size: tuple[float, float] = (0.0, 0.0),
) -> tuple[bool, bool]:
    """
    The `selected` argument indicates whether the item is selected or not.

    When `size[0] == 0.0` use remaining width.  Use `size[0] > 0.0` to specify width.
    When `size[1] == 0.0` use label height.  Use `size[1] > 0.0` to specify height.

    The returned pair contains:

    - first element: a boolean indicating whether the item was clicked.
    - second element: the updated selection state of the item.
    """
```
:::

## Multi-selection system for `selectable()`, `checkbox()`, `tree_node()` functions [BETA]

*TODO* Multi-selection is currently NOT supported in Slimgui.  [Issue #16](https://github.com/nurpax/slimgui/issues/16) tracks this implementation.

- This enables standard multi-selection/range-selection idioms (CTRL+Mouse/Keyboard, SHIFT+Mouse/Keyboard, etc.) in a way that also allows a clipper to be used.
- `SelectionUserData` is often used to store your item index within the current view (but may store something else).
- Read comments near `MultiSelectIO` for instructions/details and see 'Demo->Widgets->Selection State & Multi-Select' for demo.
- `tree_node()` is technically supported but... using this correctly is more complicated. You need some sort of linear/random access to your tree, which is suited to advanced tree setups already implementing filters and clipper. We will work on simplifying the current demo.
- `selection_size` and `items_count` parameters are optional and used by a few features. If they are costly for you to compute, you may avoid them.



## Widgets: List Boxes

- This is essentially a thin wrapper to using `begin_child()`/`end_child()` with the `ChildFlags.FRAME_STYLE` flag for stylistic changes and displaying a label.
- If you don't need a label, you can probably simply use `begin_child()` with the `ChildFlags.FRAME_STYLE` flag for the same result.
- You can submit contents and manage your selection state however you want, by creating e.g. `selectable()` or any other items.
- The simplified/old `list_box()` API are helpers over `begin_list_box()`/`end_list_box()` which are kept available for convenience purposes. This is analogous to how combos are created.
- Choose frame width:
  - `size.x > 0`: custom
  - `size.x < 0` or `-FLT_MIN`: right-align
  - `size.x = 0` (default): use current `item_width`
- Choose frame height:
  - `size.y > 0`: custom
  - `size.y < 0` or `-FLT_MIN`: bottom-align
  - `size.y = 0` (default): arbitrary default height which can fit ~7 items

### Functions
::: api-signature
```python
def begin_list_box(
    label: str,
    size: tuple[float, float] = (0.0, 0.0),
) -> bool:
    """
    Open a framed scrolling region
    """
```
:::

::: api-signature
```python
def end_list_box() -> None:
    """
    Only call `end_list_box()` if `begin_list_box()` returned true!
    """
```
:::

::: api-signature
```python
def list_box(
    label: str,
    current_item: int,
    items: Sequence[str],
    height_in_items: int = -1,
) -> tuple[bool, int]:
```
:::

## Widgets: Data Plotting

Consider using [ImPlot](https://github.com/epezent/implot) which is much better! Slimgui includes ImPlot bindings; see the [Slimgui ImPlot API reference](/api/implot) for details.

### Functions
::: api-signature
```python
def plot_lines(
    label: str,
    values: Annotated[NDArray[Any], dict(shape=(None,), device='cpu', writable=False)],
    overlay_text: str | None = None,
    scale_min: float = FLT_MAX,
    scale_max: float = FLT_MAX,
    graph_size: tuple[float, float] = (0.0, 0.0),
) -> None:
```
:::

::: api-signature
```python
def plot_histogram(
    label: str,
    values: Annotated[NDArray[Any], dict(shape=(None,), device='cpu', writable=False)],
    overlay_text: str | None = None,
    scale_min: float = FLT_MAX,
    scale_max: float = FLT_MAX,
    graph_size: tuple[float, float] = (0.0, 0.0),
) -> None:
```
:::

## Widgets: Value() Helpers

These are merely shortcuts to calling `text()` with a format string. Output single value in "name: value" format.

### Functions


## Widgets: Menus

- Use `begin_menu_bar()` on a window `WindowFlags.MENU_BAR` to append to its menu bar.
- Use `begin_main_menu_bar()` to create a menu bar at the top of the screen and append to it.
- Use `begin_menu()` to create a menu. You can call `begin_menu()` multiple times with the same identifier to append more items to it.
- Note that `menu_item()` keyboard shortcuts are displayed as a convenience but _not processed_ by Dear ImGui at the moment.

### Functions
::: api-signature
```python
def begin_menu_bar() -> bool:
    """
    Append to menu-bar of current window (requires `WindowFlags.MENU_BAR` flag set on parent window).
    """
```
:::

::: api-signature
```python
def end_menu_bar() -> None:
    """
    Only call `end_menu_bar()` if `begin_menu_bar()` returns true!
    """
```
:::

::: api-signature
```python
def begin_main_menu_bar() -> bool:
    """
    Create and append to a full screen menu-bar.
    """
```
:::

::: api-signature
```python
def end_main_menu_bar() -> None:
    """
    Only call `end_main_menu_bar()` if `begin_main_menu_bar()` returns true!
    """
```
:::

::: api-signature
```python
def begin_menu(
    label: str,
    enabled: bool = True,
) -> bool:
    """
    Create a sub-menu entry. only call `end_menu()` if this returns true!
    """
```
:::

::: api-signature
```python
def end_menu() -> None:
    """
    Only call `end_menu()` if `begin_menu()` returns true!
    """
```
:::

::: api-signature
```python
def menu_item(
    label: str,
    shortcut: str | None = None,
    selected: bool = False,
    enabled: bool = True,
) -> tuple[bool, bool]:
    """
    Return true when activated.
    """
```
:::

## Tooltips

- Tooltips are windows following the mouse. They do not take focus away.
- A tooltip window can contain items of any types.
- `set_tooltip()` is more or less a shortcut for the below idiom  (with a subtlety that it discards any previously submitted tooltip):
  ```
  if begin_tooltip():
      text(...)
      end_tooltip()
  ```

::: api-signature
```python
def begin_tooltip() -> bool:
    """
    Begin/append a tooltip window.
    """
```
:::

::: api-signature
```python
def end_tooltip() -> None:
    """
    Only call `end_tooltip()` if `begin_tooltip()`/`begin_item_tooltip()` returns true!
    """
```
:::

::: api-signature
```python
def set_tooltip(
    text: str,
) -> None:
    """
    Set a text-only tooltip. Often used after a `is_item_hovered()` check. Override any previous call to `set_tooltip()`.
    """
```
:::

## Tooltip helpers

Tooltip helpers for showing a tooltip when hovering an item:

- `begin_item_tooltip()` is a shortcut for the `if is_item_hovered(HoveredFlags.FOR_TOOLTIP) and begin_tooltip()` idiom.
- `set_item_tooltip()` is a shortcut for the `if is_item_hovered(HoveredFlags.FOR_TOOLTIP): set_tooltip(...)` idiom.
- Where `HoveredFlags.FOR_TOOLTIP` itself is a shortcut to use `Style.hover_flags_for_tooltip_mouse` or `Style.hover_flags_for_tooltip_nav` depending on the active input type. For mouse, it defaults to `HoveredFlags.STATIONARY | HoveredFlags.DELAY_SHORT`.

### Functions
::: api-signature
```python
def begin_item_tooltip() -> bool:
    """
    Begin/append a tooltip window if preceding item was hovered.
    """
```
:::

::: api-signature
```python
def set_item_tooltip(
    text: str,
) -> None:
    """
    Set a text-only tooltip if preceding item was hovered. override any previous call to `set_tooltip()`.
    """
```
:::

## Popups, Modals

- Popups and modals block normal mouse hovering detection (and therefore most mouse interactions) behind them.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- Their visibility state (~bool) is held internally instead of being held by the programmer as we are used to with regular `begin_*()` calls.
- The 3 properties above are related: we need to retain popup visibility state in the library because popups may be closed at any time.
- You can bypass the hovering restriction by using `HoveredFlags.ALLOW_WHEN_BLOCKED_BY_POPUP` when calling `is_item_hovered()` or `is_window_hovered()`.
- IMPORTANT: Popup identifiers are relative to the current ID stack, so `open_popup()` and `begin_popup()` generally need to be at the same level of the stack. This sometimes leads to confusing mistakes. May rework this in the future.
- `begin_popup()`: query popup state, if open start appending into the window. Call `end_popup()` afterwards if returned true. `WindowFlags` are forwarded to the window.
- `begin_popup_modal()`: block every interaction behind the window, cannot be closed by user, add a dimming background, has a title bar.

### Functions
::: api-signature
```python
def begin_popup(
    str_id: str,
    flags: WindowFlags = WindowFlags.NONE,
) -> bool:
    """
    Return true if the popup is open, and you can start outputting to it.
    """
```
:::

::: api-signature
```python
def begin_popup_modal(
    str_id: str,
    closable: bool = False,
    flags: WindowFlags = WindowFlags.NONE,
) -> tuple[bool, bool]:
    """
    Returns a tuple of bools.  If the first returned bool is `True`, the modal is open and you can start outputting to it.
    """
```
:::

::: api-signature
```python
def end_popup() -> None:
    """
    Only call `end_popup()` if BeginPopupXXX() returns true!
    """
```
:::

## Popups: open/close functions

- `open_popup()`: set popup state to open. `PopupFlags` are available for opening options.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- `close_current_popup()`: use inside the `begin_popup()`/`end_popup()` scope to close manually.
- `close_current_popup()` is called by default by `selectable()`/`menu_item()` when activated.
- Use `PopupFlags.NO_OPEN_OVER_EXISTING_POPUP` to avoid opening a popup if there's already one at the same level. This is equivalent to e.g. testing for `not is_any_popup_open()` prior to `open_popup()`.
- Use `is_window_appearing()` after `begin_popup()` to tell if a window just opened.

### Functions
::: api-signature
```python
def open_popup(
    str_id: str,
    flags: PopupFlags = PopupFlags.NONE,
) -> None:
    """
    Call to mark popup as open (don't call every frame!).
    """
```
:::

::: api-signature
```python
def open_popup_on_item_click(
    str_id: str | None = None,
    flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT,
) -> None:
    """
    Helper to open popup when clicked on last item. Default to `PopupFlags.MOUSE_BUTTON_RIGHT` == 1. (note: actually triggers on the mouse _released_ event to be consistent with popup behaviors)
    """
```
:::

::: api-signature
```python
def close_current_popup() -> None:
    """
    Manually close the popup we have begin-ed into.
    """
```
:::

## Popups: open+begin combined functions helpers

- Helpers to do `open_popup()` + `begin_popup()` where the open action is triggered by, e.g., hovering an item and right-clicking.
- They are convenient to easily create context menus, hence the name.
- IMPORTANT: Notice that `begin_popup_context_xxx()` takes `PopupFlags` just like `open_popup()` and unlike `begin_popup()`. For full consistency, we may add `WindowFlags` to the `begin_popup_context_xxx()` functions in the future.

### Functions
::: api-signature
```python
def begin_popup_context_item(
    str_id: str | None = None,
    flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT,
) -> bool:
    """
    Open+begin popup when clicked on last item. Use str_id==NULL to associate the popup to previous item. If you want to use that on a non-interactive item such as `text()` you need to pass in an explicit ID here. read comments in .cpp!
    """
```
:::

::: api-signature
```python
def begin_popup_context_window(
    str_id: str | None = None,
    flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT,
) -> bool:
    """
    Open+begin popup when clicked on current window.
    """
```
:::

::: api-signature
```python
def begin_popup_context_void(
    str_id: str | None = None,
    flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT,
) -> bool:
    """
    Open+begin popup when clicked in void (where there are no windows).
    """
```
:::

## Popups: query functions

- `is_popup_open()`: return true if the popup is open at the current `begin_popup()` level of the popup stack.
- `is_popup_open()` with `PopupFlags.ANY_POPUP_ID`: return true if any popup is open at the current `begin_popup()` level of the popup stack.
- `is_popup_open()` with `PopupFlags.ANY_POPUP_ID` + `PopupFlags.ANY_POPUP_LEVEL`: return true if any popup is open.

### Functions
::: api-signature
```python
def is_popup_open(
    str_id: str,
    flags: PopupFlags = PopupFlags.NONE,
) -> bool:
    """
    Return true if the popup is open.
    """
```
:::

## Tables

- Full-featured replacement for old Columns API.
- See Demo->Tables for demo code. See top of imgui_tables.cpp for general commentary.
- See `TableFlags` and `TableColumnFlags` enums for a description of available flags.

The typical call flow is:

1. Call `begin_table()`, early out if returning `False`.
2. Optionally call `table_setup_column()` to submit column name/flags/defaults.
3. Optionally call `table_setup_scroll_freeze()` to request scroll freezing of columns/rows.
4. Optionally call `table_headers_row()` to submit a header row. Names are pulled from `table_setup_column()` data.
5. Populate contents:
  - In most situations you can use `table_next_row()` + `table_set_column_index(N)` to start appending into a column.
  - If you are using tables as a sort of grid, where every column is holding the same type of contents, you may prefer using `table_next_column()` instead of `table_next_row()` + `table_set_column_index()`. `table_next_column()` will automatically wrap-around into the next row if needed.
  - IMPORTANT: Comparatively to the old `columns()` API, we need to call `table_next_column()` for the first column!
  - Summary of possible call flow:
    - `table_next_row()` -> `table_set_column_index(0)` -> `text("Hello 0")` -> `table_set_column_index(1)` -> `text("Hello 1")`  // OK
    - `table_next_row()` -> `table_next_column()` -> `text("Hello 0")` -> `table_next_column()` -> `text("Hello 1")`  // OK
    - `table_next_column()` -> `text("Hello 0")` -> `table_next_column()` -> `text("Hello 1")`  // OK: `table_next_column()` automatically gets to next row!
    - `table_next_row()` -> `text("Hello 0")`  // Not OK! Missing `table_set_column_index()` or `table_next_column()`! Text will not appear!
6. Call `end_table()`


### Functions
::: api-signature
```python
def begin_table(
    str_id: str,
    column: int,
    flags: TableFlags = TableFlags.NONE,
    outer_size: tuple[float, float] = (0.0, 0.0),
    inner_width: float = 0.0,
) -> bool:
```
:::

::: api-signature
```python
def end_table() -> None:
    """
    Only call `end_table()` if `begin_table()` returns true!
    """
```
:::

::: api-signature
```python
def table_next_row(
    flags: TableRowFlags = TableRowFlags.NONE,
    min_row_height: float = 0.0,
) -> None:
    """
    Append into the first cell of a new row. 'min_row_height' include the minimum top and bottom padding aka CellPadding.y * 2.0f.
    """
```
:::

::: api-signature
```python
def table_next_column() -> bool:
    """
    Append into the next column (or first column of next row if currently in last column). Return true when column is visible.
    """
```
:::

::: api-signature
```python
def table_set_column_index(
    column_n: int,
) -> bool:
    """
    Append into the specified column. Return true when column is visible.
    """
```
:::

## Tables: Headers & Columns declaration

- Use `table_setup_column()` to specify label, resizing policy, default width/weight, id, various other flags, etc.
- Use `table_headers_row()` to create a header row and automatically submit a `table_header()` for each column.
  Headers are required to perform: reordering, sorting, and opening the context menu.
  The context menu can also be made available in columns body using `TableFlags.CONTEXT_MENU_IN_BODY`.
- You may manually submit headers using `table_next_row()` + `table_header()` calls, but this is only useful in
  some advanced use cases (e.g., adding custom widgets in header row).
- Use `table_setup_scroll_freeze()` to lock columns/rows so they stay visible when scrolled.

### Functions
::: api-signature
```python
def table_setup_column(
    label: str,
    flags: TableColumnFlags = TableColumnFlags.NONE,
    init_width_or_weight: float = 0.0,
    user_id: int = 0,
) -> None:
```
:::

::: api-signature
```python
def table_setup_scroll_freeze(
    cols: int,
    rows: int,
) -> None:
    """
    Lock columns/rows so they stay visible when scrolled.
    """
```
:::

::: api-signature
```python
def table_header(
    label: str,
) -> None:
    """
    Submit one header cell manually (rarely used)
    """
```
:::

::: api-signature
```python
def table_headers_row() -> None:
    """
    Submit a row with headers cells based on data provided to `table_setup_column()` + submit context menu
    """
```
:::

::: api-signature
```python
def table_angled_headers_row() -> None:
    """
    Submit a row with angled headers for every column with the `TableColumnFlags.ANGLED_HEADER` flag. MUST BE FIRST ROW.
    """
```
:::

## Tables: Sorting & Miscellaneous functions

- Sorting: call `table_get_sort_specs()` to retrieve the latest sort specs for the table. Returns `None` when not sorting.
  When `sort_specs->SpecsDirty == True` you should sort your data. It will be `True` when sorting specs have changed since the last call, or the first time. Make sure to set `SpecsDirty = False` after sorting, else you may wastefully sort your data every frame!
- Functions args `column_n` treat the default value of -1 as the same as passing the current column index.

### Functions
::: api-signature
```python
def table_get_column_count() -> int:
    """
    Return number of columns (value passed to `begin_table`)
    """
```
:::

::: api-signature
```python
def table_get_column_index() -> int:
    """
    Return current column index.
    """
```
:::

::: api-signature
```python
def table_get_row_index() -> int:
    """
    Return current row index (header rows are accounted for)
    """
```
:::

::: api-signature
```python
def table_get_column_name(
    column_n: int = -1,
) -> str:
    """
    Return "" if column didn't have a name declared by `table_setup_column()`. Pass -1 to use current column.
    """
```
:::

::: api-signature
```python
def table_get_column_flags(
    column_n: int = -1,
) -> TableColumnFlags:
    """
    Return column flags so you can query their Enabled/Visible/Sorted/Hovered status flags. Pass -1 to use current column.
    """
```
:::

::: api-signature
```python
def table_set_column_enabled(
    column_n: int,
    v: bool,
) -> None:
    """
    Change user accessible enabled/disabled state of a column. Set to false to hide the column. User can use the context menu to change this themselves (right-click in headers, or right-click in columns body with `TableFlags.CONTEXT_MENU_IN_BODY`)
    """
```
:::

::: api-signature
```python
def table_get_hovered_column() -> int:
    """
    Return hovered column. return -1 when table is not hovered. return columns_count if the unused space at the right of visible columns is hovered. Can also use (`table_get_column_flags()` & `TableColumnFlags.IS_HOVERED`) instead.
    """
```
:::

::: api-signature
```python
def table_set_bg_color(
    target: TableBgTarget,
    color: tuple[float, float, float, float],
    column_n: int = -1,
) -> None:
    """
    Change the color of a cell, row, or column. See `TableBgTarget` flags for details.
    """
```
:::

## Legacy Columns API (prefer using Tables!)

- You can also use `same_line(pos_x)` to mimic simplified columns.

### Functions
::: api-signature
```python
def columns(
    count: int = 1,
    id: str | None = None,
    border: bool = True,
) -> None:
```
:::

::: api-signature
```python
def next_column() -> None:
    """
    Next column, defaults to current row or next row if the current row is finished
    """
```
:::

::: api-signature
```python
def get_column_index() -> int:
    """
    Get current column index
    """
```
:::

::: api-signature
```python
def get_column_width(
    column_index: int = -1,
) -> float:
    """
    Get column width (in pixels). pass -1 to use current column
    """
```
:::

::: api-signature
```python
def set_column_width(
    column_index: int,
    width: float,
) -> None:
    """
    Set column width (in pixels). pass -1 to use current column
    """
```
:::

::: api-signature
```python
def get_column_offset(
    column_index: int = -1,
) -> float:
    """
    Get position of column line (in pixels, from the left side of the contents region). pass -1 to use current column, otherwise 0..`get_columns_count()` inclusive. column 0 is typically 0.0f
    """
```
:::

::: api-signature
```python
def set_column_offset(
    column_index: int,
    offset_x: float,
) -> None:
    """
    Set position of column line (in pixels, from the left side of the contents region). pass -1 to use current column
    """
```
:::

::: api-signature
```python
def get_columns_count() -> int:
```
:::

## Tab Bars, Tabs

- Note: Tabs are automatically created by the docking system (when in 'docking' branch). Use this to create tab bars/tabs yourself.

### Functions
::: api-signature
```python
def begin_tab_bar(
    str_id: str,
    flags: TabBarFlags = TabBarFlags.NONE,
) -> bool:
    """
    Create and append into a TabBar
    """
```
:::

::: api-signature
```python
def end_tab_bar() -> None:
    """
    Only call `end_tab_bar()` if `begin_tab_bar()` returns true!
    """
```
:::

::: api-signature
```python
def tab_item_button(
    label: str,
    flags: TabItemFlags = TabItemFlags.NONE,
) -> bool:
    """
    Create a Tab behaving like a button. return true when clicked. cannot be selected in the tab bar.
    """
```
:::

::: api-signature
```python
def set_tab_item_closed(
    label: str,
) -> None:
    """
    Notify TabBar or Docking system of a closed tab/window ahead (useful to reduce visual flicker on reorderable tab bars). For tab-bar: call after `begin_tab_bar()` and before Tab submissions. Otherwise call with a window name.
    """
```
:::

::: api-signature
```python
def begin_tab_item(
    str_id: str,
    closable: bool = False,
    flags: TabItemFlags = TabItemFlags.NONE,
) -> tuple[bool, bool]:
    """
    When the `closable` argument is set to `True`, the created tab will display a close button.  The second bool of the return value will be `False` if the close button was pressed.  The intended usage is as follows:

    ```
    tab_open = True  # open/closed state

    visible, tab_open = imgui.begin_tab_item(..., closable=tab_open)
    if visible:
        # render tab contents here..
    ```
    """
```
:::

::: api-signature
```python
def end_tab_item() -> None:
    """
    Only call `end_tab_item()` if `begin_tab_item()` returns true!
    """
```
:::

## Drag and Drop

- On source items, call `begin_drag_drop_source()`, if it returns true also call `set_drag_drop_payload()` + `end_drag_drop_source()`.
- On target candidates, call `begin_drag_drop_target()`, if it returns true also call `accept_drag_drop_payload()` + `end_drag_drop_target()`.
- If you stop calling `begin_drag_drop_source()` the payload is preserved however it won't have a preview tooltip (we currently display a fallback "..." tooltip, see [#1725](https://github.com/ocornut/imgui/issues/1725)).
- An item can be both drag source and drop target.

::: api-signature
```python
def begin_drag_drop_source(
    flags: DragDropFlags = DragDropFlags.NONE,
) -> bool:
    """
    Call after submitting an item which may be dragged. when this return true, you can call `set_drag_drop_payload()` + `end_drag_drop_source()`
    """
```
:::

::: api-signature
```python
def set_drag_drop_payload(
    type: str,
    data: bytes,
    cond: Cond = Cond.NONE,
) -> bool:
    """
    Type is a user defined string of maximum 32 characters. Strings starting with '_' are reserved for dear imgui internal types. Data is copied and held by imgui. Return true when payload has been accepted.
    """
```
:::

::: api-signature
```python
def end_drag_drop_source() -> None:
    """
    Only call `end_drag_drop_source()` if `begin_drag_drop_source()` returns true!
    """
```
:::

::: api-signature
```python
def begin_drag_drop_target() -> bool:
    """
    Call after submitting an item that may receive a payload. If this returns true, you can call `accept_drag_drop_payload()` + `end_drag_drop_target()`
    """
```
:::

::: api-signature
```python
def accept_drag_drop_payload(
    type: str,
    flags: slimgui.slimgui_ext.imgui.DragDropFlags = 0,
) -> slimgui.slimgui_ext.imgui.Payload | None:
    """
    Accept contents of a given type. If `DragDropFlags.ACCEPT_BEFORE_DELIVERY` is set you can peek into the payload before the mouse button is released.
    """
```
:::

::: api-signature
```python
def end_drag_drop_target() -> None:
    """
    Only call `end_drag_drop_target()` if `begin_drag_drop_target()` returns true!
    """
```
:::

::: api-signature
```python
def get_drag_drop_payload() -> slimgui.slimgui_ext.imgui.Payload | None:
    """
    Peek directly into the current payload from anywhere. Returns `None` when drag and drop is finished or inactive. Use `Payload.is_data_type()` to test for the payload type.
    """
```
:::

## Disabling [BETA API]

- Disable all user interactions and dim items visuals (applying `Style.disabled_alpha` over current colors).
- These can be nested but cannot be used to enable an already disabled section (a single `begin_disabled(True)` in the stack is enough to keep everything disabled).
- Tooltip windows, by exception, are opted out of disabling.
- `begin_disabled(False)`/`end_disabled()` essentially does nothing but is provided to facilitate the use of boolean expressions (as a micro-optimization: if you have tens of thousands of `begin_disabled(False)`/`end_disabled()` pairs, you might want to reformulate your code to avoid making those calls).

### Functions
::: api-signature
```python
def begin_disabled(
    disabled: bool = True,
) -> None:
```
:::

::: api-signature
```python
def end_disabled() -> None:
```
:::

## Clipping
- Mouse hovering is affected by `push_clip_rect()` calls, unlike direct calls to `DrawList.push_clip_rect()` which are render only.

### Functions
::: api-signature
```python
def push_clip_rect(
    clip_rect_min: tuple[float, float],
    clip_rect_max: tuple[float, float],
    intersect_with_current_clip_rect: bool,
) -> None:
```
:::

::: api-signature
```python
def pop_clip_rect() -> None:
```
:::

## Focus, Activation

### Functions
::: api-signature
```python
def set_item_default_focus() -> None:
    """
    Make last item the default focused item of a newly appearing window.
    """
```
:::

::: api-signature
```python
def set_keyboard_focus_here(
    offset: int = 0,
) -> None:
    """
    Focus keyboard on the next widget. Use positive 'offset' to access sub components of a multiple component widget. Use -1 to access previous widget.
    """
```
:::

## Keyboard/Gamepad Navigation

::: api-signature
```python
def set_nav_cursor_visible(
    visible: bool,
) -> None:
    """
    Alter visibility of keyboard/gamepad cursor. by default: show when using an arrow key, hide when clicking with mouse.
    """
```
:::

## Overlapping mode

### Functions
::: api-signature
```python
def set_next_item_allow_overlap() -> None:
    """
    Allow next item to be overlapped by a subsequent item. Typically useful with `invisible_button()`, `selectable()`, `tree_node()` covering an area where subsequent items may need to be added. Note that both `selectable()` and `tree_node()` have dedicated flags doing this.
    """
```
:::

## Item/Widgets Utilities and Query Functions
- Most of the functions are referring to the previous Item that has been submitted.
- See Demo Window under "Widgets->Querying Status" for an interactive visualization of most of those functions.

### Functions
::: api-signature
```python
def is_item_hovered(
    flags: HoveredFlags = HoveredFlags.NONE,
) -> bool:
    """
    Is the last item hovered? (and usable, aka not blocked by a popup, etc.). See ImGuiHoveredFlags for more options.
    """
```
:::

::: api-signature
```python
def is_item_active() -> bool:
    """
    Is the last item active? (e.g. button being held, text field being edited. This will continuously return true while holding mouse button on an item. Items that don't interact will always return false)
    """
```
:::

::: api-signature
```python
def is_item_focused() -> bool:
    """
    Is the last item focused for keyboard/gamepad navigation?
    """
```
:::

::: api-signature
```python
def is_item_clicked(
    mouse_button: MouseButton = MouseButton.LEFT,
) -> bool:
    """
    Is the last item hovered and mouse clicked on? (**)  == `is_mouse_clicked(mouse_button)` && `is_item_hovered()`Important. (**) this is NOT equivalent to the behavior of e.g. `button()`. Read comments in function definition.
    """
```
:::

::: api-signature
```python
def is_item_visible() -> bool:
    """
    Is the last item visible? (items may be out of sight because of clipping/scrolling)
    """
```
:::

::: api-signature
```python
def is_item_edited() -> bool:
    """
    Did the last item modify its underlying value this frame? or was pressed? This is generally the same as the "bool" return value of many widgets.
    """
```
:::

::: api-signature
```python
def is_item_activated() -> bool:
    """
    Was the last item just made active (item was previously inactive).
    """
```
:::

::: api-signature
```python
def is_item_deactivated() -> bool:
    """
    Was the last item just made inactive (item was previously active). Useful for Undo/Redo patterns with widgets that require continuous editing.
    """
```
:::

::: api-signature
```python
def is_item_deactivated_after_edit() -> bool:
    """
    Was the last item just made inactive and made a value change when it was active? (e.g. Slider/Drag moved). Useful for Undo/Redo patterns with widgets that require continuous editing. Note that you may get false positives (some widgets such as `combo()`/`list_box()`/`selectable()` will return true even when clicking an already selected item).
    """
```
:::

::: api-signature
```python
def is_item_toggled_open() -> bool:
    """
    Was the last item open state toggled? set by `tree_node()`.
    """
```
:::

::: api-signature
```python
def is_any_item_hovered() -> bool:
    """
    Is any item hovered?
    """
```
:::

::: api-signature
```python
def is_any_item_active() -> bool:
    """
    Is any item active?
    """
```
:::

::: api-signature
```python
def is_any_item_focused() -> bool:
    """
    Is any item focused?
    """
```
:::

::: api-signature
```python
def get_item_id() -> int:
    """
    Get ID of last item (often roughly the same as `get_id(label)` beforehand)
    """
```
:::

::: api-signature
```python
def get_item_rect_min() -> tuple[float, float]:
    """
    Get upper-left bounding rectangle of the last item (screen space)
    """
```
:::

::: api-signature
```python
def get_item_rect_max() -> tuple[float, float]:
    """
    Get lower-right bounding rectangle of the last item (screen space)
    """
```
:::

::: api-signature
```python
def get_item_rect_size() -> tuple[float, float]:
    """
    Get size of last item
    """
```
:::

## Viewports
- Currently represents the Platform Window created by the application which is hosting our Dear ImGui windows.
- In 'docking' branch with multi-viewport enabled, we extend this concept to have multiple active viewports.
- In the future we will extend this concept further to also represent Platform Monitor and support a "no main platform window" operation mode.

### Functions
::: api-signature
```python
def get_main_viewport() -> Viewport:
    """
    Return primary/default viewport. This can never be NULL.
    """
```
:::

## Background/Foreground Draw Lists

### Functions
::: api-signature
```python
def get_background_draw_list() -> slimgui.imgui.DrawList:
    """
    This draw list will be the first rendered one. Useful to quickly draw shapes/text behind dear imgui contents.
    """
```
:::

::: api-signature
```python
def get_foreground_draw_list() -> slimgui.imgui.DrawList:
    """
    This draw list will be the last rendered one. Useful to quickly draw shapes/text over dear imgui contents.
    """
```
:::

## Miscellaneous Utilities

### Functions
::: api-signature
```python
def is_rect_visible(
    size: tuple[float, float],
) -> bool:
    """
    Test if rectangle (of given size, starting from cursor position) is visible / not clipped.
    """
```
:::

::: api-signature
```python
def is_rect_visible(
    rect_min: tuple[float, float],
    rect_max: tuple[float, float],
) -> bool:
    """
    Test if rectangle (of given size, starting from cursor position) is visible / not clipped.
    """
```
:::

::: api-signature
```python
def get_time() -> float:
    """
    Get global imgui time. incremented by io.DeltaTime every frame.
    """
```
:::

::: api-signature
```python
def get_frame_count() -> int:
    """
    Get global imgui frame count. incremented by 1 every frame.
    """
```
:::

::: api-signature
```python
def get_style_color_name(
    col: Col,
) -> str:
    """
    Get a string corresponding to the enum value (for display, saving, etc.).
    """
```
:::

### Clipboard

::: api-signature
```python
def get_clipboard_text() -> str:
    """
    Get clipboard text from the current platform backend.
    """
```
:::

::: api-signature
```python
def set_clipboard_text(
    text: str,
) -> None:
    """
    Set clipboard text through the current platform backend.
    """
```
:::

## Text Utilities

### Functions
::: api-signature
```python
def calc_text_size(
    text: str,
    hide_text_after_double_hash: bool = False,
    wrap_width: float = -1.0,
) -> tuple[float, float]:
```
:::

## Color Utilities

### Functions
::: api-signature
```python
def color_convert_u32_to_float4(
    arg: int,
    /,
) -> tuple[float, float, float, float]:
```
:::

::: api-signature
```python
def color_convert_float4_to_u32(
    arg: tuple[float, float, float, float],
    /,
) -> int:
```
:::

::: api-signature
```python
def color_convert_rgb_to_hsv(
    rgba: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
```
:::

::: api-signature
```python
def color_convert_hsv_to_rgb(
    hsv: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
```
:::

## Inputs Utilities: Keyboard/Mouse/Gamepad

- The `Key` enum contains all possible keyboard, mouse, and gamepad inputs (e.g., `Key.KEY_A`, `Key.MOUSE_LEFT`, `Key.GAMEPAD_DPAD_UP`).

### Functions
::: api-signature
```python
def is_key_down(
    key: Key,
) -> bool:
    """
    Is key being held.
    """
```
:::

::: api-signature
```python
def is_key_pressed(
    key: Key,
    repeat: bool = True,
) -> bool:
    """
    Was key pressed (went from !Down to Down)? Repeat rate uses io.KeyRepeatDelay / KeyRepeatRate.
    """
```
:::

::: api-signature
```python
def is_key_released(
    key: Key,
) -> bool:
    """
    Was key released (went from Down to !Down)?
    """
```
:::

::: api-signature
```python
def is_key_chord_pressed(
    key_chord: Key | int,
) -> bool:
    """
    Was key chord (mods + key) pressed, e.g. you can pass 'ImGuiMod_Ctrl | ImGuiKey_S' as a key-chord. This doesn't do any routing or focus check, please consider using `shortcut()` function instead.
    """
```
:::

::: api-signature
```python
def get_key_pressed_amount(
    key: Key,
    repeat_delay: float,
    rate: float,
) -> int:
    """
    Uses provided repeat rate/delay. return a count, most often 0 or 1 but might be >1 if RepeatRate is small enough that DeltaTime > RepeatRate
    """
```
:::

::: api-signature
```python
def get_key_name(
    key: Key,
) -> str:
    """
    [DEBUG] returns English name of the key. Those names are provided for debugging purpose and are not meant to be saved persistently nor compared.
    """
```
:::

::: api-signature
```python
def set_next_frame_want_capture_keyboard(
    want_capture_keyboard: bool,
) -> None:
```
:::

## Inputs Utilities: Shortcut Testing & Routing [BETA]

A `key_chord` passed to the below shortcut functions is a `Key` value + an optional `Key.MOD_ALT/CTRL_SHIFT_SUPER`.  E.g.,

- `Key.KEY_C`: accepted by functions taking `Key` or `Key | int` (keychord arguments)
- `Key.MOD_CTRL | Key.KEY_C`: accepted by functions taking `Key | int` keychord arguments
- It's legal to only combine `KEY_*` values with a `MOD_*` value.

The general idea is that several callers may register interest in a shortcut, and only one owner gets it:

- Parent -> call Shortcut(Ctrl+S)  - when Parent is focused, Parent gets the shortcut
  - Child1 -> call Shortcut(Ctrl+S) - when Child1 is focused, Child1 gets the shortcut (Child1 overrides Parent shortcuts)
  - Child2 -> no call - when Child2 is focused, Parent gets the shortcut.

The whole system is order independent, so if Child1 makes its calls before Parent, results will be identical.
This is an important property as it facilitates working with foreign code or a larger codebase. To understand the difference:

- `is_key_chord_pressed()` compares mods and calls `is_key_pressed()` -> function has no side-effect.
- `shortcut()` submits a route, routes are resolved, if it currently can be routed it calls `is_key_chord_pressed()` -> function has (desirable) side-effects as it can prevent another call from getting the route.

You can visualize registered routes in the "Metrics/Debugger->Inputs" window.

### Functions
::: api-signature
```python
def shortcut(
    key_chord: Key | int,
    flags: InputFlags = InputFlags.NONE,
) -> bool:
    """
    Python bindings note: The original ImGui type for a ImGuiKeyChord is basically ImGuiKey that can be optionally bitwise-OR'd with a modifier key like ImGuiMod_Alt, ImGuiMod_Ctrl, etc.  In Python, this is modeled as a union of `Key` and int.  The int value is the modifier key.  You can use the `|` operator to combine them, e.g. `Key.A | Key.MOD_CTRL`.
    """
```
:::

::: api-signature
```python
def set_next_item_shortcut(
    key_chord: Key | int,
    flags: InputFlags = InputFlags.NONE,
) -> None:
    """
    Python bindings note: The original ImGui type for a ImGuiKeyChord is basically ImGuiKey that can be optionally bitwise-OR'd with a modifier key like ImGuiMod_Alt, ImGuiMod_Ctrl, etc.  In Python, this is modeled as a union of `Key` and int.  The int value is the modifier key.  You can use the `|` operator to combine them, e.g. `Key.A | Key.MOD_CTRL`.
    """
```
:::

::: api-signature
```python
def set_item_key_owner(
    key: Key,
) -> None:
    """
    Set key owner to last item ID if it is hovered or active.
    """
```
:::

## Inputs Utilities: Mouse

- To refer to a mouse button, you may use named enums in your code, e.g., `MouseButton.LEFT`, `MouseButton.RIGHT`.

### Functions
::: api-signature
```python
def is_mouse_down(
    button: MouseButton,
) -> bool:
    """
    Is mouse button held?
    """
```
:::

::: api-signature
```python
def is_mouse_clicked(
    button: MouseButton,
    repeat: bool = False,
) -> bool:
    """
    Did mouse button clicked? (went from !Down to Down). Same as `get_mouse_clicked_count()` == 1.
    """
```
:::

::: api-signature
```python
def is_mouse_released(
    button: MouseButton,
) -> bool:
    """
    Did mouse button released? (went from Down to !Down)
    """
```
:::

::: api-signature
```python
def is_mouse_double_clicked(
    button: MouseButton,
) -> bool:
    """
    Did mouse button double-clicked? Same as `get_mouse_clicked_count()` == 2. (note that a double-click will also report `is_mouse_clicked()` == true)
    """
```
:::

::: api-signature
```python
def is_mouse_released_with_delay(
    button: MouseButton,
    delay: float,
) -> bool:
    """
    Delayed mouse release (use very sparingly!). Generally used with 'delay >= io.MouseDoubleClickTime' + combined with a 'io.MouseClickedLastCount==1' test. This is a very rarely used UI idiom, but some apps use this: e.g. MS Explorer single click on an icon to rename.
    """
```
:::

::: api-signature
```python
def get_mouse_clicked_count(
    button: MouseButton,
) -> int:
    """
    Return the number of successive mouse-clicks at the time where a click happen (otherwise 0).
    """
```
:::

::: api-signature
```python
def is_mouse_hovering_rect(
    r_min: tuple[float, float],
    r_max: tuple[float, float],
    clip: bool = True,
) -> bool:
    """
    Is mouse hovering given bounding rect (in screen space). clipped by current clipping settings, but disregarding of other consideration of focus/window ordering/popup-block.
    """
```
:::

::: api-signature
```python
def is_mouse_pos_valid(
    mouse_pos: tuple[float, float] | None = None,
) -> bool:
    """
    By convention we use (-FLT_MAX,-FLT_MAX) to denote that there is no mouse available
    """
```
:::

::: api-signature
```python
def get_mouse_pos() -> tuple[float, float]:
    """
    Shortcut to `get_io()`.MousePos provided by user, to be consistent with other calls
    """
```
:::

::: api-signature
```python
def get_mouse_pos_on_opening_current_popup() -> tuple[float, float]:
    """
    Retrieve mouse position at the time of opening popup we have `begin_popup()` into (helper to avoid user backing that value themselves)
    """
```
:::

::: api-signature
```python
def is_mouse_dragging(
    button: MouseButton,
    lock_threshold: float = -1.0,
) -> bool:
    """
    Is mouse dragging? (uses io.MouseDraggingThreshold if lock_threshold < 0.0f)
    """
```
:::

::: api-signature
```python
def get_mouse_drag_delta(
    button: MouseButton = MouseButton.LEFT,
    lock_threshold: float = -1.0,
) -> tuple[float, float]:
    """
    Return the delta from the initial clicking position while the mouse button is pressed or was just released. This is locked and return 0.0f until the mouse moves past a distance threshold at least once (uses io.MouseDraggingThreshold if lock_threshold < 0.0f)
    """
```
:::

::: api-signature
```python
def reset_mouse_drag_delta(
    button: MouseButton = MouseButton.LEFT,
) -> None:
```
:::

::: api-signature
```python
def get_mouse_cursor() -> MouseCursor:
    """
    Get desired mouse cursor shape. Important: reset in `new_frame()`, this is updated during the frame. valid before `render()`. If you use software rendering by setting io.MouseDrawCursor ImGui will render those for you
    """
```
:::

::: api-signature
```python
def set_mouse_cursor(
    cursor_type: MouseCursor,
) -> None:
    """
    Set desired mouse cursor shape
    """
```
:::

::: api-signature
```python
def set_next_frame_want_capture_mouse(
    capture: bool,
) -> None:
```
:::

## Enum Reference

### Enum: BackendFlags

| Name | Description |
| --- | --- |
| NONE |  |
| HAS_GAMEPAD | Backend Platform supports gamepad and currently has one connected. |
| HAS_MOUSE_CURSORS | Backend Platform supports honoring `get_mouse_cursor()` value to change the OS cursor shape. |
| HAS_SET_MOUSE_POS | Backend Platform supports io.WantSetMousePos requests to reposition the OS mouse position (only used if io.ConfigNavMoveSetMousePos is set). |
| RENDERER_HAS_VTX_OFFSET | Backend Renderer supports ImDrawCmd::VtxOffset. This enables output of large meshes (64K+ vertices) while still using 16-bit indices. |
| RENDERER_HAS_TEXTURES | Backend Renderer supports ImTextureData requests to create/update/destroy textures. This enables incremental texture updates and texture reloads. See https://github.com/ocornut/imgui/blob/master/docs/BACKENDS.md for instructions on how to upgrade your custom backend. |

### Enum: ButtonFlags

| Name | Description |
| --- | --- |
| NONE |  |
| MOUSE_BUTTON_LEFT | React on left mouse button (default) |
| MOUSE_BUTTON_RIGHT | React on right mouse button |
| MOUSE_BUTTON_MIDDLE | React on center mouse button |
| ENABLE_NAV | `invisible_button()`: do not disable navigation/tabbing. Otherwise disabled by default. |
| ALLOW_OVERLAP | Hit testing will allow subsequent widgets to overlap this one. Require previous frame HoveredId to match before being usable. Shortcut to calling `set_next_item_allow_overlap()`. |

### Enum: ChildFlags

| Name | Description |
| --- | --- |
| NONE |  |
| BORDERS | Show an outer border and enable WindowPadding. (IMPORTANT: this is always == 1 == true for legacy reason) |
| ALWAYS_USE_WINDOW_PADDING | Pad with style.WindowPadding even if no border are drawn (no padding by default for non-bordered child windows because it makes more sense) |
| RESIZE_X | Allow resize from right border (layout direction). Enable .ini saving (unless `WindowFlags.NO_SAVED_SETTINGS` passed to window flags) |
| RESIZE_Y | Allow resize from bottom border (layout direction). |
| AUTO_RESIZE_X | Enable auto-resizing width. Read IMPORTANT: Size measurement" details above. |
| AUTO_RESIZE_Y | Enable auto-resizing height. Read IMPORTANT: Size measurement" details above. |
| ALWAYS_AUTO_RESIZE | Combined with AutoResizeX/AutoResizeY. Always measure size even when child is hidden, always return true, always disable clipping optimization! NOT RECOMMENDED. |
| FRAME_STYLE | Style the child window like a framed item: use FrameBg, FrameRounding, FrameBorderSize, FramePadding instead of ChildBg, ChildRounding, ChildBorderSize, WindowPadding. |
| NAV_FLATTENED | [BETA] Share focus scope, allow keyboard/gamepad navigation to cross over parent border to this child or between sibling child windows. |

### Enum: Col

| Name | Description |
| --- | --- |
| TEXT |  |
| TEXT_DISABLED |  |
| WINDOW_BG | Background of normal windows |
| CHILD_BG | Background of child windows |
| POPUP_BG | Background of popups, menus, tooltips windows |
| BORDER |  |
| BORDER_SHADOW |  |
| FRAME_BG | Background of checkbox, radio button, plot, slider, text input |
| FRAME_BG_HOVERED |  |
| FRAME_BG_ACTIVE |  |
| TITLE_BG | Title bar |
| TITLE_BG_ACTIVE | Title bar when focused |
| TITLE_BG_COLLAPSED | Title bar when collapsed |
| MENU_BAR_BG |  |
| SCROLLBAR_BG |  |
| SCROLLBAR_GRAB |  |
| SCROLLBAR_GRAB_HOVERED |  |
| SCROLLBAR_GRAB_ACTIVE |  |
| CHECK_MARK | `checkbox` tick and `radio_button` circle |
| SLIDER_GRAB |  |
| SLIDER_GRAB_ACTIVE |  |
| BUTTON |  |
| BUTTON_HOVERED |  |
| BUTTON_ACTIVE |  |
| HEADER | Header* colors are used for `collapsing_header`, `tree_node`, `selectable`, `menu_item` |
| HEADER_HOVERED |  |
| HEADER_ACTIVE |  |
| SEPARATOR |  |
| SEPARATOR_HOVERED |  |
| SEPARATOR_ACTIVE |  |
| RESIZE_GRIP | Resize grip in lower-right and lower-left corners of windows. |
| RESIZE_GRIP_HOVERED |  |
| RESIZE_GRIP_ACTIVE |  |
| INPUT_TEXT_CURSOR | `input_text` cursor/caret |
| TAB_HOVERED | Tab background, when hovered |
| TAB | Tab background, when tab-bar is focused & tab is unselected |
| TAB_SELECTED | Tab background, when tab-bar is focused & tab is selected |
| TAB_SELECTED_OVERLINE | Tab horizontal overline, when tab-bar is focused & tab is selected |
| TAB_DIMMED | Tab background, when tab-bar is unfocused & tab is unselected |
| TAB_DIMMED_SELECTED | Tab background, when tab-bar is unfocused & tab is selected |
| TAB_DIMMED_SELECTED_OVERLINE |  |
| PLOT_LINES |  |
| PLOT_LINES_HOVERED |  |
| PLOT_HISTOGRAM |  |
| PLOT_HISTOGRAM_HOVERED |  |
| TABLE_HEADER_BG | Table header background |
| TABLE_BORDER_STRONG | Table outer and header borders (prefer using Alpha=1.0 here) |
| TABLE_BORDER_LIGHT | Table inner borders (prefer using Alpha=1.0 here) |
| TABLE_ROW_BG | Table row background (even rows) |
| TABLE_ROW_BG_ALT | Table row background (odd rows) |
| TEXT_LINK | Hyperlink color |
| TEXT_SELECTED_BG | Selected text inside an `input_text` |
| TREE_LINES | Tree node hierarchy outlines when using `TreeNodeFlags.DRAW_LINES` |
| DRAG_DROP_TARGET | Rectangle border highlighting a drop target |
| DRAG_DROP_TARGET_BG | Rectangle background highlighting a drop target |
| UNSAVED_MARKER | Unsaved Document marker (in window title and tabs) |
| NAV_CURSOR | Color of keyboard/gamepad navigation cursor/rectangle, when visible |
| NAV_WINDOWING_HIGHLIGHT | Highlight window when using Ctrl+Tab |
| NAV_WINDOWING_DIM_BG | Darken/colorize entire screen behind the Ctrl+Tab window list, when active |
| MODAL_WINDOW_DIM_BG | Darken/colorize entire screen behind a modal window, when one is active |
| COUNT |  |

### Enum: ColorEditFlags

| Name | Description |
| --- | --- |
| NONE |  |
| NO_ALPHA | ColorEdit, ColorPicker, `color_button`: ignore Alpha component (will only read 3 components from the input pointer). |
| NO_PICKER | ColorEdit: disable picker when clicking on color square. |
| NO_OPTIONS | ColorEdit: disable toggling options menu when right-clicking on inputs/small preview. |
| NO_SMALL_PREVIEW | ColorEdit, ColorPicker: disable color square preview next to the inputs. (e.g. to show only the inputs) |
| NO_INPUTS | ColorEdit, ColorPicker: disable inputs sliders/text widgets (e.g. to show only the small preview color square). |
| NO_TOOLTIP | ColorEdit, ColorPicker, `color_button`: disable tooltip when hovering the preview. |
| NO_LABEL | ColorEdit, ColorPicker: disable display of inline text label (the label is still forwarded to the tooltip and picker). |
| NO_SIDE_PREVIEW | ColorPicker: disable bigger color preview on right side of the picker, use small color square preview instead. |
| NO_DRAG_DROP | ColorEdit: disable drag and drop target/source. `color_button`: disable drag and drop source. |
| NO_BORDER | `color_button`: disable border (which is enforced by default) |
| NO_COLOR_MARKERS | ColorEdit: disable rendering R/G/B/A color marker. May also be disabled globally by setting style.ColorMarkerSize = 0. |
| ALPHA_OPAQUE | ColorEdit, ColorPicker, `color_button`: disable alpha in the preview,. Contrary to _NoAlpha it may still be edited when calling `color_edit4()`/`color_picker4()`. For `color_button()` this does the same as _NoAlpha. |
| ALPHA_NO_BG | ColorEdit, ColorPicker, `color_button`: disable rendering a checkerboard background behind transparent color. |
| ALPHA_PREVIEW_HALF | ColorEdit, ColorPicker, `color_button`: display half opaque / half transparent preview. |
| ALPHA_BAR | ColorEdit, ColorPicker: show vertical alpha bar/gradient in picker. |
| HDR | (WIP) ColorEdit: Currently only disable 0.0f..1.0f limits in RGBA edition (note: you probably want to use `ColorEditFlags.FLOAT` flag as well). |
| DISPLAY_RGB | ColorEdit: override _display_ type among RGB/HSV/Hex. ColorPicker: select any combination using one or more of RGB/HSV/Hex. |
| DISPLAY_HSV |  |
| DISPLAY_HEX |  |
| UINT8 | ColorEdit, ColorPicker, `color_button`: _display_ values formatted as 0..255. |
| FLOAT | ColorEdit, ColorPicker, `color_button`: _display_ values formatted as 0.0f..1.0f floats instead of 0..255 integers. No round-trip of value via integers. |
| PICKER_HUE_BAR | ColorPicker: bar for Hue, rectangle for Sat/Value. |
| PICKER_HUE_WHEEL | ColorPicker: wheel for Hue, triangle for Sat/Value. |
| INPUT_RGB | ColorEdit, ColorPicker: input and output data in RGB format. |
| INPUT_HSV | ColorEdit, ColorPicker: input and output data in HSV format. |

### Enum: ComboFlags

| Name | Description |
| --- | --- |
| NONE |  |
| POPUP_ALIGN_LEFT | Align the popup toward the left by default |
| HEIGHT_SMALL | Max ~4 items visible. Tip: If you want your combo popup to be a specific size you can use `set_next_window_size_constraints()` prior to calling `begin_combo()` |
| HEIGHT_REGULAR | Max ~8 items visible (default) |
| HEIGHT_LARGE | Max ~20 items visible |
| HEIGHT_LARGEST | As many fitting items as possible |
| NO_ARROW_BUTTON | Display on the preview box without the square arrow button |
| NO_PREVIEW | Display only a square arrow button |
| WIDTH_FIT_PREVIEW | Width dynamically calculated from preview contents |

### Enum: Cond

| Name | Description |
| --- | --- |
| NONE | No condition (always set the variable), same as _Always |
| ALWAYS | No condition (always set the variable), same as _None |
| ONCE | Set the variable once per runtime session (only the first call will succeed) |
| FIRST_USE_EVER | Set the variable if the object/window has no persistently saved data (no entry in .ini file) |
| APPEARING | Set the variable if the object/window is appearing after being hidden/inactive (or the first time) |

### Enum: ConfigFlags

| Name | Description |
| --- | --- |
| NONE |  |
| NAV_ENABLE_KEYBOARD | Master keyboard navigation enable flag. Enable full Tabbing + directional arrows + Space/Enter to activate. Note: some features such as basic Tabbing and CtrL+Tab are enabled by regardless of this flag (and may be disabled via other means, see #4828, #9218). |
| NAV_ENABLE_GAMEPAD | Master gamepad navigation enable flag. Backend also needs to set `BackendFlags.HAS_GAMEPAD`. |
| NO_MOUSE | Instruct dear imgui to disable mouse inputs and interactions. |
| NO_MOUSE_CURSOR_CHANGE | Instruct backend to not alter mouse cursor shape and visibility. Use if the backend cursor changes are interfering with yours and you don't want to use `set_mouse_cursor()` to change mouse cursor. You may want to honor requests from imgui by reading `get_mouse_cursor()` yourself instead. |
| NO_KEYBOARD | Instruct dear imgui to disable keyboard inputs and interactions. This is done by ignoring keyboard events and clearing existing states. |
| IS_SRGB | Application is SRGB-aware. |
| IS_TOUCH_SCREEN | Application is using a touch screen instead of a mouse. |

### Enum: Dir

| Name | Description |
| --- | --- |
| NONE |  |
| LEFT |  |
| RIGHT |  |
| UP |  |
| DOWN |  |
| COUNT |  |

### Enum: DragDropFlags

| Name | Description |
| --- | --- |
| NONE |  |
| SOURCE_NO_PREVIEW_TOOLTIP | Disable preview tooltip. By default, a successful call to `begin_drag_drop_source` opens a tooltip so you can display a preview or description of the source contents. This flag disables this behavior. |
| SOURCE_NO_DISABLE_HOVER | By default, when dragging we clear data so that `is_item_hovered()` will return false, to avoid subsequent user code submitting tooltips. This flag disables this behavior so you can still call `is_item_hovered()` on the source item. |
| SOURCE_NO_HOLD_TO_OPEN_OTHERS | Disable the behavior that allows to open tree nodes and collapsing header by holding over them while dragging a source item. |
| SOURCE_ALLOW_NULL_ID | Allow items such as `text()`, `image()` that have no unique identifier to be used as drag source, by manufacturing a temporary identifier based on their window-relative position. This is extremely unusual within the dear imgui ecosystem and so we made it explicit. |
| SOURCE_EXTERN | External source (from outside of dear imgui), won't attempt to read current item/window info. Will always return true. Only one Extern source can be active simultaneously. |
| PAYLOAD_AUTO_EXPIRE | Automatically expire the payload if the source cease to be submitted (otherwise payloads are persisting while being dragged) |
| PAYLOAD_NO_CROSS_CONTEXT | Hint to specify that the payload may not be copied outside current dear imgui context. |
| PAYLOAD_NO_CROSS_PROCESS | Hint to specify that the payload may not be copied outside current process. |
| ACCEPT_BEFORE_DELIVERY | `accept_drag_drop_payload()` will returns true even before the mouse button is released. You can then call IsDelivery() to test if the payload needs to be delivered. |
| ACCEPT_NO_DRAW_DEFAULT_RECT | Do not draw the default highlight rectangle when hovering over target. |
| ACCEPT_NO_PREVIEW_TOOLTIP | Request hiding the `begin_drag_drop_source` tooltip from the `begin_drag_drop_target` site. |
| ACCEPT_DRAW_AS_HOVERED | Accepting item will render as if hovered. Useful for e.g. a `button()` used as a drop target. |
| ACCEPT_PEEK_ONLY | For peeking ahead and inspecting the payload before delivery. |

### Enum: DrawFlags

| Name | Description |
| --- | --- |
| NONE |  |
| CLOSED | PathStroke(), AddPolyline(): specify that shape should be closed (Important: this is always == 1 for legacy reason) |
| ROUND_CORNERS_TOP_LEFT | AddRect(), AddRectFilled(), PathRect(): enable rounding top-left corner only (when rounding > 0.0f, we default to all corners). Was 0x01. |
| ROUND_CORNERS_TOP_RIGHT | AddRect(), AddRectFilled(), PathRect(): enable rounding top-right corner only (when rounding > 0.0f, we default to all corners). Was 0x02. |
| ROUND_CORNERS_BOTTOM_LEFT | AddRect(), AddRectFilled(), PathRect(): enable rounding bottom-left corner only (when rounding > 0.0f, we default to all corners). Was 0x04. |
| ROUND_CORNERS_BOTTOM_RIGHT | AddRect(), AddRectFilled(), PathRect(): enable rounding bottom-right corner only (when rounding > 0.0f, we default to all corners). Wax 0x08. |
| ROUND_CORNERS_NONE | AddRect(), AddRectFilled(), PathRect(): disable rounding on all corners (when rounding > 0.0f). This is NOT zero, NOT an implicit flag! |
| ROUND_CORNERS_TOP |  |
| ROUND_CORNERS_BOTTOM |  |
| ROUND_CORNERS_LEFT |  |
| ROUND_CORNERS_RIGHT |  |
| ROUND_CORNERS_ALL |  |

### Enum: FocusedFlags

| Name | Description |
| --- | --- |
| NONE |  |
| CHILD_WINDOWS | Return true if any children of the window is focused |
| ROOT_WINDOW | Test from root window (top most parent of the current hierarchy) |
| ANY_WINDOW | Return true if any window is focused. Important: If you are trying to tell how to dispatch your low-level inputs, do NOT use this. Use 'io.WantCaptureMouse' instead! Please read the FAQ! |
| NO_POPUP_HIERARCHY | Do not consider popup hierarchy (do not treat popup emitter as parent of popup) (when used with _ChildWindows or _RootWindow) |
| ROOT_AND_CHILD_WINDOWS |  |

### Enum: HoveredFlags

| Name | Description |
| --- | --- |
| NONE | Return true if directly over the item/window, not obstructed by another window, not obstructed by an active popup or modal blocking inputs under them. |
| CHILD_WINDOWS | `is_window_hovered()` only: Return true if any children of the window is hovered |
| ROOT_WINDOW | `is_window_hovered()` only: Test from root window (top most parent of the current hierarchy) |
| ANY_WINDOW | `is_window_hovered()` only: Return true if any window is hovered |
| NO_POPUP_HIERARCHY | `is_window_hovered()` only: Do not consider popup hierarchy (do not treat popup emitter as parent of popup) (when used with _ChildWindows or _RootWindow) |
| ALLOW_WHEN_BLOCKED_BY_POPUP | Return true even if a popup window is normally blocking access to this item/window |
| ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM | Return true even if an active item is blocking access to this item/window. Useful for Drag and Drop patterns. |
| ALLOW_WHEN_OVERLAPPED_BY_ITEM | `is_item_hovered()` only: Return true even if the item uses AllowOverlap mode and is overlapped by another hoverable item. |
| ALLOW_WHEN_OVERLAPPED_BY_WINDOW | `is_item_hovered()` only: Return true even if the position is obstructed or overlapped by another window. |
| ALLOW_WHEN_DISABLED | `is_item_hovered()` only: Return true even if the item is disabled |
| NO_NAV_OVERRIDE | `is_item_hovered()` only: Disable using keyboard/gamepad navigation state when active, always query mouse |
| ALLOW_WHEN_OVERLAPPED |  |
| RECT_ONLY |  |
| ROOT_AND_CHILD_WINDOWS |  |
| FOR_TOOLTIP | Shortcut for standard flags when using `is_item_hovered()` + `set_tooltip()` sequence. |
| STATIONARY | Require mouse to be stationary for style.HoverStationaryDelay (~0.15 sec) _at least one time_. After this, can move on same item/window. Using the stationary test tends to reduces the need for a long delay. |
| DELAY_NONE | `is_item_hovered()` only: Return true immediately (default). As this is the default you generally ignore this. |
| DELAY_SHORT | `is_item_hovered()` only: Return true after style.HoverDelayShort elapsed (~0.15 sec) (shared between items) + requires mouse to be stationary for style.HoverStationaryDelay (once per item). |
| DELAY_NORMAL | `is_item_hovered()` only: Return true after style.HoverDelayNormal elapsed (~0.40 sec) (shared between items) + requires mouse to be stationary for style.HoverStationaryDelay (once per item). |
| NO_SHARED_DELAY | `is_item_hovered()` only: Disable shared delay system where moving from one item to the next keeps the previous timer for a short time (standard for tooltips with long delays) |

### Enum: InputFlags

| Name | Description |
| --- | --- |
| NONE |  |
| REPEAT | Enable repeat. Return true on successive repeats. Default for legacy `is_key_pressed()`. NOT Default for legacy `is_mouse_clicked()`. MUST BE == 1. |
| ROUTE_ACTIVE | Route to active item only. |
| ROUTE_FOCUSED | Route to windows in the focus stack (DEFAULT). Deep-most focused window takes inputs. Active item takes inputs over deep-most focused window. |
| ROUTE_GLOBAL | Global route (unless a focused window or active item registered the route). |
| ROUTE_ALWAYS | Do not register route, poll keys directly. |
| ROUTE_OVER_FOCUSED | Option: global route: higher priority than focused route (unless active item in focused route). |
| ROUTE_OVER_ACTIVE | Option: global route: higher priority than active item. Unlikely you need to use that: will interfere with every active items, e.g. Ctrl+A registered by `input_text` will be overridden by this. May not be fully honored as user/internal code is likely to always assume they can access keys when active. |
| ROUTE_UNLESS_BG_FOCUSED | Option: global route: will not be applied if underlying background/void is focused (== no Dear ImGui windows are focused). Useful for overlay applications. |
| ROUTE_FROM_ROOT_WINDOW | Option: route evaluated from the point of view of root window rather than current window. |
| TOOLTIP | Automatically display a tooltip when hovering item [BETA] Unsure of right api (opt-in/opt-out) |

### Enum: InputTextFlags

| Name | Description |
| --- | --- |
| NONE |  |
| CHARS_DECIMAL | Allow 0123456789.+-*/ |
| CHARS_HEXADECIMAL | Allow 0123456789ABCDEFabcdef |
| CHARS_SCIENTIFIC | Allow 0123456789.+-*/eE (Scientific notation input) |
| CHARS_UPPERCASE | Turn a..z into A..Z |
| CHARS_NO_BLANK | Filter out spaces, tabs |
| ALLOW_TAB_INPUT | Pressing TAB input a '  ' character into the text field |
| ENTER_RETURNS_TRUE | Return 'true' when Enter is pressed (as opposed to every time the value was modified). Consider using `is_item_deactivated_after_edit()` instead! |
| ESCAPE_CLEARS_ALL | Escape key clears content if not empty, and deactivate otherwise (contrast to default behavior of Escape to revert) |
| CTRL_ENTER_FOR_NEW_LINE | In multi-line mode: validate with Enter, add new line with Ctrl+Enter (default is opposite: validate with Ctrl+Enter, add line with Enter). Note that Shift+Enter always enter a new line either way. |
| READ_ONLY | Read-only mode |
| PASSWORD | Password mode, display all characters as '*', disable copy |
| ALWAYS_OVERWRITE | Overwrite mode |
| AUTO_SELECT_ALL | Select entire text when first taking mouse focus |
| PARSE_EMPTY_REF_VAL | `input_float()`, `input_int()`, `input_scalar()` etc. only: parse empty string as zero value. |
| DISPLAY_EMPTY_REF_VAL | `input_float()`, `input_int()`, `input_scalar()` etc. only: when value is zero, do not display it. Generally used with `InputTextFlags.PARSE_EMPTY_REF_VAL`. |
| NO_HORIZONTAL_SCROLL | Disable following the cursor horizontally |
| NO_UNDO_REDO | Disable undo/redo. Note that input text owns the text data while active, if you want to provide your own undo/redo stack you need e.g. to call `clear_active_id()`. |
| ELIDE_LEFT | When text doesn't fit, elide left side to ensure right side stays visible. Useful for path/filenames. Single-line only! |
| CALLBACK_COMPLETION | Callback on pressing TAB (for completion handling) |
| CALLBACK_HISTORY | Callback on pressing Up/Down arrows (for history handling) |
| CALLBACK_ALWAYS | Callback on each iteration. User code may query cursor position, modify text buffer. |
| CALLBACK_CHAR_FILTER | Callback on character inputs to replace or discard them. Modify 'EventChar' to replace or discard, or return 1 in callback to discard. |
| CALLBACK_RESIZE | Callback on buffer capacity changes request (beyond 'buf_size' parameter value), allowing the string to grow. Notify when the string wants to be resized (for string types which hold a cache of their Size). You will be provided a new BufSize in the callback and NEED to honor it. (see misc/cpp/imgui_stdlib.h for an example of using this) |
| CALLBACK_EDIT | Callback on any edit. Note that `input_text()` already returns true on edit + you can always use `is_item_edited()`. The callback is useful to manipulate the underlying buffer while focus is active. |
| WORD_WRAP | `input_text_multiline()`: word-wrap lines that are too long. |

### Enum: ItemFlags

| Name | Description |
| --- | --- |
| NONE | (Default) |
| NO_TAB_STOP | Disable keyboard tabbing. This is a "lighter" version of `ItemFlags.NO_NAV`. |
| NO_NAV | Disable any form of focusing (keyboard/gamepad directional navigation and `set_keyboard_focus_here()` calls). |
| NO_NAV_DEFAULT_FOCUS | Disable item being a candidate for default focus (e.g. used by title bar items). |
| BUTTON_REPEAT | Any button-like behavior will have repeat mode enabled (based on io.KeyRepeatDelay and io.KeyRepeatRate values). Note that you can also call `is_item_active()` after any button to tell if it is being held. |
| AUTO_CLOSE_POPUPS | `menu_item()`/`selectable()` automatically close their parent popup window. |
| ALLOW_DUPLICATE_ID | Allow submitting an item with the same identifier as an item already submitted this frame without triggering a warning tooltip if io.ConfigDebugHighlightIdConflicts is set. |
| DISABLED | [Internal] Disable interactions. DOES NOT affect visuals. This is used by `begin_disabled()`/`end_disabled()` and only provided here so you can read back via `get_item_flags()`. |

### Enum: Key

| Name | Description |
| --- | --- |
| KEY_NONE |  |
| KEY_NAMED_KEY_BEGIN |  |
| KEY_TAB |  |
| KEY_LEFT_ARROW |  |
| KEY_RIGHT_ARROW |  |
| KEY_UP_ARROW |  |
| KEY_DOWN_ARROW |  |
| KEY_PAGE_UP |  |
| KEY_PAGE_DOWN |  |
| KEY_HOME |  |
| KEY_END |  |
| KEY_INSERT |  |
| KEY_DELETE |  |
| KEY_BACKSPACE |  |
| KEY_SPACE |  |
| KEY_ENTER |  |
| KEY_ESCAPE |  |
| KEY_LEFT_CTRL |  |
| KEY_LEFT_SHIFT |  |
| KEY_LEFT_ALT |  |
| KEY_LEFT_SUPER |  |
| KEY_RIGHT_CTRL |  |
| KEY_RIGHT_SHIFT |  |
| KEY_RIGHT_ALT |  |
| KEY_RIGHT_SUPER |  |
| KEY_MENU |  |
| KEY_0 |  |
| KEY_1 |  |
| KEY_2 |  |
| KEY_3 |  |
| KEY_4 |  |
| KEY_5 |  |
| KEY_6 |  |
| KEY_7 |  |
| KEY_8 |  |
| KEY_9 |  |
| KEY_A |  |
| KEY_B |  |
| KEY_C |  |
| KEY_D |  |
| KEY_E |  |
| KEY_F |  |
| KEY_G |  |
| KEY_H |  |
| KEY_I |  |
| KEY_J |  |
| KEY_K |  |
| KEY_L |  |
| KEY_M |  |
| KEY_N |  |
| KEY_O |  |
| KEY_P |  |
| KEY_Q |  |
| KEY_R |  |
| KEY_S |  |
| KEY_T |  |
| KEY_U |  |
| KEY_V |  |
| KEY_W |  |
| KEY_X |  |
| KEY_Y |  |
| KEY_Z |  |
| KEY_F1 |  |
| KEY_F2 |  |
| KEY_F3 |  |
| KEY_F4 |  |
| KEY_F5 |  |
| KEY_F6 |  |
| KEY_F7 |  |
| KEY_F8 |  |
| KEY_F9 |  |
| KEY_F10 |  |
| KEY_F11 |  |
| KEY_F12 |  |
| KEY_F13 |  |
| KEY_F14 |  |
| KEY_F15 |  |
| KEY_F16 |  |
| KEY_F17 |  |
| KEY_F18 |  |
| KEY_F19 |  |
| KEY_F20 |  |
| KEY_F21 |  |
| KEY_F22 |  |
| KEY_F23 |  |
| KEY_F24 |  |
| KEY_APOSTROPHE |  |
| KEY_COMMA |  |
| KEY_MINUS |  |
| KEY_PERIOD |  |
| KEY_SLASH |  |
| KEY_SEMICOLON |  |
| KEY_EQUAL |  |
| KEY_LEFT_BRACKET |  |
| KEY_BACKSLASH |  |
| KEY_RIGHT_BRACKET |  |
| KEY_GRAVE_ACCENT |  |
| KEY_CAPS_LOCK |  |
| KEY_SCROLL_LOCK |  |
| KEY_NUM_LOCK |  |
| KEY_PRINT_SCREEN |  |
| KEY_PAUSE |  |
| KEY_KEYPAD0 |  |
| KEY_KEYPAD1 |  |
| KEY_KEYPAD2 |  |
| KEY_KEYPAD3 |  |
| KEY_KEYPAD4 |  |
| KEY_KEYPAD5 |  |
| KEY_KEYPAD6 |  |
| KEY_KEYPAD7 |  |
| KEY_KEYPAD8 |  |
| KEY_KEYPAD9 |  |
| KEY_KEYPAD_DECIMAL |  |
| KEY_KEYPAD_DIVIDE |  |
| KEY_KEYPAD_MULTIPLY |  |
| KEY_KEYPAD_SUBTRACT |  |
| KEY_KEYPAD_ADD |  |
| KEY_KEYPAD_ENTER |  |
| KEY_KEYPAD_EQUAL |  |
| KEY_APP_BACK |  |
| KEY_APP_FORWARD |  |
| KEY_OEM102 |  |
| KEY_GAMEPAD_START |  |
| KEY_GAMEPAD_BACK |  |
| KEY_GAMEPAD_FACE_LEFT |  |
| KEY_GAMEPAD_FACE_RIGHT |  |
| KEY_GAMEPAD_FACE_UP |  |
| KEY_GAMEPAD_FACE_DOWN |  |
| KEY_GAMEPAD_DPAD_LEFT |  |
| KEY_GAMEPAD_DPAD_RIGHT |  |
| KEY_GAMEPAD_DPAD_UP |  |
| KEY_GAMEPAD_DPAD_DOWN |  |
| KEY_GAMEPAD_L1 |  |
| KEY_GAMEPAD_R1 |  |
| KEY_GAMEPAD_L2 |  |
| KEY_GAMEPAD_R2 |  |
| KEY_GAMEPAD_L3 |  |
| KEY_GAMEPAD_R3 |  |
| KEY_GAMEPAD_L_STICK_LEFT |  |
| KEY_GAMEPAD_L_STICK_RIGHT |  |
| KEY_GAMEPAD_L_STICK_UP |  |
| KEY_GAMEPAD_L_STICK_DOWN |  |
| KEY_GAMEPAD_R_STICK_LEFT |  |
| KEY_GAMEPAD_R_STICK_RIGHT |  |
| KEY_GAMEPAD_R_STICK_UP |  |
| KEY_GAMEPAD_R_STICK_DOWN |  |
| KEY_MOUSE_LEFT |  |
| KEY_MOUSE_RIGHT |  |
| KEY_MOUSE_MIDDLE |  |
| KEY_MOUSE_X1 |  |
| KEY_MOUSE_X2 |  |
| KEY_MOUSE_WHEEL_X |  |
| KEY_MOUSE_WHEEL_Y |  |
| KEY_RESERVED_FOR_MOD_CTRL |  |
| KEY_RESERVED_FOR_MOD_SHIFT |  |
| KEY_RESERVED_FOR_MOD_ALT |  |
| KEY_RESERVED_FOR_MOD_SUPER |  |
| KEY_NAMED_KEY_END |  |
| KEY_NAMED_KEY_COUNT |  |
| MOD_NONE |  |
| MOD_CTRL |  |
| MOD_SHIFT |  |
| MOD_ALT |  |
| MOD_SUPER |  |

### Enum: MouseButton

| Name | Description |
| --- | --- |
| LEFT |  |
| RIGHT |  |
| MIDDLE |  |
| COUNT |  |

### Enum: MouseCursor

| Name | Description |
| --- | --- |
| NONE |  |
| ARROW |  |
| TEXT_INPUT | When hovering over `input_text`, etc. |
| RESIZE_ALL | (Unused by Dear ImGui functions) |
| RESIZE_NS | When hovering over a horizontal border |
| RESIZE_EW | When hovering over a vertical border or a column |
| RESIZE_NESW | When hovering over the bottom-left corner of a window |
| RESIZE_NWSE | When hovering over the bottom-right corner of a window |
| HAND | (Unused by Dear ImGui functions. Use for e.g. hyperlinks) |
| WAIT | When waiting for something to process/load. |
| PROGRESS | When waiting for something to process/load, but application is still interactive. |
| NOT_ALLOWED | When hovering something with disallowed interaction. Usually a crossed circle. |
| COUNT |  |

### Enum: MouseSource

| Name | Description |
| --- | --- |
| MOUSE | Input is coming from an actual mouse. |
| TOUCH_SCREEN | Input is coming from a touch screen (no hovering prior to initial press, less precise initial press aiming, dual-axis wheeling possible). |
| PEN | Input is coming from a pressure/magnetic pen (often used in conjunction with high-sampling rates). |
| COUNT |  |

### Enum: PopupFlags

| Name | Description |
| --- | --- |
| NONE |  |
| MOUSE_BUTTON_LEFT | For BeginPopupContext*(): open on Left Mouse release. Only one button allowed! |
| MOUSE_BUTTON_RIGHT | For BeginPopupContext*(): open on Right Mouse release. Only one button allowed! (default) |
| MOUSE_BUTTON_MIDDLE | For BeginPopupContext*(): open on Middle Mouse release. Only one button allowed! |
| NO_REOPEN | For `open_popup`*(), BeginPopupContext*(): don't reopen same popup if already open (won't reposition, won't reinitialize navigation) |
| NO_OPEN_OVER_EXISTING_POPUP | For `open_popup`*(), BeginPopupContext*(): don't open if there's already a popup at the same level of the popup stack |
| NO_OPEN_OVER_ITEMS | For `begin_popup_context_window()`: don't return true when hovering items, only when hovering empty space |
| ANY_POPUP_ID | For `is_popup_open()`: ignore the ImGuiID parameter and test for any popup. |
| ANY_POPUP_LEVEL | For `is_popup_open()`: search/test at any level of the popup stack (default test in the current level) |
| ANY_POPUP |  |

### Enum: SelectableFlags

| Name | Description |
| --- | --- |
| NONE |  |
| NO_AUTO_CLOSE_POPUPS | Clicking this doesn't close parent popup window (overrides `ItemFlags.AUTO_CLOSE_POPUPS`) |
| SPAN_ALL_COLUMNS | Frame will span all columns of its container table (text will still fit in current column) |
| ALLOW_DOUBLE_CLICK | Generate press events on double clicks too |
| DISABLED | Cannot be selected, display grayed out text |
| ALLOW_OVERLAP | Hit testing will allow subsequent widgets to overlap this one. Require previous frame HoveredId to match before being usable. Shortcut to calling `set_next_item_allow_overlap()`. |
| HIGHLIGHT | Make the item be displayed as if it is hovered |
| SELECT_ON_NAV | Auto-select when moved into, unless Ctrl is held. Automatic when in a `begin_multi_select()` block. |

### Enum: SliderFlags

| Name | Description |
| --- | --- |
| NONE |  |
| LOGARITHMIC | Make the widget logarithmic (linear otherwise). Consider using `SliderFlags.NO_ROUND_TO_FORMAT` with this if using a format-string with small amount of digits. |
| NO_ROUND_TO_FORMAT | Disable rounding underlying value to match precision of the display format string (e.g. %.3f values are rounded to those 3 digits). |
| NO_INPUT | Disable Ctrl+Click or Enter key allowing to input text directly into the widget. |
| WRAP_AROUND | Enable wrapping around from max to min and from min to max. Only supported by DragXXX() functions for now. |
| CLAMP_ON_INPUT | Clamp value to min/max bounds when input manually with Ctrl+Click. By default Ctrl+Click allows going out of bounds. |
| CLAMP_ZERO_RANGE | Clamp even if min==max==0.0f. Otherwise due to legacy reason DragXXX functions don't clamp with those values. When your clamping limits are dynamic you almost always want to use it. |
| NO_SPEED_TWEAKS | Disable keyboard modifiers altering tweak speed. Useful if you want to alter tweak speed yourself based on your own logic. |
| COLOR_MARKERS | `drag_scalar_n()`, `slider_scalar_n()`: Draw R/G/B/A color markers on each component. |
| ALWAYS_CLAMP |  |

### Enum: StyleVar

| Name | Description |
| --- | --- |
| ALPHA | Float     Alpha |
| DISABLED_ALPHA | Float     DisabledAlpha |
| WINDOW_PADDING | ImVec2    WindowPadding |
| WINDOW_ROUNDING | Float     WindowRounding |
| WINDOW_BORDER_SIZE | Float     WindowBorderSize |
| WINDOW_MIN_SIZE | ImVec2    WindowMinSize |
| WINDOW_TITLE_ALIGN | ImVec2    WindowTitleAlign |
| CHILD_ROUNDING | Float     ChildRounding |
| CHILD_BORDER_SIZE | Float     ChildBorderSize |
| POPUP_ROUNDING | Float     PopupRounding |
| POPUP_BORDER_SIZE | Float     PopupBorderSize |
| FRAME_PADDING | ImVec2    FramePadding |
| FRAME_ROUNDING | Float     FrameRounding |
| FRAME_BORDER_SIZE | Float     FrameBorderSize |
| ITEM_SPACING | ImVec2    ItemSpacing |
| ITEM_INNER_SPACING | ImVec2    ItemInnerSpacing |
| INDENT_SPACING | Float     IndentSpacing |
| CELL_PADDING | ImVec2    CellPadding |
| SCROLLBAR_SIZE | Float     ScrollbarSize |
| SCROLLBAR_ROUNDING | Float     ScrollbarRounding |
| SCROLLBAR_PADDING | Float     ScrollbarPadding |
| GRAB_MIN_SIZE | Float     GrabMinSize |
| GRAB_ROUNDING | Float     GrabRounding |
| IMAGE_ROUNDING | Float     ImageRounding |
| IMAGE_BORDER_SIZE | Float     ImageBorderSize |
| TAB_ROUNDING | Float     TabRounding |
| TAB_BORDER_SIZE | Float     TabBorderSize |
| TAB_MIN_WIDTH_BASE | Float     TabMinWidthBase |
| TAB_MIN_WIDTH_SHRINK | Float     TabMinWidthShrink |
| TAB_BAR_BORDER_SIZE | Float     TabBarBorderSize |
| TAB_BAR_OVERLINE_SIZE | Float     TabBarOverlineSize |
| TABLE_ANGLED_HEADERS_ANGLE | Float     TableAngledHeadersAngle |
| TABLE_ANGLED_HEADERS_TEXT_ALIGN | ImVec2  TableAngledHeadersTextAlign |
| TREE_LINES_SIZE | Float     TreeLinesSize |
| TREE_LINES_ROUNDING | Float     TreeLinesRounding |
| BUTTON_TEXT_ALIGN | ImVec2    ButtonTextAlign |
| SELECTABLE_TEXT_ALIGN | ImVec2    SelectableTextAlign |
| SEPARATOR_SIZE | Float     SeparatorSize |
| SEPARATOR_TEXT_BORDER_SIZE | Float     SeparatorTextBorderSize |
| SEPARATOR_TEXT_ALIGN | ImVec2    SeparatorTextAlign |
| SEPARATOR_TEXT_PADDING | ImVec2    SeparatorTextPadding |
| COUNT |  |

### Enum: TabBarFlags

| Name | Description |
| --- | --- |
| NONE |  |
| REORDERABLE | Allow manually dragging tabs to re-order them + New tabs are appended at the end of list |
| AUTO_SELECT_NEW_TABS | Automatically select new tabs when they appear |
| TAB_LIST_POPUP_BUTTON | Disable buttons to open the tab list popup |
| NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON | Disable behavior of closing tabs (that are submitted with p_open != NULL) with middle mouse button. You may handle this behavior manually on user's side with if (`is_item_hovered()` && `is_mouse_clicked(2)`) *p_open = false. |
| NO_TAB_LIST_SCROLLING_BUTTONS | Disable scrolling buttons (apply when fitting policy is `TabBarFlags.FITTING_POLICY_SCROLL`) |
| NO_TOOLTIP | Disable tooltips when hovering a tab |
| DRAW_SELECTED_OVERLINE | Draw selected overline markers over selected tab |
| FITTING_POLICY_MIXED | Shrink down tabs when they don't fit, until width is style.TabMinWidthShrink, then enable scrolling buttons. |
| FITTING_POLICY_SHRINK | Shrink down tabs when they don't fit |
| FITTING_POLICY_SCROLL | Enable scrolling buttons when tabs don't fit |

### Enum: TabItemFlags

| Name | Description |
| --- | --- |
| NONE |  |
| UNSAVED_DOCUMENT | Display a dot next to the title + set `TabItemFlags.NO_ASSUMED_CLOSURE`. |
| SET_SELECTED | Trigger flag to programmatically make the tab selected when calling `begin_tab_item()` |
| NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON | Disable behavior of closing tabs (that are submitted with p_open != NULL) with middle mouse button. You may handle this behavior manually on user's side with if (`is_item_hovered()` && `is_mouse_clicked(2)`) *p_open = false. |
| NO_PUSH_ID | Don't call `push_id()`/`pop_id()` on `begin_tab_item()`/`end_tab_item()` |
| NO_TOOLTIP | Disable tooltip for the given tab |
| NO_REORDER | Disable reordering this tab or having another tab cross over this tab |
| LEADING | Enforce the tab position to the left of the tab bar (after the tab list popup button) |
| TRAILING | Enforce the tab position to the right of the tab bar (before the scrolling buttons) |
| NO_ASSUMED_CLOSURE | Tab is selected when trying to close + closure is not immediately assumed (will wait for user to stop submitting the tab). Otherwise closure is assumed when pressing the X, so if you keep submitting the tab may reappear at end of tab bar. |

### Enum: TableBgTarget

| Name | Description |
| --- | --- |
| NONE |  |
| ROW_BG0 | Set row background color 0 (generally used for background, automatically set when `TableFlags.ROW_BG` is used) |
| ROW_BG1 | Set row background color 1 (generally used for selection marking) |
| CELL_BG | Set cell background color (top-most color) |

### Enum: TableColumnFlags

| Name | Description |
| --- | --- |
| NONE |  |
| DISABLED | Overriding/master disable flag: hide column, won't show in context menu (unlike calling `table_set_column_enabled()` which manipulates the user accessible state) |
| DEFAULT_HIDE | Default as a hidden/disabled column. |
| DEFAULT_SORT | Default as a sorting column. |
| WIDTH_STRETCH | Column will stretch. Preferable with horizontal scrolling disabled (default if table sizing policy is _SizingStretchSame or _SizingStretchProp). |
| WIDTH_FIXED | Column will not stretch. Preferable with horizontal scrolling enabled (default if table sizing policy is _SizingFixedFit and table is resizable). |
| NO_RESIZE | Disable manual resizing. |
| NO_REORDER | Disable manual reordering this column, this will also prevent other columns from crossing over this column. |
| NO_HIDE | Disable ability to hide/disable this column. |
| NO_CLIP | Disable clipping for this column (all NoClip columns will render in a same draw command). |
| NO_SORT | Disable ability to sort on this field (even if `TableFlags.SORTABLE` is set on the table). |
| NO_SORT_ASCENDING | Disable ability to sort in the ascending direction. |
| NO_SORT_DESCENDING | Disable ability to sort in the descending direction. |
| NO_HEADER_LABEL | `table_headers_row()` will submit an empty label for this column. Convenient for some small columns. Name will still appear in context menu or in angled headers. You may append into this cell by calling `table_set_column_index()` right after the `table_headers_row()` call. |
| NO_HEADER_WIDTH | Disable header text width contribution to automatic column width. |
| PREFER_SORT_ASCENDING | Make the initial sort direction Ascending when first sorting on this column (default). |
| PREFER_SORT_DESCENDING | Make the initial sort direction Descending when first sorting on this column. |
| INDENT_ENABLE | Use current `indent` value when entering cell (default for column 0). |
| INDENT_DISABLE | Ignore current `indent` value when entering cell (default for columns > 0). Indentation changes _within_ the cell will still be honored. |
| ANGLED_HEADER | `table_headers_row()` will submit an angled header row for this column. Note this will add an extra row. |
| IS_ENABLED | Status: is enabled == not hidden by user/api (referred to as "Hide" in _DefaultHide and _NoHide) flags. |
| IS_VISIBLE | Status: is visible == is enabled AND not clipped by scrolling. |
| IS_SORTED | Status: is currently part of the sort specs |
| IS_HOVERED | Status: is hovered by mouse |

### Enum: TableFlags

| Name | Description |
| --- | --- |
| NONE |  |
| RESIZABLE | Enable resizing columns. |
| REORDERABLE | Enable reordering columns in header row. (Need calling `table_setup_column()` + `table_headers_row()` to display headers, or using `TableFlags.CONTEXT_MENU_IN_BODY` to access context-menu without headers). |
| HIDEABLE | Enable hiding/disabling columns in context menu. |
| SORTABLE | Enable sorting. Call `table_get_sort_specs()` to obtain sort specs. Also see `TableFlags.SORT_MULTI` and `TableFlags.SORT_TRISTATE`. |
| NO_SAVED_SETTINGS | Disable persisting columns order, width, visibility and sort settings in the .ini file. |
| CONTEXT_MENU_IN_BODY | Right-click on columns body/contents will also display table context menu. By default it is available in `table_headers_row()`. |
| ROW_BG | Set each RowBg color with `Col.TABLE_ROW_BG` or `Col.TABLE_ROW_BG_ALT` (equivalent of calling `table_set_bg_color` with ImGuiTableBgFlags_RowBg0 on each row manually) |
| BORDERS_INNER_H | Draw horizontal borders between rows. |
| BORDERS_OUTER_H | Draw horizontal borders at the top and bottom. |
| BORDERS_INNER_V | Draw vertical borders between columns. |
| BORDERS_OUTER_V | Draw vertical borders on the left and right sides. |
| BORDERS_H | Draw horizontal borders. |
| BORDERS_V | Draw vertical borders. |
| BORDERS_INNER | Draw inner borders. |
| BORDERS_OUTER | Draw outer borders. |
| BORDERS | Draw all borders. |
| NO_BORDERS_IN_BODY | [ALPHA] Disable vertical borders in columns Body (borders will always appear in Headers). -> May move to style |
| NO_BORDERS_IN_BODY_UNTIL_RESIZE | [ALPHA] Disable vertical borders in columns Body until hovered for resize (borders will always appear in Headers). -> May move to style |
| SIZING_FIXED_FIT | `columns` default to _WidthFixed or _WidthAuto (if resizable or not resizable), matching contents width. |
| SIZING_FIXED_SAME | `columns` default to _WidthFixed or _WidthAuto (if resizable or not resizable), matching the maximum contents width of all columns. Implicitly enable `TableFlags.NO_KEEP_COLUMNS_VISIBLE`. |
| SIZING_STRETCH_PROP | `columns` default to _WidthStretch with default weights proportional to each columns contents widths. |
| SIZING_STRETCH_SAME | `columns` default to _WidthStretch with default weights all equal, unless overridden by `table_setup_column()`. |
| NO_HOST_EXTEND_X | Make outer width auto-fit to columns, overriding outer_size.x value. Only available when ScrollX/ScrollY are disabled and Stretch columns are not used. |
| NO_HOST_EXTEND_Y | Make outer height stop exactly at outer_size.y (prevent auto-extending table past the limit). Only available when ScrollX/ScrollY are disabled. Data below the limit will be clipped and not visible. |
| NO_KEEP_COLUMNS_VISIBLE | Disable keeping column always minimally visible when ScrollX is off and table gets too small. Not recommended if columns are resizable. |
| PRECISE_WIDTHS | Disable distributing remainder width to stretched columns (width allocation on a 100-wide table with 3 columns: Without this flag: 33,33,34. With this flag: 33,33,33). With larger number of columns, resizing will appear to be less smooth. |
| NO_CLIP | Disable clipping rectangle for every individual columns (reduce draw command count, items will be able to overflow into other columns). Generally incompatible with `table_setup_scroll_freeze()`. |
| PAD_OUTER_X | Default if BordersOuterV is on. Enable outermost padding. Generally desirable if you have headers. |
| NO_PAD_OUTER_X | Default if BordersOuterV is off. Disable outermost padding. |
| NO_PAD_INNER_X | Disable inner padding between columns (double inner padding if BordersOuterV is on, single inner padding if BordersOuterV is off). |
| SCROLL_X | Enable horizontal scrolling. Require 'outer_size' parameter of `begin_table()` to specify the container size. Changes default sizing policy. Because this creates a child window, ScrollY is currently generally recommended when using ScrollX. |
| SCROLL_Y | Enable vertical scrolling. Require 'outer_size' parameter of `begin_table()` to specify the container size. |
| SORT_MULTI | Hold shift when clicking headers to sort on multiple column. `table_get_sort_specs()` may return specs where (SpecsCount > 1). |
| SORT_TRISTATE | Allow no sorting, disable default sorting. `table_get_sort_specs()` may return specs where (SpecsCount == 0). |
| HIGHLIGHT_HOVERED_COLUMN | Highlight column headers when hovered (may evolve into a fuller highlight) |

### Enum: TableRowFlags

| Name | Description |
| --- | --- |
| NONE |  |
| HEADERS | Identify header row (set default background color + width of its contents accounted differently for auto column width) |

### Enum: TextureFormat

| Name | Description |
| --- | --- |
| RGBA32 | 4 components per pixel, each is unsigned 8-bit. Total size = TexWidth * TexHeight * 4 |
| ALPHA8 | 1 component per pixel, each is unsigned 8-bit. Total size = TexWidth * TexHeight |

### Enum: TextureStatus

| Name | Description |
| --- | --- |
| OK |  |
| DESTROYED | Backend destroyed the texture. |
| WANT_CREATE | Requesting backend to create the texture. Set status OK when done. |
| WANT_UPDATES | Requesting backend to update specific blocks of pixels (write to texture portions which have never been used before). Set status OK when done. |
| WANT_DESTROY | Requesting backend to destroy the texture. Set status to Destroyed when done. |

### Enum: TreeNodeFlags

| Name | Description |
| --- | --- |
| NONE |  |
| SELECTED | Draw as selected |
| FRAMED | Draw frame with background (e.g. for `collapsing_header`) |
| ALLOW_OVERLAP | Hit testing will allow subsequent widgets to overlap this one. Require previous frame HoveredId to match before being usable. Shortcut to calling `set_next_item_allow_overlap()`. |
| NO_TREE_PUSH_ON_OPEN | Don't do a `tree_push()` when open (e.g. for `collapsing_header`) = no extra indent nor pushing on ID stack |
| NO_AUTO_OPEN_ON_LOG | Don't automatically and temporarily open node when Logging is active (by default logging will automatically open tree nodes) |
| DEFAULT_OPEN | Default node to be open |
| OPEN_ON_DOUBLE_CLICK | Open on double-click instead of simple click (default for multi-select unless any _OpenOnXXX behavior is set explicitly). Both behaviors may be combined. |
| OPEN_ON_ARROW | Open when clicking on the arrow part (default for multi-select unless any _OpenOnXXX behavior is set explicitly). Both behaviors may be combined. |
| LEAF | No collapsing, no arrow (use as a convenience for leaf nodes). Note: will always open a tree/id scope and return true. If you never use that scope, add `TreeNodeFlags.NO_TREE_PUSH_ON_OPEN`. |
| BULLET | Display a bullet instead of arrow. IMPORTANT: node can still be marked open/close if you don't set the _Leaf flag! |
| FRAME_PADDING | Use FramePadding (even for an unframed text node) to vertically align text baseline to regular widget height. Equivalent to calling `align_text_to_frame_padding()` before the node. |
| SPAN_AVAIL_WIDTH | Extend hit box to the right-most edge, even if not framed. This is not the default in order to allow adding other items on the same line without using AllowOverlap mode. |
| SPAN_FULL_WIDTH | Extend hit box to the left-most and right-most edges (cover the indent area). |
| SPAN_LABEL_WIDTH | Narrow hit box + narrow hovering highlight, will only cover the label text. |
| SPAN_ALL_COLUMNS | Frame will span all columns of its container table (label will still fit in current column) |
| LABEL_SPAN_ALL_COLUMNS | Label will span all columns of its container table |
| NAV_LEFT_JUMPS_TO_PARENT | Nav: left arrow moves back to parent. This is processed in `tree_pop()` when there's an unfulfilled Left nav request remaining. |
| COLLAPSING_HEADER |  |
| DRAW_LINES_NONE | No lines drawn |
| DRAW_LINES_FULL | Horizontal lines to child nodes. Vertical line drawn down to `tree_pop()` position: cover full contents. Faster (for large trees). |
| DRAW_LINES_TO_NODES | Horizontal lines to child nodes. Vertical line drawn down to bottom-most child node. Slower (for large trees). |

### Enum: WindowFlags

| Name | Description |
| --- | --- |
| NONE |  |
| NO_TITLE_BAR | Disable title-bar |
| NO_RESIZE | Disable user resizing with the lower-right grip |
| NO_MOVE | Disable user moving the window |
| NO_SCROLLBAR | Disable scrollbars (window can still scroll with mouse or programmatically) |
| NO_SCROLL_WITH_MOUSE | Disable user vertically scrolling with mouse wheel. On child window, mouse wheel will be forwarded to the parent unless NoScrollbar is also set. |
| NO_COLLAPSE | Disable user collapsing window by double-clicking on it. Also referred to as Window Menu Button (e.g. within a docking node). |
| ALWAYS_AUTO_RESIZE | Resize every window to its content every frame |
| NO_BACKGROUND | Disable drawing background color (WindowBg, etc.) and outside border. Similar as using `set_next_window_bg_alpha(0.0)`. |
| NO_SAVED_SETTINGS | Never load/save settings in .ini file |
| NO_MOUSE_INPUTS | Disable catching mouse, hovering test with pass through. |
| MENU_BAR | Has a menu-bar |
| HORIZONTAL_SCROLLBAR | Allow horizontal scrollbar to appear (off by default). You may use `set_next_window_content_size((width,0.0))`; prior to calling `begin()` to specify width. Read code in imgui_demo in the "Horizontal Scrolling" section. |
| NO_FOCUS_ON_APPEARING | Disable taking focus when transitioning from hidden to visible state |
| NO_BRING_TO_FRONT_ON_FOCUS | Disable bringing window to front when taking focus (e.g. clicking on it or programmatically giving it focus) |
| ALWAYS_VERTICAL_SCROLLBAR | Always show vertical scrollbar (even if ContentSize.y < Size.y) |
| ALWAYS_HORIZONTAL_SCROLLBAR | Always show horizontal scrollbar (even if ContentSize.x < Size.x) |
| NO_NAV_INPUTS | No keyboard/gamepad navigation within the window |
| NO_NAV_FOCUS | No focusing toward this window with keyboard/gamepad navigation (e.g. skipped by Ctrl+Tab) |
| UNSAVED_DOCUMENT | Display a dot next to the title. When used in a tab/docking context, tab is selected when clicking the X + closure is not assumed (will wait for user to stop submitting the tab). Otherwise closure is assumed when pressing the X, so if you keep submitting the tab may reappear at end of tab bar. |
| NO_NAV |  |
| NO_DECORATION |  |
| NO_INPUTS |  |
| CHILD_WINDOW | Don't use! For internal use by `begin_child()` |
| TOOLTIP | Don't use! For internal use by `begin_tooltip()` |
| POPUP | Don't use! For internal use by `begin_popup()` |
| MODAL | Don't use! For internal use by `begin_popup_modal()` |
| CHILD_MENU | Don't use! For internal use by `begin_menu()` |

### Enum: DrawListCallbackResult

| Name | Description |
| --- | --- |
| DRAW | No callback, backend should draw elements. |
| CALLBACK | Callback executed, no further processing of this command necessary. |
| RESET_RENDER_STATE | Reset render state token, backend should perform render state reset. |

## Class Reference

### Class: DrawList

::: api-signature
```python
DrawList.add_bezier_cubic(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
    col: int,
    thickness: float,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_bezier_quadratic(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    col: int,
    thickness: float,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_callback(
    callable: int | Callable[[DrawList, DrawCmd, int | bytes], None],
    userdata: int | bytes,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_circle(
    center: tuple[float, float],
    radius: float,
    col: int,
    num_segments: int = 0,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_circle_filled(
    center: tuple[float, float],
    radius: float,
    col: int,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_concave_poly_filled(
    points: Sequence[tuple[float, float]],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_concave_poly_filled(
    points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_convex_poly_filled(
    points: Sequence[tuple[float, float]],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_convex_poly_filled(
    points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_draw_cmd() -> None:
    """
    This is useful if you need to forcefully create a new draw call (to allow for dependent rendering / blending). Otherwise primitives are merged into the same draw-call as much as possible.
    """
```
:::

::: api-signature
```python
DrawList.add_ellipse(
    center: tuple[float, float],
    radius: tuple[float, float],
    col: int,
    rot: float = 0.0,
    num_segments: int = 0,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_ellipse_filled(
    center: tuple[float, float],
    radius: tuple[float, float],
    col: int,
    rot: float = 0.0,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_image(
    tex_ref: TextureRef | int,
    p_min: tuple[float, float],
    p_max: tuple[float, float],
    uv_min: tuple[float, float] = (0.0, 0.0),
    uv_max: tuple[float, float] = (1.0, 1.0),
    col: int = COL32_WHITE,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_image_quad(
    tex_ref: TextureRef | int,
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
    uv1: tuple[float, float] = (0.0, 0.0),
    uv2: tuple[float, float] = (1.0, 0.0),
    uv3: tuple[float, float] = (1.0, 1.0),
    uv4: tuple[float, float] = (0.0, 1.0),
    col: int = COL32_WHITE,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_image_rounded(
    tex_ref: TextureRef | int,
    p_min: tuple[float, float],
    p_max: tuple[float, float],
    uv_min: tuple[float, float],
    uv_max: tuple[float, float],
    col: int,
    rounding: float,
    flags: DrawFlags = DrawFlags.NONE,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_line(
    p1: tuple[float, float],
    p2: tuple[float, float],
    col: int,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_ngon(
    center: tuple[float, float],
    radius: float,
    col: int,
    num_segments: int,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_ngon_filled(
    center: tuple[float, float],
    radius: float,
    col: int,
    num_segments: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_polyline(
    points: Sequence[tuple[float, float]],
    col: int,
    flags: DrawFlags,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_polyline(
    points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)],
    col: int,
    flags: DrawFlags,
    thickness: float,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_quad(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
    col: int,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_quad_filled(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_rect(
    p_min: tuple[float, float],
    p_max: tuple[float, float],
    col: int,
    rounding: float = 0.0,
    flags: DrawFlags = DrawFlags.NONE,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_rect_filled(
    p_min: tuple[float, float],
    p_max: tuple[float, float],
    col: int,
    rounding: float = 0.0,
    flags: DrawFlags = DrawFlags.NONE,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_rect_filled_multi_color(
    p_min: tuple[float, float],
    p_max: tuple[float, float],
    col_upr_left: int,
    col_upr_right: int,
    col_bot_right: int,
    col_bot_left: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_text(
    pos: tuple[float, float],
    col: int,
    text: str,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_text(
    font: Font,
    font_size: float,
    pos: tuple[float, float],
    col: int,
    text: str,
    wrap_width: float = 0.0,
    cpu_fine_clip_rect: tuple[float, float, float, float] | None = None,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_triangle(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    col: int,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.add_triangle_filled(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.channels_merge() -> None:
```
:::

::: api-signature
```python
DrawList.channels_set_current(
    n: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.channels_split(
    count: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.commands -> Iterator[DrawCmd]:
```
:::

::: api-signature
```python
DrawList.get_clip_rect_max() -> tuple[float, float]:
```
:::

::: api-signature
```python
DrawList.get_clip_rect_min() -> tuple[float, float]:
```
:::

::: api-signature
```python
DrawList.idx_buffer_data -> int:
```
:::

::: api-signature
```python
DrawList.idx_buffer_size -> int:
```
:::

::: api-signature
```python
DrawList.path_arc_to(
    center: tuple[float, float],
    radius: float,
    a_min: float,
    a_max: float,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_arc_to_fast(
    center: tuple[float, float],
    radius: float,
    a_min_of_12: int,
    a_max_of_12: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_bezier_cubic_curve_to(
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_bezier_quadratic_curve_to(
    p2: tuple[float, float],
    p3: tuple[float, float],
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_clear() -> None:
```
:::

::: api-signature
```python
DrawList.path_elliptical_arc_to(
    center: tuple[float, float],
    radius: tuple[float, float],
    rot: float,
    a_min: float,
    a_max: float,
    num_segments: int = 0,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_fill_concave(
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_fill_convex(
    col: int,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_line_to(
    pos: tuple[float, float],
) -> None:
```
:::

::: api-signature
```python
DrawList.path_line_to_merge_duplicate(
    pos: tuple[float, float],
) -> None:
```
:::

::: api-signature
```python
DrawList.path_rect(
    rect_min: tuple[float, float],
    rect_max: tuple[float, float],
    rounding: float = 0.0,
    flags: DrawFlags = DrawFlags.NONE,
) -> None:
```
:::

::: api-signature
```python
DrawList.path_stroke(
    col: int,
    flags: DrawFlags = DrawFlags.NONE,
    thickness: float = 1.0,
) -> None:
```
:::

::: api-signature
```python
DrawList.pop_clip_rect() -> None:
```
:::

::: api-signature
```python
DrawList.pop_texture() -> None:
```
:::

::: api-signature
```python
DrawList.ptr() -> int:
    """
    Internal function for reference book keeping.
    """
```
:::

::: api-signature
```python
DrawList.push_clip_rect(
    clip_rect_min: tuple[float, float],
    clip_rect_max: tuple[float, float],
    intersect_with_current_clip_rect: bool = False,
) -> None:
    """
    Render-level scissoring. This is passed down to your render function but not used for CPU-side coarse clipping. Prefer using higher-level `imgui.push_clip_rect()` to affect logic (hit-testing and widget culling)
    """
```
:::

::: api-signature
```python
DrawList.push_clip_rect_full_screen() -> None:
```
:::

::: api-signature
```python
DrawList.push_texture(
    tex_ref: TextureRef | int,
) -> None:
```
:::

::: api-signature
```python
DrawList.vtx_buffer_data -> int:
```
:::

::: api-signature
```python
DrawList.vtx_buffer_size -> int:
```
:::
