from collections.abc import Sequence
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike

import slimgui_ext


AUTO: int = -1

AUTO_COL: tuple = (0.0, 0.0, 0.0, -1.0)

class Axis(enum.IntEnum):
    X1 = 0

    X2 = 1

    X3 = 2

    Y1 = 3

    Y2 = 4

    Y3 = 5

    COUNT = 6

class AxisFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_LABEL = 1

    NO_GRID_LINES = 2

    NO_TICK_MARKS = 4

    NO_TICK_LABELS = 8

    NO_INITIAL_FIT = 16

    NO_MENUS = 32

    NO_SIDE_SWITCH = 64

    NO_HIGHLIGHT = 128

    OPPOSITE = 256

    FOREGROUND = 512

    INVERT = 1024

    AUTO_FIT = 2048

    RANGE_FIT = 4096

    PAN_STRETCH = 8192

    LOCK_MIN = 16384

    LOCK_MAX = 32768

    LOCK = 49152

    NO_DECORATIONS = 15

    AUX_DEFAULT = 258

class BarGroupsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

    STACKED = 2048

class BarsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

class Bin(enum.IntEnum):
    SQRT = -1

    STURGES = -2

    RICE = -3

    SCOTT = -4

class Col(enum.IntEnum):
    LINE = 0

    FILL = 1

    MARKER_OUTLINE = 2

    MARKER_FILL = 3

    ERROR_BAR = 4

    FRAME_BG = 5

    PLOT_BG = 6

    PLOT_BORDER = 7

    LEGEND_BG = 8

    LEGEND_BORDER = 9

    LEGEND_TEXT = 10

    TITLE_TEXT = 11

    INLAY_TEXT = 12

    AXIS_TEXT = 13

    AXIS_GRID = 14

    AXIS_TICK = 15

    AXIS_BG = 16

    AXIS_BG_HOVERED = 17

    AXIS_BG_ACTIVE = 18

    SELECTION = 19

    CROSSHAIRS = 20

    COUNT = 21

class Colormap(enum.IntEnum):
    DEEP = 0

    DARK = 1

    PASTEL = 2

    PAIRED = 3

    VIRIDIS = 4

    PLASMA = 5

    HOT = 6

    COOL = 7

    PINK = 8

    JET = 9

    TWILIGHT = 10

    RD_BU = 11

    BR_BG = 12

    PI_YG = 13

    SPECTRAL = 14

    GREYS = 15

class ColormapScaleFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_LABEL = 1

    OPPOSITE = 2

    INVERT = 4

class Cond(enum.IntEnum):
    NONE = 0

    ALWAYS = 1

    ONCE = 2

class Context:
    def get_plot_draw_list_internal(self) -> slimgui_ext.imgui.DrawList: ...

    def get_style_internal(self) -> Style: ...

    def get_input_map_internal(self) -> InputMap: ...

class DigitalFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

class DragToolFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_CURSORS = 1

    NO_FIT = 2

    NO_INPUTS = 4

    DELAYED = 8

class DummyFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

class ErrorBarsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

class HeatmapFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    COL_MAJOR = 1024

class HistogramFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

    CUMULATIVE = 2048

    DENSITY = 4096

    NO_OUTLIERS = 8192

    COL_MAJOR = 16384

class ImageFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

class InfLinesFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

class InputMap:
    pass

class ItemFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_LEGEND = 1

    NO_FIT = 2

class LegendFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_BUTTONS = 1

    NO_HIGHLIGHT_ITEM = 2

    NO_HIGHLIGHT_AXIS = 4

    NO_MENUS = 8

    OUTSIDE = 16

    HORIZONTAL = 32

    SORT = 64

class LineFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    SEGMENTS = 1024

    LOOP = 2048

    SKIP_NA_N = 4096

    NO_CLIP = 8192

    SHADED = 16384

class Location(enum.IntEnum):
    CENTER = 0

    NORTH = 1

    SOUTH = 2

    WEST = 4

    EAST = 8

    NORTH_WEST = 5

    NORTH_EAST = 9

    SOUTH_WEST = 6

    SOUTH_EAST = 10

class Marker(enum.IntEnum):
    NONE = -1

    CIRCLE = 0

    SQUARE = 1

    DIAMOND = 2

    UP = 3

    DOWN = 4

    LEFT = 5

    RIGHT = 6

    CROSS = 7

    PLUS = 8

    ASTERISK = 9

    COUNT = 10

class MouseTextFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_AUX_AXES = 1

    NO_FORMAT = 2

    SHOW_ALWAYS = 4

class PieChartFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NORMALIZE = 1024

    IGNORE_HIDDEN = 2048

    EXPLODING = 4096

class PlotFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_TITLE = 1

    NO_LEGEND = 2

    NO_MOUSE_TEXT = 4

    NO_INPUTS = 8

    NO_MENUS = 16

    NO_BOX_SELECT = 32

    NO_FRAME = 64

    EQUAL = 128

    CROSSHAIRS = 256

    CANVAS_ONLY = 55

class Scale(enum.IntEnum):
    LINEAR = 0

    TIME = 1

    LOG10 = 2

    SYM_LOG = 3

class ScatterFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_CLIP = 1024

class ShadedFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

class StairsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    PRE_STEP = 1024

    SHADED = 2048

class StemsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    HORIZONTAL = 1024

class Style:
    pass

class StyleVar(enum.IntEnum):
    LINE_WEIGHT = 0

    MARKER = 1

    MARKER_SIZE = 2

    MARKER_WEIGHT = 3

    FILL_ALPHA = 4

    ERROR_BAR_SIZE = 5

    ERROR_BAR_WEIGHT = 6

    DIGITAL_BIT_HEIGHT = 7

    DIGITAL_BIT_GAP = 8

    PLOT_BORDER_SIZE = 9

    MINOR_ALPHA = 10

    MAJOR_TICK_LEN = 11

    MINOR_TICK_LEN = 12

    MAJOR_TICK_SIZE = 13

    MINOR_TICK_SIZE = 14

    MAJOR_GRID_SIZE = 15

    MINOR_GRID_SIZE = 16

    PLOT_PADDING = 17

    LABEL_PADDING = 18

    LEGEND_PADDING = 19

    LEGEND_INNER_PADDING = 20

    LEGEND_SPACING = 21

    MOUSE_POS_PADDING = 22

    ANNOTATION_PADDING = 23

    FIT_PADDING = 24

    PLOT_DEFAULT_SIZE = 25

    PLOT_MIN_SIZE = 26

    COUNT = 27

class SubplotFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    NO_TITLE = 1

    NO_LEGEND = 2

    NO_MENUS = 4

    NO_RESIZE = 8

    NO_ALIGN = 16

    SHARE_ITEMS = 32

    LINK_ROWS = 64

    LINK_COLS = 128

    LINK_ALL_X = 256

    LINK_ALL_Y = 512

    COL_MAJOR = 1024

class TextFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0

    VERTICAL = 1024

@overload
def annotation(x: float, y: float, col: tuple[float, float, float, float], pix_offset: tuple[float, float], clamp: bool, round: bool = False) -> None: ...

@overload
def annotation(x: float, y: float, col: tuple[float, float, float, float], pix_offset: tuple[float, float], clamp: bool, text: str) -> None: ...

def begin_aligned_plots(group_id: str, vertical: bool = True) -> bool: ...

