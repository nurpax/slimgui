from collections.abc import Iterator, Sequence
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike


class BackendFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HAS_GAMEPAD = 1

    HAS_MOUSE_CURSORS = 2

    HAS_SET_MOUSE_POS = 4

    RENDERER_HAS_VTX_OFFSET = 8

class ButtonFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    MOUSE_BUTTON_LEFT = 1

    MOUSE_BUTTON_RIGHT = 2

    MOUSE_BUTTON_MIDDLE = 4

class ChildFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    BORDER = 1

    ALWAYS_USE_WINDOW_PADDING = 2

    RESIZE_X = 4

    RESIZE_Y = 8

    AUTO_RESIZE_X = 16

    AUTO_RESIZE_Y = 32

    ALWAYS_AUTO_RESIZE = 64

    FRAME_STYLE = 128

class Col(enum.IntEnum):
    TEXT = 0

    TEXT_DISABLED = 1

    WINDOW_BG = 2

    CHILD_BG = 3

    POPUP_BG = 4

    BORDER = 5

    BORDER_SHADOW = 6

    FRAME_BG = 7

    FRAME_BG_HOVERED = 8

    FRAME_BG_ACTIVE = 9

    TITLE_BG = 10

    TITLE_BG_ACTIVE = 11

    TITLE_BG_COLLAPSED = 12

    MENU_BAR_BG = 13

    SCROLLBAR_BG = 14

    SCROLLBAR_GRAB = 15

    SCROLLBAR_GRAB_HOVERED = 16

    SCROLLBAR_GRAB_ACTIVE = 17

    CHECK_MARK = 18

    SLIDER_GRAB = 19

    SLIDER_GRAB_ACTIVE = 20

    BUTTON = 21

    BUTTON_HOVERED = 22

    BUTTON_ACTIVE = 23

    HEADER = 24

    HEADER_HOVERED = 25

    HEADER_ACTIVE = 26

    SEPARATOR = 27

    SEPARATOR_HOVERED = 28

    SEPARATOR_ACTIVE = 29

    RESIZE_GRIP = 30

    RESIZE_GRIP_HOVERED = 31

    RESIZE_GRIP_ACTIVE = 32

    TAB = 33

    TAB_HOVERED = 34

    TAB_ACTIVE = 35

    TAB_UNFOCUSED = 36

    TAB_UNFOCUSED_ACTIVE = 37

    PLOT_LINES = 38

    PLOT_LINES_HOVERED = 39

    PLOT_HISTOGRAM = 40

    PLOT_HISTOGRAM_HOVERED = 41

    TABLE_HEADER_BG = 42

    TABLE_BORDER_STRONG = 43

    TABLE_BORDER_LIGHT = 44

    TABLE_ROW_BG = 45

    TABLE_ROW_BG_ALT = 46

    TEXT_SELECTED_BG = 47

    DRAG_DROP_TARGET = 48

    NAV_HIGHLIGHT = 49

    NAV_WINDOWING_HIGHLIGHT = 50

    NAV_WINDOWING_DIM_BG = 51

    MODAL_WINDOW_DIM_BG = 52

    COUNT = 53

class ColorEditFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_ALPHA = 2

    NO_PICKER = 4

    NO_OPTIONS = 8

    NO_SMALL_PREVIEW = 16

    NO_INPUTS = 32

    NO_TOOLTIP = 64

    NO_LABEL = 128

    NO_SIDE_PREVIEW = 256

    NO_DRAG_DROP = 512

    NO_BORDER = 1024

    ALPHA_BAR = 65536

    ALPHA_PREVIEW = 131072

    ALPHA_PREVIEW_HALF = 262144

    HDR = 524288

    DISPLAY_RGB = 1048576

    DISPLAY_HSV = 2097152

    DISPLAY_HEX = 4194304

    UINT8 = 8388608

    FLOAT = 16777216

    PICKER_HUE_BAR = 33554432

    PICKER_HUE_WHEEL = 67108864

    INPUT_RGB = 134217728

    INPUT_HSV = 268435456

class ColorsArray:
    def __getitem__(self, arg: Col, /) -> tuple[float, float, float, float]: ...

    def __setitem__(self, arg0: Col, arg1: tuple[float, float, float, float], /) -> None: ...

    def __iter__(self) -> Iterator[tuple[float, float, float, float]]: ...

    def __len__(self) -> int: ...

class ComboFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    POPUP_ALIGN_LEFT = 1

    HEIGHT_SMALL = 2

    HEIGHT_REGULAR = 4

    HEIGHT_LARGE = 8

    HEIGHT_LARGEST = 16

    NO_ARROW_BUTTON = 32

    NO_PREVIEW = 64

    WIDTH_FIT_PREVIEW = 128

class Cond(enum.IntEnum):
    NONE = 0

    ALWAYS = 1

    ONCE = 2

    FIRST_USE_EVER = 4

    APPEARING = 8

class ConfigFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NAV_ENABLE_KEYBOARD = 1

    NAV_ENABLE_GAMEPAD = 2

    NAV_ENABLE_SET_MOUSE_POS = 4

    NAV_NO_CAPTURE_KEYBOARD = 8

    NO_MOUSE = 16

    NO_MOUSE_CURSOR_CHANGE = 32

    IS_SRGB = 1048576

    IS_TOUCH_SCREEN = 2097152

class Context:
    def get_io_internal(self) -> IO: ...

    def get_style_internal(self) -> Style: ...

class Dir(enum.IntEnum):
    NONE = -1

    LEFT = 0

    RIGHT = 1

    UP = 2

    DOWN = 3

    COUNT = 4

class DragDropFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    SOURCE_NO_PREVIEW_TOOLTIP = 1

    SOURCE_NO_DISABLE_HOVER = 2

    SOURCE_NO_HOLD_TO_OPEN_OTHERS = 4

    SOURCE_ALLOW_NULL_ID = 8

    SOURCE_EXTERN = 16

    SOURCE_AUTO_EXPIRE_PAYLOAD = 32

    ACCEPT_BEFORE_DELIVERY = 1024

    ACCEPT_NO_DRAW_DEFAULT_RECT = 2048

    ACCEPT_NO_PREVIEW_TOOLTIP = 4096

    ACCEPT_PEEK_ONLY = 3072

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

class DrawFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    CLOSED = 1

    ROUND_CORNERS_TOP_LEFT = 16

    ROUND_CORNERS_TOP_RIGHT = 32

    ROUND_CORNERS_BOTTOM_LEFT = 64

    ROUND_CORNERS_BOTTOM_RIGHT = 128

    ROUND_CORNERS_NONE = 256

    ROUND_CORNERS_TOP = 48

    ROUND_CORNERS_BOTTOM = 192

    ROUND_CORNERS_LEFT = 80

    ROUND_CORNERS_RIGHT = 160

    ROUND_CORNERS_ALL = 240

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
    def add_font_default(self, font_cfg: FontConfig | None = None) -> Font: ...

    def add_font_from_memory_ttf(self, font_data: bytes, size_pixels: float, font_cfg: FontConfig | None = None) -> Font: ...

    def clear_tex_data(self) -> None: ...

    def get_tex_data_as_rgba32(self) -> tuple[int, int, bytes]: ...

    @property
    def texture_id(self) -> int: ...

    @texture_id.setter
    def texture_id(self, arg: int, /) -> None: ...

