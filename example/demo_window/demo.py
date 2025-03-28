
import math
from typing import Any
import warnings

from slimgui import imgui
from slimgui.imgui import WindowFlags

from .types import State
from .utils import help_marker
from . import widgets, widgets2, layout, property_editor, shapes

st = State()

def show_demo_window(show_window: bool, texture: dict[str, Any]):
    if st.show_app_main_menu_bar:
        show_example_app_main_menu_bar()

    if st.show_app_layout:
        layout.show_example_app_layout(st)

    if st.show_app_property_editor:
        property_editor.show_example_app_property_editor(st)

    if st.show_app_simple_overlay:
        show_example_app_simple_overlay(st)

    if st.show_tool_metrics:
        st.show_tool_metrics = imgui.show_metrics_window(closable=True)

    if st.show_tool_debug_log:
        st.show_tool_debug_log = imgui.show_debug_log_window(closable=True)

    if st.show_tool_id_stack_tool:
        st.show_tool_id_stack_tool = imgui.show_id_stack_tool_window(closable=True)

    if st.show_tool_style_editor:
        _, st.show_tool_style_editor = imgui.begin("Dear ImGui Style Editor", closable=True)
        imgui.show_style_editor()
        imgui.end()

    if st.show_tool_about:
        st.show_tool_about = imgui.show_about_window(closable=True)

    if st.show_native_imgui_demo_window:
        st.show_native_imgui_demo_window = imgui.show_demo_window(closable=True)

    no_menu = st.no_menu
    window_flags = imgui.WindowFlags.NONE
    if st.no_titlebar:
        window_flags |= imgui.WindowFlags.NO_TITLE_BAR
    if st.no_scrollbar:
        window_flags |= imgui.WindowFlags.NO_SCROLLBAR
    if not no_menu:
        window_flags |= imgui.WindowFlags.MENU_BAR
    if st.no_move:
        window_flags |= imgui.WindowFlags.NO_MOVE
    if st.no_resize:
        window_flags |= imgui.WindowFlags.NO_RESIZE
    if st.no_collapse:
        window_flags |= imgui.WindowFlags.NO_COLLAPSE
    if st.no_nav:
        window_flags |= imgui.WindowFlags.NO_NAV
    if st.no_background:
        window_flags |= imgui.WindowFlags.NO_BACKGROUND
    if st.no_bring_to_front:
        window_flags |= imgui.WindowFlags.NO_BRING_TO_FRONT_ON_FOCUS
    if st.unsaved_document:
        window_flags |= imgui.WindowFlags.UNSAVED_DOCUMENT

    closable = show_window
    if st.no_close:
        closable = False

    main_viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos((main_viewport.work_pos[0] + 250, main_viewport.work_pos[1] + 20), imgui.Cond.FIRST_USE_EVER)
    imgui.set_next_window_size((550, 680), imgui.Cond.FIRST_USE_EVER)

    visible, show_window = imgui.begin("Python mini-port of Dear ImGui Demo", closable=closable, flags=window_flags)
    if not visible:
        imgui.end()
        return show_window

    imgui.push_item_width(imgui.get_font_size() * -12)

    if imgui.begin_menu_bar():
        if imgui.begin_menu("Menu"):
            show_example_menu_file()
            imgui.end_menu()

        if imgui.begin_menu("Examples"):
            _, st.show_app_main_menu_bar = imgui.menu_item("Main menu bar", selected=st.show_app_main_menu_bar)
            imgui.separator_text("Mini apps")
            _, st.show_app_console = imgui.menu_item("Console", selected=st.show_app_console)
            _, st.show_app_custom_rendering = imgui.menu_item("Custom rendering", selected=st.show_app_custom_rendering)
            _, st.show_app_documents = imgui.menu_item("Documents", selected=st.show_app_documents)
            _, st.show_app_log = imgui.menu_item("Log", selected=st.show_app_log)
            _, st.show_app_property_editor = imgui.menu_item("Property editor", selected=st.show_app_property_editor)
            _, st.show_app_layout = imgui.menu_item("Simple layout", selected=st.show_app_layout)
            _, st.show_app_simple_overlay = imgui.menu_item("Simple overlay", selected=st.show_app_simple_overlay)

            imgui.separator_text("Concepts")
            _, st.show_app_auto_resize = imgui.menu_item("Auto-resizing window", selected=st.show_app_auto_resize)
            _, st.show_app_constrained_resize = imgui.menu_item("Constrained-resizing window", selected=st.show_app_constrained_resize)
            _, st.show_app_fullscreen = imgui.menu_item("Fullscreen window", selected=st.show_app_fullscreen)
            _, st.show_app_window_titles = imgui.menu_item("Manipulating window titles", selected=st.show_app_window_titles)
            imgui.end_menu()

        if imgui.begin_menu("Tools"):
            _, st.show_tool_metrics = imgui.menu_item("Metrics/Debugger", selected=st.show_tool_metrics)
            _, st.show_tool_debug_log = imgui.menu_item("Debug Log", selected=st.show_tool_debug_log)
            _, st.show_tool_id_stack_tool = imgui.menu_item("ID Stack Tool", selected=st.show_tool_id_stack_tool)
            _, st.show_tool_style_editor = imgui.menu_item("Style Editor", selected=st.show_tool_style_editor)
            _, st.show_tool_about = imgui.menu_item("About Dear ImGui", selected=st.show_tool_about)
            imgui.separator()
            _, st.show_native_imgui_demo_window = imgui.menu_item("ImGui Native Demo Window", selected=st.show_native_imgui_demo_window)
            imgui.end_menu()
        imgui.end_menu_bar()

    # ----

    imgui.text(f"dear imgui says hello! ({imgui.IMGUI_VERSION}) ({imgui.IMGUI_VERSION_NUM})")
    imgui.spacing()

