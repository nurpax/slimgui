---
title: 'slimgui'
subtitle: 'Python bindings for Dear ImGui'
---

## Overview of slimgui

- TODO binding principles
  - tuple return values
  - imvec -> tuple

Source code: [github.com/nurpax/slimgui](https://github.com/nurpax/slimgui)

## Dear ImGui end-user API functions

- TODO explain how the below docs are mostly directly adapted from imgui.h

### Context creation and access

- Each context create its own ImFontAtlas by default. You may instance one yourself and pass it to CreateContext() to share a font atlas between contexts.

#### Functions
<div class="raw-html-insert" data-apirefs="create_context, destroy_context, get_current_context, set_current_context"></div>

### Main

#### Functions
<div class="raw-html-insert" data-apirefs="get_io, get_style, new_frame, end_frame, render, get_draw_data"></div>

### Demo, Debug, Information

#### Functions
<div class="raw-html-insert" data-apirefs="show_demo_window, show_metrics_window, show_debug_log_window, show_id_stack_tool_window, show_about_window, show_style_editor, show_style_selector, show_font_selector, show_user_guide, get_version"></div>

### Styles

#### Functions
<div class="raw-html-insert" data-apirefs="style_colors_dark, style_colors_light, style_colors_classic"></div>

### Windows

- `begin()` = push window to the stack and start appending to it. `end()` = pop window from the stack.
- Passing 'bool* p_open != NULL' shows a window-closing widget in the upper-right corner of the window,
  which clicking will set the boolean to false when clicked.
- You may append multiple times to the same window during the same frame by calling Begin()/End() pairs multiple times.
  Some information such as 'flags' or 'p_open' will only be considered by the first call to Begin().
- Begin() return false to indicate the window is collapsed or fully clipped, so you may early out and omit submitting
  anything to the window. Always call a matching End() for each Begin() call, regardless of its return value!
  [Important: due to legacy reason, Begin/End and BeginChild/EndChild are inconsistent with all other functions
   such as BeginMenu/EndMenu, BeginPopup/EndPopup, etc. where the EndXXX call should only be called if the corresponding
   BeginXXX function returned true. Begin and BeginChild are the only odd ones out. Will be fixed in a future update.]
- Note that the bottom of window stack always contains a window called "Debug".

#### Functions
<div class="raw-html-insert" data-apirefs="begin, end"></div>

### Child Windows

- Use child windows to begin into a self-contained independent scrolling/clipping regions within a host window. Child windows can embed their own child.
- Manual sizing (each axis can use a different setting e.g. ImVec2(0.0f, 400.0f)):
    == 0.0f: use remaining parent window size for this axis.
     > 0.0f: use specified size for this axis.
     < 0.0f: right/bottom-align to specified distance from available content boundaries.
- Specifying ImGuiChildFlags_AutoResizeX or ImGuiChildFlags_AutoResizeY makes the sizing automatic based on child contents.
  Combining both ImGuiChildFlags_AutoResizeX _and_ ImGuiChildFlags_AutoResizeY defeats purpose of a scrolling region and is NOT recommended.
- BeginChild() returns false to indicate the window is collapsed or fully clipped, so you may early out and omit submitting
  anything to the window. Always call a matching EndChild() for each BeginChild() call, regardless of its return value.
  [Important: due to legacy reason, Begin/End and BeginChild/EndChild are inconsistent with all other functions
  such as BeginMenu/EndMenu, BeginPopup/EndPopup, etc. where the EndXXX call should only be called if the corresponding BeginXXX function returned true. Begin and BeginChild are the only odd ones out. Will be fixed in a future update.]

#### Functions
<div class="raw-html-insert" data-apirefs="begin_child, end_child"></div>

### Window Utilities

- 'current window' = the window we are appending into while inside a Begin()/End() block. 'next window' = next
  window we will Begin() into.

#### Functions
<div class="raw-html-insert" data-apirefs="is_window_appearing, is_window_collapsed, is_window_focused, is_window_hovered, get_window_draw_list, get_window_pos, get_window_size, get_window_width, get_window_height"></div>

### Window Manipulation

- Prefer using SetNextXXX functions (before Begin) rather than SetXXX functions (after Begin).

#### Functions
<div class="raw-html-insert" data-apirefs="set_next_window_pos, set_next_window_size, set_next_window_size_constraints, set_next_window_content_size, set_next_window_collapsed, set_next_window_focus, set_next_window_scroll, set_next_window_bg_alpha, set_window_pos, set_window_size, set_window_collapsed, set_window_focus, set_window_font_scale, set_window_pos, set_window_size, set_window_collapsed, set_window_focus"></div>

### Content Region

- Retrieve available space from a given point. GetContentRegionAvail() is frequently useful.

#### Functions
<div class="raw-html-insert" data-apirefs="get_content_region_avail, get_content_region_max, get_window_content_region_min, get_window_content_region_max"></div>

### Windows Scrolling

- Any change of Scroll will be applied at the beginning of next frame in the first call to Begin().
- You may instead use SetNextWindowScroll() prior to calling Begin() to avoid this delay, as an alternative to using SetScrollX()/SetScrollY().

#### Functions
<div class="raw-html-insert" data-apirefs="set_next_window_scroll, get_scroll_x, get_scroll_y, set_scroll_x, set_scroll_y, get_scroll_max_x, get_scroll_max_y, set_scroll_here_x, set_scroll_here_y, set_scroll_from_pos_x, set_scroll_from_pos_y"></div>

### Parameter stacks (shared)

#### Functions
<div class="raw-html-insert" data-apirefs="push_font, pop_font, push_style_color, pop_style_color, push_style_var, pop_style_var, push_tab_stop, pop_tab_stop, push_button_repeat, pop_button_repeat"></div>

### Parameter stacks (current window)

#### Functions
<div class="raw-html-insert" data-apirefs="push_item_width, pop_item_width, set_next_item_width, calc_item_width, push_text_wrap_pos, pop_text_wrap_pos"></div>


### Style read access

- Use the ShowStyleEditor() function to interactively see/edit the colors.

#### Functions
<div class="raw-html-insert" data-apirefs="get_font, get_font_size, get_font_tex_uv_white_pixel, get_color_u32, get_style_color_vec4"></div>

### Layout cursor positioning

- By "cursor" we mean the current output position.
- The typical widget behavior is to output themselves at the current cursor position, then move the cursor one line down.
- You can call SameLine() between widgets to undo the last carriage return and output at the right of the preceding widget.
- Attention! We currently have inconsistencies between window-local and absolute positions we will aim to fix with future API:
    - Absolute coordinate:        GetCursorScreenPos(), SetCursorScreenPos(), all ImDrawList:: functions. -> this is the preferred way forward.
    - Window-local coordinates:   SameLine(), GetCursorPos(), SetCursorPos(), GetCursorStartPos(), GetContentRegionMax(), GetWindowContentRegion*(), PushTextWrapPos()
- GetCursorScreenPos() = GetCursorPos() + GetWindowPos(). GetWindowPos() is almost only ever useful to convert from window-local to absolute coordinates.

#### Functions
<div class="raw-html-insert" data-apirefs="get_cursor_screen_pos, set_cursor_screen_pos, get_cursor_pos, get_cursor_pos_x, get_cursor_pos_y, set_cursor_pos, set_cursor_pos_x, set_cursor_pos_y, get_cursor_start_pos"></div>

### Other layout functions

#### Functions
<div class="raw-html-insert" data-apirefs="separator, same_line, new_line, spacing, dummy, indent, unindent, begin_group, end_group, align_text_to_frame_padding, get_text_line_height, get_text_line_height_with_spacing, get_frame_height, get_frame_height_with_spacing"></div>

### ID stack/scopes

Read the FAQ (docs/FAQ.md or http://dearimgui.com/faq) for more details about how ID are handled in dear imgui.

Those questions are answered and impacted by understanding of the ID stack system:

  - "Q: Why is my widget not reacting when I click on it?"
  - "Q: How can I have widgets with an empty label?"
  - "Q: How can I have multiple widgets with the same label?"

Short version: ID are hashes of the entire ID stack. If you are creating widgets in a loop you most likely
want to push a unique identifier (e.g. object pointer, loop index) to uniquely differentiate them.

You can also use the "Label##foobar" syntax within widget label to distinguish them from each others.

In this header file we use the "label"/"name" terminology to denote a string that will be displayed + used as an ID,
whereas "str_id" denote a string that is only used as an ID and not normally displayed.

#### Functions
<div class="raw-html-insert" data-apirefs="push_id, pop_id, get_id"></div>

### Widgets: Text

#### Functions
<div class="raw-html-insert" data-apirefs="text_unformatted, text, text_colored, text_disabled, text_wrapped, label_text, bullet_text, separator_text"></div>

### Widgets: Main

- Most widgets return true when the value has been changed or when pressed/selected
- You may also use one of the many IsItemXXX functions (e.g. IsItemActive, IsItemHovered, etc.) to query widget state.

#### Functions
<div class="raw-html-insert" data-apirefs="button, small_button, invisible_button, arrow_button, checkbox, checkbox_flags, radio_button, progress_bar, bullet"></div>

### Widgets: Images

- Read about ImTextureID here: https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples
- 'uv0' and 'uv1' are texture coordinates. Read about them from the same link above.
- Note that Image() may add +2.0f to provided size if a border is visible, ImageButton() adds style.FramePadding*2.0f to provided size.

#### Functions
<div class="raw-html-insert" data-apirefs="image, image_button"></div>

### Widgets: Combo Box (Dropdown)

- The BeginCombo()/EndCombo() api allows you to manage your contents and selection state however you want it, by creating e.g. Selectable() items.
- The old Combo() api are helpers over BeginCombo()/EndCombo() which are kept available for convenience purpose. This is analogous to how ListBox are created.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_combo, end_combo, combo"></div>

### Widgets: Drag Sliders

- CTRL+Click on any drag box to turn them into an input box. Manually input values aren't clamped by default and can go off-bounds. Use ImGuiSliderFlags_AlwaysClamp to always clamp.
- For all the Float2/Float3/Float4/Int2/Int3/Int4 versions of every function, note that a 'float v[X]' function argument is the same as 'float* v',
  the array syntax is just a way to document the number of elements that are expected to be accessible. You can pass address of your first element out of a contiguous set, e.g. &myvector.x
- Adjust format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision e.g. "%.3f" -> 1.234; "%5.2f secs" -> 01.23 secs; "Biscuit: %.0f" -> Biscuit: 1; etc.
- Format string may also be set to NULL or use the default format ("%f" or "%d").
- Speed are per-pixel of mouse movement (v_speed=0.2f: mouse needs to move by 5 pixels to increase value by 1). For gamepad/keyboard navigation, minimum speed is Max(v_speed, minimum_step_at_given_precision).
- Use v_min < v_max to clamp edits to given limits. Note that CTRL+Click manual input can override those limits if ImGuiSliderFlags_AlwaysClamp is not used.
- Use v_max = FLT_MAX / INT_MAX etc to avoid clamping to a maximum, same with v_min = -FLT_MAX / INT_MIN to avoid clamping to a minimum.
- We use the same sets of flags for DragXXX() and SliderXXX() functions as the features are the same and it makes it easier to swap them.

#### Functions
<div class="raw-html-insert" data-apirefs="drag_float, drag_float2, drag_float3, drag_float4, drag_float_range2, drag_int, drag_int2, drag_int3, drag_int4, drag_int_range2, drag_scalar, drag_scalar_n"></div>

### Widgets: Regular Sliders

- CTRL+Click on any slider to turn them into an input box. Manually input values aren't clamped by default and can go off-bounds. Use ImGuiSliderFlags_AlwaysClamp to always clamp.
- Adjust format string to decorate the value with a prefix, a suffix, or adapt the editing and display precision e.g. "%.3f" -> 1.234; "%5.2f secs" -> 01.23 secs; "Biscuit: %.0f" -> Biscuit: 1; etc.
- Format string may also be set to NULL or use the default format ("%f" or "%d").

#### Functions
<div class="raw-html-insert" data-apirefs="slider_float, slider_float2, slider_float3, slider_float4, slider_angle, slider_int, slider_int2, slider_int3, slider_int4, slider_scalar, slider_scalar_n, vslider_float, vslider_int, vslider_scalar"></div>

### Widgets: Input with Keyboard

- If you want to use InputText() with std::string or any custom dynamic string type, see misc/cpp/imgui_stdlib.h and comments in imgui_demo.cpp.
- Most of the ImGuiInputTextFlags flags are only useful for InputText() and not for InputFloatX, InputIntX, InputDouble etc.

#### Functions
<div class="raw-html-insert" data-apirefs="input_text, input_text_multiline, input_text_with_hint, input_float, input_float2, input_float3, input_float4, input_int, input_int2, input_int3, input_int4, input_double, input_scalar, input_scalar_n"></div>

### Widgets: Color Editor/Picker

- The ColorEdit* functions have a little color square that can be left-clicked to open a picker, and right-clicked to open an option menu.

#### Functions
<div class="raw-html-insert" data-apirefs="color_edit3, color_edit4, color_picker3, color_picker4, color_button, set_color_edit_options"></div>

### Widgets: Trees

- TreeNode functions return true when the node is open, in which case you need to also call TreePop() when you are finished displaying the tree node contents.

#### Functions
<div class="raw-html-insert" data-apirefs="tree_node, tree_node_ex, tree_push, tree_pop, get_tree_node_to_label_spacing, collapsing_header, set_next_item_open"></div>

### Widgets: Selectables

- A selectable highlights when hovered, and can display another color when selected.
- Neighbors selectable extend their highlight bounds in order to leave no gap between them. This is so a series of selected Selectable appear contiguous.

#### Functions
<div class="raw-html-insert" data-apirefs="selectable"></div>

### Widgets: List Boxes

- This is essentially a thin wrapper to using BeginChild/EndChild with the ImGuiChildFlags_FrameStyle flag for stylistic changes + displaying a label.
- You can submit contents and manage your selection state however you want it, by creating e.g. Selectable() or any other items.
- The simplified/old ListBox() api are helpers over BeginListBox()/EndListBox() which are kept available for convenience purpose. This is analogous to how Combos are created.
- Choose frame width: size.x > 0.0f: custom / size.x < 0.0f or -FLT_MIN: right-align / size.x = 0.0f (default): use current ItemWidth
- Choose frame height: size.y > 0.0f: custom / size.y < 0.0f or -FLT_MIN: bottom-align / size.y = 0.0f (default): arbitrary default height which can fit ~7 items

#### Functions
<div class="raw-html-insert" data-apirefs="begin_list_box, end_list_box, list_box"></div>

### Widgets: Data Plotting

- Consider using ImPlot (https://github.com/epezent/implot) which is much better!

#### Functions
<div class="raw-html-insert" data-apirefs="plot_lines, plot_histogram"></div>

### Widgets: Value() Helpers

- Those are merely shortcut to calling Text() with a format string. Output single value in "name: value" format (tip: freely declare more in your code to handle your types. you can add functions to the ImGui namespace)

#### Functions
<div class="raw-html-insert" data-apirefs="value"></div>

### Widgets: Menus

- Use BeginMenuBar() on a window ImGuiWindowFlags_MenuBar to append to its menu bar.
- Use BeginMainMenuBar() to create a menu bar at the top of the screen and append to it.
- Use BeginMenu() to create a menu. You can call BeginMenu() multiple times with the same identifier to append more items to it.
- Note that MenuItem() keyboard shortcuts are displayed as a convenience but _not processed_ by Dear ImGui at the moment.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_menu_bar, end_menu_bar, begin_main_menu_bar, end_main_menu_bar, begin_menu, end_menu, menu_item"></div>

### Tooltips

- Tooltips are windows following the mouse. They do not take focus away.
- A tooltip window can contain items of any types. SetTooltip() is a shortcut for the 'if (BeginTooltip()) { Text(...); EndTooltip(); }' idiom.

Tooltip helpers for showing a tooltip when hovering an item:

- BeginItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip) && BeginTooltip())' idiom.
- SetItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip)) { SetTooltip(...); }' idiom.
- Where 'ImGuiHoveredFlags_ForTooltip' itself is a shortcut to use 'style.HoverFlagsForTooltipMouse' or 'style.HoverFlagsForTooltipNav' depending on active input type. For mouse it defaults to 'ImGuiHoveredFlags_Stationary | ImGuiHoveredFlags_DelayShort'.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_item_tooltip, set_item_tooltip"></div>

