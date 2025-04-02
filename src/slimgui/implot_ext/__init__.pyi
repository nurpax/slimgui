from collections.abc import Sequence
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike


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
    pass

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

IMPLOT_AUTO: int = -1

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

def begin_plot(title_id: str, size: tuple[float, float] = (-1,0), flags: PlotFlags = PlotFlags.NONE) -> bool: ...

def create_context_internal() -> Context: ...

def destroy_context_internal(arg: Context, /) -> None: ...

def end_plot() -> None: ...

def get_colormap_size(cmap: Colormap | int = IMPLOT_AUTO) -> int: ...

def plot_bar_groups(label_ids: Sequence[str], values: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', device='cpu', writable=False)], group_size: float = 0.67, shift: float = 0.0, flags: BarGroupsFlags = BarGroupsFlags.NONE) -> None: ...

@overload
def plot_bars(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float = 0.67, shift: float = 0.0, flags: BarsFlags = BarFlags.NONE) -> None: ...

@overload
def plot_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float, flags: BarsFlags = BarFlags.NONE) -> None: ...

def plot_dummy(label_id: str, flags: DummyFlag = DummyFlag.NONE) -> None: ...

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

def plot_text(text: str, x: float, y: float, pix_offset: tuple[float, float] = (0,0), flags: TextFlag = TextFlag.NONE) -> None: ...

def set_current_context_internal(arg: Context, /) -> None: ...

def set_next_axes_limits(x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond.ONCE) -> None: ...

def set_next_axes_to_fit() -> None: ...

def set_next_axis_limits(axis: Axis, v_min: float, v_max: float, cond: Cond = Cond.ONCE) -> None: ...

def set_next_axis_to_fit(axis: Axis) -> None: ...

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

def show_demo_window(closable: bool = False) -> bool: ...