#   IMGUI_DEMO_MARKER("Help");
    if imgui.collapsing_header("Help")[0]:
        imgui.separator_text("ABOUT THIS DEMO:")
        imgui.bullet_text("Sections below are demonstrating many aspects of the library.")
        imgui.bullet_text("The \"Examples\" menu above leads to more demo contents.")
        imgui.bullet_text("The \"Tools\" menu above gives access to: About Box, Style Editor,\n"
                          "and Metrics/Debugger (general purpose Dear ImGui debugging tool).")
        imgui.separator_text("PROGRAMMER GUIDE:")
        imgui.bullet_text("See the ShowDemoWindow() code in imgui_demo.cpp. <- you are here!")
        imgui.bullet_text("See comments in imgui.cpp.")
        imgui.bullet_text("See example applications in the examples/ folder.")
        imgui.bullet_text("Read the FAQ at https://www.dearimgui.com/faq/")
        imgui.bullet_text("Set 'io.ConfigFlags |= NavEnableKeyboard' for keyboard controls.")
        imgui.bullet_text("Set 'io.ConfigFlags |= NavEnableGamepad' for gamepad controls.")
        imgui.separator_text("USER GUIDE:")
        imgui.show_user_guide()
#     }

    if imgui.collapsing_header("Configuration")[0]:
        io = imgui.get_io()
        if imgui.tree_node("Configuration##2"):
            imgui.separator_text("General")
            config_flags = int(io.config_flags)
            _, config_flags = imgui.checkbox_flags("io.ConfigFlags: NAV_ENABLE_KEYBOARD", config_flags, imgui.ConfigFlags.NAV_ENABLE_KEYBOARD)
            imgui.same_line(); help_marker("Enable keyboard controls.")
            _, config_flags = imgui.checkbox_flags("io.ConfigFlags: NAV_ENABLE_GAMEPAD", config_flags, imgui.ConfigFlags.NAV_ENABLE_GAMEPAD)
            imgui.same_line(); help_marker("Enable gamepad controls. Require backend to set io.BackendFlags |= ImGuiBackendFlags_HasGamepad.\n\nRead instructions in imgui.cpp for details.")
            _, config_flags = imgui.checkbox_flags("io.ConfigFlags: NO_MOUSE", config_flags, imgui.ConfigFlags.NO_MOUSE)
            if (config_flags & imgui.ConfigFlags.NO_MOUSE) != 0:
                if math.fmod(imgui.get_time(), 0.40) < 0.2:
                    imgui.same_line()
                    imgui.text("<<PRESS SPACE TO DISABLE>>")
                    if imgui.is_key_pressed(imgui.Key.KEY_SPACE):
                        config_flags &= ~imgui.ConfigFlags.NO_MOUSE
            _, config_flags = imgui.checkbox_flags("io.ConfigFlags: NO_MOUSE_CURSOR_CHANGE", config_flags, imgui.ConfigFlags.NO_MOUSE_CURSOR_CHANGE)
            io.config_flags = imgui.ConfigFlags(config_flags)
            imgui.same_line(); help_marker("Instruct backend to not alter mouse cursor shape and visibility.")
            imgui.tree_pop()
            imgui.spacing()

            _, io.config_input_trickle_event_queue = imgui.checkbox("io.config_input_trickle_event_queue", io.config_input_trickle_event_queue)
            imgui.same_line(); help_marker("Enable input queue trickling: some types of events submitted during the same frame (e.g. button down + up) will be spread over multiple frames, improving interactions with low framerates.")
            _, io.mouse_draw_cursor = imgui.checkbox("io.mouse_draw_cursor", io.mouse_draw_cursor)
            imgui.same_line(); help_marker("Instruct Dear ImGui to render a mouse cursor itself. Note that a mouse cursor rendered via your application GPU rendering path will feel more laggy than hardware cursor, but will be more in sync with your other visuals.\n\nSome desktop applications may use both kinds of cursors (e.g. enable software cursor only when resizing/dragging something).")

            imgui.separator_text("Docking"); imgui.same_line(); help_marker("TBD docking currently disabled")

            imgui.separator_text("Widgets")
            _, io.config_input_text_cursor_blink = imgui.checkbox("io.config_input_text_cursor_blink", io.config_input_text_cursor_blink)
            imgui.same_line(); help_marker("Enable blinking cursor (optional as some users consider it to be distracting).")
            _, io.config_input_text_enter_keep_active = imgui.checkbox("io.config_input_text_enter_keep_active", io.config_input_text_enter_keep_active)
            imgui.same_line(); help_marker("Pressing Enter will keep item active and select contents (single-line only).")
            _, io.config_drag_click_to_input_text = imgui.checkbox("io.config_drag_click_to_input_text", io.config_drag_click_to_input_text)
            imgui.same_line(); help_marker("Enable turning DragXXX widgets into text input with a simple mouse click-release (without moving).")
            _, io.config_windows_resize_from_edges = imgui.checkbox("io.config_windows_resize_from_edges", io.config_windows_resize_from_edges)
            imgui.same_line(); help_marker("Enable resizing of windows from their edges and from the lower-left corner.\nThis requires (io.BackendFlags & ImGuiBackendFlags_HasMouseCursors) because it needs mouse cursor feedback.")
            _, io.config_windows_move_from_title_bar_only = imgui.checkbox("io.config_windows_move_from_title_bar_only", io.config_windows_move_from_title_bar_only)
            _, io.config_mac_osx_behaviors = imgui.checkbox("io.config_mac_osx_behaviors", io.config_mac_osx_behaviors)
            imgui.text("Also see Style->Rendering for rendering options.")
            imgui.separator_text("Debug")
            imgui.text("TODO")

        if imgui.tree_node("Backend Flags"):
            help_marker(
                "Those flags are set by the backends (imgui_impl_xxx files) to specify their capabilities.\n"
                "Here we expose them as read-only fields to avoid breaking interactions with your backend.")

            imgui.begin_disabled()

            backend_flags_int = int(io.config_flags)
            _, backend_flags_int = imgui.checkbox_flags("io.BackendFlags: HAS_GAMEPAD", backend_flags_int, imgui.BackendFlags.HAS_GAMEPAD)
            _, backend_flags_int = imgui.checkbox_flags("io.BackendFlags: HAS_MOUSE_CURSORS", backend_flags_int, imgui.BackendFlags.HAS_MOUSE_CURSORS)
            _, backend_flags_int = imgui.checkbox_flags("io.BackendFlags: HAS_SET_MOUSE_POS", backend_flags_int, imgui.BackendFlags.HAS_SET_MOUSE_POS)
            _, backend_flags_int = imgui.checkbox_flags("io.BackendFlags: RENDERER_HAS_VTX_OFFSET", backend_flags_int, imgui.BackendFlags.RENDERER_HAS_VTX_OFFSET)
            io.backend_flags = imgui.BackendFlags(backend_flags_int)

            imgui.end_disabled()

            imgui.tree_pop()
            imgui.spacing()

        if imgui.tree_node("Style"):
            help_marker("The same contents can be accessed in 'Tools->Style Editor' or by calling the ShowStyleEditor() function.")
            imgui.show_style_editor()
            imgui.tree_pop()
            imgui.spacing()

        if imgui.tree_node("Capture/Logging"):
            help_marker(
                "The logging API redirects all text output so you can easily capture the content of "
                "a window or a block. Tree nodes can be automatically expanded.\n"
                "Try opening any of the contents below in this window and then click one of the \"Log To\" button.")
            imgui.log_buttons()
            help_marker("You can also call ImGui::LogText() to output directly to the log without a visual output.")
            if imgui.button("Copy \"Hello, world!\" to clipboard"):
                imgui.log_to_clipboard()
                imgui.log_text("Hello, world!")
                imgui.log_finish()
            imgui.tree_pop()

    if imgui.collapsing_header("Window options")[0]:
        if imgui.begin_table("split", 3):
            imgui.table_next_column()
            _, st.no_titlebar = imgui.checkbox("No titlebar", st.no_titlebar)
            imgui.table_next_column()
            _, st.no_scrollbar = imgui.checkbox("No scrollbar", st.no_scrollbar)
            imgui.table_next_column()
            _, st.no_menu = imgui.checkbox("No menu", st.no_menu)
            imgui.table_next_column()
            _, st.no_move = imgui.checkbox("No move", st.no_move)
            imgui.table_next_column()
            _, st.no_resize = imgui.checkbox("No resize", st.no_resize)
            imgui.table_next_column()
            _, st.no_collapse = imgui.checkbox("No collapse", st.no_collapse)
            imgui.table_next_column()
            _, st.no_close = imgui.checkbox("No close", st.no_close)
            imgui.table_next_column()
            _, st.no_nav = imgui.checkbox("No nav", st.no_nav)
            imgui.table_next_column()
            _, st.no_background = imgui.checkbox("No background", st.no_background)
            imgui.table_next_column()
            _, st.no_bring_to_front = imgui.checkbox("No bring to front", st.no_bring_to_front)
            imgui.table_next_column()
            _, st.no_docking = imgui.checkbox("No docking", st.no_docking)
            imgui.table_next_column()
            _, st.unsaved_document = imgui.checkbox("Unsaved document", st.unsaved_document)
            imgui.end_table()