### Popups, Modals

- They block normal mouse hovering detection (and therefore most mouse interactions) behind them.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- Their visibility state (~bool) is held internally instead of being held by the programmer as we are used to with regular Begin*() calls.
- The 3 properties above are related: we need to retain popup visibility state in the library because popups may be closed at any time.
- You can bypass the hovering restriction by using ImGuiHoveredFlags_AllowWhenBlockedByPopup when calling IsItemHovered() or IsWindowHovered().
- IMPORTANT: Popup identifiers are relative to the current ID stack, so OpenPopup and BeginPopup generally need to be at the same level of the stack. This is sometimes leading to confusing mistakes. May rework this in the future.
- BeginPopup(): query popup state, if open start appending into the window. Call EndPopup() afterwards if returned true. ImGuiWindowFlags are forwarded to the window.
- BeginPopupModal(): block every interaction behind the window, cannot be closed by user, add a dimming background, has a title bar.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_popup, begin_popup_modal, end_popup"></div>

### Popups: open/close functions

- OpenPopup(): set popup state to open. ImGuiPopupFlags are available for opening options.
- If not modal: they can be closed by clicking anywhere outside them, or by pressing ESCAPE.
- CloseCurrentPopup(): use inside the BeginPopup()/EndPopup() scope to close manually.
- CloseCurrentPopup() is called by default by Selectable()/MenuItem() when activated (FIXME: need some options).
- Use ImGuiPopupFlags_NoOpenOverExistingPopup to avoid opening a popup if there's already one at the same level. This is equivalent to e.g. testing for !IsAnyPopupOpen() prior to OpenPopup().
- Use IsWindowAppearing() after BeginPopup() to tell if a window just opened.
- IMPORTANT: Notice that for OpenPopupOnItemClick() we exceptionally default flags to 1 (== ImGuiPopupFlags_MouseButtonRight) for backward compatibility with older API taking 'int mouse_button = 1' parameter.

