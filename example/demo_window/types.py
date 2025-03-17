from dataclasses import dataclass

@dataclass
class State:
    show_app_main_menu_bar = False
    show_app_documents = False
    show_app_console = False
    show_app_custom_rendering = False
    show_app_log = False
    show_app_layout = False
    show_app_property_editor = False
    show_app_simple_overlay = False
    show_app_auto_resize = False
    show_app_constrained_resize = False
    show_app_fullscreen = False
    show_app_long_text = False
    show_app_window_titles = False

    no_titlebar = False
    no_scrollbar = False
    no_menu = False
    no_move = False
    no_resize = False
    no_collapse = False
    no_close = False
    no_nav = False
    no_background = False
    no_bring_to_front = False
    no_docking = False
    unsaved_document = False

    show_tool_metrics = False
    show_tool_debug_log = False
    show_tool_id_stack_tool = False
    show_tool_style_editor = False
    show_tool_about = False
    show_native_imgui_demo_window = False

    widgets_disable_all = False