class FontConfig:
    def __init__(self) -> None: ...

    @property
    def font_no(self) -> int: ...

    @font_no.setter
    def font_no(self, arg: int, /) -> None: ...

    @property
    def size_pixels(self) -> float: ...

    @size_pixels.setter
    def size_pixels(self, arg: float, /) -> None: ...

    @property
    def oversample_h(self) -> int: ...

    @oversample_h.setter
    def oversample_h(self, arg: int, /) -> None: ...

    @property
    def oversample_v(self) -> int: ...

    @oversample_v.setter
    def oversample_v(self, arg: int, /) -> None: ...

    @property
    def pixel_snap_h(self) -> bool: ...

    @pixel_snap_h.setter
    def pixel_snap_h(self, arg: bool, /) -> None: ...

    @property
    def glyph_extra_spacing(self) -> tuple[float, float]: ...

    @glyph_extra_spacing.setter
    def glyph_extra_spacing(self, arg: tuple[float, float], /) -> None: ...

    @property
    def glyph_offset(self) -> tuple[float, float]: ...

    @glyph_offset.setter
    def glyph_offset(self, arg: tuple[float, float], /) -> None: ...

    @property
    def glyph_min_advance_x(self) -> float: ...

    @glyph_min_advance_x.setter
    def glyph_min_advance_x(self, arg: float, /) -> None: ...

    @property
    def glyph_max_advance_x(self) -> float: ...

    @glyph_max_advance_x.setter
    def glyph_max_advance_x(self, arg: float, /) -> None: ...

    @property
    def merge_mode(self) -> bool: ...

    @merge_mode.setter
    def merge_mode(self, arg: bool, /) -> None: ...

    @property
    def font_builder_flags(self) -> int: ...

    @font_builder_flags.setter
    def font_builder_flags(self, arg: int, /) -> None: ...

    @property
    def rasterizer_multiply(self) -> float: ...

    @rasterizer_multiply.setter
    def rasterizer_multiply(self, arg: float, /) -> None: ...

    @property
    def rasterizer_density(self) -> float: ...

    @rasterizer_density.setter
    def rasterizer_density(self, arg: float, /) -> None: ...

    @property
    def ellipsis_char(self) -> int: ...

    @ellipsis_char.setter
    def ellipsis_char(self, arg: int, /) -> None: ...

class HoveredFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    CHILD_WINDOWS = 1

    ROOT_WINDOW = 2

    ANY_WINDOW = 4

    NO_POPUP_HIERARCHY = 8

    ALLOW_WHEN_BLOCKED_BY_POPUP = 32

    ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM = 128

    ALLOW_WHEN_OVERLAPPED_BY_ITEM = 256

    ALLOW_WHEN_OVERLAPPED_BY_WINDOW = 512

    ALLOW_WHEN_DISABLED = 1024

    NO_NAV_OVERRIDE = 2048

    ALLOW_WHEN_OVERLAPPED = 768

    RECT_ONLY = 928

    ROOT_AND_CHILD_WINDOWS = 3

    FOR_TOOLTIP = 4096

    STATIONARY = 8192

    DELAY_NONE = 16384

    DELAY_SHORT = 32768

    DELAY_NORMAL = 65536

    NO_SHARED_DELAY = 131072

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
    def config_flags(self) -> int: ...

    @config_flags.setter
    def config_flags(self, arg: int, /) -> None: ...

    @property
    def backend_flags(self) -> int: ...

    @backend_flags.setter
    def backend_flags(self, arg: int, /) -> None: ...

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
    def ini_saving_rate(self) -> float: ...

    @ini_saving_rate.setter
    def ini_saving_rate(self, arg: float, /) -> None: ...

    @property
    def ini_filename(self, /) -> str | None: ...

    @ini_filename.setter
    def ini_filename(self, filename: str | None, /) -> None: ...

    @property
    def log_filename(self, /) -> str | None: ...

    @log_filename.setter
    def log_filename(self, filename: str | None, /) -> None: ...

    @property
    def fonts(self) -> FontAtlas: ...

    @fonts.setter
    def fonts(self, arg: FontAtlas, /) -> None: ...

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

    @property
    def want_capture_mouse(self) -> bool: ...

    @property
    def want_capture_keyboard(self) -> bool: ...

    @property
    def want_text_input(self) -> bool: ...

    @property
    def want_set_mouse_pos(self) -> bool: ...

    @property
    def want_save_ini_settings(self) -> bool: ...

    @property
    def nav_active(self) -> bool: ...

    @property
    def nav_visible(self) -> bool: ...

    @property
    def framerate(self) -> float: ...

    @property
    def metrics_render_vertices(self) -> int: ...

    @property
    def metrics_render_indices(self) -> int: ...

    @property
    def metrics_render_windows(self) -> int: ...

    @property
    def metrics_active_windows(self) -> int: ...

    @property
    def mouse_delta(self) -> tuple[float, float]: ...

class InputTextFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    CHARS_DECIMAL = 1

    CHARS_HEXADECIMAL = 2

    CHARS_UPPERCASE = 4

    CHARS_NO_BLANK = 8

    AUTO_SELECT_ALL = 16

    ENTER_RETURNS_TRUE = 32

    CALLBACK_COMPLETION = 64

    CALLBACK_HISTORY = 128

    CALLBACK_ALWAYS = 256

    CALLBACK_CHAR_FILTER = 512

    ALLOW_TAB_INPUT = 1024

    CTRL_ENTER_FOR_NEW_LINE = 2048

    NO_HORIZONTAL_SCROLL = 4096

    ALWAYS_OVERWRITE = 8192

    READ_ONLY = 16384

    PASSWORD = 32768

    NO_UNDO_REDO = 65536

    CHARS_SCIENTIFIC = 131072

    CALLBACK_RESIZE = 262144

    CALLBACK_EDIT = 524288

    ESCAPE_CLEARS_ALL = 1048576