#### Functions
<div class="raw-html-insert" data-apirefs="open_popup, open_popup_on_item_click, close_current_popup"></div>

### Popups: open+begin combined functions helpers

- Helpers to do OpenPopup+BeginPopup where the Open action is triggered by e.g. hovering an item and right-clicking.
- They are convenient to easily create context menus, hence the name.
- IMPORTANT: Notice that BeginPopupContextXXX takes ImGuiPopupFlags just like OpenPopup() and unlike BeginPopup(). For full consistency, we may add ImGuiWindowFlags to the BeginPopupContextXXX functions in the future.
- IMPORTANT: Notice that we exceptionally default their flags to 1 (== ImGuiPopupFlags_MouseButtonRight) for backward compatibility with older API taking 'int mouse_button = 1' parameter, so if you add other flags remember to re-add the ImGuiPopupFlags_MouseButtonRight.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_popup_context_item, begin_popup_context_window, begin_popup_context_void"></div>

### Popups: query functions

- IsPopupOpen(): return true if the popup is open at the current BeginPopup() level of the popup stack.
- IsPopupOpen() with ImGuiPopupFlags_AnyPopupId: return true if any popup is open at the current BeginPopup() level of the popup stack.
- IsPopupOpen() with ImGuiPopupFlags_AnyPopupId + ImGuiPopupFlags_AnyPopupLevel: return true if any popup is open.

