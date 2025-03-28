nb::enum_<ImDrawFlags_>(m, "DrawFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImDrawFlags_None)
    .value("CLOSED", ImDrawFlags_Closed,
           "PathStroke(), AddPolyline(): specify that shape should be closed "
           "(Important: this is always == 1 for legacy reason)")
    .value("ROUND_CORNERS_TOP_LEFT", ImDrawFlags_RoundCornersTopLeft,
           "AddRect(), AddRectFilled(), PathRect(): enable rounding top-left "
           "corner only (when rounding > 0.0f, we default to all corners). Was "
           "0x01.")
    .value("ROUND_CORNERS_TOP_RIGHT", ImDrawFlags_RoundCornersTopRight,
           "AddRect(), AddRectFilled(), PathRect(): enable rounding top-right "
           "corner only (when rounding > 0.0f, we default to all corners). Was "
           "0x02.")
    .value("ROUND_CORNERS_BOTTOM_LEFT", ImDrawFlags_RoundCornersBottomLeft,
           "AddRect(), AddRectFilled(), PathRect(): enable rounding "
           "bottom-left corner only (when rounding > 0.0f, we default to all "
           "corners). Was 0x04.")
    .value("ROUND_CORNERS_BOTTOM_RIGHT", ImDrawFlags_RoundCornersBottomRight,
           "AddRect(), AddRectFilled(), PathRect(): enable rounding "
           "bottom-right corner only (when rounding > 0.0f, we default to all "
           "corners). Wax 0x08.")
    .value("ROUND_CORNERS_NONE", ImDrawFlags_RoundCornersNone,
           "AddRect(), AddRectFilled(), PathRect(): disable rounding on all "
           "corners (when rounding > 0.0f). This is NOT zero, NOT an implicit "
           "flag!")
    .value("ROUND_CORNERS_TOP", ImDrawFlags_RoundCornersTop)
    .value("ROUND_CORNERS_BOTTOM", ImDrawFlags_RoundCornersBottom)
    .value("ROUND_CORNERS_LEFT", ImDrawFlags_RoundCornersLeft)
    .value("ROUND_CORNERS_RIGHT", ImDrawFlags_RoundCornersRight)
    .value("ROUND_CORNERS_ALL", ImDrawFlags_RoundCornersAll)
    .value("ROUND_CORNERS_DEFAULT_", ImDrawFlags_RoundCornersDefault_,
           "Default to ALL corners if none of the _RoundCornersXX flags are "
           "specified.")
    .value("ROUND_CORNERS_MASK_", ImDrawFlags_RoundCornersMask_);
nb::enum_<ImGuiInputTextFlags_>(m, "InputTextFlags", nb::is_flag(),
                                nb::is_arithmetic())
    .value("NONE", ImGuiInputTextFlags_None)
    .value("CHARS_DECIMAL", ImGuiInputTextFlags_CharsDecimal,
           "Allow 0123456789.+-*/")
    .value("CHARS_HEXADECIMAL", ImGuiInputTextFlags_CharsHexadecimal,
           "Allow 0123456789ABCDEFabcdef")
    .value("CHARS_SCIENTIFIC", ImGuiInputTextFlags_CharsScientific,
           "Allow 0123456789.+-*/eE (Scientific notation input)")
    .value("CHARS_UPPERCASE", ImGuiInputTextFlags_CharsUppercase,
           "Turn a..z into A..Z")
    .value("CHARS_NO_BLANK", ImGuiInputTextFlags_CharsNoBlank,
           "Filter out spaces, tabs")
    .value("ALLOW_TAB_INPUT", ImGuiInputTextFlags_AllowTabInput,
           "Pressing TAB input a '\t' character into the text field")
    .value("ENTER_RETURNS_TRUE", ImGuiInputTextFlags_EnterReturnsTrue,
           "Return 'true' when Enter is pressed (as opposed to every time the "
           "value was modified). Consider using "
           "`is_item_deactivated_after_edit()` instead!")
    .value("ESCAPE_CLEARS_ALL", ImGuiInputTextFlags_EscapeClearsAll,
           "Escape key clears content if not empty, and deactivate otherwise "
           "(contrast to default behavior of Escape to revert)")
    .value(
        "CTRL_ENTER_FOR_NEW_LINE", ImGuiInputTextFlags_CtrlEnterForNewLine,
        "In multi-line mode, validate with Enter, add new line with Ctrl+Enter "
        "(default is opposite: validate with Ctrl+Enter, add line with Enter).")
    .value("READ_ONLY", ImGuiInputTextFlags_ReadOnly, "Read-only mode")
    .value("PASSWORD", ImGuiInputTextFlags_Password,
           "Password mode, display all characters as '*', disable copy")
    .value("ALWAYS_OVERWRITE", ImGuiInputTextFlags_AlwaysOverwrite,
           "Overwrite mode")
    .value("AUTO_SELECT_ALL", ImGuiInputTextFlags_AutoSelectAll,
           "Select entire text when first taking mouse focus")
    .value("PARSE_EMPTY_REF_VAL", ImGuiInputTextFlags_ParseEmptyRefVal,
           "`input_float()`, `input_int()`, `input_scalar()` etc. only: parse "
           "empty string as zero value.")
    .value("DISPLAY_EMPTY_REF_VAL", ImGuiInputTextFlags_DisplayEmptyRefVal,
           "`input_float()`, `input_int()`, `input_scalar()` etc. only: when "
           "value is zero, do not display it. Generally used with "
           "`InputTextFlags.PARSE_EMPTY_REF_VAL`.")
    .value("NO_HORIZONTAL_SCROLL", ImGuiInputTextFlags_NoHorizontalScroll,
           "Disable following the cursor horizontally")
    .value("NO_UNDO_REDO", ImGuiInputTextFlags_NoUndoRedo,
           "Disable undo/redo. Note that input text owns the text data while "
           "active, if you want to provide your own undo/redo stack you need "
           "e.g. to call `clear_active_id()`.")
    .value("ELIDE_LEFT", ImGuiInputTextFlags_ElideLeft,
           "When text doesn't fit, elide left side to ensure right side stays "
           "visible. Useful for path/filenames. Single-line only!")
    .value("CALLBACK_COMPLETION", ImGuiInputTextFlags_CallbackCompletion,
           "Callback on pressing TAB (for completion handling)")
    .value("CALLBACK_HISTORY", ImGuiInputTextFlags_CallbackHistory,
           "Callback on pressing Up/Down arrows (for history handling)")
    .value("CALLBACK_ALWAYS", ImGuiInputTextFlags_CallbackAlways,
           "Callback on each iteration. User code may query cursor position, "
           "modify text buffer.")
    .value("CALLBACK_CHAR_FILTER", ImGuiInputTextFlags_CallbackCharFilter,
           "Callback on character inputs to replace or discard them. Modify "
           "'EventChar' to replace or discard, or return 1 in callback to "
           "discard.")
    .value(
        "CALLBACK_RESIZE", ImGuiInputTextFlags_CallbackResize,
        "Callback on buffer capacity changes request (beyond 'buf_size' "
        "parameter value), allowing the string to grow. Notify when the string "
        "wants to be resized (for string types which hold a cache of their "
        "Size). You will be provided a new BufSize in the callback and NEED to "
        "honor it. (see misc/cpp/imgui_stdlib.h for an example of using this)")
    .value(
        "CALLBACK_EDIT", ImGuiInputTextFlags_CallbackEdit,
        "Callback on any edit. Note that `input_text()` already returns true "
        "on edit + you can always use `is_item_edited()`. The callback is "
        "useful to manipulate the underlying buffer while focus is active.");
nb::enum_<ImGuiButtonFlags_>(m, "ButtonFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImGuiButtonFlags_None)
    .value("MOUSE_BUTTON_LEFT", ImGuiButtonFlags_MouseButtonLeft,
           "React on left mouse button (default)")
    .value("MOUSE_BUTTON_RIGHT", ImGuiButtonFlags_MouseButtonRight,
           "React on right mouse button")
    .value("MOUSE_BUTTON_MIDDLE", ImGuiButtonFlags_MouseButtonMiddle,
           "React on center mouse button")
    .value("MOUSE_BUTTON_MASK_", ImGuiButtonFlags_MouseButtonMask_,
           "[Internal]")
    .value("ENABLE_NAV", ImGuiButtonFlags_EnableNav,
           "`invisible_button()`: do not disable navigation/tabbing. Otherwise "
           "disabled by default.");
nb::enum_<ImGuiChildFlags_>(m, "ChildFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImGuiChildFlags_None)
    .value("BORDERS", ImGuiChildFlags_Borders,
           "Show an outer border and enable WindowPadding. (IMPORTANT: this is "
           "always == 1 == true for legacy reason)")
    .value("ALWAYS_USE_WINDOW_PADDING", ImGuiChildFlags_AlwaysUseWindowPadding,
           "Pad with style.WindowPadding even if no border are drawn (no "
           "padding by default for non-bordered child windows because it makes "
           "more sense)")
    .value(
        "RESIZE_X", ImGuiChildFlags_ResizeX,
        "Allow resize from right border (layout direction). Enable .ini saving "
        "(unless `WindowFlags.NO_SAVED_SETTINGS` passed to window flags)")
    .value("RESIZE_Y", ImGuiChildFlags_ResizeY,
           "Allow resize from bottom border (layout direction). ")
    .value("AUTO_RESIZE_X", ImGuiChildFlags_AutoResizeX,
           "Enable auto-resizing width. Read IMPORTANT: Size measurement\" "
           "details above.")
    .value("AUTO_RESIZE_Y", ImGuiChildFlags_AutoResizeY,
           "Enable auto-resizing height. Read IMPORTANT: Size measurement\" "
           "details above.")
    .value("ALWAYS_AUTO_RESIZE", ImGuiChildFlags_AlwaysAutoResize,
           "Combined with AutoResizeX/AutoResizeY. Always measure size even "
           "when child is hidden, always return true, always disable clipping "
           "optimization! NOT RECOMMENDED.")
    .value("FRAME_STYLE", ImGuiChildFlags_FrameStyle,
           "Style the child window like a framed item: use FrameBg, "
           "FrameRounding, FrameBorderSize, FramePadding instead of ChildBg, "
           "ChildRounding, ChildBorderSize, WindowPadding.")
    .value(
        "NAV_FLATTENED", ImGuiChildFlags_NavFlattened,
        "[BETA] Share focus scope, allow keyboard/gamepad navigation to cross "
        "over parent border to this child or between sibling child windows.");
nb::enum_<ImGuiDragDropFlags_>(m, "DragDropFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImGuiDragDropFlags_None)
    .value("SOURCE_NO_PREVIEW_TOOLTIP",
           ImGuiDragDropFlags_SourceNoPreviewTooltip,
           "Disable preview tooltip. By default, a successful call to "
           "`begin_drag_drop_source` opens a tooltip so you can display a "
           "preview or description of the source contents. This flag disables "
           "this behavior.")
    .value("SOURCE_NO_DISABLE_HOVER", ImGuiDragDropFlags_SourceNoDisableHover,
           "By default, when dragging we clear data so that "
           "`is_item_hovered()` will return false, to avoid subsequent user "
           "code submitting tooltips. This flag disables this behavior so you "
           "can still call `is_item_hovered()` on the source item.")
    .value("SOURCE_NO_HOLD_TO_OPEN_OTHERS",
           ImGuiDragDropFlags_SourceNoHoldToOpenOthers,
           "Disable the behavior that allows to open tree nodes and collapsing "
           "header by holding over them while dragging a source item.")
    .value(
        "SOURCE_ALLOW_NULL_ID", ImGuiDragDropFlags_SourceAllowNullID,
        "Allow items such as `text()`, `image()` that have no unique "
        "identifier to be used as drag source, by manufacturing a temporary "
        "identifier based on their window-relative position. This is extremely "
        "unusual within the dear imgui ecosystem and so we made it explicit.")
    .value("SOURCE_EXTERN", ImGuiDragDropFlags_SourceExtern,
           "External source (from outside of dear imgui), won't attempt to "
           "read current item/window info. Will always return true. Only one "
           "Extern source can be active simultaneously.")
    .value("PAYLOAD_AUTO_EXPIRE", ImGuiDragDropFlags_PayloadAutoExpire,
           "Automatically expire the payload if the source cease to be "
           "submitted (otherwise payloads are persisting while being dragged)")
    .value("PAYLOAD_NO_CROSS_CONTEXT", ImGuiDragDropFlags_PayloadNoCrossContext,
           "Hint to specify that the payload may not be copied outside current "
           "dear imgui context.")
    .value("PAYLOAD_NO_CROSS_PROCESS", ImGuiDragDropFlags_PayloadNoCrossProcess,
           "Hint to specify that the payload may not be copied outside current "
           "process.")
    .value("ACCEPT_BEFORE_DELIVERY", ImGuiDragDropFlags_AcceptBeforeDelivery,
           "`accept_drag_drop_payload()` will returns true even before the "
           "mouse button is released. You can then call IsDelivery() to test "
           "if the payload needs to be delivered.")
    .value("ACCEPT_NO_DRAW_DEFAULT_RECT",
           ImGuiDragDropFlags_AcceptNoDrawDefaultRect,
           "Do not draw the default highlight rectangle when hovering over "
           "target.")
    .value("ACCEPT_NO_PREVIEW_TOOLTIP",
           ImGuiDragDropFlags_AcceptNoPreviewTooltip,
           "Request hiding the `begin_drag_drop_source` tooltip from the "
           "`begin_drag_drop_target` site.")
    .value("ACCEPT_PEEK_ONLY", ImGuiDragDropFlags_AcceptPeekOnly,
           "For peeking ahead and inspecting the payload before delivery.");
nb::enum_<ImGuiFocusedFlags_>(m, "FocusedFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImGuiFocusedFlags_None)
    .value("CHILD_WINDOWS", ImGuiFocusedFlags_ChildWindows,
           "Return true if any children of the window is focused")
    .value("ROOT_WINDOW", ImGuiFocusedFlags_RootWindow,
           "Test from root window (top most parent of the current hierarchy)")
    .value("ANY_WINDOW", ImGuiFocusedFlags_AnyWindow,
           "Return true if any window is focused. Important: If you are trying "
           "to tell how to dispatch your low-level inputs, do NOT use this. "
           "Use 'io.WantCaptureMouse' instead! Please read the FAQ!")
    .value("NO_POPUP_HIERARCHY", ImGuiFocusedFlags_NoPopupHierarchy,
           "Do not consider popup hierarchy (do not treat popup emitter as "
           "parent of popup) (when used with _ChildWindows or _RootWindow)")
    .value("ROOT_AND_CHILD_WINDOWS", ImGuiFocusedFlags_RootAndChildWindows);
nb::enum_<ImGuiWindowFlags_>(m, "WindowFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImGuiWindowFlags_None)
    .value("NO_TITLE_BAR", ImGuiWindowFlags_NoTitleBar, "Disable title-bar")
    .value("NO_RESIZE", ImGuiWindowFlags_NoResize,
           "Disable user resizing with the lower-right grip")
    .value("NO_MOVE", ImGuiWindowFlags_NoMove, "Disable user moving the window")
    .value("NO_SCROLLBAR", ImGuiWindowFlags_NoScrollbar,
           "Disable scrollbars (window can still scroll with mouse or "
           "programmatically)")
    .value("NO_SCROLL_WITH_MOUSE", ImGuiWindowFlags_NoScrollWithMouse,
           "Disable user vertically scrolling with mouse wheel. On child "
           "window, mouse wheel will be forwarded to the parent unless "
           "NoScrollbar is also set.")
    .value("NO_COLLAPSE", ImGuiWindowFlags_NoCollapse,
           "Disable user collapsing window by double-clicking on it. Also "
           "referred to as Window Menu Button (e.g. within a docking node).")
    .value("ALWAYS_AUTO_RESIZE", ImGuiWindowFlags_AlwaysAutoResize,
           "Resize every window to its content every frame")
    .value("NO_BACKGROUND", ImGuiWindowFlags_NoBackground,
           "Disable drawing background color (WindowBg, etc.) and outside "
           "border. Similar as using `set_next_window_bg_alpha(0.0)`.")
    .value("NO_SAVED_SETTINGS", ImGuiWindowFlags_NoSavedSettings,
           "Never load/save settings in .ini file")
    .value("NO_MOUSE_INPUTS", ImGuiWindowFlags_NoMouseInputs,
           "Disable catching mouse, hovering test with pass through.")
    .value("MENU_BAR", ImGuiWindowFlags_MenuBar, "Has a menu-bar")
    .value("HORIZONTAL_SCROLLBAR", ImGuiWindowFlags_HorizontalScrollbar,
           "Allow horizontal scrollbar to appear (off by default). You may use "
           "`set_next_window_content_size((width,0.0))`; prior to calling "
           "`begin()` to specify width. Read code in imgui_demo in the "
           "\"Horizontal Scrolling\" section.")
    .value(
        "NO_FOCUS_ON_APPEARING", ImGuiWindowFlags_NoFocusOnAppearing,
        "Disable taking focus when transitioning from hidden to visible state")
    .value("NO_BRING_TO_FRONT_ON_FOCUS", ImGuiWindowFlags_NoBringToFrontOnFocus,
           "Disable bringing window to front when taking focus (e.g. clicking "
           "on it or programmatically giving it focus)")
    .value("ALWAYS_VERTICAL_SCROLLBAR",
           ImGuiWindowFlags_AlwaysVerticalScrollbar,
           "Always show vertical scrollbar (even if ContentSize.y < Size.y)")
    .value("ALWAYS_HORIZONTAL_SCROLLBAR",
           ImGuiWindowFlags_AlwaysHorizontalScrollbar,
           "Always show horizontal scrollbar (even if ContentSize.x < Size.x)")
    .value("NO_NAV_INPUTS", ImGuiWindowFlags_NoNavInputs,
           "No keyboard/gamepad navigation within the window")
    .value("NO_NAV_FOCUS", ImGuiWindowFlags_NoNavFocus,
           "No focusing toward this window with keyboard/gamepad navigation "
           "(e.g. skipped by CTRL+TAB)")
    .value("UNSAVED_DOCUMENT", ImGuiWindowFlags_UnsavedDocument,
           "Display a dot next to the title. When used in a tab/docking "
           "context, tab is selected when clicking the X + closure is not "
           "assumed (will wait for user to stop submitting the tab). Otherwise "
           "closure is assumed when pressing the X, so if you keep submitting "
           "the tab may reappear at end of tab bar.")
    .value("NO_NAV", ImGuiWindowFlags_NoNav)
    .value("NO_DECORATION", ImGuiWindowFlags_NoDecoration)
    .value("NO_INPUTS", ImGuiWindowFlags_NoInputs)
    .value("CHILD_WINDOW", ImGuiWindowFlags_ChildWindow,
           "Don't use! For internal use by `begin_child()`")
    .value("TOOLTIP", ImGuiWindowFlags_Tooltip,
           "Don't use! For internal use by `begin_tooltip()`")
    .value("POPUP", ImGuiWindowFlags_Popup,
           "Don't use! For internal use by `begin_popup()`")
    .value("MODAL", ImGuiWindowFlags_Modal,
           "Don't use! For internal use by `begin_popup_modal()`")
    .value("CHILD_MENU", ImGuiWindowFlags_ChildMenu,
           "Don't use! For internal use by `begin_menu()`");
nb::enum_<ImGuiTreeNodeFlags_>(m, "TreeNodeFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImGuiTreeNodeFlags_None)
    .value("SELECTED", ImGuiTreeNodeFlags_Selected, "Draw as selected")
    .value("FRAMED", ImGuiTreeNodeFlags_Framed,
           "Draw frame with background (e.g. for `collapsing_header`)")
    .value("ALLOW_OVERLAP", ImGuiTreeNodeFlags_AllowOverlap,
           "Hit testing to allow subsequent widgets to overlap this one")
    .value("NO_TREE_PUSH_ON_OPEN", ImGuiTreeNodeFlags_NoTreePushOnOpen,
           "Don't do a `tree_push()` when open (e.g. for `collapsing_header`) "
           "= no extra indent nor pushing on ID stack")
    .value("NO_AUTO_OPEN_ON_LOG", ImGuiTreeNodeFlags_NoAutoOpenOnLog,
           "Don't automatically and temporarily open node when Logging is "
           "active (by default logging will automatically open tree nodes)")
    .value("DEFAULT_OPEN", ImGuiTreeNodeFlags_DefaultOpen,
           "Default node to be open")
    .value("OPEN_ON_DOUBLE_CLICK", ImGuiTreeNodeFlags_OpenOnDoubleClick,
           "Open on double-click instead of simple click (default for "
           "multi-select unless any _OpenOnXXX behavior is set explicitly). "
           "Both behaviors may be combined.")
    .value("OPEN_ON_ARROW", ImGuiTreeNodeFlags_OpenOnArrow,
           "Open when clicking on the arrow part (default for multi-select "
           "unless any _OpenOnXXX behavior is set explicitly). Both behaviors "
           "may be combined.")
    .value("LEAF", ImGuiTreeNodeFlags_Leaf,
           "No collapsing, no arrow (use as a convenience for leaf nodes).")
    .value("BULLET", ImGuiTreeNodeFlags_Bullet,
           "Display a bullet instead of arrow. IMPORTANT: node can still be "
           "marked open/close if you don't set the _Leaf flag!")
    .value("FRAME_PADDING", ImGuiTreeNodeFlags_FramePadding,
           "Use FramePadding (even for an unframed text node) to vertically "
           "align text baseline to regular widget height. Equivalent to "
           "calling `align_text_to_frame_padding()` before the node.")
    .value("SPAN_AVAIL_WIDTH", ImGuiTreeNodeFlags_SpanAvailWidth,
           "Extend hit box to the right-most edge, even if not framed. This is "
           "not the default in order to allow adding other items on the same "
           "line without using AllowOverlap mode.")
    .value("SPAN_FULL_WIDTH", ImGuiTreeNodeFlags_SpanFullWidth,
           "Extend hit box to the left-most and right-most edges (cover the "
           "indent area).")
    .value("SPAN_LABEL_WIDTH", ImGuiTreeNodeFlags_SpanLabelWidth,
           "Narrow hit box + narrow hovering highlight, will only cover the "
           "label text.")
    .value("SPAN_ALL_COLUMNS", ImGuiTreeNodeFlags_SpanAllColumns,
           "Frame will span all columns of its container table (label will "
           "still fit in current column)")
    .value("LABEL_SPAN_ALL_COLUMNS", ImGuiTreeNodeFlags_LabelSpanAllColumns,
           "Label will span all columns of its container table")
    .value("NAV_LEFT_JUMPS_BACK_HERE", ImGuiTreeNodeFlags_NavLeftJumpsBackHere,
           "(WIP) Nav: left direction may move to this `tree_node()` from any "
           "of its child (items submitted between `tree_node` and `tree_pop`)")
    .value("COLLAPSING_HEADER", ImGuiTreeNodeFlags_CollapsingHeader);
nb::enum_<ImGuiTabBarFlags_>(m, "TabBarFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImGuiTabBarFlags_None)
    .value("REORDERABLE", ImGuiTabBarFlags_Reorderable,
           "Allow manually dragging tabs to re-order them + New tabs are "
           "appended at the end of list")
    .value("AUTO_SELECT_NEW_TABS", ImGuiTabBarFlags_AutoSelectNewTabs,
           "Automatically select new tabs when they appear")
    .value("TAB_LIST_POPUP_BUTTON", ImGuiTabBarFlags_TabListPopupButton,
           "Disable buttons to open the tab list popup")
    .value("NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON",
           ImGuiTabBarFlags_NoCloseWithMiddleMouseButton,
           "Disable behavior of closing tabs (that are submitted with p_open "
           "!= NULL) with middle mouse button. You may handle this behavior "
           "manually on user's side with if (`is_item_hovered()` && "
           "`is_mouse_clicked(2)`) *p_open = false.")
    .value("NO_TAB_LIST_SCROLLING_BUTTONS",
           ImGuiTabBarFlags_NoTabListScrollingButtons,
           "Disable scrolling buttons (apply when fitting policy is "
           "`TabBarFlags.FITTING_POLICY_SCROLL`)")
    .value("NO_TOOLTIP", ImGuiTabBarFlags_NoTooltip,
           "Disable tooltips when hovering a tab")
    .value("DRAW_SELECTED_OVERLINE", ImGuiTabBarFlags_DrawSelectedOverline,
           "Draw selected overline markers over selected tab")
    .value("FITTING_POLICY_RESIZE_DOWN",
           ImGuiTabBarFlags_FittingPolicyResizeDown,
           "Resize tabs when they don't fit")
    .value("FITTING_POLICY_SCROLL", ImGuiTabBarFlags_FittingPolicyScroll,
           "Add scroll buttons when tabs don't fit")
    .value("FITTING_POLICY_MASK_", ImGuiTabBarFlags_FittingPolicyMask_)
    .value("FITTING_POLICY_DEFAULT_", ImGuiTabBarFlags_FittingPolicyDefault_);
nb::enum_<ImGuiTabItemFlags_>(m, "TabItemFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImGuiTabItemFlags_None)
    .value("UNSAVED_DOCUMENT", ImGuiTabItemFlags_UnsavedDocument,
           "Display a dot next to the title + set "
           "`TabItemFlags.NO_ASSUMED_CLOSURE`.")
    .value("SET_SELECTED", ImGuiTabItemFlags_SetSelected,
           "Trigger flag to programmatically make the tab selected when "
           "calling `begin_tab_item()`")
    .value("NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON",
           ImGuiTabItemFlags_NoCloseWithMiddleMouseButton,
           "Disable behavior of closing tabs (that are submitted with p_open "
           "!= NULL) with middle mouse button. You may handle this behavior "
           "manually on user's side with if (`is_item_hovered()` && "
           "`is_mouse_clicked(2)`) *p_open = false.")
    .value("NO_PUSH_ID", ImGuiTabItemFlags_NoPushId,
           "Don't call `push_id()`/`pop_id()` on "
           "`begin_tab_item()`/`end_tab_item()`")
    .value("NO_TOOLTIP", ImGuiTabItemFlags_NoTooltip,
           "Disable tooltip for the given tab")
    .value(
        "NO_REORDER", ImGuiTabItemFlags_NoReorder,
        "Disable reordering this tab or having another tab cross over this tab")
    .value("LEADING", ImGuiTabItemFlags_Leading,
           "Enforce the tab position to the left of the tab bar (after the tab "
           "list popup button)")
    .value("TRAILING", ImGuiTabItemFlags_Trailing,
           "Enforce the tab position to the right of the tab bar (before the "
           "scrolling buttons)")
    .value("NO_ASSUMED_CLOSURE", ImGuiTabItemFlags_NoAssumedClosure,
           "Tab is selected when trying to close + closure is not immediately "
           "assumed (will wait for user to stop submitting the tab). Otherwise "
           "closure is assumed when pressing the X, so if you keep submitting "
           "the tab may reappear at end of tab bar.");
nb::enum_<ImGuiTableFlags_>(m, "TableFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImGuiTableFlags_None)
    .value("RESIZABLE", ImGuiTableFlags_Resizable, "Enable resizing columns.")
    .value("REORDERABLE", ImGuiTableFlags_Reorderable,
           "Enable reordering columns in header row (need calling "
           "`table_setup_column()` + `table_headers_row()` to display headers)")
    .value("HIDEABLE", ImGuiTableFlags_Hideable,
           "Enable hiding/disabling columns in context menu.")
    .value(
        "SORTABLE", ImGuiTableFlags_Sortable,
        "Enable sorting. Call `table_get_sort_specs()` to obtain sort specs. "
        "Also see `TableFlags.SORT_MULTI` and `TableFlags.SORT_TRISTATE`.")
    .value("NO_SAVED_SETTINGS", ImGuiTableFlags_NoSavedSettings,
           "Disable persisting columns order, width and sort settings in the "
           ".ini file.")
    .value("CONTEXT_MENU_IN_BODY", ImGuiTableFlags_ContextMenuInBody,
           "Right-click on columns body/contents will display table context "
           "menu. By default it is available in `table_headers_row()`.")
    .value("ROW_BG", ImGuiTableFlags_RowBg,
           "Set each RowBg color with `Col.TABLE_ROW_BG` or "
           "`Col.TABLE_ROW_BG_ALT` (equivalent of calling `table_set_bg_color` "
           "with ImGuiTableBgFlags_RowBg0 on each row manually)")
    .value("BORDERS_INNER_H", ImGuiTableFlags_BordersInnerH,
           "Draw horizontal borders between rows.")
    .value("BORDERS_OUTER_H", ImGuiTableFlags_BordersOuterH,
           "Draw horizontal borders at the top and bottom.")
    .value("BORDERS_INNER_V", ImGuiTableFlags_BordersInnerV,
           "Draw vertical borders between columns.")
    .value("BORDERS_OUTER_V", ImGuiTableFlags_BordersOuterV,
           "Draw vertical borders on the left and right sides.")
    .value("BORDERS_H", ImGuiTableFlags_BordersH, "Draw horizontal borders.")
    .value("BORDERS_V", ImGuiTableFlags_BordersV, "Draw vertical borders.")
    .value("BORDERS_INNER", ImGuiTableFlags_BordersInner, "Draw inner borders.")
    .value("BORDERS_OUTER", ImGuiTableFlags_BordersOuter, "Draw outer borders.")
    .value("BORDERS", ImGuiTableFlags_Borders, "Draw all borders.")
    .value("NO_BORDERS_IN_BODY", ImGuiTableFlags_NoBordersInBody,
           "[ALPHA] Disable vertical borders in columns Body (borders will "
           "always appear in Headers). -> May move to style")
    .value(
        "NO_BORDERS_IN_BODY_UNTIL_RESIZE",
        ImGuiTableFlags_NoBordersInBodyUntilResize,
        "[ALPHA] Disable vertical borders in columns Body until hovered for "
        "resize (borders will always appear in Headers). -> May move to style")
    .value("SIZING_FIXED_FIT", ImGuiTableFlags_SizingFixedFit,
           "`columns` default to _WidthFixed or _WidthAuto (if resizable or "
           "not resizable), matching contents width.")
    .value("SIZING_FIXED_SAME", ImGuiTableFlags_SizingFixedSame,
           "`columns` default to _WidthFixed or _WidthAuto (if resizable or "
           "not resizable), matching the maximum contents width of all "
           "columns. Implicitly enable `TableFlags.NO_KEEP_COLUMNS_VISIBLE`.")
    .value("SIZING_STRETCH_PROP", ImGuiTableFlags_SizingStretchProp,
           "`columns` default to _WidthStretch with default weights "
           "proportional to each columns contents widths.")
    .value("SIZING_STRETCH_SAME", ImGuiTableFlags_SizingStretchSame,
           "`columns` default to _WidthStretch with default weights all equal, "
           "unless overridden by `table_setup_column()`.")
    .value("NO_HOST_EXTEND_X", ImGuiTableFlags_NoHostExtendX,
           "Make outer width auto-fit to columns, overriding outer_size.x "
           "value. Only available when ScrollX/ScrollY are disabled and "
           "Stretch columns are not used.")
    .value("NO_HOST_EXTEND_Y", ImGuiTableFlags_NoHostExtendY,
           "Make outer height stop exactly at outer_size.y (prevent "
           "auto-extending table past the limit). Only available when "
           "ScrollX/ScrollY are disabled. Data below the limit will be clipped "
           "and not visible.")
    .value(
        "NO_KEEP_COLUMNS_VISIBLE", ImGuiTableFlags_NoKeepColumnsVisible,
        "Disable keeping column always minimally visible when ScrollX is off "
        "and table gets too small. Not recommended if columns are resizable.")
    .value("PRECISE_WIDTHS", ImGuiTableFlags_PreciseWidths,
           "Disable distributing remainder width to stretched columns (width "
           "allocation on a 100-wide table with 3 columns: Without this flag: "
           "33,33,34. With this flag: 33,33,33). With larger number of "
           "columns, resizing will appear to be less smooth.")
    .value(
        "NO_CLIP", ImGuiTableFlags_NoClip,
        "Disable clipping rectangle for every individual columns (reduce draw "
        "command count, items will be able to overflow into other columns). "
        "Generally incompatible with `table_setup_scroll_freeze()`.")
    .value("PAD_OUTER_X", ImGuiTableFlags_PadOuterX,
           "Default if BordersOuterV is on. Enable outermost padding. "
           "Generally desirable if you have headers.")
    .value("NO_PAD_OUTER_X", ImGuiTableFlags_NoPadOuterX,
           "Default if BordersOuterV is off. Disable outermost padding.")
    .value(
        "NO_PAD_INNER_X", ImGuiTableFlags_NoPadInnerX,
        "Disable inner padding between columns (double inner padding if "
        "BordersOuterV is on, single inner padding if BordersOuterV is off).")
    .value("SCROLL_X", ImGuiTableFlags_ScrollX,
           "Enable horizontal scrolling. Require 'outer_size' parameter of "
           "`begin_table()` to specify the container size. Changes default "
           "sizing policy. Because this creates a child window, ScrollY is "
           "currently generally recommended when using ScrollX.")
    .value("SCROLL_Y", ImGuiTableFlags_ScrollY,
           "Enable vertical scrolling. Require 'outer_size' parameter of "
           "`begin_table()` to specify the container size.")
    .value("SORT_MULTI", ImGuiTableFlags_SortMulti,
           "Hold shift when clicking headers to sort on multiple column. "
           "`table_get_sort_specs()` may return specs where (SpecsCount > 1).")
    .value("SORT_TRISTATE", ImGuiTableFlags_SortTristate,
           "Allow no sorting, disable default sorting. "
           "`table_get_sort_specs()` may return specs where (SpecsCount == 0).")
    .value("HIGHLIGHT_HOVERED_COLUMN", ImGuiTableFlags_HighlightHoveredColumn,
           "Highlight column headers when hovered (may evolve into a fuller "
           "highlight)")
    .value("SIZING_MASK_", ImGuiTableFlags_SizingMask_);
nb::enum_<ImGuiTableRowFlags_>(m, "TableRowFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImGuiTableRowFlags_None)
    .value("HEADERS", ImGuiTableRowFlags_Headers,
           "Identify header row (set default background color + width of its "
           "contents accounted differently for auto column width)");
nb::enum_<ImGuiTableColumnFlags_>(m, "TableColumnFlags", nb::is_flag(),
                                  nb::is_arithmetic())
    .value("NONE", ImGuiTableColumnFlags_None)
    .value("DISABLED", ImGuiTableColumnFlags_Disabled,
           "Overriding/master disable flag: hide column, won't show in context "
           "menu (unlike calling `table_set_column_enabled()` which "
           "manipulates the user accessible state)")
    .value("DEFAULT_HIDE", ImGuiTableColumnFlags_DefaultHide,
           "Default as a hidden/disabled column.")
    .value("DEFAULT_SORT", ImGuiTableColumnFlags_DefaultSort,
           "Default as a sorting column.")
    .value("WIDTH_STRETCH", ImGuiTableColumnFlags_WidthStretch,
           "Column will stretch. Preferable with horizontal scrolling disabled "
           "(default if table sizing policy is _SizingStretchSame or "
           "_SizingStretchProp).")
    .value("WIDTH_FIXED", ImGuiTableColumnFlags_WidthFixed,
           "Column will not stretch. Preferable with horizontal scrolling "
           "enabled (default if table sizing policy is _SizingFixedFit and "
           "table is resizable).")
    .value("NO_RESIZE", ImGuiTableColumnFlags_NoResize,
           "Disable manual resizing.")
    .value("NO_REORDER", ImGuiTableColumnFlags_NoReorder,
           "Disable manual reordering this column, this will also prevent "
           "other columns from crossing over this column.")
    .value("NO_HIDE", ImGuiTableColumnFlags_NoHide,
           "Disable ability to hide/disable this column.")
    .value("NO_CLIP", ImGuiTableColumnFlags_NoClip,
           "Disable clipping for this column (all NoClip columns will render "
           "in a same draw command).")
    .value("NO_SORT", ImGuiTableColumnFlags_NoSort,
           "Disable ability to sort on this field (even if "
           "`TableFlags.SORTABLE` is set on the table).")
    .value("NO_SORT_ASCENDING", ImGuiTableColumnFlags_NoSortAscending,
           "Disable ability to sort in the ascending direction.")
    .value("NO_SORT_DESCENDING", ImGuiTableColumnFlags_NoSortDescending,
           "Disable ability to sort in the descending direction.")
    .value("NO_HEADER_LABEL", ImGuiTableColumnFlags_NoHeaderLabel,
           "`table_headers_row()` will submit an empty label for this column. "
           "Convenient for some small columns. Name will still appear in "
           "context menu or in angled headers. You may append into this cell "
           "by calling `table_set_column_index()` right after the "
           "`table_headers_row()` call.")
    .value("NO_HEADER_WIDTH", ImGuiTableColumnFlags_NoHeaderWidth,
           "Disable header text width contribution to automatic column width.")
    .value("PREFER_SORT_ASCENDING", ImGuiTableColumnFlags_PreferSortAscending,
           "Make the initial sort direction Ascending when first sorting on "
           "this column (default).")
    .value("PREFER_SORT_DESCENDING", ImGuiTableColumnFlags_PreferSortDescending,
           "Make the initial sort direction Descending when first sorting on "
           "this column.")
    .value(
        "INDENT_ENABLE", ImGuiTableColumnFlags_IndentEnable,
        "Use current `indent` value when entering cell (default for column 0).")
    .value(
        "INDENT_DISABLE", ImGuiTableColumnFlags_IndentDisable,
        "Ignore current `indent` value when entering cell (default for columns "
        "> 0). Indentation changes _within_ the cell will still be honored.")
    .value("ANGLED_HEADER", ImGuiTableColumnFlags_AngledHeader,
           "`table_headers_row()` will submit an angled header row for this "
           "column. Note this will add an extra row.")
    .value("IS_ENABLED", ImGuiTableColumnFlags_IsEnabled,
           "Status: is enabled == not hidden by user/api (referred to as "
           "\"Hide\" in _DefaultHide and _NoHide) flags.")
    .value("IS_VISIBLE", ImGuiTableColumnFlags_IsVisible,
           "Status: is visible == is enabled AND not clipped by scrolling.")
    .value("IS_SORTED", ImGuiTableColumnFlags_IsSorted,
           "Status: is currently part of the sort specs")
    .value("IS_HOVERED", ImGuiTableColumnFlags_IsHovered,
           "Status: is hovered by mouse")
    .value("WIDTH_MASK_", ImGuiTableColumnFlags_WidthMask_)
    .value("INDENT_MASK_", ImGuiTableColumnFlags_IndentMask_)
    .value("STATUS_MASK_", ImGuiTableColumnFlags_StatusMask_)
    .value("NO_DIRECT_RESIZE_", ImGuiTableColumnFlags_NoDirectResize_,
           "[Internal] Disable user resizing this column directly (it may "
           "however we resized indirectly from its left edge)");
nb::enum_<ImGuiColorEditFlags_>(m, "ColorEditFlags", nb::is_flag(),
                                nb::is_arithmetic())
    .value("NONE", ImGuiColorEditFlags_None)
    .value("NO_ALPHA", ImGuiColorEditFlags_NoAlpha,
           "ColorEdit, ColorPicker, `color_button`: ignore Alpha component "
           "(will only read 3 components from the input pointer).")
    .value("NO_PICKER", ImGuiColorEditFlags_NoPicker,
           "ColorEdit: disable picker when clicking on color square.")
    .value("NO_OPTIONS", ImGuiColorEditFlags_NoOptions,
           "ColorEdit: disable toggling options menu when right-clicking on "
           "inputs/small preview.")
    .value("NO_SMALL_PREVIEW", ImGuiColorEditFlags_NoSmallPreview,
           "ColorEdit, ColorPicker: disable color square preview next to the "
           "inputs. (e.g. to show only the inputs)")
    .value("NO_INPUTS", ImGuiColorEditFlags_NoInputs,
           "ColorEdit, ColorPicker: disable inputs sliders/text widgets (e.g. "
           "to show only the small preview color square).")
    .value("NO_TOOLTIP", ImGuiColorEditFlags_NoTooltip,
           "ColorEdit, ColorPicker, `color_button`: disable tooltip when "
           "hovering the preview.")
    .value("NO_LABEL", ImGuiColorEditFlags_NoLabel,
           "ColorEdit, ColorPicker: disable display of inline text label (the "
           "label is still forwarded to the tooltip and picker).")
    .value("NO_SIDE_PREVIEW", ImGuiColorEditFlags_NoSidePreview,
           "ColorPicker: disable bigger color preview on right side of the "
           "picker, use small color square preview instead.")
    .value("NO_DRAG_DROP", ImGuiColorEditFlags_NoDragDrop,
           "ColorEdit: disable drag and drop target. `color_button`: disable "
           "drag and drop source.")
    .value("NO_BORDER", ImGuiColorEditFlags_NoBorder,
           "`color_button`: disable border (which is enforced by default)")
    .value("ALPHA_OPAQUE", ImGuiColorEditFlags_AlphaOpaque,
           "ColorEdit, ColorPicker, `color_button`: disable alpha in the "
           "preview,. Contrary to _NoAlpha it may still be edited when calling "
           "`color_edit4()`/`color_picker4()`. For `color_button()` this does "
           "the same as _NoAlpha.")
    .value("ALPHA_NO_BG", ImGuiColorEditFlags_AlphaNoBg,
           "ColorEdit, ColorPicker, `color_button`: disable rendering a "
           "checkerboard background behind transparent color.")
    .value("ALPHA_PREVIEW_HALF", ImGuiColorEditFlags_AlphaPreviewHalf,
           "ColorEdit, ColorPicker, `color_button`: display half opaque / half "
           "transparent preview.")
    .value(
        "ALPHA_BAR", ImGuiColorEditFlags_AlphaBar,
        "ColorEdit, ColorPicker: show vertical alpha bar/gradient in picker.")
    .value("HDR", ImGuiColorEditFlags_HDR,
           "(WIP) ColorEdit: Currently only disable 0.0f..1.0f limits in RGBA "
           "edition (note: you probably want to use `ColorEditFlags.FLOAT` "
           "flag as well).")
    .value("DISPLAY_RGB", ImGuiColorEditFlags_DisplayRGB,
           "ColorEdit: override _display_ type among RGB/HSV/Hex. ColorPicker: "
           "select any combination using one or more of RGB/HSV/Hex.")
    .value("DISPLAY_HSV", ImGuiColorEditFlags_DisplayHSV)
    .value("DISPLAY_HEX", ImGuiColorEditFlags_DisplayHex)
    .value("UINT8", ImGuiColorEditFlags_Uint8,
           "ColorEdit, ColorPicker, `color_button`: _display_ values formatted "
           "as 0..255.")
    .value("FLOAT", ImGuiColorEditFlags_Float,
           "ColorEdit, ColorPicker, `color_button`: _display_ values formatted "
           "as 0.0f..1.0f floats instead of 0..255 integers. No round-trip of "
           "value via integers.")
    .value("PICKER_HUE_BAR", ImGuiColorEditFlags_PickerHueBar,
           "ColorPicker: bar for Hue, rectangle for Sat/Value.")
    .value("PICKER_HUE_WHEEL", ImGuiColorEditFlags_PickerHueWheel,
           "ColorPicker: wheel for Hue, triangle for Sat/Value.")
    .value("INPUT_RGB", ImGuiColorEditFlags_InputRGB,
           "ColorEdit, ColorPicker: input and output data in RGB format.")
    .value("INPUT_HSV", ImGuiColorEditFlags_InputHSV,
           "ColorEdit, ColorPicker: input and output data in HSV format.")
    .value("DEFAULT_OPTIONS_", ImGuiColorEditFlags_DefaultOptions_)
    .value("ALPHA_MASK_", ImGuiColorEditFlags_AlphaMask_)
    .value("DISPLAY_MASK_", ImGuiColorEditFlags_DisplayMask_)
    .value("DATA_TYPE_MASK_", ImGuiColorEditFlags_DataTypeMask_)
    .value("PICKER_MASK_", ImGuiColorEditFlags_PickerMask_)
    .value("INPUT_MASK_", ImGuiColorEditFlags_InputMask_);
nb::enum_<ImGuiComboFlags_>(m, "ComboFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImGuiComboFlags_None)
    .value("POPUP_ALIGN_LEFT", ImGuiComboFlags_PopupAlignLeft,
           "Align the popup toward the left by default")
    .value("HEIGHT_SMALL", ImGuiComboFlags_HeightSmall,
           "Max ~4 items visible. Tip: If you want your combo popup to be a "
           "specific size you can use `set_next_window_size_constraints()` "
           "prior to calling `begin_combo()`")
    .value("HEIGHT_REGULAR", ImGuiComboFlags_HeightRegular,
           "Max ~8 items visible (default)")
    .value("HEIGHT_LARGE", ImGuiComboFlags_HeightLarge, "Max ~20 items visible")
    .value("HEIGHT_LARGEST", ImGuiComboFlags_HeightLargest,
           "As many fitting items as possible")
    .value("NO_ARROW_BUTTON", ImGuiComboFlags_NoArrowButton,
           "Display on the preview box without the square arrow button")
    .value("NO_PREVIEW", ImGuiComboFlags_NoPreview,
           "Display only a square arrow button")
    .value("WIDTH_FIT_PREVIEW", ImGuiComboFlags_WidthFitPreview,
           "Width dynamically calculated from preview contents")
    .value("HEIGHT_MASK_", ImGuiComboFlags_HeightMask_);
nb::enum_<ImGuiSelectableFlags_>(m, "SelectableFlags", nb::is_flag(),
                                 nb::is_arithmetic())
    .value("NONE", ImGuiSelectableFlags_None)
    .value("NO_AUTO_CLOSE_POPUPS", ImGuiSelectableFlags_NoAutoClosePopups,
           "Clicking this doesn't close parent popup window (overrides "
           "`ItemFlags.AUTO_CLOSE_POPUPS`)")
    .value("SPAN_ALL_COLUMNS", ImGuiSelectableFlags_SpanAllColumns,
           "Frame will span all columns of its container table (text will "
           "still fit in current column)")
    .value("ALLOW_DOUBLE_CLICK", ImGuiSelectableFlags_AllowDoubleClick,
           "Generate press events on double clicks too")
    .value("DISABLED", ImGuiSelectableFlags_Disabled,
           "Cannot be selected, display grayed out text")
    .value("ALLOW_OVERLAP", ImGuiSelectableFlags_AllowOverlap,
           "(WIP) Hit testing to allow subsequent widgets to overlap this one")
    .value("HIGHLIGHT", ImGuiSelectableFlags_Highlight,
           "Make the item be displayed as if it is hovered");
nb::enum_<ImGuiConfigFlags_>(m, "ConfigFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImGuiConfigFlags_None)
    .value("NAV_ENABLE_KEYBOARD", ImGuiConfigFlags_NavEnableKeyboard,
           "Master keyboard navigation enable flag. Enable full Tabbing + "
           "directional arrows + space/enter to activate.")
    .value("NAV_ENABLE_GAMEPAD", ImGuiConfigFlags_NavEnableGamepad,
           "Master gamepad navigation enable flag. Backend also needs to set "
           "`BackendFlags.HAS_GAMEPAD`.")
    .value("NO_MOUSE", ImGuiConfigFlags_NoMouse,
           "Instruct dear imgui to disable mouse inputs and interactions.")
    .value("NO_MOUSE_CURSOR_CHANGE", ImGuiConfigFlags_NoMouseCursorChange,
           "Instruct backend to not alter mouse cursor shape and visibility. "
           "Use if the backend cursor changes are interfering with yours and "
           "you don't want to use `set_mouse_cursor()` to change mouse cursor. "
           "You may want to honor requests from imgui by reading "
           "`get_mouse_cursor()` yourself instead.")
    .value(
        "NO_KEYBOARD", ImGuiConfigFlags_NoKeyboard,
        "Instruct dear imgui to disable keyboard inputs and interactions. This "
        "is done by ignoring keyboard events and clearing existing states.")
    .value("IS_SRGB", ImGuiConfigFlags_IsSRGB, "Application is SRGB-aware.")
    .value("IS_TOUCH_SCREEN", ImGuiConfigFlags_IsTouchScreen,
           "Application is using a touch screen instead of a mouse.");
nb::enum_<ImGuiBackendFlags_>(m, "BackendFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImGuiBackendFlags_None)
    .value("HAS_GAMEPAD", ImGuiBackendFlags_HasGamepad,
           "Backend Platform supports gamepad and currently has one connected.")
    .value("HAS_MOUSE_CURSORS", ImGuiBackendFlags_HasMouseCursors,
           "Backend Platform supports honoring `get_mouse_cursor()` value to "
           "change the OS cursor shape.")
    .value("HAS_SET_MOUSE_POS", ImGuiBackendFlags_HasSetMousePos,
           "Backend Platform supports io.WantSetMousePos requests to "
           "reposition the OS mouse position (only used if "
           "io.ConfigNavMoveSetMousePos is set).")
    .value(
        "RENDERER_HAS_VTX_OFFSET", ImGuiBackendFlags_RendererHasVtxOffset,
        "Backend Renderer supports ImDrawCmd::VtxOffset. This enables output "
        "of large meshes (64K+ vertices) while still using 16-bit indices.");
nb::enum_<ImGuiCond_>(m, "Cond", nb::is_arithmetic())
    .value("NONE", ImGuiCond_None,
           "No condition (always set the variable), same as _Always")
    .value("ALWAYS", ImGuiCond_Always,
           "No condition (always set the variable), same as _None")
    .value("ONCE", ImGuiCond_Once,
           "Set the variable once per runtime session (only the first call "
           "will succeed)")
    .value("FIRST_USE_EVER", ImGuiCond_FirstUseEver,
           "Set the variable if the object/window has no persistently saved "
           "data (no entry in .ini file)")
    .value("APPEARING", ImGuiCond_Appearing,
           "Set the variable if the object/window is appearing after being "
           "hidden/inactive (or the first time)");
nb::enum_<ImGuiHoveredFlags_>(m, "HoveredFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImGuiHoveredFlags_None,
           "Return true if directly over the item/window, not obstructed by "
           "another window, not obstructed by an active popup or modal "
           "blocking inputs under them.")
    .value("CHILD_WINDOWS", ImGuiHoveredFlags_ChildWindows,
           "`is_window_hovered()` only: Return true if any children of the "
           "window is hovered")
    .value("ROOT_WINDOW", ImGuiHoveredFlags_RootWindow,
           "`is_window_hovered()` only: Test from root window (top most parent "
           "of the current hierarchy)")
    .value("ANY_WINDOW", ImGuiHoveredFlags_AnyWindow,
           "`is_window_hovered()` only: Return true if any window is hovered")
    .value("NO_POPUP_HIERARCHY", ImGuiHoveredFlags_NoPopupHierarchy,
           "`is_window_hovered()` only: Do not consider popup hierarchy (do "
           "not treat popup emitter as parent of popup) (when used with "
           "_ChildWindows or _RootWindow)")
    .value("ALLOW_WHEN_BLOCKED_BY_POPUP",
           ImGuiHoveredFlags_AllowWhenBlockedByPopup,
           "Return true even if a popup window is normally blocking access to "
           "this item/window")
    .value("ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM",
           ImGuiHoveredFlags_AllowWhenBlockedByActiveItem,
           "Return true even if an active item is blocking access to this "
           "item/window. Useful for Drag and Drop patterns.")
    .value("ALLOW_WHEN_OVERLAPPED_BY_ITEM",
           ImGuiHoveredFlags_AllowWhenOverlappedByItem,
           "`is_item_hovered()` only: Return true even if the item uses "
           "AllowOverlap mode and is overlapped by another hoverable item.")
    .value("ALLOW_WHEN_OVERLAPPED_BY_WINDOW",
           ImGuiHoveredFlags_AllowWhenOverlappedByWindow,
           "`is_item_hovered()` only: Return true even if the position is "
           "obstructed or overlapped by another window.")
    .value("ALLOW_WHEN_DISABLED", ImGuiHoveredFlags_AllowWhenDisabled,
           "`is_item_hovered()` only: Return true even if the item is disabled")
    .value("NO_NAV_OVERRIDE", ImGuiHoveredFlags_NoNavOverride,
           "`is_item_hovered()` only: Disable using keyboard/gamepad "
           "navigation state when active, always query mouse")
    .value("ALLOW_WHEN_OVERLAPPED", ImGuiHoveredFlags_AllowWhenOverlapped)
    .value("RECT_ONLY", ImGuiHoveredFlags_RectOnly)
    .value("ROOT_AND_CHILD_WINDOWS", ImGuiHoveredFlags_RootAndChildWindows)
    .value("FOR_TOOLTIP", ImGuiHoveredFlags_ForTooltip,
           "Shortcut for standard flags when using `is_item_hovered()` + "
           "`set_tooltip()` sequence.")
    .value(
        "STATIONARY", ImGuiHoveredFlags_Stationary,
        "Require mouse to be stationary for style.HoverStationaryDelay (~0.15 "
        "sec) _at least one time_. After this, can move on same item/window. "
        "Using the stationary test tends to reduces the need for a long delay.")
    .value("DELAY_NONE", ImGuiHoveredFlags_DelayNone,
           "`is_item_hovered()` only: Return true immediately (default). As "
           "this is the default you generally ignore this.")
    .value("DELAY_SHORT", ImGuiHoveredFlags_DelayShort,
           "`is_item_hovered()` only: Return true after style.HoverDelayShort "
           "elapsed (~0.15 sec) (shared between items) + requires mouse to be "
           "stationary for style.HoverStationaryDelay (once per item).")
    .value("DELAY_NORMAL", ImGuiHoveredFlags_DelayNormal,
           "`is_item_hovered()` only: Return true after style.HoverDelayNormal "
           "elapsed (~0.40 sec) (shared between items) + requires mouse to be "
           "stationary for style.HoverStationaryDelay (once per item).")
    .value("NO_SHARED_DELAY", ImGuiHoveredFlags_NoSharedDelay,
           "`is_item_hovered()` only: Disable shared delay system where moving "
           "from one item to the next keeps the previous timer for a short "
           "time (standard for tooltips with long delays)");
nb::enum_<ImGuiItemFlags_>(m, "ItemFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImGuiItemFlags_None, "(Default)")
    .value("NO_TAB_STOP", ImGuiItemFlags_NoTabStop,
           "Disable keyboard tabbing. This is a \"lighter\" version of "
           "`ItemFlags.NO_NAV`.")
    .value("NO_NAV", ImGuiItemFlags_NoNav,
           "Disable any form of focusing (keyboard/gamepad directional "
           "navigation and `set_keyboard_focus_here()` calls).")
    .value("NO_NAV_DEFAULT_FOCUS", ImGuiItemFlags_NoNavDefaultFocus,
           "Disable item being a candidate for default focus (e.g. used by "
           "title bar items).")
    .value("BUTTON_REPEAT", ImGuiItemFlags_ButtonRepeat,
           "Any button-like behavior will have repeat mode enabled (based on "
           "io.KeyRepeatDelay and io.KeyRepeatRate values). Note that you can "
           "also call `is_item_active()` after any button to tell if it is "
           "being held.")
    .value("AUTO_CLOSE_POPUPS", ImGuiItemFlags_AutoClosePopups,
           "`menu_item()`/`selectable()` automatically close their parent "
           "popup window.")
    .value("ALLOW_DUPLICATE_ID", ImGuiItemFlags_AllowDuplicateId,
           "Allow submitting an item with the same identifier as an item "
           "already submitted this frame without triggering a warning tooltip "
           "if io.ConfigDebugHighlightIdConflicts is set.");
nb::enum_<ImGuiSliderFlags_>(m, "SliderFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImGuiSliderFlags_None)
    .value("LOGARITHMIC", ImGuiSliderFlags_Logarithmic,
           "Make the widget logarithmic (linear otherwise). Consider using "
           "`SliderFlags.NO_ROUND_TO_FORMAT` with this if using a "
           "format-string with small amount of digits.")
    .value(
        "NO_ROUND_TO_FORMAT", ImGuiSliderFlags_NoRoundToFormat,
        "Disable rounding underlying value to match precision of the display "
        "format string (e.g. %.3f values are rounded to those 3 digits).")
    .value("NO_INPUT", ImGuiSliderFlags_NoInput,
           "Disable CTRL+Click or Enter key allowing to input text directly "
           "into the widget.")
    .value("WRAP_AROUND", ImGuiSliderFlags_WrapAround,
           "Enable wrapping around from max to min and from min to max. Only "
           "supported by DragXXX() functions for now.")
    .value("CLAMP_ON_INPUT", ImGuiSliderFlags_ClampOnInput,
           "Clamp value to min/max bounds when input manually with CTRL+Click. "
           "By default CTRL+Click allows going out of bounds.")
    .value("CLAMP_ZERO_RANGE", ImGuiSliderFlags_ClampZeroRange,
           "Clamp even if min==max==0.0f. Otherwise due to legacy reason "
           "DragXXX functions don't clamp with those values. When your "
           "clamping limits are dynamic you almost always want to use it.")
    .value("NO_SPEED_TWEAKS", ImGuiSliderFlags_NoSpeedTweaks,
           "Disable keyboard modifiers altering tweak speed. Useful if you "
           "want to alter tweak speed yourself based on your own logic.")
    .value("ALWAYS_CLAMP", ImGuiSliderFlags_AlwaysClamp)
    .value("INVALID_MASK_", ImGuiSliderFlags_InvalidMask_,
           "[Internal] We treat using those bits as being potentially a 'float "
           "power' argument from the previous API that has got miscast to this "
           "enum, and will trigger an assert if needed.");
nb::enum_<ImGuiPopupFlags_>(m, "PopupFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImGuiPopupFlags_None)
    .value("MOUSE_BUTTON_LEFT", ImGuiPopupFlags_MouseButtonLeft,
           "For BeginPopupContext*(): open on Left Mouse release. Guaranteed "
           "to always be == 0 (same as `MouseButton.LEFT`)")
    .value("MOUSE_BUTTON_RIGHT", ImGuiPopupFlags_MouseButtonRight,
           "For BeginPopupContext*(): open on Right Mouse release. Guaranteed "
           "to always be == 1 (same as `MouseButton.RIGHT`)")
    .value("MOUSE_BUTTON_MIDDLE", ImGuiPopupFlags_MouseButtonMiddle,
           "For BeginPopupContext*(): open on Middle Mouse release. Guaranteed "
           "to always be == 2 (same as `MouseButton.MIDDLE`)")
    .value("MOUSE_BUTTON_MASK_", ImGuiPopupFlags_MouseButtonMask_)
    .value("MOUSE_BUTTON_DEFAULT_", ImGuiPopupFlags_MouseButtonDefault_)
    .value("NO_REOPEN", ImGuiPopupFlags_NoReopen,
           "For `open_popup`*(), BeginPopupContext*(): don't reopen same popup "
           "if already open (won't reposition, won't reinitialize navigation)")
    .value("NO_OPEN_OVER_EXISTING_POPUP",
           ImGuiPopupFlags_NoOpenOverExistingPopup,
           "For `open_popup`*(), BeginPopupContext*(): don't open if there's "
           "already a popup at the same level of the popup stack")
    .value("NO_OPEN_OVER_ITEMS", ImGuiPopupFlags_NoOpenOverItems,
           "For `begin_popup_context_window()`: don't return true when "
           "hovering items, only when hovering empty space")
    .value("ANY_POPUP_ID", ImGuiPopupFlags_AnyPopupId,
           "For `is_popup_open()`: ignore the ImGuiID parameter and test for "
           "any popup.")
    .value("ANY_POPUP_LEVEL", ImGuiPopupFlags_AnyPopupLevel,
           "For `is_popup_open()`: search/test at any level of the popup stack "
           "(default test in the current level)")
    .value("ANY_POPUP", ImGuiPopupFlags_AnyPopup);
nb::enum_<ImGuiMouseButton_>(m, "MouseButton", nb::is_arithmetic())
    .value("LEFT", ImGuiMouseButton_Left)
    .value("RIGHT", ImGuiMouseButton_Right)
    .value("MIDDLE", ImGuiMouseButton_Middle)
    .value("COUNT", ImGuiMouseButton_COUNT);
nb::enum_<ImGuiMouseCursor_>(m, "MouseCursor", nb::is_arithmetic())
    .value("NONE", ImGuiMouseCursor_None)
    .value("ARROW", ImGuiMouseCursor_Arrow)
    .value("TEXT_INPUT", ImGuiMouseCursor_TextInput,
           "When hovering over `input_text`, etc.")
    .value("RESIZE_ALL", ImGuiMouseCursor_ResizeAll,
           "(Unused by Dear ImGui functions)")
    .value("RESIZE_NS", ImGuiMouseCursor_ResizeNS,
           "When hovering over a horizontal border")
    .value("RESIZE_EW", ImGuiMouseCursor_ResizeEW,
           "When hovering over a vertical border or a column")
    .value("RESIZE_NESW", ImGuiMouseCursor_ResizeNESW,
           "When hovering over the bottom-left corner of a window")
    .value("RESIZE_NWSE", ImGuiMouseCursor_ResizeNWSE,
           "When hovering over the bottom-right corner of a window")
    .value("HAND", ImGuiMouseCursor_Hand,
           "(Unused by Dear ImGui functions. Use for e.g. hyperlinks)")
    .value("WAIT", ImGuiMouseCursor_Wait,
           "When waiting for something to process/load.")
    .value("PROGRESS", ImGuiMouseCursor_Progress,
           "When waiting for something to process/load, but application is "
           "still interactive.")
    .value("NOT_ALLOWED", ImGuiMouseCursor_NotAllowed,
           "When hovering something with disallowed interaction. Usually a "
           "crossed circle.")
    .value("COUNT", ImGuiMouseCursor_COUNT);
nb::enum_<ImGuiCol_>(m, "Col", nb::is_arithmetic())
    .value("TEXT", ImGuiCol_Text)
    .value("TEXT_DISABLED", ImGuiCol_TextDisabled)
    .value("WINDOW_BG", ImGuiCol_WindowBg, "Background of normal windows")
    .value("CHILD_BG", ImGuiCol_ChildBg, "Background of child windows")
    .value("POPUP_BG", ImGuiCol_PopupBg,
           "Background of popups, menus, tooltips windows")
    .value("BORDER", ImGuiCol_Border)
    .value("BORDER_SHADOW", ImGuiCol_BorderShadow)
    .value("FRAME_BG", ImGuiCol_FrameBg,
           "Background of checkbox, radio button, plot, slider, text input")
    .value("FRAME_BG_HOVERED", ImGuiCol_FrameBgHovered)
    .value("FRAME_BG_ACTIVE", ImGuiCol_FrameBgActive)
    .value("TITLE_BG", ImGuiCol_TitleBg, "Title bar")
    .value("TITLE_BG_ACTIVE", ImGuiCol_TitleBgActive, "Title bar when focused")
    .value("TITLE_BG_COLLAPSED", ImGuiCol_TitleBgCollapsed,
           "Title bar when collapsed")
    .value("MENU_BAR_BG", ImGuiCol_MenuBarBg)
    .value("SCROLLBAR_BG", ImGuiCol_ScrollbarBg)
    .value("SCROLLBAR_GRAB", ImGuiCol_ScrollbarGrab)
    .value("SCROLLBAR_GRAB_HOVERED", ImGuiCol_ScrollbarGrabHovered)
    .value("SCROLLBAR_GRAB_ACTIVE", ImGuiCol_ScrollbarGrabActive)
    .value("CHECK_MARK", ImGuiCol_CheckMark,
           "`checkbox` tick and `radio_button` circle")
    .value("SLIDER_GRAB", ImGuiCol_SliderGrab)
    .value("SLIDER_GRAB_ACTIVE", ImGuiCol_SliderGrabActive)
    .value("BUTTON", ImGuiCol_Button)
    .value("BUTTON_HOVERED", ImGuiCol_ButtonHovered)
    .value("BUTTON_ACTIVE", ImGuiCol_ButtonActive)
    .value("HEADER", ImGuiCol_Header,
           "Header* colors are used for `collapsing_header`, `tree_node`, "
           "`selectable`, `menu_item`")
    .value("HEADER_HOVERED", ImGuiCol_HeaderHovered)
    .value("HEADER_ACTIVE", ImGuiCol_HeaderActive)
    .value("SEPARATOR", ImGuiCol_Separator)
    .value("SEPARATOR_HOVERED", ImGuiCol_SeparatorHovered)
    .value("SEPARATOR_ACTIVE", ImGuiCol_SeparatorActive)
    .value("RESIZE_GRIP", ImGuiCol_ResizeGrip,
           "Resize grip in lower-right and lower-left corners of windows.")
    .value("RESIZE_GRIP_HOVERED", ImGuiCol_ResizeGripHovered)
    .value("RESIZE_GRIP_ACTIVE", ImGuiCol_ResizeGripActive)
    .value("TAB_HOVERED", ImGuiCol_TabHovered, "Tab background, when hovered")
    .value("TAB", ImGuiCol_Tab,
           "Tab background, when tab-bar is focused & tab is unselected")
    .value("TAB_SELECTED", ImGuiCol_TabSelected,
           "Tab background, when tab-bar is focused & tab is selected")
    .value("TAB_SELECTED_OVERLINE", ImGuiCol_TabSelectedOverline,
           "Tab horizontal overline, when tab-bar is focused & tab is selected")
    .value("TAB_DIMMED", ImGuiCol_TabDimmed,
           "Tab background, when tab-bar is unfocused & tab is unselected")
    .value("TAB_DIMMED_SELECTED", ImGuiCol_TabDimmedSelected,
           "Tab background, when tab-bar is unfocused & tab is selected")
    .value("TAB_DIMMED_SELECTED_OVERLINE", ImGuiCol_TabDimmedSelectedOverline)
    .value("PLOT_LINES", ImGuiCol_PlotLines)
    .value("PLOT_LINES_HOVERED", ImGuiCol_PlotLinesHovered)
    .value("PLOT_HISTOGRAM", ImGuiCol_PlotHistogram)
    .value("PLOT_HISTOGRAM_HOVERED", ImGuiCol_PlotHistogramHovered)
    .value("TABLE_HEADER_BG", ImGuiCol_TableHeaderBg, "Table header background")
    .value("TABLE_BORDER_STRONG", ImGuiCol_TableBorderStrong,
           "Table outer and header borders (prefer using Alpha=1.0 here)")
    .value("TABLE_BORDER_LIGHT", ImGuiCol_TableBorderLight,
           "Table inner borders (prefer using Alpha=1.0 here)")
    .value("TABLE_ROW_BG", ImGuiCol_TableRowBg,
           "Table row background (even rows)")
    .value("TABLE_ROW_BG_ALT", ImGuiCol_TableRowBgAlt,
           "Table row background (odd rows)")
    .value("TEXT_LINK", ImGuiCol_TextLink, "Hyperlink color")
    .value("TEXT_SELECTED_BG", ImGuiCol_TextSelectedBg)
    .value("DRAG_DROP_TARGET", ImGuiCol_DragDropTarget,
           "Rectangle highlighting a drop target")
    .value(
        "NAV_CURSOR", ImGuiCol_NavCursor,
        "Color of keyboard/gamepad navigation cursor/rectangle, when visible")
    .value("NAV_WINDOWING_HIGHLIGHT", ImGuiCol_NavWindowingHighlight,
           "Highlight window when using CTRL+TAB")
    .value("NAV_WINDOWING_DIM_BG", ImGuiCol_NavWindowingDimBg,
           "Darken/colorize entire screen behind the CTRL+TAB window list, "
           "when active")
    .value("MODAL_WINDOW_DIM_BG", ImGuiCol_ModalWindowDimBg,
           "Darken/colorize entire screen behind a modal window, when one is "
           "active")
    .value("COUNT", ImGuiCol_COUNT);
nb::enum_<ImGuiDir>(m, "Dir", nb::is_arithmetic())
    .value("NONE", ImGuiDir_None)
    .value("LEFT", ImGuiDir_Left)
    .value("RIGHT", ImGuiDir_Right)
    .value("UP", ImGuiDir_Up)
    .value("DOWN", ImGuiDir_Down)
    .value("COUNT", ImGuiDir_COUNT);
nb::enum_<ImGuiStyleVar_>(m, "StyleVar", nb::is_arithmetic())
    .value("ALPHA", ImGuiStyleVar_Alpha, "Float     Alpha")
    .value("DISABLED_ALPHA", ImGuiStyleVar_DisabledAlpha,
           "Float     DisabledAlpha")
    .value("WINDOW_PADDING", ImGuiStyleVar_WindowPadding,
           "ImVec2    WindowPadding")
    .value("WINDOW_ROUNDING", ImGuiStyleVar_WindowRounding,
           "Float     WindowRounding")
    .value("WINDOW_BORDER_SIZE", ImGuiStyleVar_WindowBorderSize,
           "Float     WindowBorderSize")
    .value("WINDOW_MIN_SIZE", ImGuiStyleVar_WindowMinSize,
           "ImVec2    WindowMinSize")
    .value("WINDOW_TITLE_ALIGN", ImGuiStyleVar_WindowTitleAlign,
           "ImVec2    WindowTitleAlign")
    .value("CHILD_ROUNDING", ImGuiStyleVar_ChildRounding,
           "Float     ChildRounding")
    .value("CHILD_BORDER_SIZE", ImGuiStyleVar_ChildBorderSize,
           "Float     ChildBorderSize")
    .value("POPUP_ROUNDING", ImGuiStyleVar_PopupRounding,
           "Float     PopupRounding")
    .value("POPUP_BORDER_SIZE", ImGuiStyleVar_PopupBorderSize,
           "Float     PopupBorderSize")
    .value("FRAME_PADDING", ImGuiStyleVar_FramePadding,
           "ImVec2    FramePadding")
    .value("FRAME_ROUNDING", ImGuiStyleVar_FrameRounding,
           "Float     FrameRounding")
    .value("FRAME_BORDER_SIZE", ImGuiStyleVar_FrameBorderSize,
           "Float     FrameBorderSize")
    .value("ITEM_SPACING", ImGuiStyleVar_ItemSpacing, "ImVec2    ItemSpacing")
    .value("ITEM_INNER_SPACING", ImGuiStyleVar_ItemInnerSpacing,
           "ImVec2    ItemInnerSpacing")
    .value("INDENT_SPACING", ImGuiStyleVar_IndentSpacing,
           "Float     IndentSpacing")
    .value("CELL_PADDING", ImGuiStyleVar_CellPadding, "ImVec2    CellPadding")
    .value("SCROLLBAR_SIZE", ImGuiStyleVar_ScrollbarSize,
           "Float     ScrollbarSize")
    .value("SCROLLBAR_ROUNDING", ImGuiStyleVar_ScrollbarRounding,
           "Float     ScrollbarRounding")
    .value("GRAB_MIN_SIZE", ImGuiStyleVar_GrabMinSize, "Float     GrabMinSize")
    .value("GRAB_ROUNDING", ImGuiStyleVar_GrabRounding,
           "Float     GrabRounding")
    .value("IMAGE_BORDER_SIZE", ImGuiStyleVar_ImageBorderSize,
           "Float     ImageBorderSize")
    .value("TAB_ROUNDING", ImGuiStyleVar_TabRounding, "Float     TabRounding")
    .value("TAB_BORDER_SIZE", ImGuiStyleVar_TabBorderSize,
           "Float     TabBorderSize")
    .value("TAB_BAR_BORDER_SIZE", ImGuiStyleVar_TabBarBorderSize,
           "Float     TabBarBorderSize")
    .value("TAB_BAR_OVERLINE_SIZE", ImGuiStyleVar_TabBarOverlineSize,
           "Float     TabBarOverlineSize")
    .value("TABLE_ANGLED_HEADERS_ANGLE", ImGuiStyleVar_TableAngledHeadersAngle,
           "Float     TableAngledHeadersAngle")
    .value("TABLE_ANGLED_HEADERS_TEXT_ALIGN",
           ImGuiStyleVar_TableAngledHeadersTextAlign,
           "ImVec2  TableAngledHeadersTextAlign")
    .value("BUTTON_TEXT_ALIGN", ImGuiStyleVar_ButtonTextAlign,
           "ImVec2    ButtonTextAlign")
    .value("SELECTABLE_TEXT_ALIGN", ImGuiStyleVar_SelectableTextAlign,
           "ImVec2    SelectableTextAlign")
    .value("SEPARATOR_TEXT_BORDER_SIZE", ImGuiStyleVar_SeparatorTextBorderSize,
           "Float     SeparatorTextBorderSize")
    .value("SEPARATOR_TEXT_ALIGN", ImGuiStyleVar_SeparatorTextAlign,
           "ImVec2    SeparatorTextAlign")
    .value("SEPARATOR_TEXT_PADDING", ImGuiStyleVar_SeparatorTextPadding,
           "ImVec2    SeparatorTextPadding")
    .value("COUNT", ImGuiStyleVar_COUNT);
nb::enum_<ImGuiTableBgTarget_>(m, "TableBgTarget", nb::is_arithmetic())
    .value("NONE", ImGuiTableBgTarget_None)
    .value("ROW_BG0", ImGuiTableBgTarget_RowBg0,
           "Set row background color 0 (generally used for background, "
           "automatically set when `TableFlags.ROW_BG` is used)")
    .value("ROW_BG1", ImGuiTableBgTarget_RowBg1,
           "Set row background color 1 (generally used for selection marking)")
    .value("CELL_BG", ImGuiTableBgTarget_CellBg,
           "Set cell background color (top-most color)");
nb::enum_<ImGuiKey>(m, "Key", nb::is_arithmetic())
    .value("KEY_NONE", ImGuiKey_None)
    .value("KEY_NAMED_KEY_BEGIN", ImGuiKey_NamedKey_BEGIN)
    .value("KEY_TAB", ImGuiKey_Tab)
    .value("KEY_LEFT_ARROW", ImGuiKey_LeftArrow)
    .value("KEY_RIGHT_ARROW", ImGuiKey_RightArrow)
    .value("KEY_UP_ARROW", ImGuiKey_UpArrow)
    .value("KEY_DOWN_ARROW", ImGuiKey_DownArrow)
    .value("KEY_PAGE_UP", ImGuiKey_PageUp)
    .value("KEY_PAGE_DOWN", ImGuiKey_PageDown)
    .value("KEY_HOME", ImGuiKey_Home)
    .value("KEY_END", ImGuiKey_End)
    .value("KEY_INSERT", ImGuiKey_Insert)
    .value("KEY_DELETE", ImGuiKey_Delete)
    .value("KEY_BACKSPACE", ImGuiKey_Backspace)
    .value("KEY_SPACE", ImGuiKey_Space)
    .value("KEY_ENTER", ImGuiKey_Enter)
    .value("KEY_ESCAPE", ImGuiKey_Escape)
    .value("KEY_LEFT_CTRL", ImGuiKey_LeftCtrl)
    .value("KEY_LEFT_SHIFT", ImGuiKey_LeftShift)
    .value("KEY_LEFT_ALT", ImGuiKey_LeftAlt)
    .value("KEY_LEFT_SUPER", ImGuiKey_LeftSuper)
    .value("KEY_RIGHT_CTRL", ImGuiKey_RightCtrl)
    .value("KEY_RIGHT_SHIFT", ImGuiKey_RightShift)
    .value("KEY_RIGHT_ALT", ImGuiKey_RightAlt)
    .value("KEY_RIGHT_SUPER", ImGuiKey_RightSuper)
    .value("KEY_MENU", ImGuiKey_Menu)
    .value("KEY_0", ImGuiKey_0)
    .value("KEY_1", ImGuiKey_1)
    .value("KEY_2", ImGuiKey_2)
    .value("KEY_3", ImGuiKey_3)
    .value("KEY_4", ImGuiKey_4)
    .value("KEY_5", ImGuiKey_5)
    .value("KEY_6", ImGuiKey_6)
    .value("KEY_7", ImGuiKey_7)
    .value("KEY_8", ImGuiKey_8)
    .value("KEY_9", ImGuiKey_9)
    .value("KEY_A", ImGuiKey_A)
    .value("KEY_B", ImGuiKey_B)
    .value("KEY_C", ImGuiKey_C)
    .value("KEY_D", ImGuiKey_D)
    .value("KEY_E", ImGuiKey_E)
    .value("KEY_F", ImGuiKey_F)
    .value("KEY_G", ImGuiKey_G)
    .value("KEY_H", ImGuiKey_H)
    .value("KEY_I", ImGuiKey_I)
    .value("KEY_J", ImGuiKey_J)
    .value("KEY_K", ImGuiKey_K)
    .value("KEY_L", ImGuiKey_L)
    .value("KEY_M", ImGuiKey_M)
    .value("KEY_N", ImGuiKey_N)
    .value("KEY_O", ImGuiKey_O)
    .value("KEY_P", ImGuiKey_P)
    .value("KEY_Q", ImGuiKey_Q)
    .value("KEY_R", ImGuiKey_R)
    .value("KEY_S", ImGuiKey_S)
    .value("KEY_T", ImGuiKey_T)
    .value("KEY_U", ImGuiKey_U)
    .value("KEY_V", ImGuiKey_V)
    .value("KEY_W", ImGuiKey_W)
    .value("KEY_X", ImGuiKey_X)
    .value("KEY_Y", ImGuiKey_Y)
    .value("KEY_Z", ImGuiKey_Z)
    .value("KEY_F1", ImGuiKey_F1)
    .value("KEY_F2", ImGuiKey_F2)
    .value("KEY_F3", ImGuiKey_F3)
    .value("KEY_F4", ImGuiKey_F4)
    .value("KEY_F5", ImGuiKey_F5)
    .value("KEY_F6", ImGuiKey_F6)
    .value("KEY_F7", ImGuiKey_F7)
    .value("KEY_F8", ImGuiKey_F8)
    .value("KEY_F9", ImGuiKey_F9)
    .value("KEY_F10", ImGuiKey_F10)
    .value("KEY_F11", ImGuiKey_F11)
    .value("KEY_F12", ImGuiKey_F12)
    .value("KEY_F13", ImGuiKey_F13)
    .value("KEY_F14", ImGuiKey_F14)
    .value("KEY_F15", ImGuiKey_F15)
    .value("KEY_F16", ImGuiKey_F16)
    .value("KEY_F17", ImGuiKey_F17)
    .value("KEY_F18", ImGuiKey_F18)
    .value("KEY_F19", ImGuiKey_F19)
    .value("KEY_F20", ImGuiKey_F20)
    .value("KEY_F21", ImGuiKey_F21)
    .value("KEY_F22", ImGuiKey_F22)
    .value("KEY_F23", ImGuiKey_F23)
    .value("KEY_F24", ImGuiKey_F24)
    .value("KEY_APOSTROPHE", ImGuiKey_Apostrophe)
    .value("KEY_COMMA", ImGuiKey_Comma)
    .value("KEY_MINUS", ImGuiKey_Minus)
    .value("KEY_PERIOD", ImGuiKey_Period)
    .value("KEY_SLASH", ImGuiKey_Slash)
    .value("KEY_SEMICOLON", ImGuiKey_Semicolon)
    .value("KEY_EQUAL", ImGuiKey_Equal)
    .value("KEY_LEFT_BRACKET", ImGuiKey_LeftBracket)
    .value("KEY_BACKSLASH", ImGuiKey_Backslash)
    .value("KEY_RIGHT_BRACKET", ImGuiKey_RightBracket)
    .value("KEY_GRAVE_ACCENT", ImGuiKey_GraveAccent)
    .value("KEY_CAPS_LOCK", ImGuiKey_CapsLock)
    .value("KEY_SCROLL_LOCK", ImGuiKey_ScrollLock)
    .value("KEY_NUM_LOCK", ImGuiKey_NumLock)
    .value("KEY_PRINT_SCREEN", ImGuiKey_PrintScreen)
    .value("KEY_PAUSE", ImGuiKey_Pause)
    .value("KEY_KEYPAD0", ImGuiKey_Keypad0)
    .value("KEY_KEYPAD1", ImGuiKey_Keypad1)
    .value("KEY_KEYPAD2", ImGuiKey_Keypad2)
    .value("KEY_KEYPAD3", ImGuiKey_Keypad3)
    .value("KEY_KEYPAD4", ImGuiKey_Keypad4)
    .value("KEY_KEYPAD5", ImGuiKey_Keypad5)
    .value("KEY_KEYPAD6", ImGuiKey_Keypad6)
    .value("KEY_KEYPAD7", ImGuiKey_Keypad7)
    .value("KEY_KEYPAD8", ImGuiKey_Keypad8)
    .value("KEY_KEYPAD9", ImGuiKey_Keypad9)
    .value("KEY_KEYPAD_DECIMAL", ImGuiKey_KeypadDecimal)
    .value("KEY_KEYPAD_DIVIDE", ImGuiKey_KeypadDivide)
    .value("KEY_KEYPAD_MULTIPLY", ImGuiKey_KeypadMultiply)
    .value("KEY_KEYPAD_SUBTRACT", ImGuiKey_KeypadSubtract)
    .value("KEY_KEYPAD_ADD", ImGuiKey_KeypadAdd)
    .value("KEY_KEYPAD_ENTER", ImGuiKey_KeypadEnter)
    .value("KEY_KEYPAD_EQUAL", ImGuiKey_KeypadEqual)
    .value("KEY_APP_BACK", ImGuiKey_AppBack)
    .value("KEY_APP_FORWARD", ImGuiKey_AppForward)
    .value("KEY_OEM102", ImGuiKey_Oem102)
    .value("KEY_GAMEPAD_START", ImGuiKey_GamepadStart)
    .value("KEY_GAMEPAD_BACK", ImGuiKey_GamepadBack)
    .value("KEY_GAMEPAD_FACE_LEFT", ImGuiKey_GamepadFaceLeft)
    .value("KEY_GAMEPAD_FACE_RIGHT", ImGuiKey_GamepadFaceRight)
    .value("KEY_GAMEPAD_FACE_UP", ImGuiKey_GamepadFaceUp)
    .value("KEY_GAMEPAD_FACE_DOWN", ImGuiKey_GamepadFaceDown)
    .value("KEY_GAMEPAD_DPAD_LEFT", ImGuiKey_GamepadDpadLeft)
    .value("KEY_GAMEPAD_DPAD_RIGHT", ImGuiKey_GamepadDpadRight)
    .value("KEY_GAMEPAD_DPAD_UP", ImGuiKey_GamepadDpadUp)
    .value("KEY_GAMEPAD_DPAD_DOWN", ImGuiKey_GamepadDpadDown)
    .value("KEY_GAMEPAD_L1", ImGuiKey_GamepadL1)
    .value("KEY_GAMEPAD_R1", ImGuiKey_GamepadR1)
    .value("KEY_GAMEPAD_L2", ImGuiKey_GamepadL2)
    .value("KEY_GAMEPAD_R2", ImGuiKey_GamepadR2)
    .value("KEY_GAMEPAD_L3", ImGuiKey_GamepadL3)
    .value("KEY_GAMEPAD_R3", ImGuiKey_GamepadR3)
    .value("KEY_GAMEPAD_L_STICK_LEFT", ImGuiKey_GamepadLStickLeft)
    .value("KEY_GAMEPAD_L_STICK_RIGHT", ImGuiKey_GamepadLStickRight)
    .value("KEY_GAMEPAD_L_STICK_UP", ImGuiKey_GamepadLStickUp)
    .value("KEY_GAMEPAD_L_STICK_DOWN", ImGuiKey_GamepadLStickDown)
    .value("KEY_GAMEPAD_R_STICK_LEFT", ImGuiKey_GamepadRStickLeft)
    .value("KEY_GAMEPAD_R_STICK_RIGHT", ImGuiKey_GamepadRStickRight)
    .value("KEY_GAMEPAD_R_STICK_UP", ImGuiKey_GamepadRStickUp)
    .value("KEY_GAMEPAD_R_STICK_DOWN", ImGuiKey_GamepadRStickDown)
    .value("KEY_MOUSE_LEFT", ImGuiKey_MouseLeft)
    .value("KEY_MOUSE_RIGHT", ImGuiKey_MouseRight)
    .value("KEY_MOUSE_MIDDLE", ImGuiKey_MouseMiddle)
    .value("KEY_MOUSE_X1", ImGuiKey_MouseX1)
    .value("KEY_MOUSE_X2", ImGuiKey_MouseX2)
    .value("KEY_MOUSE_WHEEL_X", ImGuiKey_MouseWheelX)
    .value("KEY_MOUSE_WHEEL_Y", ImGuiKey_MouseWheelY)
    .value("KEY_RESERVED_FOR_MOD_CTRL", ImGuiKey_ReservedForModCtrl)
    .value("KEY_RESERVED_FOR_MOD_SHIFT", ImGuiKey_ReservedForModShift)
    .value("KEY_RESERVED_FOR_MOD_ALT", ImGuiKey_ReservedForModAlt)
    .value("KEY_RESERVED_FOR_MOD_SUPER", ImGuiKey_ReservedForModSuper)
    .value("KEY_NAMED_KEY_END", ImGuiKey_NamedKey_END)
    .value("MOD_NONE", ImGuiMod_None)
    .value("MOD_CTRL", ImGuiMod_Ctrl)
    .value("MOD_SHIFT", ImGuiMod_Shift)
    .value("MOD_ALT", ImGuiMod_Alt)
    .value("MOD_SUPER", ImGuiMod_Super)
    .value("MOD_MASK_", ImGuiMod_Mask_)
    .value("KEY_NAMED_KEY_COUNT", ImGuiKey_NamedKey_COUNT);
