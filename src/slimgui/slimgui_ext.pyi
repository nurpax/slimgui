from collections.abc import Iterator, Sequence
import enum
from typing import overload

import MouseButton


class BackendFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: BackendFlags

    HAS_GAMEPAD: BackendFlags

    HAS_MOUSE_CURSORS: BackendFlags

    HAS_SET_MOUSE_POS: BackendFlags

    RENDERER_HAS_VTX_OFFSET: BackendFlags

class ButtonFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: ButtonFlags

    MOUSE_BUTTON_LEFT: ButtonFlags

    MOUSE_BUTTON_RIGHT: ButtonFlags

    MOUSE_BUTTON_MIDDLE: ButtonFlags

    MOUSE_BUTTON_MASK_: ButtonFlags

    MOUSE_BUTTON_DEFAULT_: ButtonFlags

class Col(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    TEXT: Col

    TEXT_DISABLED: Col

    WINDOW_BG: Col

    CHILD_BG: Col

    POPUP_BG: Col

    BORDER: Col

    BORDER_SHADOW: Col

    FRAME_BG: Col

    FRAME_BG_HOVERED: Col

    FRAME_BG_ACTIVE: Col

    TITLE_BG: Col

    TITLE_BG_ACTIVE: Col

    TITLE_BG_COLLAPSED: Col

    MENU_BAR_BG: Col

    SCROLLBAR_BG: Col

    SCROLLBAR_GRAB: Col

    SCROLLBAR_GRAB_HOVERED: Col

    SCROLLBAR_GRAB_ACTIVE: Col

    CHECK_MARK: Col

    SLIDER_GRAB: Col

    SLIDER_GRAB_ACTIVE: Col

    BUTTON: Col

    BUTTON_HOVERED: Col

    BUTTON_ACTIVE: Col

    HEADER: Col

    HEADER_HOVERED: Col

    HEADER_ACTIVE: Col

    SEPARATOR: Col

    SEPARATOR_HOVERED: Col

    SEPARATOR_ACTIVE: Col

    RESIZE_GRIP: Col

    RESIZE_GRIP_HOVERED: Col

    RESIZE_GRIP_ACTIVE: Col

    TAB: Col

    TAB_HOVERED: Col

    TAB_ACTIVE: Col

    TAB_UNFOCUSED: Col

    TAB_UNFOCUSED_ACTIVE: Col

    PLOT_LINES: Col

    PLOT_LINES_HOVERED: Col

    PLOT_HISTOGRAM: Col

    PLOT_HISTOGRAM_HOVERED: Col

    TABLE_HEADER_BG: Col

    TABLE_BORDER_STRONG: Col

    TABLE_BORDER_LIGHT: Col

    TABLE_ROW_BG: Col

    TABLE_ROW_BG_ALT: Col

    TEXT_SELECTED_BG: Col

    DRAG_DROP_TARGET: Col

    NAV_HIGHLIGHT: Col

    NAV_WINDOWING_HIGHLIGHT: Col

    NAV_WINDOWING_DIM_BG: Col

    MODAL_WINDOW_DIM_BG: Col

    COUNT: Col

class ColorEditFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: ColorEditFlags

    NO_ALPHA: ColorEditFlags

    NO_PICKER: ColorEditFlags

    NO_OPTIONS: ColorEditFlags

    NO_SMALL_PREVIEW: ColorEditFlags

    NO_INPUTS: ColorEditFlags

    NO_TOOLTIP: ColorEditFlags

    NO_LABEL: ColorEditFlags

    NO_SIDE_PREVIEW: ColorEditFlags

    NO_DRAG_DROP: ColorEditFlags

    NO_BORDER: ColorEditFlags

    ALPHA_BAR: ColorEditFlags

    ALPHA_PREVIEW: ColorEditFlags

    ALPHA_PREVIEW_HALF: ColorEditFlags

    HDR: ColorEditFlags

    DISPLAY_RGB: ColorEditFlags

    DISPLAY_HSV: ColorEditFlags

    DISPLAY_HEX: ColorEditFlags

    UINT8: ColorEditFlags

    FLOAT: ColorEditFlags

    PICKER_HUE_BAR: ColorEditFlags

    PICKER_HUE_WHEEL: ColorEditFlags

    INPUT_RGB: ColorEditFlags

    INPUT_HSV: ColorEditFlags

    DEFAULT_OPTIONS_: ColorEditFlags

    DISPLAY_MASK_: ColorEditFlags

    DATA_TYPE_MASK_: ColorEditFlags

    PICKER_MASK_: ColorEditFlags

    INPUT_MASK_: ColorEditFlags

class ComboFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: ComboFlags

    POPUP_ALIGN_LEFT: ComboFlags

    HEIGHT_SMALL: ComboFlags

    HEIGHT_REGULAR: ComboFlags

    HEIGHT_LARGE: ComboFlags

    HEIGHT_LARGEST: ComboFlags

    NO_ARROW_BUTTON: ComboFlags

    NO_PREVIEW: ComboFlags

    WIDTH_FIT_PREVIEW: ComboFlags

    HEIGHT_MASK_: ComboFlags

class Cond(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: Cond

    ALWAYS: Cond

    ONCE: Cond

    FIRST_USE_EVER: Cond

    APPEARING: Cond

class ConfigFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: ConfigFlags

    NAV_ENABLE_KEYBOARD: ConfigFlags

    NAV_ENABLE_GAMEPAD: ConfigFlags

    NAV_ENABLE_SET_MOUSE_POS: ConfigFlags

    NAV_NO_CAPTURE_KEYBOARD: ConfigFlags

    NO_MOUSE: ConfigFlags

    NO_MOUSE_CURSOR_CHANGE: ConfigFlags

    IS_SRGB: ConfigFlags

    IS_TOUCH_SCREEN: ConfigFlags

class Context:
    pass

class Dir(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ['NONE', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'COUNT']

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: Dir

    LEFT: Dir

    RIGHT: Dir

    UP: Dir

    DOWN: Dir

    COUNT: Dir

class DrawCmd:
    @property
    def texture_id(self) -> int: ...

    @property
    def clip_rect(self) -> tuple[float, float, float, float]: ...

    @property
    def vtx_offset(self) -> int: ...

    @property
    def idx_offset(self) -> int: ...

    @property
    def elem_count(self) -> int: ...

class DrawData:
    def scale_clip_rects(self, fb_scale: tuple[float, float]) -> None: ...

    @property
    def commands_lists(self) -> Iterator[DrawList]: ...

class DrawFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: DrawFlags

    CLOSED: DrawFlags

    ROUND_CORNERS_TOP_LEFT: DrawFlags

    ROUND_CORNERS_TOP_RIGHT: DrawFlags

    ROUND_CORNERS_BOTTOM_LEFT: DrawFlags

    ROUND_CORNERS_BOTTOM_RIGHT: DrawFlags

    ROUND_CORNERS_NONE: DrawFlags

    ROUND_CORNERS_TOP: DrawFlags

    ROUND_CORNERS_BOTTOM: DrawFlags

    ROUND_CORNERS_LEFT: DrawFlags

    ROUND_CORNERS_RIGHT: DrawFlags

    ROUND_CORNERS_ALL: DrawFlags

    ROUND_CORNERS_DEFAULT_: DrawFlags

    ROUND_CORNERS_MASK_: DrawFlags

class DrawList:
    @property
    def vtx_buffer_size(self) -> int: ...

    @property
    def vtx_buffer_data(self) -> int: ...

    @property
    def idx_buffer_size(self) -> int: ...

    @property
    def idx_buffer_data(self) -> int: ...

    @property
    def commands(self) -> Iterator[DrawCmd]: ...

FLOAT_MAX: float = 3.4028234663852886e+38

FLOAT_MIN: float = 1.1754943508222875e-38

class Font:
    pass

class FontAtlas:
    def add_font_default(self, font_cfg: FontConfig | None) -> Font: ...

    def clear_tex_data(self) -> None: ...

    def get_tex_data_as_rgba32(self) -> tuple[int, int, bytes]: ...

    @property
    def texture_id(self) -> int: ...

    @texture_id.setter
    def texture_id(self, arg: int, /) -> None: ...

class FontConfig:
    pass

class HoveredFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: HoveredFlags

    CHILD_WINDOWS: HoveredFlags

    ROOT_WINDOW: HoveredFlags

    ANY_WINDOW: HoveredFlags

    NO_POPUP_HIERARCHY: HoveredFlags

    ALLOW_WHEN_BLOCKED_BY_POPUP: HoveredFlags

    ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM: HoveredFlags

    ALLOW_WHEN_OVERLAPPED_BY_ITEM: HoveredFlags

    ALLOW_WHEN_OVERLAPPED_BY_WINDOW: HoveredFlags

    ALLOW_WHEN_DISABLED: HoveredFlags

    NO_NAV_OVERRIDE: HoveredFlags

    ALLOW_WHEN_OVERLAPPED: HoveredFlags

    RECT_ONLY: HoveredFlags

    ROOT_AND_CHILD_WINDOWS: HoveredFlags

    FOR_TOOLTIP: HoveredFlags

    STATIONARY: HoveredFlags

    DELAY_NONE: HoveredFlags

    DELAY_SHORT: HoveredFlags

    DELAY_NORMAL: HoveredFlags

    NO_SHARED_DELAY: HoveredFlags

IMGUI_VERSION: str = '1.90.5'

IMGUI_VERSION_NUM: int = 19050

INDEX_SIZE: int = 2

class IO:
    def add_mouse_pos_event(self, x: float, y: float) -> None: ...

    def add_mouse_button_event(self, button: int, down: bool) -> None: ...

    def add_mouse_wheel_event(self, wheel_x: float, wheel_y: float) -> None: ...

    def add_input_character(self, c: int) -> None: ...

    def add_key_event(self, key: Key, down: bool) -> None: ...

    @property
    def display_size(self) -> tuple[float, float]: ...

    @display_size.setter
    def display_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def display_fb_scale(self) -> tuple[float, float]: ...

    @display_fb_scale.setter
    def display_fb_scale(self, arg: tuple[float, float], /) -> None: ...

    @property
    def delta_time(self) -> float: ...

    @delta_time.setter
    def delta_time(self, arg: float, /) -> None: ...

    @property
    def fonts(self) -> FontAtlas: ...

    @fonts.setter
    def fonts(self, arg: FontAtlas, /) -> None: ...

    @property
    def config_flags(self) -> int: ...

    @config_flags.setter
    def config_flags(self, arg: int, /) -> None: ...

    @property
    def backend_flags(self) -> int: ...

    @backend_flags.setter
    def backend_flags(self, arg: int, /) -> None: ...

    @property
    def mouse_draw_cursor(self) -> bool: ...

    @mouse_draw_cursor.setter
    def mouse_draw_cursor(self, arg: bool, /) -> None: ...

    @property
    def config_mac_osx_behaviors(self) -> bool: ...

    @config_mac_osx_behaviors.setter
    def config_mac_osx_behaviors(self, arg: bool, /) -> None: ...

    @property
    def config_input_trickle_event_queue(self) -> bool: ...

    @config_input_trickle_event_queue.setter
    def config_input_trickle_event_queue(self, arg: bool, /) -> None: ...

    @property
    def config_input_text_cursor_blink(self) -> bool: ...

    @config_input_text_cursor_blink.setter
    def config_input_text_cursor_blink(self, arg: bool, /) -> None: ...

    @property
    def config_input_text_enter_keep_active(self) -> bool: ...

    @config_input_text_enter_keep_active.setter
    def config_input_text_enter_keep_active(self, arg: bool, /) -> None: ...

    @property
    def config_drag_click_to_input_text(self) -> bool: ...

    @config_drag_click_to_input_text.setter
    def config_drag_click_to_input_text(self, arg: bool, /) -> None: ...

    @property
    def config_windows_resize_from_edges(self) -> bool: ...

    @config_windows_resize_from_edges.setter
    def config_windows_resize_from_edges(self, arg: bool, /) -> None: ...

    @property
    def config_windows_move_from_title_bar_only(self) -> bool: ...

    @config_windows_move_from_title_bar_only.setter
    def config_windows_move_from_title_bar_only(self, arg: bool, /) -> None: ...

    @property
    def config_memory_compact_timer(self) -> float: ...

    @config_memory_compact_timer.setter
    def config_memory_compact_timer(self, arg: float, /) -> None: ...

    @property
    def mouse_double_click_time(self) -> float: ...

    @mouse_double_click_time.setter
    def mouse_double_click_time(self, arg: float, /) -> None: ...

    @property
    def mouse_double_click_max_dist(self) -> float: ...

    @mouse_double_click_max_dist.setter
    def mouse_double_click_max_dist(self, arg: float, /) -> None: ...

    @property
    def mouse_drag_threshold(self) -> float: ...

    @mouse_drag_threshold.setter
    def mouse_drag_threshold(self, arg: float, /) -> None: ...

    @property
    def key_repeat_delay(self) -> float: ...

    @key_repeat_delay.setter
    def key_repeat_delay(self, arg: float, /) -> None: ...

    @property
    def key_repeat_rate(self) -> float: ...

    @key_repeat_rate.setter
    def key_repeat_rate(self, arg: float, /) -> None: ...

class InputTextFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: InputTextFlags

    CHARS_DECIMAL: InputTextFlags

    CHARS_HEXADECIMAL: InputTextFlags

    CHARS_UPPERCASE: InputTextFlags

    CHARS_NO_BLANK: InputTextFlags

    AUTO_SELECT_ALL: InputTextFlags

    ENTER_RETURNS_TRUE: InputTextFlags

    CALLBACK_COMPLETION: InputTextFlags

    CALLBACK_HISTORY: InputTextFlags

    CALLBACK_ALWAYS: InputTextFlags

    CALLBACK_CHAR_FILTER: InputTextFlags

    ALLOW_TAB_INPUT: InputTextFlags

    CTRL_ENTER_FOR_NEW_LINE: InputTextFlags

    NO_HORIZONTAL_SCROLL: InputTextFlags

    ALWAYS_OVERWRITE: InputTextFlags

    READ_ONLY: InputTextFlags

    PASSWORD: InputTextFlags

    NO_UNDO_REDO: InputTextFlags

    CHARS_SCIENTIFIC: InputTextFlags

    CALLBACK_RESIZE: InputTextFlags

    CALLBACK_EDIT: InputTextFlags

    ESCAPE_CLEARS_ALL: InputTextFlags

class Key(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    KEY_NONE: Key

    KEY_TAB: Key

    KEY_LEFT_ARROW: Key

    KEY_RIGHT_ARROW: Key

    KEY_UP_ARROW: Key

    KEY_DOWN_ARROW: Key

    KEY_PAGE_UP: Key

    KEY_PAGE_DOWN: Key

    KEY_HOME: Key

    KEY_END: Key

    KEY_INSERT: Key

    KEY_DELETE: Key

    KEY_BACKSPACE: Key

    KEY_SPACE: Key

    KEY_ENTER: Key

    KEY_ESCAPE: Key

    KEY_LEFT_CTRL: Key

    KEY_LEFT_SHIFT: Key

    KEY_LEFT_ALT: Key

    KEY_LEFT_SUPER: Key

    KEY_RIGHT_CTRL: Key

    KEY_RIGHT_SHIFT: Key

    KEY_RIGHT_ALT: Key

    KEY_RIGHT_SUPER: Key

    KEY_MENU: Key

    KEY_0: Key

    KEY_1: Key

    KEY_2: Key

    KEY_3: Key

    KEY_4: Key

    KEY_5: Key

    KEY_6: Key

    KEY_7: Key

    KEY_8: Key

    KEY_9: Key

    KEY_A: Key

    KEY_B: Key

    KEY_C: Key

    KEY_D: Key

    KEY_E: Key

    KEY_F: Key

    KEY_G: Key

    KEY_H: Key

    KEY_I: Key

    KEY_J: Key

    KEY_K: Key

    KEY_L: Key

    KEY_M: Key

    KEY_N: Key

    KEY_O: Key

    KEY_P: Key

    KEY_Q: Key

    KEY_R: Key

    KEY_S: Key

    KEY_T: Key

    KEY_U: Key

    KEY_V: Key

    KEY_W: Key

    KEY_X: Key

    KEY_Y: Key

    KEY_Z: Key

    KEY_F1: Key

    KEY_F2: Key

    KEY_F3: Key

    KEY_F4: Key

    KEY_F5: Key

    KEY_F6: Key

    KEY_F7: Key

    KEY_F8: Key

    KEY_F9: Key

    KEY_F10: Key

    KEY_F11: Key

    KEY_F12: Key

    KEY_F13: Key

    KEY_F14: Key

    KEY_F15: Key

    KEY_F16: Key

    KEY_F17: Key

    KEY_F18: Key

    KEY_F19: Key

    KEY_F20: Key

    KEY_F21: Key

    KEY_F22: Key

    KEY_F23: Key

    KEY_F24: Key

    KEY_APOSTROPHE: Key

    KEY_COMMA: Key

    KEY_MINUS: Key

    KEY_PERIOD: Key

    KEY_SLASH: Key

    KEY_SEMICOLON: Key

    KEY_EQUAL: Key

    KEY_LEFT_BRACKET: Key

    KEY_BACKSLASH: Key

    KEY_RIGHT_BRACKET: Key

    KEY_GRAVE_ACCENT: Key

    KEY_CAPS_LOCK: Key

    KEY_SCROLL_LOCK: Key

    KEY_NUM_LOCK: Key

    KEY_PRINT_SCREEN: Key

    KEY_PAUSE: Key

    KEY_KEYPAD0: Key

    KEY_KEYPAD1: Key

    KEY_KEYPAD2: Key

    KEY_KEYPAD3: Key

    KEY_KEYPAD4: Key

    KEY_KEYPAD5: Key

    KEY_KEYPAD6: Key

    KEY_KEYPAD7: Key

    KEY_KEYPAD8: Key

    KEY_KEYPAD9: Key

    KEY_KEYPAD_DECIMAL: Key

    KEY_KEYPAD_DIVIDE: Key

    KEY_KEYPAD_MULTIPLY: Key

    KEY_KEYPAD_SUBTRACT: Key

    KEY_KEYPAD_ADD: Key

    KEY_KEYPAD_ENTER: Key

    KEY_KEYPAD_EQUAL: Key

    KEY_APP_BACK: Key

    KEY_APP_FORWARD: Key

    KEY_GAMEPAD_START: Key

    KEY_GAMEPAD_BACK: Key

    KEY_GAMEPAD_FACE_LEFT: Key

    KEY_GAMEPAD_FACE_RIGHT: Key

    KEY_GAMEPAD_FACE_UP: Key

    KEY_GAMEPAD_FACE_DOWN: Key

    KEY_GAMEPAD_DPAD_LEFT: Key

    KEY_GAMEPAD_DPAD_RIGHT: Key

    KEY_GAMEPAD_DPAD_UP: Key

    KEY_GAMEPAD_DPAD_DOWN: Key

    KEY_GAMEPAD_L1: Key

    KEY_GAMEPAD_R1: Key

    KEY_GAMEPAD_L2: Key

    KEY_GAMEPAD_R2: Key

    KEY_GAMEPAD_L3: Key

    KEY_GAMEPAD_R3: Key

    KEY_GAMEPAD_L_STICK_LEFT: Key

    KEY_GAMEPAD_L_STICK_RIGHT: Key

    KEY_GAMEPAD_L_STICK_UP: Key

    KEY_GAMEPAD_L_STICK_DOWN: Key

    KEY_GAMEPAD_R_STICK_LEFT: Key

    KEY_GAMEPAD_R_STICK_RIGHT: Key

    KEY_GAMEPAD_R_STICK_UP: Key

    KEY_GAMEPAD_R_STICK_DOWN: Key

    KEY_MOUSE_LEFT: Key

    KEY_MOUSE_RIGHT: Key

    KEY_MOUSE_MIDDLE: Key

    KEY_MOUSE_X1: Key

    KEY_MOUSE_X2: Key

    KEY_MOUSE_WHEEL_X: Key

    KEY_MOUSE_WHEEL_Y: Key

    KEY_RESERVED_FOR_MOD_CTRL: Key

    KEY_RESERVED_FOR_MOD_SHIFT: Key

    KEY_RESERVED_FOR_MOD_ALT: Key

    KEY_RESERVED_FOR_MOD_SUPER: Key

    KEY_COUNT: Key

    MOD_NONE: Key

    MOD_CTRL: Key

    MOD_SHIFT: Key

    MOD_ALT: Key

    MOD_SUPER: Key

    MOD_SHORTCUT: Key

    MOD_MASK_: Key

    KEY_NAMED_KEY_BEGIN: Key

    KEY_NAMED_KEY_END: Key

    KEY_NAMED_KEY_COUNT: Key

    KEY_KEYS_DATA_SIZE: Key

    KEY_KEYS_DATA_OFFSET: Key

class MouseButton(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ['LEFT', 'RIGHT', 'MIDDLE', 'COUNT']

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    LEFT: MouseButton

    RIGHT: MouseButton

    MIDDLE: MouseButton

    COUNT: MouseButton

class PopupFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: PopupFlags

    MOUSE_BUTTON_LEFT: PopupFlags

    MOUSE_BUTTON_RIGHT: PopupFlags

    MOUSE_BUTTON_MIDDLE: PopupFlags

    MOUSE_BUTTON_MASK_: PopupFlags

    MOUSE_BUTTON_DEFAULT_: PopupFlags

    NO_REOPEN: PopupFlags

    NO_OPEN_OVER_EXISTING_POPUP: PopupFlags

    NO_OPEN_OVER_ITEMS: PopupFlags

    ANY_POPUP_ID: PopupFlags

    ANY_POPUP_LEVEL: PopupFlags

    ANY_POPUP: PopupFlags

class SelectableFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: SelectableFlags

    DONT_CLOSE_POPUPS: SelectableFlags

    SPAN_ALL_COLUMNS: SelectableFlags

    ALLOW_DOUBLE_CLICK: SelectableFlags

    DISABLED: SelectableFlags

    ALLOW_OVERLAP: SelectableFlags

class SliderFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: SliderFlags

    ALWAYS_CLAMP: SliderFlags

    LOGARITHMIC: SliderFlags

    NO_ROUND_TO_FORMAT: SliderFlags

    NO_INPUT: SliderFlags

    INVALID_MASK_: SliderFlags

class StyleVar(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    ALPHA: StyleVar

    DISABLED_ALPHA: StyleVar

    WINDOW_PADDING: StyleVar

    WINDOW_ROUNDING: StyleVar

    WINDOW_BORDER_SIZE: StyleVar

    WINDOW_MIN_SIZE: StyleVar

    WINDOW_TITLE_ALIGN: StyleVar

    CHILD_ROUNDING: StyleVar

    CHILD_BORDER_SIZE: StyleVar

    POPUP_ROUNDING: StyleVar

    POPUP_BORDER_SIZE: StyleVar

    FRAME_PADDING: StyleVar

    FRAME_ROUNDING: StyleVar

    FRAME_BORDER_SIZE: StyleVar

    ITEM_SPACING: StyleVar

    ITEM_INNER_SPACING: StyleVar

    INDENT_SPACING: StyleVar

    CELL_PADDING: StyleVar

    SCROLLBAR_SIZE: StyleVar

    SCROLLBAR_ROUNDING: StyleVar

    GRAB_MIN_SIZE: StyleVar

    GRAB_ROUNDING: StyleVar

    TAB_ROUNDING: StyleVar

    TAB_BORDER_SIZE: StyleVar

    TAB_BAR_BORDER_SIZE: StyleVar

    TABLE_ANGLED_HEADERS_ANGLE: StyleVar

    BUTTON_TEXT_ALIGN: StyleVar

    SELECTABLE_TEXT_ALIGN: StyleVar

    SEPARATOR_TEXT_BORDER_SIZE: StyleVar

    SEPARATOR_TEXT_ALIGN: StyleVar

    SEPARATOR_TEXT_PADDING: StyleVar

    COUNT: StyleVar

class TableFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: TableFlags

    RESIZABLE: TableFlags

    REORDERABLE: TableFlags

    HIDEABLE: TableFlags

    SORTABLE: TableFlags

    NO_SAVED_SETTINGS: TableFlags

    CONTEXT_MENU_IN_BODY: TableFlags

    ROW_BG: TableFlags

    BORDERS_INNER_H: TableFlags

    BORDERS_OUTER_H: TableFlags

    BORDERS_INNER_V: TableFlags

    BORDERS_OUTER_V: TableFlags

    BORDERS_H: TableFlags

    BORDERS_V: TableFlags

    BORDERS_INNER: TableFlags

    BORDERS_OUTER: TableFlags

    BORDERS: TableFlags

    NO_BORDERS_IN_BODY: TableFlags

    NO_BORDERS_IN_BODY_UNTIL_RESIZE: TableFlags

    SIZING_FIXED_FIT: TableFlags

    SIZING_FIXED_SAME: TableFlags

    SIZING_STRETCH_PROP: TableFlags

    SIZING_STRETCH_SAME: TableFlags

    NO_HOST_EXTEND_X: TableFlags

    NO_HOST_EXTEND_Y: TableFlags

    NO_KEEP_COLUMNS_VISIBLE: TableFlags

    PRECISE_WIDTHS: TableFlags

    NO_CLIP: TableFlags

    PAD_OUTER_X: TableFlags

    NO_PAD_OUTER_X: TableFlags

    NO_PAD_INNER_X: TableFlags

    SCROLL_X: TableFlags

    SCROLL_Y: TableFlags

    SORT_MULTI: TableFlags

    SORT_TRISTATE: TableFlags

    HIGHLIGHT_HOVERED_COLUMN: TableFlags

    SIZING_MASK_: TableFlags

class TableRowFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ['NONE', 'HEADERS']

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: TableRowFlags

    HEADERS: TableRowFlags

class TreeNodeFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: TreeNodeFlags

    SELECTED: TreeNodeFlags

    FRAMED: TreeNodeFlags

    ALLOW_OVERLAP: TreeNodeFlags

    NO_TREE_PUSH_ON_OPEN: TreeNodeFlags

    NO_AUTO_OPEN_ON_LOG: TreeNodeFlags

    DEFAULT_OPEN: TreeNodeFlags

    OPEN_ON_DOUBLE_CLICK: TreeNodeFlags

    OPEN_ON_ARROW: TreeNodeFlags

    LEAF: TreeNodeFlags

    BULLET: TreeNodeFlags

    FRAME_PADDING: TreeNodeFlags

    SPAN_AVAIL_WIDTH: TreeNodeFlags

    SPAN_FULL_WIDTH: TreeNodeFlags

    SPAN_ALL_COLUMNS: TreeNodeFlags

    NAV_LEFT_JUMPS_BACK_HERE: TreeNodeFlags

    COLLAPSING_HEADER: TreeNodeFlags

VERTEX_BUFFER_COL_OFFSET: int = 16

VERTEX_BUFFER_POS_OFFSET: int = 0

VERTEX_BUFFER_UV_OFFSET: int = 8

VERTEX_SIZE: int = 20

class Viewport:
    @property
    def pos(self) -> tuple[float, float]: ...

    @pos.setter
    def pos(self, arg: tuple[float, float], /) -> None: ...

    @property
    def size(self) -> tuple[float, float]: ...

    @size.setter
    def size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def work_pos(self) -> tuple[float, float]: ...

    @work_pos.setter
    def work_pos(self, arg: tuple[float, float], /) -> None: ...

    @property
    def work_size(self) -> tuple[float, float]: ...

    @work_size.setter
    def work_size(self, arg: tuple[float, float], /) -> None: ...

class WindowFlags(enum.IntEnum):
    _new_member_ = __new__

    _use_args_: bool = True

    _member_names_: list = ...

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    _unhashable_values_: list = []

    _value_repr_ = __repr__

    NONE: WindowFlags

    NO_TITLE_BAR: WindowFlags

    NO_RESIZE: WindowFlags

    NO_MOVE: WindowFlags

    NO_SCROLLBAR: WindowFlags

    NO_SCROLL_WITH_MOUSE: WindowFlags

    NO_COLLAPSE: WindowFlags

    ALWAYS_AUTO_RESIZE: WindowFlags

    NO_BACKGROUND: WindowFlags

    NO_SAVED_SETTINGS: WindowFlags

    NO_MOUSE_INPUTS: WindowFlags

    MENU_BAR: WindowFlags

    HORIZONTAL_SCROLLBAR: WindowFlags

    NO_FOCUS_ON_APPEARING: WindowFlags

    NO_BRING_TO_FRONT_ON_FOCUS: WindowFlags

    ALWAYS_VERTICAL_SCROLLBAR: WindowFlags

    ALWAYS_HORIZONTAL_SCROLLBAR: WindowFlags

    NO_NAV_INPUTS: WindowFlags

    NO_NAV_FOCUS: WindowFlags

    UNSAVED_DOCUMENT: WindowFlags

    NO_NAV: WindowFlags

    NO_DECORATION: WindowFlags

    NO_INPUTS: WindowFlags

    NAV_FLATTENED: WindowFlags

    CHILD_WINDOW: WindowFlags

    TOOLTIP: WindowFlags

    POPUP: WindowFlags

    MODAL: WindowFlags

    CHILD_MENU: WindowFlags

def align_text_to_frame_padding() -> None: ...

def arrow_button(str_id: str, dir: int) -> bool: ...

def begin(name: str, closable: bool = False, flags: int = 0) -> tuple[bool, bool]: ...

def begin_combo(label: str, preview_value: str, flags: int = ComboFlags.NONE) -> bool: ...

def begin_disabled(disabled: bool = True) -> None: ...

def begin_group() -> None: ...

def begin_item_tooltip() -> bool: ...

def begin_list_box(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool: ...

def begin_main_menu_bar() -> bool: ...

def begin_menu(label: str, enabled: bool = True) -> bool: ...

def begin_menu_bar() -> bool: ...

def begin_popup(str_id: str, flags: int = WindowFlags.NONE) -> bool: ...

def begin_table(str_id: str, column: int, flags: int = 0, outer_size: tuple[float, float] = (0.0, 0.0), inner_width: float = 0.0) -> bool: ...

def begin_tooltip() -> bool: ...

def bullet_text(text: str) -> None: ...

def button(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool: ...

def calc_item_width() -> float: ...

def checkbox(label: str, v: bool) -> tuple[bool, bool]: ...

def checkbox_flags(label: str, flags: int, flags_value: int) -> tuple[bool, int]: ...

def close_current_popup() -> None: ...

def collapsing_header(label: str, visible: object | None = None, flags: int = 0) -> tuple[bool, bool | None]: ...

def color_convert_hsv_to_rgb(hsv: tuple[float, float, float, float]) -> tuple[float, float, float, float]: ...

def color_convert_rgb_to_hsv(rgba: tuple[float, float, float, float]) -> tuple[float, float, float, float]: ...

def color_edit3(label: str, col: tuple[float, float, float], flags: int = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float]]: ...

def color_edit4(label: str, col: tuple[float, float, float, float], flags: int = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]: ...

def combo(label: str, current_item: int, items: Sequence[str], popup_max_height_in_items: int = -1) -> tuple[bool, int]: ...

def create_context(shared_font_atlas: FontAtlas | None = None) -> Context:
    """create context"""

def destroy_context(arg: Context, /) -> None: ...

def dummy(size: tuple[float, float]) -> None: ...

def end() -> None: ...

def end_combo() -> None: ...

def end_disabled() -> None: ...

def end_group() -> None: ...

def end_list_box() -> None: ...

def end_main_menu_bar() -> None: ...

def end_menu() -> None: ...

def end_menu_bar() -> None: ...

def end_popup() -> None: ...

def end_table() -> None: ...

def end_tooltip() -> None: ...

def get_current_context() -> Context: ...

def get_draw_data() -> DrawData: ...

def get_font_size() -> float: ...

def get_font_tex_uv_white_pixel() -> tuple[float, float]: ...

def get_frame_height() -> float: ...

def get_frame_height_with_spacing() -> float: ...

def get_io() -> IO: ...

def get_item_rect_max() -> tuple[float, float]: ...

def get_item_rect_min() -> tuple[float, float]: ...

def get_item_rect_size() -> tuple[float, float]: ...

def get_key_name(key: Key) -> str: ...

def get_key_pressed_amount(key: Key, repeat_delay: float, rate: float) -> int: ...

def get_main_viewport() -> Viewport: ...

def get_text_line_height() -> float: ...

def get_text_line_height_with_spacing() -> float: ...

def get_time() -> float: ...

def get_tree_node_to_label_spacing() -> float: ...

def get_version() -> str: ...

def image(user_texture_id: int, image_size: tuple[float, float], uv0: tuple[float, float] = (0.0, 0.0), uv1: tuple[float, float] = (1.0, 1.0), tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), border_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)) -> None: ...

def indent(indent_w: float = 0.0) -> None: ...

def input_double(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.6f', flags: int = 0) -> tuple[bool, float]: ...

def input_float(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.3f', flags: int = 0) -> tuple[bool, float]: ...

def input_int(label: str, v: int, step: int = 1, step_fast: int = 100, flags: int = 0) -> tuple[bool, int]: ...

def input_text(label: str, text: str, flags: int = InputTextFlags.NONE) -> tuple[bool, str]: ...

def input_text_with_hint(label: str, hint: str, text: str, flags: int = InputTextFlags.NONE) -> tuple[bool, str]: ...

def invisible_button(str_id: str, size: tuple[float, float], flags: int = ButtonFlags.NONE) -> bool: ...

def is_any_item_active() -> bool: ...

def is_any_item_focused() -> bool: ...

def is_any_item_hovered() -> bool: ...

def is_item_activated() -> bool: ...

def is_item_active() -> bool: ...

def is_item_clicked(mouse_button: MouseButton | int = MouseButton.LEFT) -> bool: ...

def is_item_deactivated() -> bool: ...

def is_item_deactivated_after_edit() -> bool: ...

def is_item_edited() -> bool: ...

def is_item_focused() -> bool: ...

def is_item_hovered(flags: int = 0) -> bool: ...

def is_item_toggled_open() -> bool: ...

def is_item_visible() -> bool: ...

def is_key_chord_pressed(key_chord: Key) -> bool: ...

def is_key_down(key: Key) -> bool: ...

def is_key_pressed(key: Key, repeat: bool = True) -> bool: ...

def is_key_released(key: Key) -> bool: ...

def is_popup_open(str_id: str, flags: int = 0) -> bool: ...

def label_text(label: str, text: str) -> None: ...

def list_box(label: str, current_item: int, items: Sequence[str], height_in_items: int = -1) -> tuple[bool, int]: ...

def log_buttons() -> None: ...

def log_finish() -> None: ...

def log_text(text: str) -> None: ...

def log_to_clipboard(auto_open_depth: int = -1) -> None: ...

def log_to_file(auto_open_depth: int = -1, filename: str | None = None) -> None: ...

def log_to_tty(auto_open_depth: int = -1) -> None: ...

def menu_item(label: str, shortcut: object | None = None, selected: bool = False, enabled: bool = True) -> tuple[bool, bool]: ...

def new_frame() -> None: ...

def new_line() -> None: ...

def open_popup(str_id: str, flags: int = PopupFlags.NONE) -> None: ...

def open_popup_on_item_click(str_id: str | None = None, flags: int = PopupFlags.MOUSE_BUTTON_RIGHT) -> None: ...

def pop_button_repeat() -> None: ...

def pop_id() -> None: ...

def pop_item_width() -> None: ...

def pop_style_color(count: int = 1) -> None: ...

def pop_style_var(count: int = 1) -> None: ...

def pop_tab_stop() -> None: ...

def pop_text_wrap_pos() -> None: ...

def push_button_repeat(repeat: bool) -> None: ...

@overload
def push_id(str_id: str) -> None: ...

@overload
def push_id(int_id: int) -> None: ...

def push_item_width(item_width: float) -> None: ...

@overload
def push_style_color(idx: int, col: int) -> None: ...

@overload
def push_style_color(idx: int, col: tuple[float, float, float, float]) -> None: ...

@overload
def push_style_var(idx: int, val: float) -> None: ...

@overload
def push_style_var(idx: int, val: tuple[float, float]) -> None: ...

def push_tab_stop(tab_stop: bool) -> None: ...

def push_text_wrap_pos(wrap_local_pos_x: float = 0.0) -> None: ...

@overload
def radio_button(label: str, active: bool) -> bool: ...

@overload
def radio_button(label: str, v: int, v_button: int) -> tuple[bool, int]: ...

def render() -> None: ...

def same_line(offset_from_start_x: float = 0.0, spacing: float = -1.0) -> None: ...

def selectable(label: str, selected: bool = False, flags: int = SelectableFlags.NONE, size: tuple[float, float] = (0.0, 0.0)) -> tuple[bool, bool]: ...

def separator() -> None: ...

def separator_text(text: str) -> None: ...

def set_item_default_focus() -> None: ...

def set_item_tooltip(text: str) -> None: ...

def set_keyboard_focus_here(offset: int = 0) -> None: ...

def set_next_frame_want_capture_keyboard(want_capture_keyboard: bool) -> None: ...

def set_next_item_open(is_open: bool, cond: int = 0) -> None: ...

def set_next_item_width(item_width: float) -> None: ...

def set_next_window_pos(pos: tuple[float, float], cond: int = 0, pivot: tuple[float, float] = (0.0, 0.0)) -> None: ...

def set_next_window_size(size: tuple[float, float], cond: int = 0) -> None: ...

def show_debug_log_window(closable: bool = False) -> bool: ...

def show_id_stack_tool_window(closable: bool = False) -> bool: ...

def show_metrics_window(closable: bool = False) -> bool: ...

def show_style_editor() -> None: ...

def show_user_guide() -> None: ...

def slider_angle(label: str, v: float, v_degrees_min: float = -360.0, v_degrees_max: float = 360.0, format: str = '%.0f deg', flags: int = 0) -> tuple[bool, float]: ...

def slider_float(label: str, v: float, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple[bool, float]: ...

def slider_float2(label: str, v: tuple[float, float], v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple[bool, tuple[float, float]]: ...

def slider_float3(label: str, v: tuple[float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple[bool, tuple[float, float, float]]: ...

def slider_float4(label: str, v: tuple[float, float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple[bool, tuple[float, float, float, float]]: ...

def slider_int(label: str, v: int, v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> tuple[bool, int]: ...

def slider_int2(label: str, v: tuple[int, int], v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> tuple[bool, tuple[int, int]]: ...

def slider_int3(label: str, v: tuple[int, int, int], v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> tuple[bool, tuple[int, int, int]]: ...

def slider_int4(label: str, v: tuple[int, int, int, int], v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> tuple[bool, tuple[int, int, int, int]]: ...

def small_button(label: str) -> bool: ...

def spacing() -> None: ...

def table_next_column() -> bool: ...

def table_next_row(row_flags: int = 0, min_row_height: float = 0.0) -> None: ...

def table_set_column_index(column_n: int) -> bool: ...

def text(text: str) -> None: ...

def text_colored(col: tuple[float, float, float, float], text: str) -> None: ...

def text_disabled(text: str) -> None: ...

def text_wrapped(text: str) -> None: ...

@overload
def tree_node(label: str, flags: int = 0) -> bool: ...

@overload
def tree_node(str_id: str, text: str, flags: int = 0) -> bool: ...

def tree_pop() -> None: ...

def tree_push(str_id: str) -> None: ...

def unindent(indent_w: float = 0.0) -> None: ...