#### Functions
<div class="raw-html-insert" data-apirefs="is_popup_open"></div>

### Tables

- Full-featured replacement for old Columns API.
- See Demo->Tables for demo code. See top of imgui_tables.cpp for general commentary.
- See ImGuiTableFlags_ and ImGuiTableColumnFlags_ enums for a description of available flags.
- The typical call flow is:
  1. Call BeginTable(), early out if returning false.
  2. Optionally call TableSetupColumn() to submit column name/flags/defaults.
  3. Optionally call TableSetupScrollFreeze() to request scroll freezing of columns/rows.
  4. Optionally call TableHeadersRow() to submit a header row. Names are pulled from TableSetupColumn() data.
  5. Populate contents:
     - In most situations you can use TableNextRow() + TableSetColumnIndex(N) to start appending into a column.
     - If you are using tables as a sort of grid, where every column is holding the same type of contents, you may prefer using TableNextColumn() instead of TableNextRow() + TableSetColumnIndex(). TableNextColumn() will automatically wrap-around into the next row if needed.
     - IMPORTANT: Comparatively to the old Columns() API, we need to call TableNextColumn() for the first column!
     - Summary of possible call flow:
        - TableNextRow() -> TableSetColumnIndex(0) -> Text("Hello 0") -> TableSetColumnIndex(1) -> Text("Hello 1")  // OK
        - TableNextRow() -> TableNextColumn()      -> Text("Hello 0") -> TableNextColumn()      -> Text("Hello 1")  // OK
        -                   TableNextColumn()      -> Text("Hello 0") -> TableNextColumn()      -> Text("Hello 1")  // OK: TableNextColumn() automatically gets to next row!
        - TableNextRow()                           -> Text("Hello 0")                                               // Not OK! Missing TableSetColumnIndex() or TableNextColumn()! Text will not appear!
  6. Call EndTable()

