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
    """Backend Platform supports gamepad and currently has one connected."""

    HAS_MOUSE_CURSORS = 2
    """
    Backend Platform supports honoring `get_mouse_cursor()` value to change the OS cursor shape.
    """

    HAS_SET_MOUSE_POS = 4
    """
    Backend Platform supports io.WantSetMousePos requests to reposition the OS mouse position (only used if io.ConfigNavMoveSetMousePos is set).
    """

    RENDERER_HAS_VTX_OFFSET = 8
    """
    Backend Renderer supports ImDrawCmd::VtxOffset. This enables output of large meshes (64K+ vertices) while still using 16-bit indices.
    """

class ButtonFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    MOUSE_BUTTON_LEFT = 1
    """React on left mouse button (default)"""

    MOUSE_BUTTON_RIGHT = 2
    """React on right mouse button"""

    MOUSE_BUTTON_MIDDLE = 4
    """React on center mouse button"""

    ENABLE_NAV = 8
    """
    `invisible_button()`: do not disable navigation/tabbing. Otherwise disabled by default.
    """

COL32_BLACK: int = 4278190080

COL32_BLACK_TRANS: int = 0

COL32_WHITE: int = 4294967295

class ChildFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    BORDERS = 1
    """
    Show an outer border and enable WindowPadding. (IMPORTANT: this is always == 1 == true for legacy reason)
    """

    ALWAYS_USE_WINDOW_PADDING = 2
    """
    Pad with style.WindowPadding even if no border are drawn (no padding by default for non-bordered child windows because it makes more sense)
    """

    RESIZE_X = 4
    """
    Allow resize from right border (layout direction). Enable .ini saving (unless `WindowFlags.NO_SAVED_SETTINGS` passed to window flags)
    """

    RESIZE_Y = 8
    """Allow resize from bottom border (layout direction)."""

    AUTO_RESIZE_X = 16
    """
    Enable auto-resizing width. Read IMPORTANT: Size measurement" details above.
    """

    AUTO_RESIZE_Y = 32
    """
    Enable auto-resizing height. Read IMPORTANT: Size measurement" details above.
    """

    ALWAYS_AUTO_RESIZE = 64
    """
    Combined with AutoResizeX/AutoResizeY. Always measure size even when child is hidden, always return true, always disable clipping optimization! NOT RECOMMENDED.
    """

    FRAME_STYLE = 128
    """
    Style the child window like a framed item: use FrameBg, FrameRounding, FrameBorderSize, FramePadding instead of ChildBg, ChildRounding, ChildBorderSize, WindowPadding.
    """

    NAV_FLATTENED = 256
    """
    [BETA] Share focus scope, allow keyboard/gamepad navigation to cross over parent border to this child or between sibling child windows.
    """

class Col(enum.IntEnum):
    TEXT = 0

    TEXT_DISABLED = 1

    WINDOW_BG = 2
    """Background of normal windows"""

    CHILD_BG = 3
    """Background of child windows"""

    POPUP_BG = 4
    """Background of popups, menus, tooltips windows"""

    BORDER = 5

    BORDER_SHADOW = 6

    FRAME_BG = 7
    """Background of checkbox, radio button, plot, slider, text input"""

    FRAME_BG_HOVERED = 8

    FRAME_BG_ACTIVE = 9

    TITLE_BG = 10
    """Title bar"""

    TITLE_BG_ACTIVE = 11
    """Title bar when focused"""

    TITLE_BG_COLLAPSED = 12
    """Title bar when collapsed"""

    MENU_BAR_BG = 13

    SCROLLBAR_BG = 14

    SCROLLBAR_GRAB = 15

    SCROLLBAR_GRAB_HOVERED = 16

    SCROLLBAR_GRAB_ACTIVE = 17

    CHECK_MARK = 18
    """`checkbox` tick and `radio_button` circle"""

    SLIDER_GRAB = 19

    SLIDER_GRAB_ACTIVE = 20

    BUTTON = 21

    BUTTON_HOVERED = 22

    BUTTON_ACTIVE = 23

    HEADER = 24
    """
    Header* colors are used for `collapsing_header`, `tree_node`, `selectable`, `menu_item`
    """

    HEADER_HOVERED = 25

    HEADER_ACTIVE = 26

    SEPARATOR = 27

    SEPARATOR_HOVERED = 28

    SEPARATOR_ACTIVE = 29

    RESIZE_GRIP = 30
    """Resize grip in lower-right and lower-left corners of windows."""

    RESIZE_GRIP_HOVERED = 31

    RESIZE_GRIP_ACTIVE = 32

    TAB_HOVERED = 33
    """Tab background, when hovered"""

    TAB = 34
    """Tab background, when tab-bar is focused & tab is unselected"""

    TAB_SELECTED = 35
    """Tab background, when tab-bar is focused & tab is selected"""

    TAB_SELECTED_OVERLINE = 36
    """Tab horizontal overline, when tab-bar is focused & tab is selected"""

    TAB_DIMMED = 37
    """Tab background, when tab-bar is unfocused & tab is unselected"""

    TAB_DIMMED_SELECTED = 38
    """Tab background, when tab-bar is unfocused & tab is selected"""

    TAB_DIMMED_SELECTED_OVERLINE = 39

    PLOT_LINES = 40

    PLOT_LINES_HOVERED = 41

    PLOT_HISTOGRAM = 42

    PLOT_HISTOGRAM_HOVERED = 43

    TABLE_HEADER_BG = 44
    """Table header background"""

    TABLE_BORDER_STRONG = 45
    """Table outer and header borders (prefer using Alpha=1.0 here)"""

    TABLE_BORDER_LIGHT = 46
    """Table inner borders (prefer using Alpha=1.0 here)"""

    TABLE_ROW_BG = 47
    """Table row background (even rows)"""

    TABLE_ROW_BG_ALT = 48
    """Table row background (odd rows)"""

    TEXT_LINK = 49
    """Hyperlink color"""

    TEXT_SELECTED_BG = 50

    DRAG_DROP_TARGET = 51
    """Rectangle highlighting a drop target"""

    NAV_CURSOR = 52
    """Color of keyboard/gamepad navigation cursor/rectangle, when visible"""

    NAV_WINDOWING_HIGHLIGHT = 53
    """Highlight window when using CTRL+TAB"""

    NAV_WINDOWING_DIM_BG = 54
    """
    Darken/colorize entire screen behind the CTRL+TAB window list, when active
    """

    MODAL_WINDOW_DIM_BG = 55
    """
    Darken/colorize entire screen behind a modal window, when one is active
    """

    COUNT = 56

class ColorEditFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_ALPHA = 2
    """
    ColorEdit, ColorPicker, `color_button`: ignore Alpha component (will only read 3 components from the input pointer).
    """

    NO_PICKER = 4
    """ColorEdit: disable picker when clicking on color square."""

    NO_OPTIONS = 8
    """
    ColorEdit: disable toggling options menu when right-clicking on inputs/small preview.
    """

    NO_SMALL_PREVIEW = 16
    """
    ColorEdit, ColorPicker: disable color square preview next to the inputs. (e.g. to show only the inputs)
    """

    NO_INPUTS = 32
    """
    ColorEdit, ColorPicker: disable inputs sliders/text widgets (e.g. to show only the small preview color square).
    """

    NO_TOOLTIP = 64
    """
    ColorEdit, ColorPicker, `color_button`: disable tooltip when hovering the preview.
    """

    NO_LABEL = 128
    """
    ColorEdit, ColorPicker: disable display of inline text label (the label is still forwarded to the tooltip and picker).
    """

    NO_SIDE_PREVIEW = 256
    """
    ColorPicker: disable bigger color preview on right side of the picker, use small color square preview instead.
    """

    NO_DRAG_DROP = 512
    """
    ColorEdit: disable drag and drop target. `color_button`: disable drag and drop source.
    """

    NO_BORDER = 1024
    """`color_button`: disable border (which is enforced by default)"""

    ALPHA_OPAQUE = 2048
    """
    ColorEdit, ColorPicker, `color_button`: disable alpha in the preview,. Contrary to _NoAlpha it may still be edited when calling `color_edit4()`/`color_picker4()`. For `color_button()` this does the same as _NoAlpha.
    """

    ALPHA_NO_BG = 4096
    """
    ColorEdit, ColorPicker, `color_button`: disable rendering a checkerboard background behind transparent color.
    """

    ALPHA_PREVIEW_HALF = 8192
    """
    ColorEdit, ColorPicker, `color_button`: display half opaque / half transparent preview.
    """

    ALPHA_BAR = 65536
    """ColorEdit, ColorPicker: show vertical alpha bar/gradient in picker."""

    HDR = 524288
    """
    (WIP) ColorEdit: Currently only disable 0.0f..1.0f limits in RGBA edition (note: you probably want to use `ColorEditFlags.FLOAT` flag as well).
    """

    DISPLAY_RGB = 1048576
    """
    ColorEdit: override _display_ type among RGB/HSV/Hex. ColorPicker: select any combination using one or more of RGB/HSV/Hex.
    """

    DISPLAY_HSV = 2097152

    DISPLAY_HEX = 4194304

    UINT8 = 8388608
    """
    ColorEdit, ColorPicker, `color_button`: _display_ values formatted as 0..255.
    """

    FLOAT = 16777216
    """
    ColorEdit, ColorPicker, `color_button`: _display_ values formatted as 0.0f..1.0f floats instead of 0..255 integers. No round-trip of value via integers.
    """

    PICKER_HUE_BAR = 33554432
    """ColorPicker: bar for Hue, rectangle for Sat/Value."""

    PICKER_HUE_WHEEL = 67108864
    """ColorPicker: wheel for Hue, triangle for Sat/Value."""

    INPUT_RGB = 134217728
    """ColorEdit, ColorPicker: input and output data in RGB format."""

    INPUT_HSV = 268435456
    """ColorEdit, ColorPicker: input and output data in HSV format."""

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
    """Align the popup toward the left by default"""

    HEIGHT_SMALL = 2
    """
    Max ~4 items visible. Tip: If you want your combo popup to be a specific size you can use `set_next_window_size_constraints()` prior to calling `begin_combo()`
    """

    HEIGHT_REGULAR = 4
    """Max ~8 items visible (default)"""

    HEIGHT_LARGE = 8
    """Max ~20 items visible"""

    HEIGHT_LARGEST = 16
    """As many fitting items as possible"""

    NO_ARROW_BUTTON = 32
    """Display on the preview box without the square arrow button"""

    NO_PREVIEW = 64
    """Display only a square arrow button"""

    WIDTH_FIT_PREVIEW = 128
    """Width dynamically calculated from preview contents"""

class Cond(enum.IntEnum):
    NONE = 0
    """No condition (always set the variable), same as _Always"""

    ALWAYS = 1
    """No condition (always set the variable), same as _None"""

    ONCE = 2
    """
    Set the variable once per runtime session (only the first call will succeed)
    """

    FIRST_USE_EVER = 4
    """
    Set the variable if the object/window has no persistently saved data (no entry in .ini file)
    """

    APPEARING = 8
    """
    Set the variable if the object/window is appearing after being hidden/inactive (or the first time)
    """

class ConfigFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NAV_ENABLE_KEYBOARD = 1
    """
    Master keyboard navigation enable flag. Enable full Tabbing + directional arrows + space/enter to activate.
    """

    NAV_ENABLE_GAMEPAD = 2
    """
    Master gamepad navigation enable flag. Backend also needs to set `BackendFlags.HAS_GAMEPAD`.
    """

    NO_MOUSE = 16
    """Instruct dear imgui to disable mouse inputs and interactions."""

    NO_MOUSE_CURSOR_CHANGE = 32
    """
    Instruct backend to not alter mouse cursor shape and visibility. Use if the backend cursor changes are interfering with yours and you don't want to use `set_mouse_cursor()` to change mouse cursor. You may want to honor requests from imgui by reading `get_mouse_cursor()` yourself instead.
    """

    NO_KEYBOARD = 64
    """
    Instruct dear imgui to disable keyboard inputs and interactions. This is done by ignoring keyboard events and clearing existing states.
    """

    IS_SRGB = 1048576
    """Application is SRGB-aware."""

    IS_TOUCH_SCREEN = 2097152
    """Application is using a touch screen instead of a mouse."""