class Key(enum.IntEnum):
    KEY_NONE = 0

    KEY_TAB = 512

    KEY_LEFT_ARROW = 513

    KEY_RIGHT_ARROW = 514

    KEY_UP_ARROW = 515

    KEY_DOWN_ARROW = 516

    KEY_PAGE_UP = 517

    KEY_PAGE_DOWN = 518

    KEY_HOME = 519

    KEY_END = 520

    KEY_INSERT = 521

    KEY_DELETE = 522

    KEY_BACKSPACE = 523

    KEY_SPACE = 524

    KEY_ENTER = 525

    KEY_ESCAPE = 526

    KEY_LEFT_CTRL = 527

    KEY_LEFT_SHIFT = 528

    KEY_LEFT_ALT = 529

    KEY_LEFT_SUPER = 530

    KEY_RIGHT_CTRL = 531

    KEY_RIGHT_SHIFT = 532

    KEY_RIGHT_ALT = 533

    KEY_RIGHT_SUPER = 534

    KEY_MENU = 535

    KEY_0 = 536

    KEY_1 = 537

    KEY_2 = 538

    KEY_3 = 539

    KEY_4 = 540

    KEY_5 = 541

    KEY_6 = 542

    KEY_7 = 543

    KEY_8 = 544

    KEY_9 = 545

    KEY_A = 546

    KEY_B = 547

    KEY_C = 548

    KEY_D = 549

    KEY_E = 550

    KEY_F = 551

    KEY_G = 552

    KEY_H = 553

    KEY_I = 554

    KEY_J = 555

    KEY_K = 556

    KEY_L = 557

    KEY_M = 558

    KEY_N = 559

    KEY_O = 560

    KEY_P = 561

    KEY_Q = 562

    KEY_R = 563

    KEY_S = 564

    KEY_T = 565

    KEY_U = 566

    KEY_V = 567

    KEY_W = 568

    KEY_X = 569

    KEY_Y = 570

    KEY_Z = 571

    KEY_F1 = 572

    KEY_F2 = 573

    KEY_F3 = 574

    KEY_F4 = 575

    KEY_F5 = 576

    KEY_F6 = 577

    KEY_F7 = 578

    KEY_F8 = 579

    KEY_F9 = 580

    KEY_F10 = 581

    KEY_F11 = 582

    KEY_F12 = 583

    KEY_F13 = 584

    KEY_F14 = 585

    KEY_F15 = 586

    KEY_F16 = 587

    KEY_F17 = 588

    KEY_F18 = 589

    KEY_F19 = 590

    KEY_F20 = 591

    KEY_F21 = 592

    KEY_F22 = 593

    KEY_F23 = 594

    KEY_F24 = 595

    KEY_APOSTROPHE = 596

    KEY_COMMA = 597

    KEY_MINUS = 598

    KEY_PERIOD = 599

    KEY_SLASH = 600

    KEY_SEMICOLON = 601

    KEY_EQUAL = 602

    KEY_LEFT_BRACKET = 603

    KEY_BACKSLASH = 604

    KEY_RIGHT_BRACKET = 605

    KEY_GRAVE_ACCENT = 606

    KEY_CAPS_LOCK = 607

    KEY_SCROLL_LOCK = 608

    KEY_NUM_LOCK = 609

    KEY_PRINT_SCREEN = 610

    KEY_PAUSE = 611

    KEY_KEYPAD0 = 612

    KEY_KEYPAD1 = 613

    KEY_KEYPAD2 = 614

    KEY_KEYPAD3 = 615

    KEY_KEYPAD4 = 616

    KEY_KEYPAD5 = 617

    KEY_KEYPAD6 = 618

    KEY_KEYPAD7 = 619

    KEY_KEYPAD8 = 620

    KEY_KEYPAD9 = 621

    KEY_KEYPAD_DECIMAL = 622

    KEY_KEYPAD_DIVIDE = 623

    KEY_KEYPAD_MULTIPLY = 624

    KEY_KEYPAD_SUBTRACT = 625

    KEY_KEYPAD_ADD = 626

    KEY_KEYPAD_ENTER = 627

    KEY_KEYPAD_EQUAL = 628

    KEY_APP_BACK = 629

    KEY_APP_FORWARD = 630

    KEY_GAMEPAD_START = 631

    KEY_GAMEPAD_BACK = 632

    KEY_GAMEPAD_FACE_LEFT = 633

    KEY_GAMEPAD_FACE_RIGHT = 634

    KEY_GAMEPAD_FACE_UP = 635

    KEY_GAMEPAD_FACE_DOWN = 636

    KEY_GAMEPAD_DPAD_LEFT = 637

    KEY_GAMEPAD_DPAD_RIGHT = 638

    KEY_GAMEPAD_DPAD_UP = 639

    KEY_GAMEPAD_DPAD_DOWN = 640

    KEY_GAMEPAD_L1 = 641

    KEY_GAMEPAD_R1 = 642

    KEY_GAMEPAD_L2 = 643

    KEY_GAMEPAD_R2 = 644

    KEY_GAMEPAD_L3 = 645

    KEY_GAMEPAD_R3 = 646

    KEY_GAMEPAD_L_STICK_LEFT = 647

    KEY_GAMEPAD_L_STICK_RIGHT = 648

    KEY_GAMEPAD_L_STICK_UP = 649

    KEY_GAMEPAD_L_STICK_DOWN = 650

    KEY_GAMEPAD_R_STICK_LEFT = 651

    KEY_GAMEPAD_R_STICK_RIGHT = 652

    KEY_GAMEPAD_R_STICK_UP = 653

    KEY_GAMEPAD_R_STICK_DOWN = 654

    KEY_MOUSE_LEFT = 655

    KEY_MOUSE_RIGHT = 656

    KEY_MOUSE_MIDDLE = 657

    KEY_MOUSE_X1 = 658

    KEY_MOUSE_X2 = 659

    KEY_MOUSE_WHEEL_X = 660

    KEY_MOUSE_WHEEL_Y = 661

    KEY_RESERVED_FOR_MOD_CTRL = 662

    KEY_RESERVED_FOR_MOD_SHIFT = 663

    KEY_RESERVED_FOR_MOD_ALT = 664

    KEY_RESERVED_FOR_MOD_SUPER = 665

    KEY_COUNT = 666

    MOD_NONE = 0

    MOD_CTRL = 4096

    MOD_SHIFT = 8192

    MOD_ALT = 16384

    MOD_SUPER = 32768

    MOD_SHORTCUT = 2048

    KEY_NAMED_KEY_BEGIN = 512

    KEY_NAMED_KEY_END = 666

    KEY_NAMED_KEY_COUNT = 154

    KEY_KEYS_DATA_SIZE = 666

    KEY_KEYS_DATA_OFFSET = 0

class MouseButton(enum.IntEnum):
    LEFT = 0

    RIGHT = 1

    MIDDLE = 2

    COUNT = 5

class MouseCursor(enum.IntEnum):
    NONE = -1

    ARROW = 0

    TEXT_INPUT = 1

    RESIZE_ALL = 2

    RESIZE_NS = 3

    RESIZE_EW = 4

    RESIZE_NESW = 5

    RESIZE_NWSE = 6

    HAND = 7

    NOT_ALLOWED = 8

    COUNT = 9

class PopupFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    MOUSE_BUTTON_LEFT = 0

    MOUSE_BUTTON_RIGHT = 1

    MOUSE_BUTTON_MIDDLE = 2

    NO_REOPEN = 32

    NO_OPEN_OVER_EXISTING_POPUP = 128

    NO_OPEN_OVER_ITEMS = 256

    ANY_POPUP_ID = 1024

    ANY_POPUP_LEVEL = 2048

    ANY_POPUP = 3072

class SelectableFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    DONT_CLOSE_POPUPS = 1

    SPAN_ALL_COLUMNS = 2

    ALLOW_DOUBLE_CLICK = 4

    DISABLED = 8

    ALLOW_OVERLAP = 16

class SliderFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    ALWAYS_CLAMP = 16

    LOGARITHMIC = 32

    NO_ROUND_TO_FORMAT = 64

    NO_INPUT = 128

class Style:
    @property
    def alpha(self) -> float: ...

    @alpha.setter
    def alpha(self, arg: float, /) -> None: ...

    @property
    def disabled_alpha(self) -> float: ...

    @disabled_alpha.setter
    def disabled_alpha(self, arg: float, /) -> None: ...

    @property
    def window_padding(self) -> tuple[float, float]: ...

    @window_padding.setter
    def window_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def window_rounding(self) -> float: ...

    @window_rounding.setter
    def window_rounding(self, arg: float, /) -> None: ...

    @property
    def window_border_size(self) -> float: ...

    @window_border_size.setter
    def window_border_size(self, arg: float, /) -> None: ...

    @property
    def window_min_size(self) -> tuple[float, float]: ...

    @window_min_size.setter
    def window_min_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def window_title_align(self) -> tuple[float, float]: ...

    @window_title_align.setter
    def window_title_align(self, arg: tuple[float, float], /) -> None: ...

    @property
    def window_menu_button_position(self) -> int: ...

    @window_menu_button_position.setter
    def window_menu_button_position(self, arg: int, /) -> None: ...

    @property
    def child_rounding(self) -> float: ...

    @child_rounding.setter
    def child_rounding(self, arg: float, /) -> None: ...

    @property
    def child_border_size(self) -> float: ...

    @child_border_size.setter
    def child_border_size(self, arg: float, /) -> None: ...

    @property
    def popup_rounding(self) -> float: ...

    @popup_rounding.setter
    def popup_rounding(self, arg: float, /) -> None: ...

    @property
    def popup_border_size(self) -> float: ...

    @popup_border_size.setter
    def popup_border_size(self, arg: float, /) -> None: ...

    @property
    def frame_padding(self) -> tuple[float, float]: ...

    @frame_padding.setter
    def frame_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def frame_rounding(self) -> float: ...

    @frame_rounding.setter
    def frame_rounding(self, arg: float, /) -> None: ...

    @property
    def frame_border_size(self) -> float: ...

    @frame_border_size.setter
    def frame_border_size(self, arg: float, /) -> None: ...

    @property
    def item_spacing(self) -> tuple[float, float]: ...

    @item_spacing.setter
    def item_spacing(self, arg: tuple[float, float], /) -> None: ...

    @property
    def item_inner_spacing(self) -> tuple[float, float]: ...

    @item_inner_spacing.setter
    def item_inner_spacing(self, arg: tuple[float, float], /) -> None: ...

    @property
    def cell_padding(self) -> tuple[float, float]: ...

    @cell_padding.setter
    def cell_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def touch_extra_padding(self) -> tuple[float, float]: ...

    @touch_extra_padding.setter
    def touch_extra_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def indent_spacing(self) -> float: ...

    @indent_spacing.setter
    def indent_spacing(self, arg: float, /) -> None: ...

    @property
    def columns_min_spacing(self) -> float: ...

    @columns_min_spacing.setter
    def columns_min_spacing(self, arg: float, /) -> None: ...

    @property
    def scrollbar_size(self) -> float: ...

    @scrollbar_size.setter
    def scrollbar_size(self, arg: float, /) -> None: ...

    @property
    def scrollbar_rounding(self) -> float: ...

    @scrollbar_rounding.setter
    def scrollbar_rounding(self, arg: float, /) -> None: ...

    @property
    def grab_min_size(self) -> float: ...

    @grab_min_size.setter
    def grab_min_size(self, arg: float, /) -> None: ...

    @property
    def grab_rounding(self) -> float: ...

    @grab_rounding.setter
    def grab_rounding(self, arg: float, /) -> None: ...

    @property
    def log_slider_deadzone(self) -> float: ...

    @log_slider_deadzone.setter
    def log_slider_deadzone(self, arg: float, /) -> None: ...

    @property
    def tab_rounding(self) -> float: ...

    @tab_rounding.setter
    def tab_rounding(self, arg: float, /) -> None: ...

    @property
    def tab_border_size(self) -> float: ...

    @tab_border_size.setter
    def tab_border_size(self, arg: float, /) -> None: ...

    @property
    def tab_min_width_for_close_button(self) -> float: ...

    @tab_min_width_for_close_button.setter
    def tab_min_width_for_close_button(self, arg: float, /) -> None: ...

    @property
    def tab_bar_border_size(self) -> float: ...

    @tab_bar_border_size.setter
    def tab_bar_border_size(self, arg: float, /) -> None: ...

    @property
    def table_angled_headers_angle(self) -> float: ...

    @table_angled_headers_angle.setter
    def table_angled_headers_angle(self, arg: float, /) -> None: ...

    @property
    def color_button_position(self) -> int: ...

    @color_button_position.setter
    def color_button_position(self, arg: int, /) -> None: ...

    @property
    def button_text_align(self) -> tuple[float, float]: ...

    @button_text_align.setter
    def button_text_align(self, arg: tuple[float, float], /) -> None: ...

    @property
    def selectable_text_align(self) -> tuple[float, float]: ...

    @selectable_text_align.setter
    def selectable_text_align(self, arg: tuple[float, float], /) -> None: ...

    @property
    def separator_text_border_size(self) -> float: ...

    @separator_text_border_size.setter
    def separator_text_border_size(self, arg: float, /) -> None: ...

    @property
    def separator_text_align(self) -> tuple[float, float]: ...

    @separator_text_align.setter
    def separator_text_align(self, arg: tuple[float, float], /) -> None: ...

    @property
    def separator_text_padding(self) -> tuple[float, float]: ...

    @separator_text_padding.setter
    def separator_text_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def display_window_padding(self) -> tuple[float, float]: ...

    @display_window_padding.setter
    def display_window_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def display_safe_area_padding(self) -> tuple[float, float]: ...

    @display_safe_area_padding.setter
    def display_safe_area_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def mouse_cursor_scale(self) -> float: ...

    @mouse_cursor_scale.setter
    def mouse_cursor_scale(self, arg: float, /) -> None: ...

    @property
    def anti_aliased_lines(self) -> bool: ...

    @anti_aliased_lines.setter
    def anti_aliased_lines(self, arg: bool, /) -> None: ...

    @property
    def anti_aliased_lines_use_tex(self) -> bool: ...

    @anti_aliased_lines_use_tex.setter
    def anti_aliased_lines_use_tex(self, arg: bool, /) -> None: ...

    @property
    def anti_aliased_fill(self) -> bool: ...

    @anti_aliased_fill.setter
    def anti_aliased_fill(self, arg: bool, /) -> None: ...

    @property
    def curve_tessellation_tol(self) -> float: ...

    @curve_tessellation_tol.setter
    def curve_tessellation_tol(self, arg: float, /) -> None: ...

    @property
    def circle_tessellation_max_error(self) -> float: ...

    @circle_tessellation_max_error.setter
    def circle_tessellation_max_error(self, arg: float, /) -> None: ...

    @property
    def colors(self) -> ColorsArray: ...

    @property
    def hover_stationary_delay(self) -> float: ...

    @hover_stationary_delay.setter
    def hover_stationary_delay(self, arg: float, /) -> None: ...

    @property
    def hover_delay_short(self) -> float: ...

    @hover_delay_short.setter
    def hover_delay_short(self, arg: float, /) -> None: ...

    @property
    def hover_delay_normal(self) -> float: ...

    @hover_delay_normal.setter
    def hover_delay_normal(self, arg: float, /) -> None: ...

    @property
    def hover_flags_for_tooltip_mouse(self) -> int: ...

    @hover_flags_for_tooltip_mouse.setter
    def hover_flags_for_tooltip_mouse(self, arg: int, /) -> None: ...

    @property
    def hover_flags_for_tooltip_nav(self) -> int: ...

    @hover_flags_for_tooltip_nav.setter
    def hover_flags_for_tooltip_nav(self, arg: int, /) -> None: ...

    def scale_all_sizes(self, scale_factor: float) -> None: ...

