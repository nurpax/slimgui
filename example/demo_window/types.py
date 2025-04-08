from dataclasses import dataclass

from slimgui import BoolRef

@dataclass
class State:
    show_app_main_menu_bar = BoolRef(False)
    show_app_documents = BoolRef(False)
    show_app_console = BoolRef(False)
    show_app_custom_rendering = BoolRef(False)
    show_app_log = BoolRef(False)
    show_app_layout = BoolRef(False)
    show_app_property_editor = BoolRef(False)
    show_app_simple_overlay = BoolRef(False)
    show_app_auto_resize = BoolRef(False)
    show_app_constrained_resize = BoolRef(False)
    show_app_fullscreen = BoolRef(False)
    show_app_long_text = BoolRef(False)
    show_app_window_titles = BoolRef(False)

    no_titlebar = BoolRef(False)
    no_scrollbar = BoolRef(False)
    no_menu = BoolRef(False)
    no_move = BoolRef(False)
    no_resize = BoolRef(False)
    no_collapse = BoolRef(False)
    no_close = BoolRef(False)
    no_nav = BoolRef(False)
    no_background = BoolRef(False)
    no_bring_to_front = BoolRef(False)
    no_docking = BoolRef(False)
    unsaved_document = BoolRef(False)

    show_tool_metrics = BoolRef(False)
    show_tool_debug_log = BoolRef(False)
    show_tool_id_stack_tool = BoolRef(False)
    show_tool_style_editor = BoolRef(False)
    show_tool_about = BoolRef(False)
    show_native_imgui_demo_window = BoolRef(False)

    widgets_disable_all = False