def begin_drag_drop_source_axis(axis: Axis, flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool: ...

def begin_drag_drop_source_item(label_id: str, flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool: ...

def begin_drag_drop_source_plot(flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool: ...

def begin_drag_drop_target_axis(axis: Axis) -> bool: ...

def begin_drag_drop_target_legend() -> bool: ...

def begin_drag_drop_target_plot() -> bool: ...

def begin_legend_popup(label_id: str, mouse_button: slimgui_ext.imgui.MouseButton = slimgui_ext.imgui.MouseButton.RIGHT) -> bool: ...

def begin_plot(title_id: str, size: tuple[float, float] = (-1,0), flags: PlotFlags = PlotFlags.NONE) -> bool: ...

def bust_color_cache(plot_title_id: str | None = None) -> None: ...

def cancel_plot_selection() -> None: ...

def colormap_button(label: str, size: tuple[float, float] = (0,0), cmap: Colormap | int = AUTO) -> bool: ...

def colormap_icon(cmap: Colormap) -> None: ...

def colormap_scale(label: str, scale_min: float, scale_max: float, size: tuple[float, float] = (0,0), format: str = '%g', flags: ColormapScaleFlags = ColormapScaleFlags.NONE, cmap: Colormap | int = AUTO) -> None: ...

def create_context_internal() -> Context: ...

def destroy_context_internal(arg: Context, /) -> None: ...

def end_aligned_plots() -> None: ...

def end_drag_drop_source() -> None: ...

def end_drag_drop_target() -> None: ...

def end_legend_popup() -> None: ...

def end_plot() -> None: ...

def get_colormap_color(idx: int, cmap: Colormap | int = AUTO) -> tuple[float, float, float, float]: ...

def get_colormap_count() -> int: ...

def get_colormap_index(name: str) -> int: ...

def get_colormap_name(cmap: Colormap) -> str: ...

def get_colormap_size(cmap: Colormap | int = AUTO) -> int: ...

def get_last_item_color() -> tuple[float, float, float, float]: ...

def get_marker_name(idx: Marker) -> str: ...

def get_plot_mouse_pos(x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

def get_plot_pos() -> tuple[float, float]: ...

def get_plot_size() -> tuple[float, float]: ...

def get_style_color_name(idx: Col) -> str: ...

def hide_next_item(hidden: bool = True, cond: Cond = Cond.ONCE) -> None: ...

def is_axis_hovered(axis: Axis) -> bool: ...

def is_legend_entry_hovered(label_id: str) -> bool: ...

def is_plot_hovered() -> bool: ...

def is_plot_selected() -> bool: ...

def is_subplots_hovered() -> bool: ...

@overload
def item_icon(col: tuple[float, float, float, float]) -> None: ...

@overload
def item_icon(col: int) -> None: ...

def map_input_default(dst: InputMap | None = None) -> None: ...

def map_input_reverse(dst: InputMap | None = None) -> None: ...

def next_colormap_color() -> tuple[float, float, float, float]: ...

@overload
def pixels_to_plot(pix: tuple[float, float], x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

@overload
def pixels_to_plot(x: float, y: float, x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

def plot_bar_groups(label_ids: Sequence[str], values: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', device='cpu', writable=False)], group_size: float = 0.67, shift: float = 0.0, flags: BarGroupsFlags = BarGroupsFlags.NONE) -> None: ...

@overload
def plot_bars(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float = 0.67, shift: float = 0.0, flags: BarsFlags = BarFlags.NONE) -> None: ...

@overload
def plot_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float, flags: BarsFlags = BarFlags.NONE) -> None: ...

def plot_digital(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: DigitalFlags = DigitalFlags.NONE) -> None: ...

def plot_dummy(label_id: str, flags: DummyFlag = DummyFlag.NONE) -> None: ...

@overload
def plot_error_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], err: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ErrorBarsFlags = ErrorBarsFlags.NONE) -> None: ...

@overload
def plot_error_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], neg: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], pos: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ErrorBarsFlags = ErrorBarsFlags.NONE) -> None: ...

def plot_heatmap(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', device='cpu', writable=False)], scale_min: float = 0, scale_max: float = 0.0, label_fmt: str | None = '%.1f', bounds_min: tuple[float, float] = (0.0, 0.0), bounds_max: tuple[float, float] = (1.0, 1.0), flags: HeatmapFlags = HeatmapFlags.NONE) -> None: ...

def plot_image(label_id: str, user_texture_id: int, bounds_min: tuple[float, float], bounds_max: tuple[float, float], uv0: tuple[float, float] = (0,0), uv1: tuple[float, float] = (1,1), tint_col: tuple[float, float, float, float] = (1,1,1,1), flags: ImageFlag = ImageFlag.NONE) -> None: ...

def plot_inf_lines(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: InfLinesFlags = InfLinesFlags.NONE) -> None: ...

@overload
def plot_line(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: LineFlags = LineFlags.NONE) -> None: ...

@overload
def plot_line(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: LineFlags = LineFlags.NONE) -> None: ...

@overload
def plot_scatter(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: ScatterFlags = ScatterFlags.NONE) -> None: ...

@overload
def plot_scatter(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ScatterFlags = ScatterFlags.NONE) -> None: ...

@overload
def plot_shaded(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], yref: float = 0, xscale: float = 1.0, xstart: float = 0.0, flags: ShadedFlags = ShadedFlags.NONE) -> None: ...

@overload
def plot_shaded(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], yref: float = 0, flags: ShadedFlags = ShadedFlags.NONE) -> None: ...

@overload
def plot_shaded(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys1: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys2: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ShadedFlags = ShadedFlags.NONE) -> None: ...

@overload
def plot_stairs(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: StairsFlags = StairsFlags.NONE) -> None: ...

@overload
def plot_stairs(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: StairsFlags = StairsFlags.NONE) -> None: ...

@overload
def plot_stems(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ref: float = 0.0, scale: float = 1.0, start: float = 0.0, flags: StemsFlags = StemsFlags.NONE) -> None: ...

@overload
def plot_stems(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ref: float = 0.0, flags: StemsFlags = StemsFlags.NONE) -> None: ...

def plot_text(text: str, x: float, y: float, pix_offset: tuple[float, float] = (0,0), flags: TextFlag = TextFlag.NONE) -> None: ...