#     // All demo contents
    widgets.show_demo_window_widgets(st)
    widgets2.show()
    shapes.show(texture['id'])

#     ShowDemoWindowLayout();
#     ShowDemoWindowPopups();
#     ShowDemoWindowTables();
#     ShowDemoWindowInputs();

#     // End of ShowDemoWindow()
#     ImGui::PopItemWidth();
    imgui.end()
    return show_window


def show_example_app_main_menu_bar():
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File"):
            show_example_menu_file()
            imgui.end_menu()

        if imgui.begin_menu("Edit"):
            if imgui.menu_item("Undo", "CTRL+Z")[0]:
                pass
            if imgui.menu_item("Redo", "CTRL+Y", False, False)[0]:
                pass
            imgui.separator()
            if imgui.menu_item("Cut", "CTRL+X")[0]:
                pass
            if imgui.menu_item("Copy", "CTRL+C")[0]:
                pass
            if imgui.menu_item("Paste", "CTRL+V")[0]:
                pass
            imgui.end_menu()
        imgui.end_main_menu_bar()


def show_example_menu_file():
    warnings.warn("unimplemented")
    pass

# //-----------------------------------------------------------------------------
# // [SECTION] Example App: Simple overlay / ShowExampleAppSimpleOverlay()
# //-----------------------------------------------------------------------------