class StyleVar(enum.IntEnum):
    ALPHA = 0

    DISABLED_ALPHA = 1

    WINDOW_PADDING = 2

    WINDOW_ROUNDING = 3

    WINDOW_BORDER_SIZE = 4

    WINDOW_MIN_SIZE = 5

    WINDOW_TITLE_ALIGN = 6

    CHILD_ROUNDING = 7

    CHILD_BORDER_SIZE = 8

    POPUP_ROUNDING = 9

    POPUP_BORDER_SIZE = 10

    FRAME_PADDING = 11

    FRAME_ROUNDING = 12

    FRAME_BORDER_SIZE = 13

    ITEM_SPACING = 14

    ITEM_INNER_SPACING = 15

    INDENT_SPACING = 16

    CELL_PADDING = 17

    SCROLLBAR_SIZE = 18

    SCROLLBAR_ROUNDING = 19

    GRAB_MIN_SIZE = 20

    GRAB_ROUNDING = 21

    TAB_ROUNDING = 22

    TAB_BORDER_SIZE = 23

    TAB_BAR_BORDER_SIZE = 24

    TABLE_ANGLED_HEADERS_ANGLE = 25

    BUTTON_TEXT_ALIGN = 26

    SELECTABLE_TEXT_ALIGN = 27

    SEPARATOR_TEXT_BORDER_SIZE = 28

    SEPARATOR_TEXT_ALIGN = 29

    SEPARATOR_TEXT_PADDING = 30

    COUNT = 31

class TabBarFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    REORDERABLE = 1

    AUTO_SELECT_NEW_TABS = 2

    TAB_LIST_POPUP_BUTTON = 4

    NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON = 8

    NO_TAB_LIST_SCROLLING_BUTTONS = 16

    NO_TOOLTIP = 32

    FITTING_POLICY_RESIZE_DOWN = 64

    FITTING_POLICY_SCROLL = 128

class TabItemFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    UNSAVED_DOCUMENT = 1

    SET_SELECTED = 2

    NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON = 4

    NO_PUSH_ID = 8

    NO_TOOLTIP = 16

    NO_REORDER = 32

    LEADING = 64

    TRAILING = 128

    NO_ASSUMED_CLOSURE = 256

class TableBgTarget(enum.IntEnum):
    NONE = 0

    ROW_BG0 = 1

    ROW_BG1 = 2

    CELL_BG = 3

class TableColumnFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    DISABLED = 1

    DEFAULT_HIDE = 2

    DEFAULT_SORT = 4

    WIDTH_STRETCH = 8

    WIDTH_FIXED = 16

    NO_RESIZE = 32

    NO_REORDER = 64

    NO_HIDE = 128

    NO_CLIP = 256

    NO_SORT = 512

    NO_SORT_ASCENDING = 1024

    NO_SORT_DESCENDING = 2048

    NO_HEADER_LABEL = 4096

    NO_HEADER_WIDTH = 8192

    PREFER_SORT_ASCENDING = 16384

    PREFER_SORT_DESCENDING = 32768

    INDENT_ENABLE = 65536

    INDENT_DISABLE = 131072

    ANGLED_HEADER = 262144

    IS_ENABLED = 16777216

    IS_VISIBLE = 33554432

    IS_SORTED = 67108864

    IS_HOVERED = 134217728

class TableFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    RESIZABLE = 1

    REORDERABLE = 2

    HIDEABLE = 4

    SORTABLE = 8

    NO_SAVED_SETTINGS = 16

    CONTEXT_MENU_IN_BODY = 32

    ROW_BG = 64

    BORDERS_INNER_H = 128

    BORDERS_OUTER_H = 256

    BORDERS_INNER_V = 512

    BORDERS_OUTER_V = 1024

    BORDERS_H = 384

    BORDERS_V = 1536

    BORDERS_INNER = 640

    BORDERS_OUTER = 1280

    BORDERS = 1920

    NO_BORDERS_IN_BODY = 2048

    NO_BORDERS_IN_BODY_UNTIL_RESIZE = 4096

    SIZING_FIXED_FIT = 8192

    SIZING_FIXED_SAME = 16384

    SIZING_STRETCH_PROP = 24576

    SIZING_STRETCH_SAME = 32768

    NO_HOST_EXTEND_X = 65536

    NO_HOST_EXTEND_Y = 131072

    NO_KEEP_COLUMNS_VISIBLE = 262144

    PRECISE_WIDTHS = 524288

    NO_CLIP = 1048576

    PAD_OUTER_X = 2097152

    NO_PAD_OUTER_X = 4194304

    NO_PAD_INNER_X = 8388608

    SCROLL_X = 16777216

    SCROLL_Y = 33554432

    SORT_MULTI = 67108864

    SORT_TRISTATE = 134217728

    HIGHLIGHT_HOVERED_COLUMN = 268435456

class TableRowFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HEADERS = 1

class TreeNodeFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    SELECTED = 1

    FRAMED = 2

    ALLOW_OVERLAP = 4

    NO_TREE_PUSH_ON_OPEN = 8

    NO_AUTO_OPEN_ON_LOG = 16

    DEFAULT_OPEN = 32

    OPEN_ON_DOUBLE_CLICK = 64

    OPEN_ON_ARROW = 128

    LEAF = 256

    BULLET = 512

    FRAME_PADDING = 1024

    SPAN_AVAIL_WIDTH = 2048

    SPAN_FULL_WIDTH = 4096

    SPAN_ALL_COLUMNS = 8192

    NAV_LEFT_JUMPS_BACK_HERE = 16384

    COLLAPSING_HEADER = 26

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

    def get_center(self) -> tuple[float, float]: ...

    def get_work_center(self) -> tuple[float, float]: ...

class WindowFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_TITLE_BAR = 1

    NO_RESIZE = 2

    NO_MOVE = 4

    NO_SCROLLBAR = 8

    NO_SCROLL_WITH_MOUSE = 16

    NO_COLLAPSE = 32

    ALWAYS_AUTO_RESIZE = 64

    NO_BACKGROUND = 128

    NO_SAVED_SETTINGS = 256

    NO_MOUSE_INPUTS = 512

    MENU_BAR = 1024

    HORIZONTAL_SCROLLBAR = 2048

    NO_FOCUS_ON_APPEARING = 4096

    NO_BRING_TO_FRONT_ON_FOCUS = 8192

    ALWAYS_VERTICAL_SCROLLBAR = 16384

    ALWAYS_HORIZONTAL_SCROLLBAR = 32768

    NO_NAV_INPUTS = 65536

    NO_NAV_FOCUS = 131072

    UNSAVED_DOCUMENT = 262144

    NO_NAV = 196608

    NO_DECORATION = 43

    NO_INPUTS = 197120

    NAV_FLATTENED = 8388608

    CHILD_WINDOW = 16777216

    TOOLTIP = 33554432

    POPUP = 67108864

    MODAL = 134217728

    CHILD_MENU = 268435456

def align_text_to_frame_padding() -> None: ...

def arrow_button(str_id: str, dir: int) -> bool: ...

def begin(name: str, closable: bool = False, flags: WindowFlags = WindowFlags.NONE) -> tuple[bool, bool]: ...

def begin_child(str_id: str, size: tuple[float, float] = (0.0, 0.0), child_flags: ChildFlags = ChildFlags.NONE, window_flags: WindowFlags = WindowFlags.NONE) -> bool: ...

def begin_combo(label: str, preview_value: str, flags: ComboFlags = ComboFlags.NONE) -> bool: ...

def begin_disabled(disabled: bool = True) -> None: ...

def begin_drag_drop_source(flags: DragDropFlags = DragDropFlags.NONE) -> bool: ...

def begin_drag_drop_target() -> bool: ...

def begin_group() -> None: ...

def begin_item_tooltip() -> bool: ...

