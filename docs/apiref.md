---
title: 'slimgui'
subtitle: 'Python bindings for Dear ImGui'
---

# slimgui - Python bindings for Dear ImGui

## Overview

The Slimgui package provides modern Python bindings for the following libraries:

 - [Dear ImGui](https://github.com/ocornut/imgui)
 - [ImPlot](https://github.com/epezent/implot)

The Python bindings documentation has been split into several parts:

- Dear ImGui bindings reference -- you're reading it.
- [ImPlot bindings API reference](./apiref_implot.html)

The project source code is hosted on [github.com/nurpax/slimgui](https://github.com/nurpax/slimgui).

Slimgui is built against Dear ImGui version %imguiversion%.

## Binding considerations

Slimgui has been developed with the following goals in mind:

- Support typing through .pyi files to enable good IDE support (auto-complete, type checking, docstrings)
- Closely match the Dear ImGui API but adapt for Python as necessary. Don't invent new API concepts.

The project has been developed using the Python `glfw` and `pyOpenGL` packages and includes integration backend for these APIs.  It should
be possible to develop integrations for other backends, such as SDL or Pygame.

The Slimgui API is similar to [pyimgui](https://github.com/pyimgui/pyimgui) except somewhat modernized:

- Enums in ImGui are exposed as typed Python enums using `enum.IntEnum` and `enum.IntFlag` to make it clear which API functions consume what type of enums.
- Vector types such as `ImVec2`, `ImVec4`, and `float*` arrays are converted to Python tuples such as `tuple[float, float]` (for `ImVec2`), `tuple[float, float, float, float]` (for `ImVec4`).
- Mutable bool args such as `bool* p_open` are input as normal `bool` values and returned as the second element of a 2-tuple.  For example `bool ImGui::Checkbox(const char* label, bool* v)` is translated to `def checkbox(label: str, v: bool) -> tuple[bool, bool]` that returns a 2-tuple where the first element is the boolean return value of `bool ImGui::Checkbox()` and the second element is the new value of the checkbox state.

## Getting started

Slimgui requires Python 3.10 or newer.

Installation: `pip install slimgui`

To run the example, clone the repo, install dependencies and run:

```
git clone https://github.com/nurpax/slimgui
cd slimgui
pip install glfw pyopengl numpy requests
python example/app.py
```

Browse the example code: [example/](https://github.com/nurpax/slimgui/blob/main/example/)

## Dear ImGui Enums

<!-- could list enums here like in a forward decl? -->
A detailed enum and class reference can be found here: [Enum Reference](#enum-reference)

## Dear ImGui API functions

The following documentation is primarily adapted from Dear ImGui main header [imgui.h](https://github.com/ocornut/imgui/blob/master/imgui.h),
with minor modifications to adapt symbol naming to Pythonic snake case.

### Context creation and access

Each context creates its own `FontAtlas` by default. You may instance one yourself and pass it to `create_context()` to share a font atlas between contexts.

#### Functions
<div class="raw-html-insert" data-apirefs="create_context, destroy_context, get_current_context, set_current_context"></div>

### Main

#### Functions
<div class="raw-html-insert" data-apirefs="get_io, get_style, new_frame, end_frame, render, get_draw_data"></div>

### Demo, Debug, Information

#### Functions
<div class="raw-html-insert" data-apirefs="show_demo_window, show_metrics_window, show_debug_log_window, show_id_stack_tool_window, show_about_window, show_style_editor, show_style_selector, show_font_selector, show_user_guide, get_version"></div>

### Styles

Note: functions shown below intentionally do not accept `None` as the destination style.  Python wrappers with same name exist in the `slimgui` module that can be called with `None` that then modifies the current context's style.

#### Functions
<div class="raw-html-insert" data-apirefs="style_colors_dark, style_colors_light, style_colors_classic"></div>

### Windows

- `begin()` = push window to the stack and start appending to it. `end()` = pop window from the stack.
- Passing `closable = True` shows a window-closing widget in the upper-right corner of the window,
  which clicking will set the boolean to false when clicked.
- You may append multiple times to the same window during the same frame by calling `begin()`/`end()` pairs multiple times. Some information such as `flags` or `closable` will only be considered by the first call to `begin()`.
- `begin()` returns `False` to indicate the window is collapsed or fully clipped, so you may early out and omit submitting
  anything to the window. Always call a matching `end()` for each `begin()` call, regardless of its return value!

  Important: due to legacy reason, `begin()`/`end()` and `begin_child()`/`end_child()` are inconsistent with all other functions such as `begin_menu()`/`end_menu()`, `begin_popup()`/`end_popup()`, etc. where the `end_xxx()` call should only be called if the corresponding
   `begin_xxx()` function returned `True`. `begin()` and `begin_child()` are the only odd ones out. Will be fixed in a future update.
- Note that the bottom of window stack always contains a window called "Debug".

#### Functions
<div class="raw-html-insert" data-apirefs="begin">
When the `closable` argument is set to `True`, the created window will display a close button.  The second bool of the return value will be `False` if the close button was pressed.  The intended usage is as follows:

```
win_open = True  # open/closed state

visible, win_open = imgui.begin(..., closable=win_open)
if visible:
    # render window contents here..
imgui.end()
```
</div>

<div class="raw-html-insert" data-apirefs="end">
Every `begin()` call must be paired with a corresponding `end()` call, regardless of the return value of `begin()` return value.
</div>

### Child Windows

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

#### Functions
<div class="raw-html-insert" data-apirefs="begin_child, end_child"></div>

### Window Utilities

- 'current window' = the window we are appending into while inside a `begin()`/`end()` block. 'next window' = next window we will `begin()` into.

#### Functions
<div class="raw-html-insert" data-apirefs="is_window_appearing, is_window_collapsed, is_window_focused, is_window_hovered, get_window_draw_list, get_window_pos, get_window_size, get_window_width, get_window_height"></div>

### Window Manipulation

- Prefer using `set_next_xxx` functions (before `begin`) rather than `set_xxx` functions (after `begin`).

#### Functions
<div class="raw-html-insert" data-apirefs="set_next_window_pos, set_next_window_size, set_next_window_size_constraints, set_next_window_content_size, set_next_window_collapsed, set_next_window_focus, set_next_window_scroll, set_next_window_bg_alpha, set_window_pos, set_window_size, set_window_collapsed, set_window_focus, set_window_pos, set_window_size, set_window_collapsed, set_window_focus"></div>

### Windows Scrolling

- Any change of scroll will be applied at the beginning of next frame in the first call to `begin()`.
- You may instead use `set_next_window_scroll()` prior to calling `begin()` to avoid this delay, as an alternative to using `set_scroll_x()`/`set_scroll_y()`.

#### Functions
<div class="raw-html-insert" data-apirefs="set_next_window_scroll, get_scroll_x, get_scroll_y, set_scroll_x, set_scroll_y, get_scroll_max_x, get_scroll_max_y, set_scroll_here_x, set_scroll_here_y, set_scroll_from_pos_x, set_scroll_from_pos_y"></div>

### Parameter stacks (shared)

#### Functions
<div class="raw-html-insert" data-apirefs="push_font, pop_font, push_style_color, pop_style_color, push_style_var, push_style_var_x, push_style_var_y, pop_style_var, push_tab_stop, pop_tab_stop, push_button_repeat, pop_button_repeat"></div>

### Parameter stacks (current window)

#### Functions
<div class="raw-html-insert" data-apirefs="push_item_width, pop_item_width, set_next_item_width, calc_item_width, push_text_wrap_pos, pop_text_wrap_pos"></div>

### Style read access

- Use `show_style_editor()` function to interactively see/edit the colors.

#### Functions
<div class="raw-html-insert" data-apirefs="get_font, get_font_size, get_font_tex_uv_white_pixel, get_color_u32, get_style_color_vec4"></div>

### Layout cursor positioning

- By "cursor" we mean the current output position.
- The typical widget behavior is to output themselves at the current cursor position, then move the cursor one line down.
- You can call `same_line()` between widgets to undo the last carriage return and output at the right of the preceding widget.
- YOU CAN DO 99% OF WHAT YOU NEED WITH ONLY `get_cursor_screen_pos()` and `get_content_region_avail()`.
- Attention! We currently have inconsistencies between window-local and absolute positions we will aim to fix with future API:
  - Absolute coordinate: `get_cursor_screen_pos()`, `set_cursor_screen_pos()`, all `DrawList` functions. -> this is the preferred way forward.
  - Window-local coordinates: `same_line(offset)`, `get_cursor_pos()`, `set_cursor_pos()`, `get_cursor_start_pos()`, `push_text_wrap_pos()`
  - Window-local coordinates: `get_content_region_max()`, `get_window_content_region_min()`, `get_window_content_region_max()` --> all obsoleted. YOU DON'T NEED THEM.
- `get_cursor_screen_pos()` = `get_cursor_pos()` + `get_window_pos()`. `get_window_pos()` is almost only ever useful to convert from window-local to absolute coordinates. Try not to use it.

#### Functions
<div class="raw-html-insert" data-apirefs="get_cursor_screen_pos, set_cursor_screen_pos, get_content_region_avail, get_cursor_pos, get_cursor_pos_x, get_cursor_pos_y, set_cursor_pos, set_cursor_pos_x, set_cursor_pos_y, get_cursor_start_pos"></div>

### Other layout functions

#### Functions
<div class="raw-html-insert" data-apirefs="separator, same_line, new_line, spacing, dummy, indent, unindent, begin_group, end_group, align_text_to_frame_padding, get_text_line_height, get_text_line_height_with_spacing, get_frame_height, get_frame_height_with_spacing"></div>

### ID stack/scopes

Read the FAQ (docs/FAQ.md or http://dearimgui.com/faq) for more details about how ID are handled in dear imgui.

Those questions are answered and impacted by understanding of the ID stack system:

  - "Q: Why is my widget not reacting when I click on it?"
  - "Q: How can I have widgets with an empty label?"
  - "Q: How can I have multiple widgets with the same label?"

Short version: ID are hashes of the entire ID stack. If you are creating widgets in a loop you most likely want to push a unique identifier (e.g. object pointer, loop index) to uniquely differentiate them.

You can also use the `"Label##foobar"` syntax within widget label to distinguish them from each others.

In this header file we use the `label`/`name` terminology to denote a string that will be displayed + used as an ID, whereas `str_id` denote a string that is only used as an ID and not normally displayed.

#### Functions
<div class="raw-html-insert" data-apirefs="push_id, pop_id, get_id"></div>

### Widgets: Text

#### Functions
<div class="raw-html-insert" data-apirefs="text_unformatted, text, text_colored, text_disabled, text_wrapped, label_text, bullet_text, separator_text"></div>

### Widgets: Main

- Most widgets return `True` when the value has been changed or when pressed/selected.
- You may also use one of the many `is_item_xxx` functions (e.g. `is_item_active()`, `is_item_hovered()`, etc.) to query widget state.

#### Functions
<div class="raw-html-insert" data-apirefs="button, small_button, invisible_button, arrow_button, checkbox, checkbox_flags, radio_button, progress_bar, bullet, text_link, text_link_open_url"></div>

### Widgets: Images

- Read about texture IDs and TextureRef in ImGui docs: [Image Loading and Displaying Examples](https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples)
  - In general, you shouldn't need to worry about `TextureRef` -- all image functions also accept an integer texture ID.
- `uv0` and `uv1` are texture coordinates. Read about them from the same link above.
  - `image()` pads adds `StyleVar.IMAGE_BORDER_SIZE` on each side, `image_button()` adds `StyleVar.FRAME_PADDING` on each side.
  - `image_button()` draws a background based on regular `button()` color and optionally an inner background if specified.

#### Functions
<div class="raw-html-insert" data-apirefs="image, image_with_bg, image_button"></div>

### Widgets: Combo Box (Dropdown)

- The `begin_combo()`/`end_combo()` API allows you to manage your contents and selection state however you want it, by creating e.g. `selectable()` items.
- The old `combo()` API are helpers over `begin_combo()`/`end_combo()` which are kept available for convenience purposes. This is analogous to how `list_box` is created.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_combo, end_combo, combo"></div>
### Widgets: Drag Sliders

- CTRL+Click on any drag box to turn them into an input box. Manually input values aren't clamped by default and can go off-bounds. Use `SliderFlags.ALWAYS_CLAMP` to always clamp.
- Adjust format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision e.g. `"%.3f"` -> `1.234`; `"%5.2f secs"` -> `01.23 secs`; `"Biscuit: %.0f"` -> `Biscuit: 1`; etc.
- Format string may also be set to `None` or use the default format (`"%f"` or `"%d"`).
- Speed is per-pixel of mouse movement (`v_speed=0.2`: mouse needs to move by 5 pixels to increase value by 1). For keyboard/gamepad navigation, minimum speed is `max(v_speed, minimum_step_at_given_precision)`.
- Use `v_min < v_max` to clamp edits to given limits. Note that CTRL+Click manual input can override those limits if `SliderFlags.ALWAYS_CLAMP` is not used.
- Use `v_max = FLT_MAX` / `INT_MAX` etc. to avoid clamping to a maximum, same with `v_min = -FLT_MAX` / `INT_MIN` to avoid clamping to a minimum.
- We use the same sets of flags for `drag_xxx()` and `slider_xxx()` functions as the features are the same and it makes it easier to swap them.

#### Functions
<div class="raw-html-insert" data-apirefs="drag_float, drag_float2, drag_float3, drag_float4, drag_float_range2, drag_int, drag_int2, drag_int3, drag_int4, drag_int_range2, drag_scalar, drag_scalar_n"></div>

### Widgets: Regular Sliders

- CTRL+Click on any slider to turn it into an input box. Manually input values aren't clamped by default and can go off-bounds. Use `SliderFlags.ALWAYS_CLAMP` to always clamp.
- Adjust the format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision, e.g., `"%.3f"` -> `1.234`; `"%5.2f secs"` -> `01.23 secs`; `"Biscuit: %.0f"` -> `Biscuit: 1`; etc.
- The format string may also be set to `None` or use the default format (`"%f"` or `"%d"`).

#### Functions
<div class="raw-html-insert" data-apirefs="slider_float, slider_float2, slider_float3, slider_float4, slider_angle, slider_int, slider_int2, slider_int3, slider_int4, slider_scalar, slider_scalar_n, vslider_float, vslider_int, vslider_scalar"></div>

### Widgets: Input with Keyboard

- Most of the `InputTextFlags` flags are only useful for `input_text()` and not for `input_float_*`, `input_float_*`, `input_int_*`, etc.

#### Functions
<div class="raw-html-insert" data-apirefs="input_text, input_text_multiline, input_text_with_hint, input_float, input_float2, input_float3, input_float4, input_int, input_int2, input_int3, input_int4, input_double, input_scalar, input_scalar_n"></div>

### Widgets: Color Editor/Picker

Tip: the `color_edit_*` functions have a little color square that can be left-clicked to open a picker, and right-clicked to open an option menu.

#### Functions
<div class="raw-html-insert" data-apirefs="color_edit3, color_edit4, color_picker3, color_picker4, color_button, set_color_edit_options"></div>

### Widgets: Trees

- `tree_node` functions return `True` when the node is open, in which case you need to also call `tree_pop()` when you are finished displaying the tree node contents.

#### Functions
<div class="raw-html-insert" data-apirefs="tree_node, tree_node_ex, tree_push, tree_pop, get_tree_node_to_label_spacing, collapsing_header, set_next_item_open"></div>

### Widgets: Selectables

- A selectable highlights when hovered, and can display another color when selected.
- Neighbors selectable extend their highlight bounds in order to leave no gap between them. This is so a series of selected `selectable` appear contiguous.

#### Functions
<div class="raw-html-insert" data-apirefs="selectable"></div>

### Multi-selection system for `selectable()`, `checkbox()`, `tree_node()` functions [BETA]
- This enables standard multi-selection/range-selection idioms (CTRL+Mouse/Keyboard, SHIFT+Mouse/Keyboard, etc.) in a way that also allows a clipper to be used.
- `SelectionUserData` is often used to store your item index within the current view (but may store something else).
- Read comments near `MultiSelectIO` for instructions/details and see 'Demo->Widgets->Selection State & Multi-Select' for demo.
- `tree_node()` is technically supported but... using this correctly is more complicated. You need some sort of linear/random access to your tree, which is suited to advanced tree setups already implementing filters and clipper. We will work on simplifying the current demo.
- `selection_size` and `items_count` parameters are optional and used by a few features. If they are costly for you to compute, you may avoid them.

<div class="raw-html-insert" data-apirefs="begin_multi_select, end_multi_select, set_next_item_selection_user_data, is_item_toggled_selection"></div>

### Widgets: List Boxes

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

#### Functions
<div class="raw-html-insert" data-apirefs="begin_list_box, end_list_box, list_box"></div>

### Widgets: Data Plotting

Consider using [ImPlot](https://github.com/epezent/implot) which is much better!  Slimgui includes ImPlot bindings, see [Slimgui ImPlot API reference](./apiref_implot.html) for details.

#### Functions
<div class="raw-html-insert" data-apirefs="plot_lines, plot_histogram"></div>

### Widgets: Value() Helpers

These are merely shortcuts to calling `text()` with a format string. Output single value in "name: value" format.

#### Functions
<div class="raw-html-insert" data-apirefs="value"></div>

### Widgets: Menus

- Use `begin_menu_bar()` on a window `WindowFlags.MENU_BAR` to append to its menu bar.
- Use `begin_main_menu_bar()` to create a menu bar at the top of the screen and append to it.
- Use `begin_menu()` to create a menu. You can call `begin_menu()` multiple times with the same identifier to append more items to it.
- Note that `menu_item()` keyboard shortcuts are displayed as a convenience but _not processed_ by Dear ImGui at the moment.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_menu_bar, end_menu_bar, begin_main_menu_bar, end_main_menu_bar, begin_menu, end_menu, menu_item"></div>

### Tooltips

- Tooltips are windows following the mouse. They do not take focus away.
- A tooltip window can contain items of any types.
- `set_tooltip()` is more or less a shortcut for the below idiom  (with a subtlety that it discards any previously submitted tooltip):
  ```
  if begin_tooltip():
      text(...)
      end_tooltip()
  ```

<div class="raw-html-insert" data-apirefs="begin_tooltip, end_tooltip, set_tooltip"></div>

### Tooltip helpers

Tooltip helpers for showing a tooltip when hovering an item:

- `begin_item_tooltip()` is a shortcut for the `if is_item_hovered(HoveredFlags.FOR_TOOLTIP) and begin_tooltip()` idiom.
- `set_item_tooltip()` is a shortcut for the `if is_item_hovered(HoveredFlags.FOR_TOOLTIP): set_tooltip(...)` idiom.
- Where `HoveredFlags.FOR_TOOLTIP` itself is a shortcut to use `Style.hover_flags_for_tooltip_mouse` or `Style.hover_flags_for_tooltip_nav` depending on the active input type. For mouse, it defaults to `HoveredFlags.STATIONARY | HoveredFlags.DELAY_SHORT`.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_item_tooltip, set_item_tooltip"></div>

### Popups, Modals

- Popups and modals block normal mouse hovering detection (and therefore most mouse interactions) behind them.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- Their visibility state (~bool) is held internally instead of being held by the programmer as we are used to with regular `begin_*()` calls.
- The 3 properties above are related: we need to retain popup visibility state in the library because popups may be closed at any time.
- You can bypass the hovering restriction by using `HoveredFlags.ALLOW_WHEN_BLOCKED_BY_POPUP` when calling `is_item_hovered()` or `is_window_hovered()`.
- IMPORTANT: Popup identifiers are relative to the current ID stack, so `open_popup()` and `begin_popup()` generally need to be at the same level of the stack. This sometimes leads to confusing mistakes. May rework this in the future.
- `begin_popup()`: query popup state, if open start appending into the window. Call `end_popup()` afterwards if returned true. `WindowFlags` are forwarded to the window.
- `begin_popup_modal()`: block every interaction behind the window, cannot be closed by user, add a dimming background, has a title bar.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_popup, begin_popup_modal, end_popup"></div>

### Popups: open/close functions

- `open_popup()`: set popup state to open. `PopupFlags` are available for opening options.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- `close_current_popup()`: use inside the `begin_popup()`/`end_popup()` scope to close manually.
- `close_current_popup()` is called by default by `selectable()`/`menu_item()` when activated.
- Use `PopupFlags.NO_OPEN_OVER_EXISTING_POPUP` to avoid opening a popup if there's already one at the same level. This is equivalent to e.g. testing for `not is_any_popup_open()` prior to `open_popup()`.
- Use `is_window_appearing()` after `begin_popup()` to tell if a window just opened.

#### Functions
<div class="raw-html-insert" data-apirefs="open_popup, open_popup_on_item_click, close_current_popup"></div>

### Popups: open+begin combined functions helpers

- Helpers to do `open_popup()` + `begin_popup()` where the open action is triggered by, e.g., hovering an item and right-clicking.
- They are convenient to easily create context menus, hence the name.
- IMPORTANT: Notice that `begin_popup_context_xxx()` takes `PopupFlags` just like `open_popup()` and unlike `begin_popup()`. For full consistency, we may add `WindowFlags` to the `begin_popup_context_xxx()` functions in the future.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_popup_context_item, begin_popup_context_window, begin_popup_context_void"></div>

### Popups: query functions

- `is_popup_open()`: return true if the popup is open at the current `begin_popup()` level of the popup stack.
- `is_popup_open()` with `PopupFlags.ANY_POPUP_ID`: return true if any popup is open at the current `begin_popup()` level of the popup stack.
- `is_popup_open()` with `PopupFlags.ANY_POPUP_ID` + `PopupFlags.ANY_POPUP_LEVEL`: return true if any popup is open.

#### Functions
<div class="raw-html-insert" data-apirefs="is_popup_open"></div>

### Tables

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


#### Functions
<div class="raw-html-insert" data-apirefs="begin_table, end_table, table_next_row, table_next_column, table_set_column_index"></div>

### Tables: Headers & Columns declaration

- Use `table_setup_column()` to specify label, resizing policy, default width/weight, id, various other flags, etc.
- Use `table_headers_row()` to create a header row and automatically submit a `table_header()` for each column.
  Headers are required to perform: reordering, sorting, and opening the context menu.
  The context menu can also be made available in columns body using `TableFlags.CONTEXT_MENU_IN_BODY`.
- You may manually submit headers using `table_next_row()` + `table_header()` calls, but this is only useful in
  some advanced use cases (e.g., adding custom widgets in header row).
- Use `table_setup_scroll_freeze()` to lock columns/rows so they stay visible when scrolled.

#### Functions
<div class="raw-html-insert" data-apirefs="table_setup_column, table_setup_scroll_freeze, table_header, table_headers_row, table_angled_headers_row"></div>

### Tables: Sorting & Miscellaneous functions

- Sorting: call `table_get_sort_specs()` to retrieve the latest sort specs for the table. Returns `None` when not sorting.
  When `sort_specs->SpecsDirty == True` you should sort your data. It will be `True` when sorting specs have changed since the last call, or the first time. Make sure to set `SpecsDirty = False` after sorting, else you may wastefully sort your data every frame!
- Functions args `column_n` treat the default value of -1 as the same as passing the current column index.

#### Functions
<div class="raw-html-insert" data-apirefs="table_get_sort_specs, table_get_column_count, table_get_column_index, table_get_row_index, table_get_column_name, table_get_column_flags, table_set_column_enabled, table_get_hovered_column, table_set_bg_color"></div>

### Legacy Columns API (prefer using Tables!)

- You can also use `same_line(pos_x)` to mimic simplified columns.

#### Functions
<div class="raw-html-insert" data-apirefs="columns, next_column, get_column_index, get_column_width, set_column_width, get_column_offset, set_column_offset, get_columns_count"></div>

### Tab Bars, Tabs

- Note: Tabs are automatically created by the docking system (when in 'docking' branch). Use this to create tab bars/tabs yourself.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_tab_bar, end_tab_bar, tab_item_button, set_tab_item_closed"></div>
<div class="raw-html-insert" data-apirefs="begin_tab_item">
When the `closable` argument is set to `True`, the created tab will display a close button.  The second bool of the return value will be `False` if the close button was pressed.  The intended usage is as follows:

```
tab_open = True  # open/closed state

visible, tab_open = imgui.begin_tab_item(..., closable=tab_open)
if visible:
    # render tab contents here..
```

</div>
<div class="raw-html-insert" data-apirefs="end_tab_item"></div>

### Drag and Drop

- On source items, call `begin_drag_drop_source()`, if it returns true also call `set_drag_drop_payload()` + `end_drag_drop_source()`.
- On target candidates, call `begin_drag_drop_target()`, if it returns true also call `accept_drag_drop_payload()` + `end_drag_drop_target()`.
- If you stop calling `begin_drag_drop_source()` the payload is preserved however it won't have a preview tooltip (we currently display a fallback "..." tooltip, see [#1725](https://github.com/ocornut/imgui/issues/1725)).
- An item can be both drag source and drop target.

<div class="raw-html-insert" data-apirefs="begin_drag_drop_source,set_drag_drop_payload,end_drag_drop_source,begin_drag_drop_target,accept_drag_drop_payload,end_drag_drop_target,get_drag_drop_payload"></div>

### Disabling [BETA API]

- Disable all user interactions and dim items visuals (applying `Style.disabled_alpha` over current colors).
- These can be nested but cannot be used to enable an already disabled section (a single `begin_disabled(True)` in the stack is enough to keep everything disabled).
- Tooltip windows, by exception, are opted out of disabling.
- `begin_disabled(False)`/`end_disabled()` essentially does nothing but is provided to facilitate the use of boolean expressions (as a micro-optimization: if you have tens of thousands of `begin_disabled(False)`/`end_disabled()` pairs, you might want to reformulate your code to avoid making those calls).

#### Functions
<div class="raw-html-insert" data-apirefs="begin_disabled, end_disabled"></div>

### Clipping
- Mouse hovering is affected by `push_clip_rect()` calls, unlike direct calls to `DrawList.push_clip_rect()` which are render only.

#### Functions
<div class="raw-html-insert" data-apirefs="push_clip_rect, pop_clip_rect"></div>

### Focus, Activation

#### Functions
<div class="raw-html-insert" data-apirefs="set_item_default_focus, set_keyboard_focus_here"></div>

### Keyboard/Gamepad Navigation

<div class="raw-html-insert" data-apirefs="set_nav_cursor_visible"></div>

### Overlapping mode

#### Functions
<div class="raw-html-insert" data-apirefs="set_next_item_allow_overlap"></div>

### Item/Widgets Utilities and Query Functions
- Most of the functions are referring to the previous Item that has been submitted.
- See Demo Window under "Widgets->Querying Status" for an interactive visualization of most of those functions.

#### Functions
<div class="raw-html-insert" data-apirefs="is_item_hovered, is_item_active, is_item_focused, is_item_clicked, is_item_visible, is_item_edited, is_item_activated, is_item_deactivated, is_item_deactivated_after_edit, is_item_toggled_open, is_any_item_hovered, is_any_item_active, is_any_item_focused, get_item_id, get_item_rect_min, get_item_rect_max, get_item_rect_size"></div>

### Viewports
- Currently represents the Platform Window created by the application which is hosting our Dear ImGui windows.
- In 'docking' branch with multi-viewport enabled, we extend this concept to have multiple active viewports.
- In the future we will extend this concept further to also represent Platform Monitor and support a "no main platform window" operation mode.

#### Functions
<div class="raw-html-insert" data-apirefs="get_main_viewport"></div>

### Background/Foreground Draw Lists

#### Functions
<div class="raw-html-insert" data-apirefs="get_background_draw_list, get_foreground_draw_list"></div>

### Miscellaneous Utilities

#### Functions
<div class="raw-html-insert" data-apirefs="is_rect_visible, get_time, get_frame_count, get_draw_list_shared_data, get_style_color_name, set_state_storage, get_state_storage"></div>

### Text Utilities

#### Functions
<div class="raw-html-insert" data-apirefs="calc_text_size"></div>

### Color Utilities

#### Functions
<div class="raw-html-insert" data-apirefs="color_convert_u32_to_float4, color_convert_float4_to_u32, color_convert_rgb_to_hsv, color_convert_hsv_to_rgb"></div>

### Inputs Utilities: Keyboard/Mouse/Gamepad

- The `Key` enum contains all possible keyboard, mouse, and gamepad inputs (e.g., `Key.KEY_A`, `Key.MOUSE_LEFT`, `Key.GAMEPAD_DPAD_UP`).

#### Functions
<div class="raw-html-insert" data-apirefs="is_key_down, is_key_pressed, is_key_released, is_key_chord_pressed, get_key_pressed_amount, get_key_name, set_next_frame_want_capture_keyboard"></div>

### Inputs Utilities: Shortcut Testing & Routing [BETA]

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

#### Functions
<div class="raw-html-insert" data-apirefs="shortcut, set_next_item_shortcut"></div>

### Inputs Utilities: Mouse

- To refer to a mouse button, you may use named enums in your code, e.g., `MouseButton.LEFT`, `MouseButton.RIGHT`.

#### Functions
<div class="raw-html-insert" data-apirefs="is_mouse_down, is_mouse_clicked, is_mouse_released, is_mouse_double_clicked, is_mouse_released_with_delay, get_mouse_clicked_count, is_mouse_hovering_rect, is_mouse_pos_valid, get_mouse_pos, get_mouse_pos_on_opening_current_popup, is_mouse_dragging, get_mouse_drag_delta, reset_mouse_drag_delta, get_mouse_cursor, set_mouse_cursor, set_next_frame_want_capture_mouse"></div>

## Enum Reference

<div class="raw-html-insert" data-apirefs="BackendFlags,ButtonFlags,ChildFlags,Col,ColorEditFlags,ComboFlags,Cond,ConfigFlags,Dir,DragDropFlags,DrawFlags,FocusedFlags,HoveredFlags,InputTextFlags,Key,MouseButton,MouseCursor,MouseSource,PopupFlags,SelectableFlags,SliderFlags,StyleVar,TabBarFlags,TabItemFlags,TableBgTarget,TableColumnFlags,TableFlags,TableRowFlags,TreeNodeFlags,WindowFlags"></div>