@overload
def plot_to_pixels(plt: tuple[float, float], x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

@overload
def plot_to_pixels(x: float, y: float, x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

def pop_colormap(count: int = 1) -> None: ...

def pop_plot_clip_rect() -> None: ...

def pop_style_color(count: int = 1) -> None: ...

def pop_style_var(count: int = 1) -> None: ...

@overload
def push_colormap(cmap: Colormap) -> None: ...

@overload
def push_colormap(name: str) -> None: ...

def push_plot_clip_rect(expand: float = 0) -> None: ...

@overload
def push_style_color(idx: Col, col: int) -> None: ...

@overload
def push_style_color(idx: Col, col: tuple[float, float, float, float]) -> None: ...

@overload
def push_style_var(idx: StyleVar, val: float) -> None: ...

@overload
def push_style_var(idx: StyleVar, val: int) -> None: ...

@overload
def push_style_var(idx: StyleVar, val: tuple[float, float]) -> None: ...

def sample_colormap(t: float, cmap: Colormap | int = AUTO) -> tuple[float, float, float, float]: ...

def set_axes(x_axis: Axis, y_axis: Axis) -> None: ...

def set_axis(axis: Axis) -> None: ...

def set_current_context_internal(arg: Context, /) -> None: ...

def set_next_axes_limits(x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond.ONCE) -> None: ...

def set_next_axes_to_fit() -> None: ...

def set_next_axis_limits(axis: Axis, v_min: float, v_max: float, cond: Cond = Cond.ONCE) -> None: ...

def set_next_axis_to_fit(axis: Axis) -> None: ...

def set_next_error_bar_style(col: tuple[float, float, float, float] = AUTO_COL, size: float = AUTO, weight: float = AUTO) -> None: ...

def set_next_fill_style(col: tuple[float, float, float, float] = AUTO_COL, alpha_mod: float = AUTO) -> None: ...

def set_next_line_style(col: tuple[float, float, float, float] = AUTO_COL, weight: float = AUTO) -> None: ...

def set_next_marker_style(marker: Marker | int = AUTO, size: float = AUTO, fill: tuple[float, float, float, float] = AUTO_COL, weight: float = AUTO, outline: tuple[float, float, float, float] = AUTO_COL) -> None: ...

def setup_axes(x_label: str | None, y_label: str | None, x_flags: AxisFlags = AxisFlags.NONE, y_flags: AxisFlags = AxisFlags.NONE) -> None: ...

def setup_axes_limits(x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond.ONCE) -> None: ...

def setup_axis(axis: Axis, label: str | None = None, flags: AxisFlags = AxisFlags.NONE) -> None: ...

def setup_axis_format(axis: Axis, fmt: str) -> None: ...

def setup_axis_limits(axis: Axis, v_min: float, v_max: float, cond: Cond = Cond.ONCE) -> None: ...

def setup_axis_limits_constraints(axis: Axis, v_min: float, v_max: float) -> None: ...

def setup_axis_scale(axis: Axis, scale: Scale) -> None: ...

@overload
def setup_axis_ticks(axis: int, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], labels: Sequence[str] | None = None, keep_default: bool = False) -> None: ...

@overload
def setup_axis_ticks(axis: int, v_min: float, v_max: float, n_ticks: int, labels: Sequence[str] | None = None, keep_default: bool = False) -> None: ...

def setup_axis_zoom_constraints(axis: Axis, z_min: float, z_max: float) -> None: ...

def setup_finish() -> None: ...

def setup_legend(location: Location, flags: LegendFlags = LegendFlags.NONE) -> None: ...

def setup_mouse_text(location: Location, flags: MouseTextFlags = MouseTextFlags.NONE) -> None: ...

def show_colormap_selector(label: str) -> bool: ...

def show_demo_window(closable: bool = False) -> bool: ...

def show_input_map_selector(label: str) -> bool: ...

def show_metrics_window(closable: bool = False) -> bool: ...

def show_style_editor(ref: Style | None = None) -> None: ...

def show_style_selector(label: str) -> bool: ...

def show_user_guide() -> None: ...

def style_colors_auto(dst: Style | None = None) -> None: ...

def style_colors_classic(dst: Style | None = None) -> None: ...

def style_colors_dark(dst: Style | None = None) -> None: ...

def style_colors_light(dst: Style | None = None) -> None: ...

@overload
def tag_x(x: float, col: tuple[float, float, float, float], round: bool = False) -> None: ...

@overload
def tag_x(x: float, col: tuple[float, float, float, float], text: str) -> None: ...

@overload
def tag_y(y: float, col: tuple[float, float, float, float], round: bool = False) -> None: ...

@overload
def tag_y(y: float, col: tuple[float, float, float, float], text: str) -> None: ...