class Context:
    def get_io_internal(self) -> IO: ...

    def get_style_internal(self) -> Style: ...

    def get_background_draw_list_internal(self) -> DrawList: ...

    def get_foreground_draw_list_internal(self) -> DrawList: ...

    def get_window_draw_list_internal(self) -> DrawList: ...

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
    """
    Disable preview tooltip. By default, a successful call to `begin_drag_drop_source` opens a tooltip so you can display a preview or description of the source contents. This flag disables this behavior.
    """

    SOURCE_NO_DISABLE_HOVER = 2
    """
    By default, when dragging we clear data so that `is_item_hovered()` will return false, to avoid subsequent user code submitting tooltips. This flag disables this behavior so you can still call `is_item_hovered()` on the source item.
    """

    SOURCE_NO_HOLD_TO_OPEN_OTHERS = 4
    """
    Disable the behavior that allows to open tree nodes and collapsing header by holding over them while dragging a source item.
    """

    SOURCE_ALLOW_NULL_ID = 8
    """
    Allow items such as `text()`, `image()` that have no unique identifier to be used as drag source, by manufacturing a temporary identifier based on their window-relative position. This is extremely unusual within the dear imgui ecosystem and so we made it explicit.
    """

    SOURCE_EXTERN = 16
    """
    External source (from outside of dear imgui), won't attempt to read current item/window info. Will always return true. Only one Extern source can be active simultaneously.
    """

    PAYLOAD_AUTO_EXPIRE = 32
    """
    Automatically expire the payload if the source cease to be submitted (otherwise payloads are persisting while being dragged)
    """

    PAYLOAD_NO_CROSS_CONTEXT = 64
    """
    Hint to specify that the payload may not be copied outside current dear imgui context.
    """

    PAYLOAD_NO_CROSS_PROCESS = 128
    """
    Hint to specify that the payload may not be copied outside current process.
    """

    ACCEPT_BEFORE_DELIVERY = 1024
    """
    `accept_drag_drop_payload()` will returns true even before the mouse button is released. You can then call IsDelivery() to test if the payload needs to be delivered.
    """

    ACCEPT_NO_DRAW_DEFAULT_RECT = 2048
    """Do not draw the default highlight rectangle when hovering over target."""

    ACCEPT_NO_PREVIEW_TOOLTIP = 4096
    """
    Request hiding the `begin_drag_drop_source` tooltip from the `begin_drag_drop_target` site.
    """

    ACCEPT_PEEK_ONLY = 3072
    """For peeking ahead and inspecting the payload before delivery."""

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
    """
    PathStroke(), AddPolyline(): specify that shape should be closed (Important: this is always == 1 for legacy reason)
    """

    ROUND_CORNERS_TOP_LEFT = 16
    """
    AddRect(), AddRectFilled(), PathRect(): enable rounding top-left corner only (when rounding > 0.0f, we default to all corners). Was 0x01.
    """

    ROUND_CORNERS_TOP_RIGHT = 32
    """
    AddRect(), AddRectFilled(), PathRect(): enable rounding top-right corner only (when rounding > 0.0f, we default to all corners). Was 0x02.
    """

    ROUND_CORNERS_BOTTOM_LEFT = 64
    """
    AddRect(), AddRectFilled(), PathRect(): enable rounding bottom-left corner only (when rounding > 0.0f, we default to all corners). Was 0x04.
    """

    ROUND_CORNERS_BOTTOM_RIGHT = 128
    """
    AddRect(), AddRectFilled(), PathRect(): enable rounding bottom-right corner only (when rounding > 0.0f, we default to all corners). Wax 0x08.
    """

    ROUND_CORNERS_NONE = 256
    """
    AddRect(), AddRectFilled(), PathRect(): disable rounding on all corners (when rounding > 0.0f). This is NOT zero, NOT an implicit flag!
    """

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

    def add_line(self, p1: tuple[float, float], p2: tuple[float, float], col: int, thickness: float = 1.0) -> None: ...

    def add_rect(self, p_min: tuple[float, float], p_max: tuple[float, float], col: int, rounding: float = 0.0, flags: DrawFlags = DrawFlags.NONE, thickness: float = 1.0) -> None: ...

    def add_rect_filled(self, p_min: tuple[float, float], p_max: tuple[float, float], col: int, rounding: float = 0.0, flags: DrawFlags = DrawFlags.NONE) -> None: ...

    def add_rect_filled_multi_color(self, p_min: tuple[float, float], p_max: tuple[float, float], col_upr_left: int, col_upr_right: int, col_bot_right: int, col_bot_left: int) -> None: ...

    def add_quad(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int, thickness: float = 1.0) -> None: ...

    def add_quad_filled(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int) -> None: ...

    def add_triangle(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int, thickness: float = 1.0) -> None: ...

    def add_triangle_filled(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int) -> None: ...

    def add_circle(self, center: tuple[float, float], radius: float, col: int, num_segments: int = 0, thickness: float = 1.0) -> None: ...

    def add_circle_filled(self, center: tuple[float, float], radius: float, col: int, num_segments: int = 0) -> None: ...

    def add_ngon(self, center: tuple[float, float], radius: float, col: int, num_segments: int, thickness: float = 1.0) -> None: ...

    def add_ngon_filled(self, center: tuple[float, float], radius: float, col: int, num_segments: int) -> None: ...

    def add_ellipse(self, center: tuple[float, float], radius: tuple[float, float], col: int, rot: float = 0.0, num_segments: int = 0, thickness: float = 1.0) -> None: ...

    def add_ellipse_filled(self, center: tuple[float, float], radius: tuple[float, float], col: int, rot: float = 0.0, num_segments: int = 0) -> None: ...

    @overload
    def add_text(self, pos: tuple[float, float], col: int, text: str) -> None: ...

    @overload
    def add_text(self, font: Font, font_size: float, pos: tuple[float, float], col: int, text: str, wrap_width: float = 0.0, cpu_fine_clip_rect: tuple[float, float, float, float] | None = None) -> None: ...

    def add_bezier_cubic(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int, thickness: float, num_segments: int = 0) -> None: ...

    def add_bezier_quadratic(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int, thickness: float, num_segments: int = 0) -> None: ...

    @overload
    def add_polyline(self, points: Sequence[tuple[float, float]], col: int, flags: DrawFlags, thickness: float = 1.0) -> None: ...

    @overload
    def add_polyline(self, points: Annotated[ArrayLike, dict(dtype='float32', shape=(None, 2), device='cpu', writable=False)], col: int, flags: DrawFlags, thickness: float) -> None: ...

    @overload
    def add_convex_poly_filled(self, points: Sequence[tuple[float, float]], col: int) -> None: ...

    @overload
    def add_convex_poly_filled(self, points: Annotated[ArrayLike, dict(dtype='float32', shape=(None, 2), device='cpu', writable=False)], col: int) -> None: ...

    @overload
    def add_concave_poly_filled(self, points: Sequence[tuple[float, float]], col: int) -> None: ...

    @overload
    def add_concave_poly_filled(self, points: Annotated[ArrayLike, dict(dtype='float32', shape=(None, 2), device='cpu', writable=False)], col: int) -> None: ...

    def add_image(self, user_texture_id: int, p_min: tuple[float, float], p_max: tuple[float, float], uv_min: tuple[float, float] = (0.0, 0.0), uv_max: tuple[float, float] = (1.0, 1.0), col: int = COL32_WHITE) -> None: ...

    def add_image_quad(self, user_texture_id: int, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], uv1: tuple[float, float] = (0.0, 0.0), uv2: tuple[float, float] = (1.0, 0.0), uv3: tuple[float, float] = (1.0, 1.0), uv4: tuple[float, float] = (0.0, 1.0), col: int = COL32_WHITE) -> None: ...

    def add_image_rounded(self, user_texture_id: int, p_min: tuple[float, float], p_max: tuple[float, float], uv_min: tuple[float, float], uv_max: tuple[float, float], col: int, rounding: float, flags: DrawFlags = DrawFlags.NONE) -> None: ...

FLOAT_MAX: float = 3.4028234663852886e+38

FLOAT_MIN: float = 1.1754943508222875e-38

FLT_MAX: float = 3.4028234663852886e+38

FLT_MIN: float = 1.1754943508222875e-38

class FocusedFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    CHILD_WINDOWS = 1
    """Return true if any children of the window is focused"""

    ROOT_WINDOW = 2
    """Test from root window (top most parent of the current hierarchy)"""

    ANY_WINDOW = 4
    """
    Return true if any window is focused. Important: If you are trying to tell how to dispatch your low-level inputs, do NOT use this. Use 'io.WantCaptureMouse' instead! Please read the FAQ!
    """

    NO_POPUP_HIERARCHY = 8
    """
    Do not consider popup hierarchy (do not treat popup emitter as parent of popup) (when used with _ChildWindows or _RootWindow)
    """

    ROOT_AND_CHILD_WINDOWS = 3

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
    """
    Return true if directly over the item/window, not obstructed by another window, not obstructed by an active popup or modal blocking inputs under them.
    """

    CHILD_WINDOWS = 1
    """
    `is_window_hovered()` only: Return true if any children of the window is hovered
    """

    ROOT_WINDOW = 2
    """
    `is_window_hovered()` only: Test from root window (top most parent of the current hierarchy)
    """

    ANY_WINDOW = 4
    """`is_window_hovered()` only: Return true if any window is hovered"""

    NO_POPUP_HIERARCHY = 8
    """
    `is_window_hovered()` only: Do not consider popup hierarchy (do not treat popup emitter as parent of popup) (when used with _ChildWindows or _RootWindow)
    """

    ALLOW_WHEN_BLOCKED_BY_POPUP = 32
    """
    Return true even if a popup window is normally blocking access to this item/window
    """

    ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM = 128
    """
    Return true even if an active item is blocking access to this item/window. Useful for Drag and Drop patterns.
    """

    ALLOW_WHEN_OVERLAPPED_BY_ITEM = 256
    """
    `is_item_hovered()` only: Return true even if the item uses AllowOverlap mode and is overlapped by another hoverable item.
    """

    ALLOW_WHEN_OVERLAPPED_BY_WINDOW = 512
    """
    `is_item_hovered()` only: Return true even if the position is obstructed or overlapped by another window.
    """

    ALLOW_WHEN_DISABLED = 1024
    """`is_item_hovered()` only: Return true even if the item is disabled"""

    NO_NAV_OVERRIDE = 2048
    """
    `is_item_hovered()` only: Disable using keyboard/gamepad navigation state when active, always query mouse
    """

    ALLOW_WHEN_OVERLAPPED = 768

    RECT_ONLY = 928

    ROOT_AND_CHILD_WINDOWS = 3

    FOR_TOOLTIP = 4096
    """
    Shortcut for standard flags when using `is_item_hovered()` + `set_tooltip()` sequence.
    """

    STATIONARY = 8192
    """
    Require mouse to be stationary for style.HoverStationaryDelay (~0.15 sec) _at least one time_. After this, can move on same item/window. Using the stationary test tends to reduces the need for a long delay.
    """

    DELAY_NONE = 16384
    """
    `is_item_hovered()` only: Return true immediately (default). As this is the default you generally ignore this.
    """

    DELAY_SHORT = 32768
    """
    `is_item_hovered()` only: Return true after style.HoverDelayShort elapsed (~0.15 sec) (shared between items) + requires mouse to be stationary for style.HoverStationaryDelay (once per item).
    """

    DELAY_NORMAL = 65536
    """
    `is_item_hovered()` only: Return true after style.HoverDelayNormal elapsed (~0.40 sec) (shared between items) + requires mouse to be stationary for style.HoverStationaryDelay (once per item).
    """

    NO_SHARED_DELAY = 131072
    """
    `is_item_hovered()` only: Disable shared delay system where moving from one item to the next keeps the previous timer for a short time (standard for tooltips with long delays)
    """

IMGUI_VERSION: str = '1.91.9'

IMGUI_VERSION_NUM: int = 19190

INDEX_SIZE: int = 2