#### Functions
<div class="raw-html-insert" data-apirefs="begin_table, end_table, table_next_row, table_next_column, table_set_column_index"></div>

### Tables: Headers & Columns declaration

- Use TableSetupColumn() to specify label, resizing policy, default width/weight, id, various other flags etc.
- Use TableHeadersRow() to create a header row and automatically submit a TableHeader() for each column. Headers are required to perform: reordering, sorting, and opening the context menu. The context menu can also be made available in columns body using ImGuiTableFlags_ContextMenuInBody.
- You may manually submit headers using TableNextRow() + TableHeader() calls, but this is only useful in some advanced use cases (e.g. adding custom widgets in header row).
- Use TableSetupScrollFreeze() to lock columns/rows so they stay visible when scrolled.

#### Functions
<div class="raw-html-insert" data-apirefs="table_setup_column, table_setup_scroll_freeze, table_header, table_headers_row, table_angled_headers_row"></div>

### Tables: Sorting & Miscellaneous functions

- Sorting: call TableGetSortSpecs() to retrieve latest sort specs for the table. NULL when not sorting. When 'sort_specs->SpecsDirty == true' you should sort your data. It will be true when sorting specs have changed since last call, or the first time. Make sure to set 'SpecsDirty = false' after sorting, else you may wastefully sort your data every frame!
- Functions args 'int column_n' treat the default value of -1 as the same as passing the current column index.