def begin_list_box(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool: ...

def begin_main_menu_bar() -> bool: ...

def begin_menu(label: str, enabled: bool = True) -> bool: ...

def begin_menu_bar() -> bool: ...

def begin_popup(str_id: str, flags: WindowFlags = WindowFlags.NONE) -> bool: ...

def begin_popup_context_window(str_id: str | None = None, flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT) -> bool: ...

def begin_tab_bar(str_id: str, flags: TabBarFlags = TabBarFlags.NONE) -> bool: ...

def begin_tab_item(str_id: str, closable: bool = False, flags: TabItemFlags = TabItemFlags.NONE) -> tuple[bool, bool]: ...

def begin_table(str_id: str, column: int, flags: TableFlags = TableFlags.NONE, outer_size: tuple[float, float] = (0.0, 0.0), inner_width: float = 0.0) -> bool: ...

def begin_tooltip() -> bool: ...

def bullet_text(text: str) -> None: ...

def button(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool: ...

def calc_item_width() -> float: ...

def calc_text_size(text: str, hide_text_after_double_hash: bool = False, wrap_width: float = -1.0) -> tuple[float, float]: ...

def checkbox(label: str, v: bool) -> tuple[bool, bool]: ...

def checkbox_flags(label: str, flags: int, flags_value: int) -> tuple[bool, int]: ...

def close_current_popup() -> None: ...

def collapsing_header(label: str, visible: object | None = None, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> tuple[bool, bool | None]: ...

def color_convert_hsv_to_rgb(hsv: tuple[float, float, float, float]) -> tuple[float, float, float, float]: ...

def color_convert_rgb_to_hsv(rgba: tuple[float, float, float, float]) -> tuple[float, float, float, float]: ...

def color_edit3(label: str, col: tuple[float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float]]: ...

def color_edit4(label: str, col: tuple[float, float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]: ...

def columns(count: int = 1, id: str | None = None, border: bool = True) -> None: ...

def combo(label: str, current_item: int, items: Sequence[str], popup_max_height_in_items: int = -1) -> tuple[bool, int]: ...

def create_context(shared_font_atlas: FontAtlas | None = None) -> Context:
    """create context"""

def destroy_context(arg: Context, /) -> None: ...

def drag_float(label: str, v: float, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]: ...

def drag_float2(label: str, v: tuple[float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float]]: ...

def drag_float3(label: str, v: tuple[float, float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float]]: ...

def drag_float4(label: str, v: tuple[float, float, float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]: ...

def drag_int(label: str, v: int, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, int]: ...

def drag_int2(label: str, v: tuple[int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int]]: ...

def drag_int3(label: str, v: tuple[int, int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int]]: ...

def drag_int4(label: str, v: tuple[int, int, int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]: ...

def dummy(size: tuple[float, float]) -> None: ...

def end() -> None: ...

def end_child() -> None: ...

def end_combo() -> None: ...

def end_disabled() -> None: ...

def end_drag_drop_source() -> None: ...

def end_drag_drop_target() -> None: ...

def end_group() -> None: ...

def end_list_box() -> None: ...

def end_main_menu_bar() -> None: ...

def end_menu() -> None: ...

def end_menu_bar() -> None: ...

def end_popup() -> None: ...

def end_tab_bar() -> None: ...

def end_tab_item() -> None: ...

def end_table() -> None: ...

def end_tooltip() -> None: ...

def get_column_index() -> int: ...

def get_column_offset(column_index: int = -1) -> float: ...

def get_column_width(column_index: int = -1) -> float: ...

def get_columns_count() -> int: ...

def get_content_region_avail() -> tuple[float, float]: ...

def get_content_region_max() -> tuple[float, float]: ...

def get_current_context() -> Context: ...

def get_cursor_pos() -> tuple[float, float]: ...

def get_cursor_pos_x() -> float: ...

def get_cursor_pos_y() -> float: ...

def get_cursor_screen_pos() -> tuple[float, float]: ...

def get_cursor_start_pos() -> tuple[float, float]: ...

def get_draw_data() -> DrawData: ...

def get_font_size() -> float: ...

def get_font_tex_uv_white_pixel() -> tuple[float, float]: ...

def get_frame_count() -> int: ...

def get_frame_height() -> float: ...

def get_frame_height_with_spacing() -> float: ...

def get_io() -> IO: ...

def get_item_rect_max() -> tuple[float, float]: ...

def get_item_rect_min() -> tuple[float, float]: ...

def get_item_rect_size() -> tuple[float, float]: ...

def get_key_name(key: Key) -> str: ...

def get_key_pressed_amount(key: Key, repeat_delay: float, rate: float) -> int: ...

def get_main_viewport() -> Viewport: ...

def get_mouse_clicked_count(button: MouseButton) -> int: ...

def get_mouse_cursor() -> MouseCursor: ...

def get_mouse_drag_delta(button: MouseButton = MouseButton.LEFT, lock_threshold: float = -1.0) -> tuple[float, float]: ...

def get_mouse_pos() -> tuple[float, float]: ...

def get_mouse_pos_on_opening_current_popup() -> tuple[float, float]: ...

def get_scroll_max_x() -> float: ...

def get_scroll_max_y() -> float: ...

def get_scroll_x() -> float: ...

def get_scroll_y() -> float: ...

def get_style() -> Style: ...

def get_style_color_vec4(col: Col) -> tuple[float, float, float, float]: ...

def get_text_line_height() -> float: ...

def get_text_line_height_with_spacing() -> float: ...

def get_time() -> float: ...

def get_tree_node_to_label_spacing() -> float: ...

def get_version() -> str: ...

def get_window_content_region_max() -> tuple[float, float]: ...

def get_window_content_region_min() -> tuple[float, float]: ...

def image(user_texture_id: int, image_size: tuple[float, float], uv0: tuple[float, float] = (0.0, 0.0), uv1: tuple[float, float] = (1.0, 1.0), tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), border_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)) -> None: ...

def indent(indent_w: float = 0.0) -> None: ...

def input_double(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.6f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, float]: ...

def input_float(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, float]: ...

def input_float2(label: str, v: tuple[float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float]]: ...

def input_float3(label: str, v: tuple[float, float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float, float]]: ...

def input_float4(label: str, v: tuple[float, float, float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]: ...

def input_int(label: str, v: int, step: int = 1, step_fast: int = 100, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, int]: ...

def input_int2(label: str, v: tuple[int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int]]: ...

def input_int3(label: str, v: tuple[int, int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int, int]]: ...

def input_int4(label: str, v: tuple[int, int, int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]: ...

def input_text(label: str, text: str, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]: ...

def input_text_multiline(label: str, text: str, size: tuple[float, float] = (0.0, 0.0), flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]: ...

def input_text_with_hint(label: str, hint: str, text: str, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]: ...

def invisible_button(str_id: str, size: tuple[float, float], flags: ButtonFlags = ButtonFlags.NONE) -> bool: ...

def is_any_item_active() -> bool: ...

def is_any_item_focused() -> bool: ...

def is_any_item_hovered() -> bool: ...

def is_item_activated() -> bool: ...

def is_item_active() -> bool: ...

def is_item_clicked(mouse_button: MouseButton = MouseButton.LEFT) -> bool: ...

def is_item_deactivated() -> bool: ...

def is_item_deactivated_after_edit() -> bool: ...

def is_item_edited() -> bool: ...

def is_item_focused() -> bool: ...

def is_item_hovered(flags: HoveredFlags = HoveredFlags.NONE) -> bool: ...

def is_item_toggled_open() -> bool: ...

def is_item_visible() -> bool: ...

def is_key_chord_pressed(key_chord: Key) -> bool: ...

def is_key_down(key: Key) -> bool: ...

def is_key_pressed(key: Key, repeat: bool = True) -> bool: ...

def is_key_released(key: Key) -> bool: ...

def is_mouse_clicked(button: MouseButton, repeat: bool = False) -> bool: ...

def is_mouse_double_clicked(button: MouseButton) -> bool: ...

def is_mouse_down(button: MouseButton) -> bool: ...

def is_mouse_dragging(button: MouseButton, lock_threshold: float = -1.0) -> bool: ...

def is_mouse_hovering_rect(r_min: tuple[float, float], r_max: tuple[float, float], clip: bool = True) -> bool: ...

def is_mouse_pos_valid(mouse_pos: tuple[float, float] | None = None) -> bool: ...

def is_mouse_released(button: MouseButton) -> bool: ...

def is_popup_open(str_id: str, flags: PopupFlags = PopupFlags.NONE) -> bool: ...

@overload
def is_rect_visible(size: tuple[float, float]) -> bool: ...

@overload
def is_rect_visible(rect_min: tuple[float, float], rect_max: tuple[float, float]) -> bool: ...

def label_text(label: str, text: str) -> None: ...

def list_box(label: str, current_item: int, items: Sequence[str], height_in_items: int = -1) -> tuple[bool, int]: ...

def log_buttons() -> None: ...

def log_finish() -> None: ...

def log_text(text: str) -> None: ...

def log_to_clipboard(auto_open_depth: int = -1) -> None: ...

def log_to_file(auto_open_depth: int = -1, filename: str | None = None) -> None: ...

def log_to_tty(auto_open_depth: int = -1) -> None: ...

def menu_item(label: str, shortcut: str | None = None, selected: bool = False, enabled: bool = True) -> tuple[bool, bool]: ...

def new_frame() -> None: ...

def new_line() -> None: ...

def next_column() -> None: ...

def open_popup(str_id: str, flags: PopupFlags = PopupFlags.NONE) -> None: ...

def open_popup_on_item_click(str_id: str | None = None, flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT) -> None: ...

def plot_histogram(label: str, values: Annotated[ArrayLike, dict(dtype='float32', shape=(None), device='cpu', writable=False)], overlay_text: str | None = None, scale_min: float = 3.4028234663852886e+38, scale_max: float = 3.4028234663852886e+38, graph_size: tuple[float, float] = (0.0, 0.0)) -> None: ...

def plot_lines(label: str, values: Annotated[ArrayLike, dict(dtype='float32', shape=(None), device='cpu', writable=False)], overlay_text: str | None = None, scale_min: float = 3.4028234663852886e+38, scale_max: float = 3.4028234663852886e+38, graph_size: tuple[float, float] = (0.0, 0.0)) -> None: ...

def pop_button_repeat() -> None: ...

def pop_font() -> None: ...

def pop_id() -> None: ...

def pop_item_width() -> None: ...

def pop_style_color(count: int = 1) -> None: ...

def pop_style_var(count: int = 1) -> None: ...

def pop_tab_stop() -> None: ...

def pop_text_wrap_pos() -> None: ...

def push_button_repeat(repeat: bool) -> None: ...

def push_font(font: Font | None) -> None: ...

@overload
def push_id(str_id: str) -> None: ...

@overload
def push_id(int_id: int) -> None: ...

def push_item_width(item_width: float) -> None: ...

@overload
def push_style_color(idx: Col, col: int) -> None: ...

@overload
def push_style_color(idx: Col, col: tuple[float, float, float, float]) -> None: ...

@overload
def push_style_color(idx: Col, col: tuple[float, float, float]) -> None: ...

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

def reset_mouse_drag_delta(button: MouseButton = MouseButton.LEFT) -> None: ...

def same_line(offset_from_start_x: float = 0.0, spacing: float = -1.0) -> None: ...

def selectable(label: str, selected: bool = False, flags: SelectableFlags = SelectableFlags.NONE, size: tuple[float, float] = (0.0, 0.0)) -> tuple[bool, bool]: ...

def separator() -> None: ...

def separator_text(text: str) -> None: ...

def set_column_offset(column_index: int, offset_x: float) -> None: ...

def set_column_width(column_index: int, width: float) -> None: ...

def set_cursor_pos(local_pos: tuple[float, float]) -> None: ...

def set_cursor_pos_x(local_x: float) -> None: ...

def set_cursor_pos_y(local_y: float) -> None: ...

def set_cursor_screen_pos(pos: tuple[float, float]) -> None: ...

def set_item_default_focus() -> None: ...

def set_item_tooltip(text: str) -> None: ...

def set_keyboard_focus_here(offset: int = 0) -> None: ...

def set_mouse_cursor(cursor_type: MouseCursor) -> None: ...

def set_next_frame_want_capture_keyboard(want_capture_keyboard: bool) -> None: ...

def set_next_frame_want_capture_mouse(capture: bool) -> None: ...

def set_next_item_open(is_open: bool, cond: Cond = Cond.NONE) -> None: ...

def set_next_item_width(item_width: float) -> None: ...

def set_next_window_bg_alpha(alpha: float) -> None: ...

def set_next_window_collapsed(collapsed: bool, cond: Cond = Cond.NONE) -> None: ...

def set_next_window_content_size(size: tuple[float, float]) -> None: ...

def set_next_window_focus() -> None: ...

def set_next_window_pos(pos: tuple[float, float], cond: Cond = Cond.NONE, pivot: tuple[float, float] = (0.0, 0.0)) -> None: ...

def set_next_window_scroll(scroll: tuple[float, float]) -> None: ...

def set_next_window_size(size: tuple[float, float], cond: Cond = Cond.NONE) -> None: ...

def set_scroll_from_pos_x(local_x: float, center_x_ratio: float = 0.5) -> None: ...

def set_scroll_from_pos_y(local_y: float, center_y_ratio: float = 0.5) -> None: ...

def set_scroll_here_x(center_x_ratio: float = 0.5) -> None: ...

def set_scroll_here_y(center_y_ratio: float = 0.5) -> None: ...

def set_scroll_x(scroll_x: float) -> None: ...

def set_scroll_y(scroll_y: float) -> None: ...

def set_tab_item_closed(label: str) -> None: ...

def set_tooltip(text: str) -> None: ...

@overload
def set_window_collapsed(collapsed: bool, cond: Cond = Cond.NONE) -> None: ...

@overload
def set_window_collapsed(name: str, collapsed: bool, cond: Cond = Cond.NONE) -> None: ...

@overload
def set_window_focus() -> None: ...

@overload
def set_window_focus(name: str) -> None: ...

def set_window_font_scale(scale: float) -> None: ...

@overload
def set_window_pos(pos: tuple[float, float], cond: Cond = Cond.NONE) -> None: ...

@overload
def set_window_pos(name: str, pos: tuple[float, float], cond: Cond = Cond.NONE) -> None: ...

@overload
def set_window_size(size: tuple[float, float], cond: Cond = Cond.NONE) -> None: ...

@overload
def set_window_size(name: str, size: tuple[float, float], cond: Cond = Cond.NONE) -> None: ...

def show_debug_log_window(closable: bool = False) -> bool: ...

def show_id_stack_tool_window(closable: bool = False) -> bool: ...

def show_metrics_window(closable: bool = False) -> bool: ...

def show_style_editor() -> None: ...

def show_user_guide() -> None: ...

def slider_angle(label: str, v: float, v_degrees_min: float = -360.0, v_degrees_max: float = 360.0, format: str = '%.0f deg', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]: ...

def slider_float(label: str, v: float, v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]: ...

def slider_float2(label: str, v: tuple[float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float]]: ...

def slider_float3(label: str, v: tuple[float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float]]: ...

def slider_float4(label: str, v: tuple[float, float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]: ...

def slider_int(label: str, v: int, v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, int]: ...

def slider_int2(label: str, v: tuple[int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int]]: ...

def slider_int3(label: str, v: tuple[int, int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int]]: ...

def slider_int4(label: str, v: tuple[int, int, int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]: ...

def small_button(label: str) -> bool: ...

def spacing() -> None: ...

def tab_item_button(label: str, flags: TabItemFlags = TabItemFlags.NONE) -> bool: ...

def table_angled_headers_row() -> None: ...

def table_get_column_count() -> int: ...

def table_get_column_flags(column_n: int = -1) -> TableColumnFlags: ...

def table_get_column_index() -> int: ...

def table_get_column_name(column_n: int = -1) -> str: ...

def table_get_row_index() -> int: ...

def table_header(label: str) -> None: ...

def table_headers_row() -> None: ...

def table_next_column() -> bool: ...

def table_next_row(flags: TableRowFlags = TableRowFlags.NONE, min_row_height: float = 0.0) -> None: ...

def table_set_bg_color(target: TableBgTarget, color: tuple[float, float, float, float], column_n: int = -1) -> None: ...

def table_set_column_enabled(column_n: int, v: bool) -> None: ...

def table_set_column_index(column_n: int) -> bool: ...

def table_setup_column(label: str, flags: TableColumnFlags = TableColumnFlags.NONE, init_width_or_weight: float = 0.0, user_id: int = 0) -> None: ...

def table_setup_scroll_freeze(cols: int, rows: int) -> None: ...

def text(text: str) -> None: ...

def text_colored(col: tuple[float, float, float, float], text: str) -> None: ...

def text_disabled(text: str) -> None: ...

def text_wrapped(text: str) -> None: ...

@overload
def tree_node(label: str, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> bool: ...

@overload
def tree_node(str_id: str, text: str, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> bool: ...

def tree_pop() -> None: ...

def tree_push(str_id: str) -> None: ...

def unindent(indent_w: float = 0.0) -> None: ...