class IO:
    def add_mouse_pos_event(self, x: float, y: float) -> None: ...

    def add_mouse_button_event(self, button: int, down: bool) -> None: ...

    def add_mouse_wheel_event(self, wheel_x: float, wheel_y: float) -> None: ...

    def add_input_character(self, c: int) -> None: ...

    def add_key_event(self, key: Key, down: bool) -> None: ...

    @property
    def config_flags(self) -> ConfigFlags: ...

    @config_flags.setter
    def config_flags(self, arg: ConfigFlags, /) -> None: ...

    @property
    def backend_flags(self) -> BackendFlags: ...

    @backend_flags.setter
    def backend_flags(self, arg: BackendFlags, /) -> None: ...

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
    """Allow 0123456789.+-*/"""

    CHARS_HEXADECIMAL = 2
    """Allow 0123456789ABCDEFabcdef"""

    CHARS_SCIENTIFIC = 4
    """Allow 0123456789.+-*/eE (Scientific notation input)"""

    CHARS_UPPERCASE = 8
    """Turn a..z into A..Z"""

    CHARS_NO_BLANK = 16
    """Filter out spaces, tabs"""

    ALLOW_TAB_INPUT = 32
    """Pressing TAB input a '	' character into the text field"""

    ENTER_RETURNS_TRUE = 64
    """
    Return 'true' when Enter is pressed (as opposed to every time the value was modified). Consider using `is_item_deactivated_after_edit()` instead!
    """

    ESCAPE_CLEARS_ALL = 128
    """
    Escape key clears content if not empty, and deactivate otherwise (contrast to default behavior of Escape to revert)
    """

    CTRL_ENTER_FOR_NEW_LINE = 256
    """
    In multi-line mode, validate with Enter, add new line with Ctrl+Enter (default is opposite: validate with Ctrl+Enter, add line with Enter).
    """

    READ_ONLY = 512
    """Read-only mode"""

    PASSWORD = 1024
    """Password mode, display all characters as '*', disable copy"""

    ALWAYS_OVERWRITE = 2048
    """Overwrite mode"""

    AUTO_SELECT_ALL = 4096
    """Select entire text when first taking mouse focus"""

    PARSE_EMPTY_REF_VAL = 8192
    """
    `input_float()`, `input_int()`, `input_scalar()` etc. only: parse empty string as zero value.
    """

    DISPLAY_EMPTY_REF_VAL = 16384
    """
    `input_float()`, `input_int()`, `input_scalar()` etc. only: when value is zero, do not display it. Generally used with `InputTextFlags.PARSE_EMPTY_REF_VAL`.
    """

    NO_HORIZONTAL_SCROLL = 32768
    """Disable following the cursor horizontally"""

    NO_UNDO_REDO = 65536
    """
    Disable undo/redo. Note that input text owns the text data while active, if you want to provide your own undo/redo stack you need e.g. to call `clear_active_id()`.
    """

    ELIDE_LEFT = 131072
    """
    When text doesn't fit, elide left side to ensure right side stays visible. Useful for path/filenames. Single-line only!
    """

    CALLBACK_COMPLETION = 262144
    """Callback on pressing TAB (for completion handling)"""

    CALLBACK_HISTORY = 524288
    """Callback on pressing Up/Down arrows (for history handling)"""

    CALLBACK_ALWAYS = 1048576
    """
    Callback on each iteration. User code may query cursor position, modify text buffer.
    """

    CALLBACK_CHAR_FILTER = 2097152
    """
    Callback on character inputs to replace or discard them. Modify 'EventChar' to replace or discard, or return 1 in callback to discard.
    """

    CALLBACK_RESIZE = 4194304
    """
    Callback on buffer capacity changes request (beyond 'buf_size' parameter value), allowing the string to grow. Notify when the string wants to be resized (for string types which hold a cache of their Size). You will be provided a new BufSize in the callback and NEED to honor it. (see misc/cpp/imgui_stdlib.h for an example of using this)
    """

    CALLBACK_EDIT = 8388608
    """
    Callback on any edit. Note that `input_text()` already returns true on edit + you can always use `is_item_edited()`. The callback is useful to manipulate the underlying buffer while focus is active.
    """

class ItemFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """(Default)"""

    NO_TAB_STOP = 1
    """
    Disable keyboard tabbing. This is a "lighter" version of `ItemFlags.NO_NAV`.
    """

    NO_NAV = 2
    """
    Disable any form of focusing (keyboard/gamepad directional navigation and `set_keyboard_focus_here()` calls).
    """

    NO_NAV_DEFAULT_FOCUS = 4
    """
    Disable item being a candidate for default focus (e.g. used by title bar items).
    """

    BUTTON_REPEAT = 8
    """
    Any button-like behavior will have repeat mode enabled (based on io.KeyRepeatDelay and io.KeyRepeatRate values). Note that you can also call `is_item_active()` after any button to tell if it is being held.
    """

    AUTO_CLOSE_POPUPS = 16
    """
    `menu_item()`/`selectable()` automatically close their parent popup window.
    """

    ALLOW_DUPLICATE_ID = 32
    """
    Allow submitting an item with the same identifier as an item already submitted this frame without triggering a warning tooltip if io.ConfigDebugHighlightIdConflicts is set.
    """

class Key(enum.IntEnum):
    KEY_NONE = 0

    KEY_NAMED_KEY_BEGIN = 512

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

    KEY_OEM102 = 631

    KEY_GAMEPAD_START = 632

    KEY_GAMEPAD_BACK = 633

    KEY_GAMEPAD_FACE_LEFT = 634

    KEY_GAMEPAD_FACE_RIGHT = 635

    KEY_GAMEPAD_FACE_UP = 636

    KEY_GAMEPAD_FACE_DOWN = 637

    KEY_GAMEPAD_DPAD_LEFT = 638

    KEY_GAMEPAD_DPAD_RIGHT = 639

    KEY_GAMEPAD_DPAD_UP = 640

    KEY_GAMEPAD_DPAD_DOWN = 641

    KEY_GAMEPAD_L1 = 642

    KEY_GAMEPAD_R1 = 643

    KEY_GAMEPAD_L2 = 644

    KEY_GAMEPAD_R2 = 645

    KEY_GAMEPAD_L3 = 646

    KEY_GAMEPAD_R3 = 647

    KEY_GAMEPAD_L_STICK_LEFT = 648

    KEY_GAMEPAD_L_STICK_RIGHT = 649

    KEY_GAMEPAD_L_STICK_UP = 650

    KEY_GAMEPAD_L_STICK_DOWN = 651

    KEY_GAMEPAD_R_STICK_LEFT = 652

    KEY_GAMEPAD_R_STICK_RIGHT = 653

    KEY_GAMEPAD_R_STICK_UP = 654

    KEY_GAMEPAD_R_STICK_DOWN = 655

    KEY_MOUSE_LEFT = 656

    KEY_MOUSE_RIGHT = 657

    KEY_MOUSE_MIDDLE = 658

    KEY_MOUSE_X1 = 659

    KEY_MOUSE_X2 = 660

    KEY_MOUSE_WHEEL_X = 661

    KEY_MOUSE_WHEEL_Y = 662

    KEY_RESERVED_FOR_MOD_CTRL = 663

    KEY_RESERVED_FOR_MOD_SHIFT = 664

    KEY_RESERVED_FOR_MOD_ALT = 665

    KEY_RESERVED_FOR_MOD_SUPER = 666

    KEY_NAMED_KEY_END = 667

    MOD_NONE = 0

    MOD_CTRL = 4096

    MOD_SHIFT = 8192

    MOD_ALT = 16384

    MOD_SUPER = 32768

    KEY_NAMED_KEY_COUNT = 155

class MouseButton(enum.IntEnum):
    LEFT = 0

    RIGHT = 1

    MIDDLE = 2

    COUNT = 5

class MouseCursor(enum.IntEnum):
    NONE = -1

    ARROW = 0

    TEXT_INPUT = 1
    """When hovering over `input_text`, etc."""

    RESIZE_ALL = 2
    """(Unused by Dear ImGui functions)"""

    RESIZE_NS = 3
    """When hovering over a horizontal border"""

    RESIZE_EW = 4
    """When hovering over a vertical border or a column"""

    RESIZE_NESW = 5
    """When hovering over the bottom-left corner of a window"""

    RESIZE_NWSE = 6
    """When hovering over the bottom-right corner of a window"""

    HAND = 7
    """(Unused by Dear ImGui functions. Use for e.g. hyperlinks)"""

    WAIT = 8
    """When waiting for something to process/load."""

    PROGRESS = 9
    """
    When waiting for something to process/load, but application is still interactive.
    """

    NOT_ALLOWED = 10
    """
    When hovering something with disallowed interaction. Usually a crossed circle.
    """

    COUNT = 11

class PopupFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    MOUSE_BUTTON_LEFT = 0
    """
    For BeginPopupContext*(): open on Left Mouse release. Guaranteed to always be == 0 (same as `MouseButton.LEFT`)
    """

    MOUSE_BUTTON_RIGHT = 1
    """
    For BeginPopupContext*(): open on Right Mouse release. Guaranteed to always be == 1 (same as `MouseButton.RIGHT`)
    """

    MOUSE_BUTTON_MIDDLE = 2
    """
    For BeginPopupContext*(): open on Middle Mouse release. Guaranteed to always be == 2 (same as `MouseButton.MIDDLE`)
    """

    NO_REOPEN = 32
    """
    For `open_popup`*(), BeginPopupContext*(): don't reopen same popup if already open (won't reposition, won't reinitialize navigation)
    """

    NO_OPEN_OVER_EXISTING_POPUP = 128
    """
    For `open_popup`*(), BeginPopupContext*(): don't open if there's already a popup at the same level of the popup stack
    """

    NO_OPEN_OVER_ITEMS = 256
    """
    For `begin_popup_context_window()`: don't return true when hovering items, only when hovering empty space
    """

    ANY_POPUP_ID = 1024
    """
    For `is_popup_open()`: ignore the ImGuiID parameter and test for any popup.
    """

    ANY_POPUP_LEVEL = 2048
    """
    For `is_popup_open()`: search/test at any level of the popup stack (default test in the current level)
    """

    ANY_POPUP = 3072

class SelectableFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_AUTO_CLOSE_POPUPS = 1
    """
    Clicking this doesn't close parent popup window (overrides `ItemFlags.AUTO_CLOSE_POPUPS`)
    """

    SPAN_ALL_COLUMNS = 2
    """
    Frame will span all columns of its container table (text will still fit in current column)
    """

    ALLOW_DOUBLE_CLICK = 4
    """Generate press events on double clicks too"""

    DISABLED = 8
    """Cannot be selected, display grayed out text"""

    ALLOW_OVERLAP = 16
    """(WIP) Hit testing to allow subsequent widgets to overlap this one"""

    HIGHLIGHT = 32
    """Make the item be displayed as if it is hovered"""

class SliderFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    LOGARITHMIC = 32
    """
    Make the widget logarithmic (linear otherwise). Consider using `SliderFlags.NO_ROUND_TO_FORMAT` with this if using a format-string with small amount of digits.
    """

    NO_ROUND_TO_FORMAT = 64
    """
    Disable rounding underlying value to match precision of the display format string (e.g. %.3f values are rounded to those 3 digits).
    """

    NO_INPUT = 128
    """
    Disable CTRL+Click or Enter key allowing to input text directly into the widget.
    """

    WRAP_AROUND = 256
    """
    Enable wrapping around from max to min and from min to max. Only supported by DragXXX() functions for now.
    """

    CLAMP_ON_INPUT = 512
    """
    Clamp value to min/max bounds when input manually with CTRL+Click. By default CTRL+Click allows going out of bounds.
    """

    CLAMP_ZERO_RANGE = 1024
    """
    Clamp even if min==max==0.0f. Otherwise due to legacy reason DragXXX functions don't clamp with those values. When your clamping limits are dynamic you almost always want to use it.
    """

    NO_SPEED_TWEAKS = 2048
    """
    Disable keyboard modifiers altering tweak speed. Useful if you want to alter tweak speed yourself based on your own logic.
    """

    ALWAYS_CLAMP = 1536

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
    def window_menu_button_position(self) -> Dir: ...

    @window_menu_button_position.setter
    def window_menu_button_position(self, arg: Dir, /) -> None: ...

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
    def tab_close_button_min_width_selected(self) -> float: ...

    @tab_close_button_min_width_selected.setter
    def tab_close_button_min_width_selected(self, arg: float, /) -> None: ...

    @property
    def tab_close_button_min_width_unselected(self) -> float: ...

    @tab_close_button_min_width_unselected.setter
    def tab_close_button_min_width_unselected(self, arg: float, /) -> None: ...

    @property
    def tab_bar_border_size(self) -> float: ...

    @tab_bar_border_size.setter
    def tab_bar_border_size(self, arg: float, /) -> None: ...

    @property
    def table_angled_headers_angle(self) -> float: ...

    @table_angled_headers_angle.setter
    def table_angled_headers_angle(self, arg: float, /) -> None: ...

    @property
    def color_button_position(self) -> Dir: ...

    @color_button_position.setter
    def color_button_position(self, arg: Dir, /) -> None: ...

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
    """Float     Alpha"""

    DISABLED_ALPHA = 1
    """Float     DisabledAlpha"""

    WINDOW_PADDING = 2
    """ImVec2    WindowPadding"""

    WINDOW_ROUNDING = 3
    """Float     WindowRounding"""

    WINDOW_BORDER_SIZE = 4
    """Float     WindowBorderSize"""

    WINDOW_MIN_SIZE = 5
    """ImVec2    WindowMinSize"""

    WINDOW_TITLE_ALIGN = 6
    """ImVec2    WindowTitleAlign"""

    CHILD_ROUNDING = 7
    """Float     ChildRounding"""

    CHILD_BORDER_SIZE = 8
    """Float     ChildBorderSize"""

    POPUP_ROUNDING = 9
    """Float     PopupRounding"""

    POPUP_BORDER_SIZE = 10
    """Float     PopupBorderSize"""

    FRAME_PADDING = 11
    """ImVec2    FramePadding"""

    FRAME_ROUNDING = 12
    """Float     FrameRounding"""

    FRAME_BORDER_SIZE = 13
    """Float     FrameBorderSize"""

    ITEM_SPACING = 14
    """ImVec2    ItemSpacing"""

    ITEM_INNER_SPACING = 15
    """ImVec2    ItemInnerSpacing"""

    INDENT_SPACING = 16
    """Float     IndentSpacing"""

    CELL_PADDING = 17
    """ImVec2    CellPadding"""

    SCROLLBAR_SIZE = 18
    """Float     ScrollbarSize"""

    SCROLLBAR_ROUNDING = 19
    """Float     ScrollbarRounding"""

    GRAB_MIN_SIZE = 20
    """Float     GrabMinSize"""

    GRAB_ROUNDING = 21
    """Float     GrabRounding"""

    IMAGE_BORDER_SIZE = 22
    """Float     ImageBorderSize"""

    TAB_ROUNDING = 23
    """Float     TabRounding"""

    TAB_BORDER_SIZE = 24
    """Float     TabBorderSize"""

    TAB_BAR_BORDER_SIZE = 25
    """Float     TabBarBorderSize"""

    TAB_BAR_OVERLINE_SIZE = 26
    """Float     TabBarOverlineSize"""

    TABLE_ANGLED_HEADERS_ANGLE = 27
    """Float     TableAngledHeadersAngle"""

    TABLE_ANGLED_HEADERS_TEXT_ALIGN = 28
    """ImVec2  TableAngledHeadersTextAlign"""

    BUTTON_TEXT_ALIGN = 29
    """ImVec2    ButtonTextAlign"""

    SELECTABLE_TEXT_ALIGN = 30
    """ImVec2    SelectableTextAlign"""

    SEPARATOR_TEXT_BORDER_SIZE = 31
    """Float     SeparatorTextBorderSize"""

    SEPARATOR_TEXT_ALIGN = 32
    """ImVec2    SeparatorTextAlign"""

    SEPARATOR_TEXT_PADDING = 33
    """ImVec2    SeparatorTextPadding"""

    COUNT = 34

class TabBarFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    REORDERABLE = 1
    """
    Allow manually dragging tabs to re-order them + New tabs are appended at the end of list
    """

    AUTO_SELECT_NEW_TABS = 2
    """Automatically select new tabs when they appear"""

    TAB_LIST_POPUP_BUTTON = 4
    """Disable buttons to open the tab list popup"""

    NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON = 8
    """
    Disable behavior of closing tabs (that are submitted with p_open != NULL) with middle mouse button. You may handle this behavior manually on user's side with if (`is_item_hovered()` && `is_mouse_clicked(2)`) *p_open = false.
    """

    NO_TAB_LIST_SCROLLING_BUTTONS = 16
    """
    Disable scrolling buttons (apply when fitting policy is `TabBarFlags.FITTING_POLICY_SCROLL`)
    """

    NO_TOOLTIP = 32
    """Disable tooltips when hovering a tab"""

    DRAW_SELECTED_OVERLINE = 64
    """Draw selected overline markers over selected tab"""

    FITTING_POLICY_RESIZE_DOWN = 128
    """Resize tabs when they don't fit"""

    FITTING_POLICY_SCROLL = 256
    """Add scroll buttons when tabs don't fit"""

class TabItemFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    UNSAVED_DOCUMENT = 1
    """
    Display a dot next to the title + set `TabItemFlags.NO_ASSUMED_CLOSURE`.
    """

    SET_SELECTED = 2
    """
    Trigger flag to programmatically make the tab selected when calling `begin_tab_item()`
    """

    NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON = 4
    """
    Disable behavior of closing tabs (that are submitted with p_open != NULL) with middle mouse button. You may handle this behavior manually on user's side with if (`is_item_hovered()` && `is_mouse_clicked(2)`) *p_open = false.
    """

    NO_PUSH_ID = 8
    """
    Don't call `push_id()`/`pop_id()` on `begin_tab_item()`/`end_tab_item()`
    """

    NO_TOOLTIP = 16
    """Disable tooltip for the given tab"""

    NO_REORDER = 32
    """Disable reordering this tab or having another tab cross over this tab"""

    LEADING = 64
    """
    Enforce the tab position to the left of the tab bar (after the tab list popup button)
    """

    TRAILING = 128
    """
    Enforce the tab position to the right of the tab bar (before the scrolling buttons)
    """

    NO_ASSUMED_CLOSURE = 256
    """
    Tab is selected when trying to close + closure is not immediately assumed (will wait for user to stop submitting the tab). Otherwise closure is assumed when pressing the X, so if you keep submitting the tab may reappear at end of tab bar.
    """

class TableBgTarget(enum.IntEnum):
    NONE = 0

    ROW_BG0 = 1
    """
    Set row background color 0 (generally used for background, automatically set when `TableFlags.ROW_BG` is used)
    """

    ROW_BG1 = 2
    """Set row background color 1 (generally used for selection marking)"""

    CELL_BG = 3
    """Set cell background color (top-most color)"""

class TableColumnFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    DISABLED = 1
    """
    Overriding/master disable flag: hide column, won't show in context menu (unlike calling `table_set_column_enabled()` which manipulates the user accessible state)
    """

    DEFAULT_HIDE = 2
    """Default as a hidden/disabled column."""

    DEFAULT_SORT = 4
    """Default as a sorting column."""

    WIDTH_STRETCH = 8
    """
    Column will stretch. Preferable with horizontal scrolling disabled (default if table sizing policy is _SizingStretchSame or _SizingStretchProp).
    """

    WIDTH_FIXED = 16
    """
    Column will not stretch. Preferable with horizontal scrolling enabled (default if table sizing policy is _SizingFixedFit and table is resizable).
    """

    NO_RESIZE = 32
    """Disable manual resizing."""

    NO_REORDER = 64
    """
    Disable manual reordering this column, this will also prevent other columns from crossing over this column.
    """

    NO_HIDE = 128
    """Disable ability to hide/disable this column."""

    NO_CLIP = 256
    """
    Disable clipping for this column (all NoClip columns will render in a same draw command).
    """

    NO_SORT = 512
    """
    Disable ability to sort on this field (even if `TableFlags.SORTABLE` is set on the table).
    """

    NO_SORT_ASCENDING = 1024
    """Disable ability to sort in the ascending direction."""

    NO_SORT_DESCENDING = 2048
    """Disable ability to sort in the descending direction."""

    NO_HEADER_LABEL = 4096
    """
    `table_headers_row()` will submit an empty label for this column. Convenient for some small columns. Name will still appear in context menu or in angled headers. You may append into this cell by calling `table_set_column_index()` right after the `table_headers_row()` call.
    """

    NO_HEADER_WIDTH = 8192
    """Disable header text width contribution to automatic column width."""

    PREFER_SORT_ASCENDING = 16384
    """
    Make the initial sort direction Ascending when first sorting on this column (default).
    """

    PREFER_SORT_DESCENDING = 32768
    """
    Make the initial sort direction Descending when first sorting on this column.
    """

    INDENT_ENABLE = 65536
    """Use current `indent` value when entering cell (default for column 0)."""

    INDENT_DISABLE = 131072
    """
    Ignore current `indent` value when entering cell (default for columns > 0). Indentation changes _within_ the cell will still be honored.
    """

    ANGLED_HEADER = 262144
    """
    `table_headers_row()` will submit an angled header row for this column. Note this will add an extra row.
    """

    IS_ENABLED = 16777216
    """
    Status: is enabled == not hidden by user/api (referred to as "Hide" in _DefaultHide and _NoHide) flags.
    """

    IS_VISIBLE = 33554432
    """Status: is visible == is enabled AND not clipped by scrolling."""

    IS_SORTED = 67108864
    """Status: is currently part of the sort specs"""

    IS_HOVERED = 134217728
    """Status: is hovered by mouse"""

class TableFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    RESIZABLE = 1
    """Enable resizing columns."""

    REORDERABLE = 2
    """
    Enable reordering columns in header row (need calling `table_setup_column()` + `table_headers_row()` to display headers)
    """

    HIDEABLE = 4
    """Enable hiding/disabling columns in context menu."""

    SORTABLE = 8
    """
    Enable sorting. Call `table_get_sort_specs()` to obtain sort specs. Also see `TableFlags.SORT_MULTI` and `TableFlags.SORT_TRISTATE`.
    """

    NO_SAVED_SETTINGS = 16
    """
    Disable persisting columns order, width and sort settings in the .ini file.
    """

    CONTEXT_MENU_IN_BODY = 32
    """
    Right-click on columns body/contents will display table context menu. By default it is available in `table_headers_row()`.
    """

    ROW_BG = 64
    """
    Set each RowBg color with `Col.TABLE_ROW_BG` or `Col.TABLE_ROW_BG_ALT` (equivalent of calling `table_set_bg_color` with ImGuiTableBgFlags_RowBg0 on each row manually)
    """

    BORDERS_INNER_H = 128
    """Draw horizontal borders between rows."""

    BORDERS_OUTER_H = 256
    """Draw horizontal borders at the top and bottom."""

    BORDERS_INNER_V = 512
    """Draw vertical borders between columns."""

    BORDERS_OUTER_V = 1024
    """Draw vertical borders on the left and right sides."""

    BORDERS_H = 384
    """Draw horizontal borders."""

    BORDERS_V = 1536
    """Draw vertical borders."""

    BORDERS_INNER = 640
    """Draw inner borders."""

    BORDERS_OUTER = 1280
    """Draw outer borders."""

    BORDERS = 1920
    """Draw all borders."""

    NO_BORDERS_IN_BODY = 2048
    """
    [ALPHA] Disable vertical borders in columns Body (borders will always appear in Headers). -> May move to style
    """

    NO_BORDERS_IN_BODY_UNTIL_RESIZE = 4096
    """
    [ALPHA] Disable vertical borders in columns Body until hovered for resize (borders will always appear in Headers). -> May move to style
    """

    SIZING_FIXED_FIT = 8192
    """
    `columns` default to _WidthFixed or _WidthAuto (if resizable or not resizable), matching contents width.
    """

    SIZING_FIXED_SAME = 16384
    """
    `columns` default to _WidthFixed or _WidthAuto (if resizable or not resizable), matching the maximum contents width of all columns. Implicitly enable `TableFlags.NO_KEEP_COLUMNS_VISIBLE`.
    """

    SIZING_STRETCH_PROP = 24576
    """
    `columns` default to _WidthStretch with default weights proportional to each columns contents widths.
    """

    SIZING_STRETCH_SAME = 32768
    """
    `columns` default to _WidthStretch with default weights all equal, unless overridden by `table_setup_column()`.
    """

    NO_HOST_EXTEND_X = 65536
    """
    Make outer width auto-fit to columns, overriding outer_size.x value. Only available when ScrollX/ScrollY are disabled and Stretch columns are not used.
    """

    NO_HOST_EXTEND_Y = 131072
    """
    Make outer height stop exactly at outer_size.y (prevent auto-extending table past the limit). Only available when ScrollX/ScrollY are disabled. Data below the limit will be clipped and not visible.
    """

    NO_KEEP_COLUMNS_VISIBLE = 262144
    """
    Disable keeping column always minimally visible when ScrollX is off and table gets too small. Not recommended if columns are resizable.
    """

    PRECISE_WIDTHS = 524288
    """
    Disable distributing remainder width to stretched columns (width allocation on a 100-wide table with 3 columns: Without this flag: 33,33,34. With this flag: 33,33,33). With larger number of columns, resizing will appear to be less smooth.
    """

    NO_CLIP = 1048576
    """
    Disable clipping rectangle for every individual columns (reduce draw command count, items will be able to overflow into other columns). Generally incompatible with `table_setup_scroll_freeze()`.
    """

    PAD_OUTER_X = 2097152
    """
    Default if BordersOuterV is on. Enable outermost padding. Generally desirable if you have headers.
    """

    NO_PAD_OUTER_X = 4194304
    """Default if BordersOuterV is off. Disable outermost padding."""

    NO_PAD_INNER_X = 8388608
    """
    Disable inner padding between columns (double inner padding if BordersOuterV is on, single inner padding if BordersOuterV is off).
    """

    SCROLL_X = 16777216
    """
    Enable horizontal scrolling. Require 'outer_size' parameter of `begin_table()` to specify the container size. Changes default sizing policy. Because this creates a child window, ScrollY is currently generally recommended when using ScrollX.
    """

    SCROLL_Y = 33554432
    """
    Enable vertical scrolling. Require 'outer_size' parameter of `begin_table()` to specify the container size.
    """

    SORT_MULTI = 67108864
    """
    Hold shift when clicking headers to sort on multiple column. `table_get_sort_specs()` may return specs where (SpecsCount > 1).
    """

    SORT_TRISTATE = 134217728
    """
    Allow no sorting, disable default sorting. `table_get_sort_specs()` may return specs where (SpecsCount == 0).
    """

    HIGHLIGHT_HOVERED_COLUMN = 268435456
    """
    Highlight column headers when hovered (may evolve into a fuller highlight)
    """

class TableRowFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HEADERS = 1
    """
    Identify header row (set default background color + width of its contents accounted differently for auto column width)
    """

class TreeNodeFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    SELECTED = 1
    """Draw as selected"""

    FRAMED = 2
    """Draw frame with background (e.g. for `collapsing_header`)"""

    ALLOW_OVERLAP = 4
    """Hit testing to allow subsequent widgets to overlap this one"""

    NO_TREE_PUSH_ON_OPEN = 8
    """
    Don't do a `tree_push()` when open (e.g. for `collapsing_header`) = no extra indent nor pushing on ID stack
    """

    NO_AUTO_OPEN_ON_LOG = 16
    """
    Don't automatically and temporarily open node when Logging is active (by default logging will automatically open tree nodes)
    """

    DEFAULT_OPEN = 32
    """Default node to be open"""

    OPEN_ON_DOUBLE_CLICK = 64
    """
    Open on double-click instead of simple click (default for multi-select unless any _OpenOnXXX behavior is set explicitly). Both behaviors may be combined.
    """

    OPEN_ON_ARROW = 128
    """
    Open when clicking on the arrow part (default for multi-select unless any _OpenOnXXX behavior is set explicitly). Both behaviors may be combined.
    """

    LEAF = 256
    """No collapsing, no arrow (use as a convenience for leaf nodes)."""

    BULLET = 512
    """
    Display a bullet instead of arrow. IMPORTANT: node can still be marked open/close if you don't set the _Leaf flag!
    """

    FRAME_PADDING = 1024
    """
    Use FramePadding (even for an unframed text node) to vertically align text baseline to regular widget height. Equivalent to calling `align_text_to_frame_padding()` before the node.
    """

    SPAN_AVAIL_WIDTH = 2048
    """
    Extend hit box to the right-most edge, even if not framed. This is not the default in order to allow adding other items on the same line without using AllowOverlap mode.
    """

    SPAN_FULL_WIDTH = 4096
    """
    Extend hit box to the left-most and right-most edges (cover the indent area).
    """

    SPAN_LABEL_WIDTH = 8192
    """
    Narrow hit box + narrow hovering highlight, will only cover the label text.
    """

    SPAN_ALL_COLUMNS = 16384
    """
    Frame will span all columns of its container table (label will still fit in current column)
    """

    LABEL_SPAN_ALL_COLUMNS = 32768
    """Label will span all columns of its container table"""

    NAV_LEFT_JUMPS_BACK_HERE = 131072
    """
    (WIP) Nav: left direction may move to this `tree_node()` from any of its child (items submitted between `tree_node` and `tree_pop`)
    """

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
    """Disable title-bar"""

    NO_RESIZE = 2
    """Disable user resizing with the lower-right grip"""

    NO_MOVE = 4
    """Disable user moving the window"""

    NO_SCROLLBAR = 8
    """
    Disable scrollbars (window can still scroll with mouse or programmatically)
    """

    NO_SCROLL_WITH_MOUSE = 16
    """
    Disable user vertically scrolling with mouse wheel. On child window, mouse wheel will be forwarded to the parent unless NoScrollbar is also set.
    """

    NO_COLLAPSE = 32
    """
    Disable user collapsing window by double-clicking on it. Also referred to as Window Menu Button (e.g. within a docking node).
    """

    ALWAYS_AUTO_RESIZE = 64
    """Resize every window to its content every frame"""

    NO_BACKGROUND = 128
    """
    Disable drawing background color (WindowBg, etc.) and outside border. Similar as using `set_next_window_bg_alpha(0.0)`.
    """

    NO_SAVED_SETTINGS = 256
    """Never load/save settings in .ini file"""

    NO_MOUSE_INPUTS = 512
    """Disable catching mouse, hovering test with pass through."""

    MENU_BAR = 1024
    """Has a menu-bar"""

    HORIZONTAL_SCROLLBAR = 2048
    """
    Allow horizontal scrollbar to appear (off by default). You may use `set_next_window_content_size((width,0.0))`; prior to calling `begin()` to specify width. Read code in imgui_demo in the "Horizontal Scrolling" section.
    """

    NO_FOCUS_ON_APPEARING = 4096
    """Disable taking focus when transitioning from hidden to visible state"""

    NO_BRING_TO_FRONT_ON_FOCUS = 8192
    """
    Disable bringing window to front when taking focus (e.g. clicking on it or programmatically giving it focus)
    """

    ALWAYS_VERTICAL_SCROLLBAR = 16384
    """Always show vertical scrollbar (even if ContentSize.y < Size.y)"""

    ALWAYS_HORIZONTAL_SCROLLBAR = 32768
    """Always show horizontal scrollbar (even if ContentSize.x < Size.x)"""

    NO_NAV_INPUTS = 65536
    """No keyboard/gamepad navigation within the window"""

    NO_NAV_FOCUS = 131072
    """
    No focusing toward this window with keyboard/gamepad navigation (e.g. skipped by CTRL+TAB)
    """

    UNSAVED_DOCUMENT = 262144
    """
    Display a dot next to the title. When used in a tab/docking context, tab is selected when clicking the X + closure is not assumed (will wait for user to stop submitting the tab). Otherwise closure is assumed when pressing the X, so if you keep submitting the tab may reappear at end of tab bar.
    """

    NO_NAV = 196608

    NO_DECORATION = 43

    NO_INPUTS = 197120

    CHILD_WINDOW = 16777216
    """Don't use! For internal use by `begin_child()`"""

    TOOLTIP = 33554432
    """Don't use! For internal use by `begin_tooltip()`"""

    POPUP = 67108864
    """Don't use! For internal use by `begin_popup()`"""

    MODAL = 134217728
    """Don't use! For internal use by `begin_popup_modal()`"""

    CHILD_MENU = 268435456
    """Don't use! For internal use by `begin_menu()`"""

def align_text_to_frame_padding() -> None:
    """Vertically align upcoming text baseline to FramePadding.y so that it will align properly to regularly framed items (call if you have text on a line before a framed item)"""
    ...


def arrow_button(str_id: str, dir: Dir) -> bool:
    """Square button with an arrow shape"""
    ...


def begin(name: str, closable: bool = False, flags: WindowFlags = WindowFlags.NONE) -> tuple[bool, bool]:
    ...


def begin_child(str_id: str, size: tuple[float, float] = (0.0, 0.0), child_flags: ChildFlags = ChildFlags.NONE, window_flags: WindowFlags = WindowFlags.NONE) -> bool:
    ...


def begin_combo(label: str, preview_value: str, flags: ComboFlags = ComboFlags.NONE) -> bool:
    ...


def begin_disabled(disabled: bool = True) -> None:
    ...


def begin_drag_drop_source(flags: DragDropFlags = DragDropFlags.NONE) -> bool:
    """Call after submitting an item which may be dragged. when this return true, you can call `set_drag_drop_payload()` + `end_drag_drop_source()`"""
    ...


def begin_drag_drop_target() -> bool:
    """Call after submitting an item that may receive a payload. If this returns true, you can call `accept_drag_drop_payload()` + `end_drag_drop_target()`"""
    ...


def begin_group() -> None:
    """Lock horizontal starting position"""
    ...


def begin_item_tooltip() -> bool:
    """Begin/append a tooltip window if preceding item was hovered."""
    ...