_location = 0
def show_example_app_simple_overlay(st: State):
    global _location

    window_flags = WindowFlags.NO_DECORATION | WindowFlags.ALWAYS_AUTO_RESIZE | WindowFlags.NO_SAVED_SETTINGS | WindowFlags.NO_FOCUS_ON_APPEARING | WindowFlags.NO_NAV
    if _location >= 0:
        pad = 10.0
        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos
        work_size = viewport.work_size
        wpos_x = (work_pos[0] + work_size[0] - pad) if _location & 1 else work_pos[0] + pad
        wpos_y = (work_pos[1] + work_size[1] - pad) if _location & 2 else work_pos[1] + pad
        wpos_pivot_x = 1 if _location & 1 else 0
        wpos_pivot_y = 1 if _location & 2 else 0

        imgui.set_next_window_pos((wpos_x, wpos_y), imgui.Cond.ALWAYS, (wpos_pivot_x, wpos_pivot_y))
        # TODO imgui.set_next_window_viewport??
        window_flags |= WindowFlags.NO_MOVE
    elif _location == -2:
        imgui.set_next_window_pos(imgui.get_main_viewport().get_center(), imgui.Cond.ALWAYS, (0.5, 0.5))

    imgui.set_next_window_bg_alpha(0.35)
    visible, st.show_app_simple_overlay = imgui.begin("Example: Simple overlay", st.show_app_simple_overlay, window_flags)
    if visible:
        imgui.text('Simple overlay\n(right-click to change position)')
        imgui.separator()

        if imgui.is_mouse_pos_valid():
            pos = imgui.get_mouse_pos()
            imgui.text(f'Mouse Position: ({pos[0]:.1f},{pos[1]:.1f})')
        else:
            imgui.text('Mouse Position: <invalid>')

        if imgui.begin_popup_context_window():
            if imgui.menu_item('Custom', None, _location == -1)[0]:
                _location = -1
            if imgui.menu_item('Center', None, _location == -2)[0]:
                _location = -2
            if imgui.menu_item('Top-left', None, _location == 0)[0]:
                _location = 0
            if imgui.menu_item('Top-right', None, _location == 1)[0]:
                _location = 1
            if imgui.menu_item('Bottom-left', None, _location == 2)[0]:
                _location = 2
            if imgui.menu_item('Bottom-right', None, _location == 3)[0]:
                _location = 3
            # TODO close
            imgui.end_popup()
        imgui.end()