#### Functions
<div class="raw-html-insert" data-apirefs="table_get_sort_specs, table_get_column_count, table_get_column_index, table_get_row_index, table_get_column_name, table_get_column_flags, table_set_column_enabled, table_set_bg_color"></div>

### Legacy Columns API (prefer using Tables!)

- You can also use SameLine(pos_x) to mimic simplified columns.

#### Functions
<div class="raw-html-insert" data-apirefs="columns, next_column, get_column_index, get_column_width, set_column_width, get_column_offset, set_column_offset, get_columns_count"></div>

### Tab Bars, Tabs

- Note: Tabs are automatically created by the docking system (when in 'docking' branch). Use this to create tab bars/tabs yourself.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_tab_bar, end_tab_bar, begin_tab_item, end_tab_item, tab_item_button, set_tab_item_closed"></div>

### Disabling [BETA API]
- Disable all user interactions and dim items visuals (applying style.DisabledAlpha over current colors)
- Those can be nested but it cannot be used to enable an already disabled section (a single BeginDisabled(true) in the stack is enough to keep everything disabled)
- BeginDisabled(false) essentially does nothing useful but is provided to facilitate use of boolean expressions. If you can avoid calling BeginDisabled(False)/EndDisabled() best to avoid it.

#### Functions
<div class="raw-html-insert" data-apirefs="begin_disabled, end_disabled"></div>

### Clipping
- Mouse hovering is affected by ImGui::PushClipRect() calls, unlike direct calls to ImDrawList::PushClipRect() which are render only.

#### Functions
<div class="raw-html-insert" data-apirefs="push_clip_rect, pop_clip_rect"></div>

### Focus, Activation
- Prefer using "SetItemDefaultFocus()" over "if (IsWindowAppearing()) SetScrollHereY()" when applicable to signify "this is the default item"

#### Functions
<div class="raw-html-insert" data-apirefs="set_item_default_focus, set_keyboard_focus_here"></div>

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
- The ImGuiKey enum contains all possible keyboard, mouse and gamepad inputs (e.g. ImGuiKey_A, ImGuiKey_MouseLeft, ImGuiKey_GamepadDpadUp...).

#### Functions
<div class="raw-html-insert" data-apirefs="is_key_down, is_key_pressed, is_key_released, is_key_chord_pressed, get_key_pressed_amount, get_key_name, set_next_frame_want_capture_keyboard"></div>

### Inputs Utilities: Mouse specific

- To refer to a mouse button, you may use named enums in your code e.g. ImGuiMouseButton_Left, ImGuiMouseButton_Right.
- You can also use regular integer: it is forever guaranteed that 0=Left, 1=Right, 2=Middle.
- Dragging operations are only reported after mouse has moved a certain distance away from the initial clicking position (see 'lock_threshold' and 'io.MouseDraggingThreshold')

#### Functions
<div class="raw-html-insert" data-apirefs="is_mouse_down, is_mouse_clicked, is_mouse_released, is_mouse_double_clicked, get_mouse_clicked_count, is_mouse_hovering_rect, is_mouse_pos_valid, is_any_mouse_down, get_mouse_pos, get_mouse_pos_on_opening_current_popup, is_mouse_dragging, get_mouse_drag_delta, reset_mouse_drag_delta, get_mouse_cursor, set_mouse_cursor, set_next_frame_want_capture_mouse"></div>

### Clipboard Utilities
- Also see the LogToClipboard() function to capture GUI into clipboard, or easily output text data to the clipboard.

#### Functions
<div class="raw-html-insert" data-apirefs="get_clipboard_text, set_clipboard_text"></div>