def begin_list_box(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool:
    """Open a framed scrolling region"""
    ...


def begin_main_menu_bar() -> bool:
    """Create and append to a full screen menu-bar."""
    ...


def begin_menu(label: str, enabled: bool = True) -> bool:
    """Create a sub-menu entry. only call `end_menu()` if this returns true!"""
    ...


def begin_menu_bar() -> bool:
    """Append to menu-bar of current window (requires `WindowFlags.MENU_BAR` flag set on parent window)."""
    ...


def begin_popup(str_id: str, flags: WindowFlags = WindowFlags.NONE) -> bool:
    """Return true if the popup is open, and you can start outputting to it."""
    ...


def begin_popup_context_window(str_id: str | None = None, flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT) -> bool:
    """Open+begin popup when clicked on current window."""
    ...


def begin_tab_bar(str_id: str, flags: TabBarFlags = TabBarFlags.NONE) -> bool:
    """Create and append into a TabBar"""
    ...


def begin_tab_item(str_id: str, closable: bool = False, flags: TabItemFlags = TabItemFlags.NONE) -> tuple[bool, bool]:
    """Create a Tab. Returns true if the Tab is selected."""
    ...


def begin_table(str_id: str, column: int, flags: TableFlags = TableFlags.NONE, outer_size: tuple[float, float] = (0.0, 0.0), inner_width: float = 0.0) -> bool:
    ...


def begin_tooltip() -> bool:
    """Begin/append a tooltip window."""
    ...


def bullet() -> None:
    """Draw a small circle + keep the cursor on the same line. advance cursor x position by `get_tree_node_to_label_spacing()`, same distance that `tree_node()` uses"""
    ...


def bullet_text(text: str) -> None:
    """Shortcut for `bullet()`+`text()`"""
    ...


def button(label: str, size: tuple[float, float] = (0.0, 0.0)) -> bool:
    """Button"""
    ...


def calc_item_width() -> float:
    """Width of item given pushed settings and current cursor position. NOT necessarily the width of last item unlike most 'Item' functions."""
    ...


def calc_text_size(text: str, hide_text_after_double_hash: bool = False, wrap_width: float = -1.0) -> tuple[float, float]:
    ...


def checkbox(label: str, v: bool) -> tuple[bool, bool]:
    ...


def checkbox_flags(label: str, flags: int, flags_value: int) -> tuple[bool, int]:
    ...


def close_current_popup() -> None:
    """Manually close the popup we have begin-ed into."""
    ...


def collapsing_header(label: str, visible: bool | None = None, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> tuple[bool, bool | None]:
    """If returning 'true' the header is open. doesn't indent nor push on ID stack. user doesn't have to call `tree_pop()`."""
    ...


def color_button(desc_id: str, col: tuple[float, float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE, size: tuple[float, float] = (0.0, 0.0)) -> bool:
    """Display a color square/button, hover for details, return true when pressed."""
    ...


def color_convert_float4_to_u32(arg: tuple[float, float, float, float], /) -> int:
    ...


def color_convert_hsv_to_rgb(hsv: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    ...


def color_convert_rgb_to_hsv(rgba: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    ...


def color_convert_u32_to_float4(arg: int, /) -> tuple[float, float, float, float]:
    ...


def color_edit3(label: str, col: tuple[float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float]]:
    ...


def color_edit4(label: str, col: tuple[float, float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]:
    ...


def color_picker3(label: str, col: tuple[float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE) -> tuple[bool, tuple[float, float, float]]:
    ...


def color_picker4(label: str, col: tuple[float, float, float, float], flags: ColorEditFlags = ColorEditFlags.NONE, ref_col: tuple[float, float, float, float] | None = None) -> tuple[bool, tuple[float, float, float, float]]:
    ...


def columns(count: int = 1, id: str | None = None, border: bool = True) -> None:
    ...


def combo(label: str, current_item: int, items: Sequence[str], popup_max_height_in_items: int = -1) -> tuple[bool, int]:
    ...


def create_context(shared_font_atlas: FontAtlas | None = None) -> Context:
    ...


def destroy_context(arg: Context, /) -> None:
    """NULL = destroy current context"""
    ...


def drag_float(label: str, v: float, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]:
    """If v_min >= v_max we have no bound"""
    ...


def drag_float2(label: str, v: tuple[float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float]]:
    ...


def drag_float3(label: str, v: tuple[float, float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float]]:
    ...


def drag_float4(label: str, v: tuple[float, float, float, float], v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]:
    ...


def drag_int(label: str, v: int, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, int]:
    """If v_min >= v_max we have no bound"""
    ...


def drag_int2(label: str, v: tuple[int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int]]:
    ...


def drag_int3(label: str, v: tuple[int, int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int]]:
    ...


def drag_int4(label: str, v: tuple[int, int, int, int], v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]:
    ...


def dummy(size: tuple[float, float]) -> None:
    """Add a dummy item of given size. unlike `invisible_button()`, `dummy()` won't take the mouse click or be navigable into."""
    ...


def end() -> None:
    ...


def end_child() -> None:
    ...


def end_combo() -> None:
    """Only call `end_combo()` if `begin_combo()` returns true!"""
    ...


def end_disabled() -> None:
    ...


def end_drag_drop_source() -> None:
    """Only call `end_drag_drop_source()` if `begin_drag_drop_source()` returns true!"""
    ...


def end_drag_drop_target() -> None:
    """Only call `end_drag_drop_target()` if `begin_drag_drop_target()` returns true!"""
    ...


def end_frame() -> None:
    """Ends the Dear ImGui frame. automatically called by `render()`. If you don't need to render data (skipping rendering) you may call `end_frame()` without `render()`... but you'll have wasted CPU already! If you don't need to render, better to not create any windows and not call `new_frame()` at all!"""
    ...


def end_group() -> None:
    """Unlock horizontal starting position + capture the whole group bounding box into one \"item\" (so you can use `is_item_hovered()` or layout primitives such as `same_line()` on whole group, etc.)"""
    ...


def end_list_box() -> None:
    """Only call `end_list_box()` if `begin_list_box()` returned true!"""
    ...


def end_main_menu_bar() -> None:
    """Only call `end_main_menu_bar()` if `begin_main_menu_bar()` returns true!"""
    ...


def end_menu() -> None:
    """Only call `end_menu()` if `begin_menu()` returns true!"""
    ...


def end_menu_bar() -> None:
    """Only call `end_menu_bar()` if `begin_menu_bar()` returns true!"""
    ...


def end_popup() -> None:
    """Only call `end_popup()` if BeginPopupXXX() returns true!"""
    ...


def end_tab_bar() -> None:
    """Only call `end_tab_bar()` if `begin_tab_bar()` returns true!"""
    ...


def end_tab_item() -> None:
    """Only call `end_tab_item()` if `begin_tab_item()` returns true!"""
    ...


def end_table() -> None:
    """Only call `end_table()` if `begin_table()` returns true!"""
    ...


def end_tooltip() -> None:
    """Only call `end_tooltip()` if `begin_tooltip()`/`begin_item_tooltip()` returns true!"""
    ...


def get_column_index() -> int:
    """Get current column index"""
    ...


def get_column_offset(column_index: int = -1) -> float:
    """Get position of column line (in pixels, from the left side of the contents region). pass -1 to use current column, otherwise 0..`get_columns_count()` inclusive. column 0 is typically 0.0f"""
    ...


def get_column_width(column_index: int = -1) -> float:
    """Get column width (in pixels). pass -1 to use current column"""
    ...


def get_columns_count() -> int:
    ...


def get_content_region_avail() -> tuple[float, float]:
    """Available space from current position. THIS IS YOUR BEST FRIEND."""
    ...


def get_current_context() -> Context:
    ...


def get_cursor_pos() -> tuple[float, float]:
    """[window-local] cursor position in window-local coordinates. This is not your best friend."""
    ...


def get_cursor_pos_x() -> float:
    """[window-local] \""""
    ...


def get_cursor_pos_y() -> float:
    """[window-local] \""""
    ...


def get_cursor_screen_pos() -> tuple[float, float]:
    """Cursor position, absolute coordinates. THIS IS YOUR BEST FRIEND (prefer using this rather than `get_cursor_pos()`, also more useful to work with ImDrawList API)."""
    ...


def get_cursor_start_pos() -> tuple[float, float]:
    """[window-local] initial cursor position, in window-local coordinates. Call `get_cursor_screen_pos()` after `begin()` to get the absolute coordinates version."""
    ...


def get_draw_data() -> DrawData:
    """Valid after `render()` and until the next call to `new_frame()`. this is what you have to render."""
    ...


def get_font_size() -> float:
    """Get current font size (= height in pixels) of current font with current scale applied"""
    ...


def get_font_tex_uv_white_pixel() -> tuple[float, float]:
    """Get UV coordinate for a white pixel, useful to draw custom shapes via the ImDrawList API"""
    ...


def get_frame_count() -> int:
    """Get global imgui frame count. incremented by 1 every frame."""
    ...


def get_frame_height() -> float:
    """~ FontSize + style.FramePadding.y * 2"""
    ...


def get_frame_height_with_spacing() -> float:
    """~ FontSize + style.FramePadding.y * 2 + style.ItemSpacing.y (distance in pixels between 2 consecutive lines of framed widgets)"""
    ...


def get_item_rect_max() -> tuple[float, float]:
    """Get lower-right bounding rectangle of the last item (screen space)"""
    ...


def get_item_rect_min() -> tuple[float, float]:
    """Get upper-left bounding rectangle of the last item (screen space)"""
    ...


def get_item_rect_size() -> tuple[float, float]:
    """Get size of last item"""
    ...


def get_key_name(key: Key) -> str:
    """[DEBUG] returns English name of the key. Those names are provided for debugging purpose and are not meant to be saved persistently nor compared."""
    ...


def get_key_pressed_amount(key: Key, repeat_delay: float, rate: float) -> int:
    """Uses provided repeat rate/delay. return a count, most often 0 or 1 but might be >1 if RepeatRate is small enough that DeltaTime > RepeatRate"""
    ...


def get_main_viewport() -> Viewport:
    """Return primary/default viewport. This can never be NULL."""
    ...


def get_mouse_clicked_count(button: MouseButton) -> int:
    """Return the number of successive mouse-clicks at the time where a click happen (otherwise 0)."""
    ...


def get_mouse_cursor() -> MouseCursor:
    """Get desired mouse cursor shape. Important: reset in ImGui::`new_frame()`, this is updated during the frame. valid before `render()`. If you use software rendering by setting io.MouseDrawCursor ImGui will render those for you"""
    ...


def get_mouse_drag_delta(button: MouseButton = MouseButton.LEFT, lock_threshold: float = -1.0) -> tuple[float, float]:
    """Return the delta from the initial clicking position while the mouse button is pressed or was just released. This is locked and return 0.0f until the mouse moves past a distance threshold at least once (uses io.MouseDraggingThreshold if lock_threshold < 0.0f)"""
    ...


def get_mouse_pos() -> tuple[float, float]:
    """Shortcut to ImGui::`get_io()`.MousePos provided by user, to be consistent with other calls"""
    ...


def get_mouse_pos_on_opening_current_popup() -> tuple[float, float]:
    """Retrieve mouse position at the time of opening popup we have `begin_popup()` into (helper to avoid user backing that value themselves)"""
    ...


def get_scroll_max_x() -> float:
    """Get maximum scrolling amount ~~ ContentSize.x - WindowSize.x - DecorationsSize.x"""
    ...


def get_scroll_max_y() -> float:
    """Get maximum scrolling amount ~~ ContentSize.y - WindowSize.y - DecorationsSize.y"""
    ...


def get_scroll_x() -> float:
    """Get scrolling amount [0 .. `get_scroll_max_x()`]"""
    ...


def get_scroll_y() -> float:
    """Get scrolling amount [0 .. `get_scroll_max_y()`]"""
    ...


def get_style() -> Style:
    """Access the Style structure (colors, sizes). Always use `push_style_color()`, `push_style_var()` to modify style mid-frame!"""
    ...


def get_style_color_name(col: Col) -> str:
    """Get a string corresponding to the enum value (for display, saving, etc.)."""
    ...


def get_style_color_vec4(col: Col) -> tuple[float, float, float, float]:
    """Retrieve style color as stored in ImGuiStyle structure. use to feed back into `push_style_color()`, otherwise use `get_color_u32()` to get style color with style alpha baked in."""
    ...


def get_text_line_height() -> float:
    """~ FontSize"""
    ...


def get_text_line_height_with_spacing() -> float:
    """~ FontSize + style.ItemSpacing.y (distance in pixels between 2 consecutive lines of text)"""
    ...


def get_time() -> float:
    """Get global imgui time. incremented by io.DeltaTime every frame."""
    ...


def get_tree_node_to_label_spacing() -> float:
    """Horizontal distance preceding label when using `tree_node`*() or `bullet()` == (g.FontSize + style.FramePadding.x*2) for a regular unframed `tree_node`"""
    ...


def get_version() -> str:
    """Get the compiled version string e.g. \"1.80 WIP\" (essentially the value for IMGUI_VERSION from the compiled version of imgui.cpp)"""
    ...


def get_window_height() -> float:
    """Get current window height (IT IS UNLIKELY YOU EVER NEED TO USE THIS). Shortcut for `get_window_size()`.y."""
    ...


def get_window_pos() -> tuple[float, float]:
    """Get current window position in screen space (IT IS UNLIKELY YOU EVER NEED TO USE THIS. Consider always using `get_cursor_screen_pos()` and `get_content_region_avail()` instead)"""
    ...


def get_window_size() -> tuple[float, float]:
    """Get current window size (IT IS UNLIKELY YOU EVER NEED TO USE THIS. Consider always using `get_cursor_screen_pos()` and `get_content_region_avail()` instead)"""
    ...


def get_window_width() -> float:
    """Get current window width (IT IS UNLIKELY YOU EVER NEED TO USE THIS). Shortcut for `get_window_size()`.x."""
    ...


def image(user_texture_id: int, image_size: tuple[float, float], uv0: tuple[float, float] = (0.0, 0.0), uv1: tuple[float, float] = (1.0, 1.0)) -> None:
    ...


def image_button(str_id: str, user_texture_id: int, image_size: tuple[float, float], uv0: tuple[float, float] = (0.0, 0.0), uv1: tuple[float, float] = (1.0, 1.0), bg_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0), tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)) -> bool:
    ...


def image_with_bg(user_texture_id: int, image_size: tuple[float, float], uv0: tuple[float, float] = (0.0, 0.0), uv1: tuple[float, float] = (1.0, 1.0), bg_col: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0), tint_col: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)) -> None:
    ...


def indent(indent_w: float = 0.0) -> None:
    """Move content position toward the right, by indent_w, or style.IndentSpacing if indent_w <= 0"""
    ...


def input_double(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.6f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, float]:
    ...


def input_float(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, float]:
    ...


def input_float2(label: str, v: tuple[float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float]]:
    ...


def input_float3(label: str, v: tuple[float, float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float, float]]:
    ...


def input_float4(label: str, v: tuple[float, float, float, float], format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]:
    ...


def input_int(label: str, v: int, step: int = 1, step_fast: int = 100, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, int]:
    ...


def input_int2(label: str, v: tuple[int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int]]:
    ...


def input_int3(label: str, v: tuple[int, int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int, int]]:
    ...


def input_int4(label: str, v: tuple[int, int, int, int], flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]:
    ...


def input_text(label: str, text: str, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]:
    ...


def input_text_multiline(label: str, text: str, size: tuple[float, float] = (0.0, 0.0), flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]:
    ...


def input_text_with_hint(label: str, hint: str, text: str, flags: InputTextFlags = InputTextFlags.NONE) -> tuple[bool, str]:
    ...


def invisible_button(str_id: str, size: tuple[float, float], flags: ButtonFlags = ButtonFlags.NONE) -> bool:
    """Flexible button behavior without the visuals, frequently useful to build custom behaviors using the public api (along with `is_item_active`, `is_item_hovered`, etc.)"""
    ...


def is_any_item_active() -> bool:
    """Is any item active?"""
    ...


def is_any_item_focused() -> bool:
    """Is any item focused?"""
    ...


def is_any_item_hovered() -> bool:
    """Is any item hovered?"""
    ...


def is_item_activated() -> bool:
    """Was the last item just made active (item was previously inactive)."""
    ...


def is_item_active() -> bool:
    """Is the last item active? (e.g. button being held, text field being edited. This will continuously return true while holding mouse button on an item. Items that don't interact will always return false)"""
    ...


def is_item_clicked(mouse_button: MouseButton = MouseButton.LEFT) -> bool:
    """Is the last item hovered and mouse clicked on? (**)  == `is_mouse_clicked(mouse_button)` && `is_item_hovered()`Important. (**) this is NOT equivalent to the behavior of e.g. `button()`. Read comments in function definition."""
    ...


def is_item_deactivated() -> bool:
    """Was the last item just made inactive (item was previously active). Useful for Undo/Redo patterns with widgets that require continuous editing."""
    ...


def is_item_deactivated_after_edit() -> bool:
    """Was the last item just made inactive and made a value change when it was active? (e.g. Slider/Drag moved). Useful for Undo/Redo patterns with widgets that require continuous editing. Note that you may get false positives (some widgets such as `combo()`/`list_box()`/`selectable()` will return true even when clicking an already selected item)."""
    ...


def is_item_edited() -> bool:
    """Did the last item modify its underlying value this frame? or was pressed? This is generally the same as the \"bool\" return value of many widgets."""
    ...


def is_item_focused() -> bool:
    """Is the last item focused for keyboard/gamepad navigation?"""
    ...


def is_item_hovered(flags: HoveredFlags = HoveredFlags.NONE) -> bool:
    """Is the last item hovered? (and usable, aka not blocked by a popup, etc.). See ImGuiHoveredFlags for more options."""
    ...


def is_item_toggled_open() -> bool:
    """Was the last item open state toggled? set by `tree_node()`."""
    ...


def is_item_visible() -> bool:
    """Is the last item visible? (items may be out of sight because of clipping/scrolling)"""
    ...


def is_key_chord_pressed(key_chord: Key) -> bool:
    """Was key chord (mods + key) pressed, e.g. you can pass 'ImGuiMod_Ctrl | ImGuiKey_S' as a key-chord. This doesn't do any routing or focus check, please consider using `shortcut()` function instead."""
    ...


def is_key_down(key: Key) -> bool:
    """Is key being held."""
    ...


def is_key_pressed(key: Key, repeat: bool = True) -> bool:
    """Was key pressed (went from !Down to Down)? if repeat=true, uses io.KeyRepeatDelay / KeyRepeatRate"""
    ...


def is_key_released(key: Key) -> bool:
    """Was key released (went from Down to !Down)?"""
    ...


def is_mouse_clicked(button: MouseButton, repeat: bool = False) -> bool:
    """Did mouse button clicked? (went from !Down to Down). Same as `get_mouse_clicked_count()` == 1."""
    ...


def is_mouse_double_clicked(button: MouseButton) -> bool:
    """Did mouse button double-clicked? Same as `get_mouse_clicked_count()` == 2. (note that a double-click will also report `is_mouse_clicked()` == true)"""
    ...


def is_mouse_down(button: MouseButton) -> bool:
    """Is mouse button held?"""
    ...


def is_mouse_dragging(button: MouseButton, lock_threshold: float = -1.0) -> bool:
    """Is mouse dragging? (uses io.MouseDraggingThreshold if lock_threshold < 0.0f)"""
    ...


def is_mouse_hovering_rect(r_min: tuple[float, float], r_max: tuple[float, float], clip: bool = True) -> bool:
    """Is mouse hovering given bounding rect (in screen space). clipped by current clipping settings, but disregarding of other consideration of focus/window ordering/popup-block."""
    ...


def is_mouse_pos_valid(mouse_pos: tuple[float, float] | None = None) -> bool:
    """By convention we use (-FLT_MAX,-FLT_MAX) to denote that there is no mouse available"""
    ...


def is_mouse_released(button: MouseButton) -> bool:
    """Did mouse button released? (went from Down to !Down)"""
    ...


def is_mouse_released_with_delay(button: MouseButton, delay: float) -> bool:
    """Delayed mouse release (use very sparingly!). Generally used with 'delay >= io.MouseDoubleClickTime' + combined with a 'io.MouseClickedLastCount==1' test. This is a very rarely used UI idiom, but some apps use this: e.g. MS Explorer single click on an icon to rename."""
    ...


def is_popup_open(str_id: str, flags: PopupFlags = PopupFlags.NONE) -> bool:
    """Return true if the popup is open."""
    ...


@overload
def is_rect_visible(size: tuple[float, float]) -> bool:
    """Test if rectangle (of given size, starting from cursor position) is visible / not clipped."""
    ...


@overload
def is_rect_visible(rect_min: tuple[float, float], rect_max: tuple[float, float]) -> bool:
    ...


def is_window_appearing() -> bool:
    ...


def is_window_collapsed() -> bool:
    ...


def is_window_focused(flags: FocusedFlags = FocusedFlags.NONE) -> bool:
    """Is current window focused? or its root/child, depending on flags. see flags for options."""
    ...


def is_window_hovered(flags: HoveredFlags = HoveredFlags.NONE) -> bool:
    """Is current window hovered and hoverable (e.g. not blocked by a popup/modal)? See `HoveredFlags` for options. IMPORTANT: If you are trying to check whether your mouse should be dispatched to Dear ImGui or to your underlying app, you should not use this function! Use the 'io.WantCaptureMouse' boolean for that! Refer to FAQ entry \"How can I tell whether to dispatch mouse/keyboard to Dear ImGui or my application?\" for details."""
    ...


def label_text(label: str, text: str) -> None:
    """Display text+label aligned the same way as value+label widgets"""
    ...


def list_box(label: str, current_item: int, items: Sequence[str], height_in_items: int = -1) -> tuple[bool, int]:
    ...


def log_buttons() -> None:
    """Helper to display buttons for logging to tty/file/clipboard"""
    ...


def log_finish() -> None:
    """Stop logging (close file, etc.)"""
    ...


def log_text(text: str) -> None:
    """Pass text data straight to log (without being displayed)"""
    ...


def log_to_clipboard(auto_open_depth: int = -1) -> None:
    """Start logging to OS clipboard"""
    ...


def log_to_file(auto_open_depth: int = -1, filename: str | None = None) -> None:
    """Start logging to file"""
    ...


def log_to_tty(auto_open_depth: int = -1) -> None:
    """Start logging to tty (stdout)"""
    ...


def menu_item(label: str, shortcut: str | None = None, selected: bool = False, enabled: bool = True) -> tuple[bool, bool]:
    """Return true when activated."""
    ...


def new_frame() -> None:
    """Start a new Dear ImGui frame, you can submit any command from this point until `render()`/`end_frame()`."""
    ...


def new_line() -> None:
    """Undo a `same_line()` or force a new line when in a horizontal-layout context."""
    ...


def next_column() -> None:
    """Next column, defaults to current row or next row if the current row is finished"""
    ...


def open_popup(str_id: str, flags: PopupFlags = PopupFlags.NONE) -> None:
    """Call to mark popup as open (don't call every frame!)."""
    ...


def open_popup_on_item_click(str_id: str | None = None, flags: PopupFlags = PopupFlags.MOUSE_BUTTON_RIGHT) -> None:
    """Helper to open popup when clicked on last item. Default to `PopupFlags.MOUSE_BUTTON_RIGHT` == 1. (note: actually triggers on the mouse _released_ event to be consistent with popup behaviors)"""
    ...


def plot_histogram(label: str, values: Annotated[ArrayLike, dict(dtype='float32', shape=(None), device='cpu', writable=False)], overlay_text: str | None = None, scale_min: float = FLT_MAX, scale_max: float = FLT_MAX, graph_size: tuple[float, float] = (0.0, 0.0)) -> None:
    ...


def plot_lines(label: str, values: Annotated[ArrayLike, dict(dtype='float32', shape=(None), device='cpu', writable=False)], overlay_text: str | None = None, scale_min: float = FLT_MAX, scale_max: float = FLT_MAX, graph_size: tuple[float, float] = (0.0, 0.0)) -> None:
    ...


def pop_clip_rect() -> None:
    ...


def pop_font() -> None:
    ...


def pop_id() -> None:
    """Pop from the ID stack."""
    ...


def pop_item_flag() -> None:
    ...


def pop_item_width() -> None:
    ...


def pop_style_color(count: int = 1) -> None:
    ...


def pop_style_var(count: int = 1) -> None:
    ...


def pop_text_wrap_pos() -> None:
    ...


def progress_bar(fraction: float, size_arg: tuple[float, float] = (-FLT_MIN, 0), overlay: str | None = None) -> None:
    ...


def push_clip_rect(clip_rect_min: tuple[float, float], clip_rect_max: tuple[float, float], intersect_with_current_clip_rect: bool) -> None:
    ...


def push_font(font: Font | None) -> None:
    """Use NULL as a shortcut to push default font"""
    ...


@overload
def push_id(str_id: str) -> None:
    """Push string into the ID stack (will hash string)."""
    ...


@overload
def push_id(int_id: int) -> None:
    ...


def push_item_flag(option: ItemFlags, enabled: bool) -> None:
    """Modify specified shared item flag, e.g. `push_item_flag(ItemFlags.NO_TAB_STOP, true)`"""
    ...


def push_item_width(item_width: float) -> None:
    """Push width of items for common large \"item+label\" widgets. >0.0f: width in pixels, <0.0f align xx pixels to the right of window (so -FLT_MIN always align width to the right side)."""
    ...


@overload
def push_style_color(idx: Col, col: int) -> None:
    """Modify a style color. always use this if you modify the style after `new_frame()`."""
    ...


@overload
def push_style_color(idx: Col, col: tuple[float, float, float, float]) -> None:
    ...


@overload
def push_style_color(idx: Col, col: tuple[float, float, float]) -> None:
    ...


@overload
def push_style_var(idx: StyleVar, val: float) -> None:
    """Modify a style float variable. always use this if you modify the style after `new_frame()`!"""
    ...


@overload
def push_style_var(idx: StyleVar, val: tuple[float, float]) -> None:
    ...


def push_style_var_x(idx: StyleVar, val_x: float) -> None:
    """Modify X component of a style ImVec2 variable. \""""
    ...


def push_style_var_y(idx: StyleVar, val_y: float) -> None:
    """Modify Y component of a style ImVec2 variable. \""""
    ...


def push_text_wrap_pos(wrap_local_pos_x: float = 0.0) -> None:
    ...


@overload
def radio_button(label: str, active: bool) -> bool:
    ...


@overload
def radio_button(label: str, v: int, v_button: int) -> tuple[bool, int]:
    ...


def render() -> None:
    """Ends the Dear ImGui frame, finalize the draw data. You can then get call `get_draw_data()`."""
    ...


def reset_mouse_drag_delta(button: MouseButton = MouseButton.LEFT) -> None:
    ...


def same_line(offset_from_start_x: float = 0.0, spacing: float = -1.0) -> None:
    """Call between widgets or groups to layout them horizontally. X position given in window coordinates."""
    ...


def selectable(label: str, selected: bool = False, flags: SelectableFlags = SelectableFlags.NONE, size: tuple[float, float] = (0.0, 0.0)) -> tuple[bool, bool]:
    """\"bool selected\" carry the selection state (read-only). `selectable()` is clicked is returns true so you can modify your selection state. size.x==0.0: use remaining width, size.x>0.0: specify width. size.y==0.0: use label height, size.y>0.0: specify height"""
    ...


def separator() -> None:
    """Separator, generally horizontal. inside a menu bar or in horizontal layout mode, this becomes a vertical separator."""
    ...


def separator_text(text: str) -> None:
    """Currently: formatted text with a horizontal line"""
    ...


def set_color_edit_options(flags: ColorEditFlags) -> None:
    """Initialize current options (generally on application startup) if you want to select a default format, picker type, etc. User will be able to change many settings, unless you pass the _NoOptions flag to your calls."""
    ...


def set_column_offset(column_index: int, offset_x: float) -> None:
    """Set position of column line (in pixels, from the left side of the contents region). pass -1 to use current column"""
    ...


def set_column_width(column_index: int, width: float) -> None:
    """Set column width (in pixels). pass -1 to use current column"""
    ...


def set_current_context(arg: Context, /) -> None:
    ...


def set_cursor_pos(local_pos: tuple[float, float]) -> None:
    """[window-local] \""""
    ...


def set_cursor_pos_x(local_x: float) -> None:
    """[window-local] \""""
    ...


def set_cursor_pos_y(local_y: float) -> None:
    """[window-local] \""""
    ...


def set_cursor_screen_pos(pos: tuple[float, float]) -> None:
    """Cursor position, absolute coordinates. THIS IS YOUR BEST FRIEND."""
    ...


def set_item_default_focus() -> None:
    """Make last item the default focused item of a newly appearing window."""
    ...


def set_item_tooltip(text: str) -> None:
    """Set a text-only tooltip if preceding item was hovered. override any previous call to `set_tooltip()`."""
    ...


def set_keyboard_focus_here(offset: int = 0) -> None:
    """Focus keyboard on the next widget. Use positive 'offset' to access sub components of a multiple component widget. Use -1 to access previous widget."""
    ...


def set_mouse_cursor(cursor_type: MouseCursor) -> None:
    """Set desired mouse cursor shape"""
    ...


def set_nanobind_leak_warnings(enable: bool) -> None:
    ...


def set_nav_cursor_visible(visible: bool) -> None:
    """Alter visibility of keyboard/gamepad cursor. by default: show when using an arrow key, hide when clicking with mouse."""
    ...


def set_next_frame_want_capture_keyboard(want_capture_keyboard: bool) -> None:
    ...


def set_next_frame_want_capture_mouse(capture: bool) -> None:
    ...


def set_next_item_allow_overlap() -> None:
    """Allow next item to be overlapped by a subsequent item. Useful with invisible buttons, selectable, treenode covering an area where subsequent items may need to be added. Note that both `selectable()` and `tree_node()` have dedicated flags doing this."""
    ...


def set_next_item_open(is_open: bool, cond: Cond = Cond.NONE) -> None:
    """Set next `tree_node`/`collapsing_header` open state."""
    ...


def set_next_item_width(item_width: float) -> None:
    """Set width of the _next_ common large \"item+label\" widget. >0.0f: width in pixels, <0.0f align xx pixels to the right of window (so -FLT_MIN always align width to the right side)"""
    ...


def set_next_window_bg_alpha(alpha: float) -> None:
    """Set next window background color alpha. helper to easily override the Alpha component of `Col.WINDOW_BG`/ChildBg/PopupBg. you may also use `WindowFlags.NO_BACKGROUND`."""
    ...


def set_next_window_collapsed(collapsed: bool, cond: Cond = Cond.NONE) -> None:
    """Set next window collapsed state. call before `begin()`"""
    ...


def set_next_window_content_size(size: tuple[float, float]) -> None:
    """Set next window content size (~ scrollable client area, which enforce the range of scrollbars). Not including window decorations (title bar, menu bar, etc.) nor WindowPadding. set an axis to 0.0f to leave it automatic. call before `begin()`"""
    ...


def set_next_window_focus() -> None:
    """Set next window to be focused / top-most. call before `begin()`"""
    ...


def set_next_window_pos(pos: tuple[float, float], cond: Cond = Cond.NONE, pivot: tuple[float, float] = (0.0, 0.0)) -> None:
    """Set next window position. call before `begin()`. use pivot=(0.5f,0.5f) to center on given point, etc."""
    ...


def set_next_window_scroll(scroll: tuple[float, float]) -> None:
    """Set next window scrolling value (use < 0.0f to not affect a given axis)."""
    ...


def set_next_window_size(size: tuple[float, float], cond: Cond = Cond.NONE) -> None:
    """Set next window size. set axis to 0.0f to force an auto-fit on this axis. call before `begin()`"""
    ...


def set_scroll_from_pos_x(local_x: float, center_x_ratio: float = 0.5) -> None:
    """Adjust scrolling amount to make given position visible. Generally `get_cursor_start_pos()` + offset to compute a valid position."""
    ...


def set_scroll_from_pos_y(local_y: float, center_y_ratio: float = 0.5) -> None:
    """Adjust scrolling amount to make given position visible. Generally `get_cursor_start_pos()` + offset to compute a valid position."""
    ...


def set_scroll_here_x(center_x_ratio: float = 0.5) -> None:
    """Adjust scrolling amount to make current cursor position visible. center_x_ratio=0.0: left, 0.5: center, 1.0: right. When using to make a \"default/current item\" visible, consider using `set_item_default_focus()` instead."""
    ...


def set_scroll_here_y(center_y_ratio: float = 0.5) -> None:
    """Adjust scrolling amount to make current cursor position visible. center_y_ratio=0.0: top, 0.5: center, 1.0: bottom. When using to make a \"default/current item\" visible, consider using `set_item_default_focus()` instead."""
    ...


def set_scroll_x(scroll_x: float) -> None:
    """Set scrolling amount [0 .. `get_scroll_max_x()`]"""
    ...


def set_scroll_y(scroll_y: float) -> None:
    """Set scrolling amount [0 .. `get_scroll_max_y()`]"""
    ...


def set_tab_item_closed(label: str) -> None:
    """Notify TabBar or Docking system of a closed tab/window ahead (useful to reduce visual flicker on reorderable tab bars). For tab-bar: call after `begin_tab_bar()` and before Tab submissions. Otherwise call with a window name."""
    ...


def set_tooltip(text: str) -> None:
    """Set a text-only tooltip. Often used after a ImGui::`is_item_hovered()` check. Override any previous call to `set_tooltip()`."""
    ...


@overload
def set_window_collapsed(collapsed: bool, cond: Cond = Cond.NONE) -> None:
    """(not recommended) set current window collapsed state. prefer using `set_next_window_collapsed()`."""
    ...


@overload
def set_window_collapsed(name: str, collapsed: bool, cond: Cond = Cond.NONE) -> None:
    ...


@overload
def set_window_focus() -> None:
    """(not recommended) set current window to be focused / top-most. prefer using `set_next_window_focus()`."""
    ...


@overload
def set_window_focus(name: str) -> None:
    ...


def set_window_font_scale(scale: float) -> None:
    """[OBSOLETE] set font scale. Adjust IO.FontGlobalScale if you want to scale all windows. This is an old API! For correct scaling, prefer to reload font + rebuild ImFontAtlas + call style.ScaleAllSizes()."""
    ...


@overload
def set_window_pos(pos: tuple[float, float], cond: Cond = Cond.NONE) -> None:
    """(not recommended) set current window position - call within `begin()`/`end()`. prefer using `set_next_window_pos()`, as this may incur tearing and side-effects."""
    ...


@overload
def set_window_pos(name: str, pos: tuple[float, float], cond: Cond = Cond.NONE) -> None:
    ...


@overload
def set_window_size(size: tuple[float, float], cond: Cond = Cond.NONE) -> None:
    """(not recommended) set current window size - call within `begin()`/`end()`. set to ImVec2(0, 0) to force an auto-fit. prefer using `set_next_window_size()`, as this may incur tearing and minor side-effects."""
    ...


@overload
def set_window_size(name: str, size: tuple[float, float], cond: Cond = Cond.NONE) -> None:
    ...


def show_about_window(closable: bool = False) -> bool:
    """Create About window. display Dear ImGui version, credits and build/system information."""
    ...


def show_debug_log_window(closable: bool = False) -> bool:
    """Create Debug Log window. display a simplified log of important dear imgui events."""
    ...


def show_demo_window(closable: bool = False) -> bool:
    """Create Demo window. demonstrate most ImGui features. call this to learn about the library! try to make it always available in your application!"""
    ...


def show_font_selector(label: str) -> None:
    """Add font selector block (not a window), essentially a combo listing the loaded fonts."""
    ...


def show_id_stack_tool_window(closable: bool = False) -> bool:
    """Create Stack Tool window. hover items with mouse to query information about the source of their unique ID."""
    ...


def show_metrics_window(closable: bool = False) -> bool:
    """Create Metrics/Debugger window. display Dear ImGui internals: windows, draw commands, various internal state, etc."""
    ...


def show_style_editor() -> None:
    """Add style editor block (not a window). you can pass in a reference ImGuiStyle structure to compare to, revert to and save to (else it uses the default style)"""
    ...


def show_style_selector(label: str) -> bool:
    """Add style selector block (not a window), essentially a combo listing the default styles."""
    ...


def show_user_guide() -> None:
    """Add basic help/info block (not a window): how to manipulate ImGui as an end-user (mouse/keyboard controls)."""
    ...


def slider_angle(label: str, v: float, v_degrees_min: float = -360.0, v_degrees_max: float = 360.0, format: str = '%.0f deg', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]:
    ...


def slider_float(label: str, v: float, v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, float]:
    """Adjust format to decorate the value with a prefix or a suffix for in-slider labels or unit display."""
    ...


def slider_float2(label: str, v: tuple[float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float]]:
    ...


def slider_float3(label: str, v: tuple[float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float]]:
    ...


def slider_float4(label: str, v: tuple[float, float, float, float], v_min: float, v_max: float, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[float, float, float, float]]:
    ...


def slider_int(label: str, v: int, v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, int]:
    ...


def slider_int2(label: str, v: tuple[int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int]]:
    ...


def slider_int3(label: str, v: tuple[int, int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int]]:
    ...


def slider_int4(label: str, v: tuple[int, int, int, int], v_min: int, v_max: int, format: str = '%d', flags: SliderFlags = SliderFlags.NONE) -> tuple[bool, tuple[int, int, int, int]]:
    ...


def small_button(label: str) -> bool:
    """Button with (FramePadding.y == 0) to easily embed within text"""
    ...


def spacing() -> None:
    """Add vertical spacing."""
    ...


def style_colors_classic(dst: Style) -> None:
    """Classic imgui style"""
    ...


def style_colors_dark(dst: Style) -> None:
    """New, recommended style (default)"""
    ...


def style_colors_light(dst: Style) -> None:
    """Best used with borders and a custom, thicker font"""
    ...


def tab_item_button(label: str, flags: TabItemFlags = TabItemFlags.NONE) -> bool:
    """Create a Tab behaving like a button. return true when clicked. cannot be selected in the tab bar."""
    ...


def table_angled_headers_row() -> None:
    """Submit a row with angled headers for every column with the `TableColumnFlags.ANGLED_HEADER` flag. MUST BE FIRST ROW."""
    ...


def table_get_column_count() -> int:
    """Return number of columns (value passed to `begin_table`)"""
    ...


def table_get_column_flags(column_n: int = -1) -> TableColumnFlags:
    """Return column flags so you can query their Enabled/Visible/Sorted/Hovered status flags. Pass -1 to use current column."""
    ...


def table_get_column_index() -> int:
    """Return current column index."""
    ...


def table_get_column_name(column_n: int = -1) -> str:
    """Return \"\" if column didn't have a name declared by `table_setup_column()`. Pass -1 to use current column."""
    ...


def table_get_row_index() -> int:
    """Return current row index."""
    ...


def table_header(label: str) -> None:
    """Submit one header cell manually (rarely used)"""
    ...


def table_headers_row() -> None:
    """Submit a row with headers cells based on data provided to `table_setup_column()` + submit context menu"""
    ...


def table_next_column() -> bool:
    """Append into the next column (or first column of next row if currently in last column). Return true when column is visible."""
    ...


def table_next_row(flags: TableRowFlags = TableRowFlags.NONE, min_row_height: float = 0.0) -> None:
    """Append into the first cell of a new row."""
    ...


def table_set_bg_color(target: TableBgTarget, color: tuple[float, float, float, float], column_n: int = -1) -> None:
    """Change the color of a cell, row, or column. See `TableBgTarget` flags for details."""
    ...


def table_set_column_enabled(column_n: int, v: bool) -> None:
    """Change user accessible enabled/disabled state of a column. Set to false to hide the column. User can use the context menu to change this themselves (right-click in headers, or right-click in columns body with `TableFlags.CONTEXT_MENU_IN_BODY`)"""
    ...


def table_set_column_index(column_n: int) -> bool:
    """Append into the specified column. Return true when column is visible."""
    ...


def table_setup_column(label: str, flags: TableColumnFlags = TableColumnFlags.NONE, init_width_or_weight: float = 0.0, user_id: int = 0) -> None:
    ...


def table_setup_scroll_freeze(cols: int, rows: int) -> None:
    """Lock columns/rows so they stay visible when scrolled."""
    ...


def text(text: str) -> None:
    """Formatted text"""
    ...


def text_colored(col: tuple[float, float, float, float], text: str) -> None:
    ...


def text_disabled(text: str) -> None:
    ...


def text_link(label: str) -> None:
    """Hyperlink text button, return true when clicked"""
    ...


def text_link_open_url(label: str, url: str | None = None) -> None:
    """Hyperlink text button, automatically open file/url when clicked"""
    ...


def text_wrapped(text: str) -> None:
    ...


@overload
def tree_node(label: str, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> bool:
    ...


@overload
def tree_node(str_id: str, text: str, flags: TreeNodeFlags = TreeNodeFlags.NONE) -> bool:
    ...


def tree_pop() -> None:
    """~ `unindent()`+`pop_id()`"""
    ...


def tree_push(str_id: str) -> None:
    """~ `indent()`+`push_id()`. Already called by `tree_node()` when returning true, but you can call `tree_push`/`tree_pop` yourself if desired."""
    ...


def unindent(indent_w: float = 0.0) -> None:
    """Move content position back to the left, by indent_w, or style.IndentSpacing if indent_w <= 0"""
    ...
