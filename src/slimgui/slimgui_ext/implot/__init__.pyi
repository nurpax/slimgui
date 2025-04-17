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
    """ImPlot context (opaque struct, see implot_internal.h)"""

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
    """
    Input mapping structure. Default values listed. See also `implot.map_input_default()`, `implot.map_input_reverse()`.
    """

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
    """Plot style structure"""

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
def annotation(x: float, y: float, col: tuple[float, float, float, float], pix_offset: tuple[float, float], clamp: bool, round: bool = False) -> None:
    """
    Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.
    """

@overload
def annotation(x: float, y: float, col: tuple[float, float, float, float], pix_offset: tuple[float, float], clamp: bool, text: str) -> None: ...

def begin_aligned_plots(group_id: str, vertical: bool = True) -> bool:
    """
    Align axis padding over multiple plots in a single row or column. `group_id` must
    be unique. If this function returns `True`, `implot.end_aligned_plots()` must be called.
    """

def begin_drag_drop_source_axis(axis: Axis, flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool:
    """
    Turns the current plot's X-axis into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!
    """

def begin_drag_drop_source_item(label_id: str, flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool:
    """
    Turns an item in the current plot's legend into drag and drop source. Don't forget to call `implot.end_drag_drop_source()`!
    """

def begin_drag_drop_source_plot(flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE) -> bool:
    """
    Turns the current plot's plotting area into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!
    """

def begin_drag_drop_target_axis(axis: Axis) -> bool:
    """
    Turns the current plot's X-axis into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """

def begin_drag_drop_target_legend() -> bool:
    """
    Turns the current plot's legend into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """

def begin_drag_drop_target_plot() -> bool:
    """
    Turns the current plot's plotting area into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """

def begin_legend_popup(label_id: str, mouse_button: slimgui_ext.imgui.MouseButton = slimgui_ext.imgui.MouseButton.RIGHT) -> bool:
    """Begin a popup for a legend entry."""

def begin_plot(title_id: str, size: tuple[float, float] = (-1,0), flags: PlotFlags = PlotFlags.NONE) -> bool:
    """
    Starts a 2D plotting context. If this function returns `True`, `implot.end_plot()` MUST
    be called! You are encouraged to use the following convention:

    ```python
    if implot.begin_plot(...):
        implot.plot_line(...)
        ...
        implot.end_plot()
    ```

    Important notes:
    - `#title_id` must be unique to the current ImGui ID scope. If you need to avoid ID
      collisions or don't want to display a title in the plot, use double hashes
      (e.g. "MyPlot##HiddenIdText" or "##NoTitle").
    - #size is the **frame** size of the plot widget, not the plot area. The default
      size of plots (i.e. when `(0,0)`) can be modified in your `implot.Style`.
    """

def bust_color_cache(plot_title_id: str | None = None) -> None:
    """
    // When items in a plot sample their color from a colormap, the color is cached and does not change
    unless explicitly overriden. Therefore, if you change the colormap after the item has already been plotted,
    item colors will NOT update. If you need item colors to resample the new colormap, then use this
    function to bust the cached colors. If #plot_title_id is nullptr, then every item in EVERY existing plot
    will be cache busted. Otherwise only the plot specified by #plot_title_id will be busted. For the
    latter, this function must be called in the same ImGui ID scope that the plot is in. You should rarely if ever
    need this function, but it is available for applications that require runtime colormap swaps (e.g. Heatmaps demo).
    """

def cancel_plot_selection() -> None:
    """Cancels a the current plot box selection."""

def colormap_button(label: str, size: tuple[float, float] = (0,0), cmap: Colormap | int = AUTO) -> bool:
    """Shows a button with a colormap gradient brackground."""

def colormap_icon(cmap: Colormap) -> None:
    """
    Render icons similar to those that appear in legends (nifty for data lists).
    """

def colormap_scale(label: str, scale_min: float, scale_max: float, size: tuple[float, float] = (0,0), format: str = '%g', flags: ColormapScaleFlags = ColormapScaleFlags.NONE, cmap: Colormap | int = AUTO) -> None:
    """
    Shows a vertical color scale with linear spaced ticks using the specified color map. Use double hashes to hide label (e.g. "##NoLabel"). If `scale_min > scale_max`, the scale to color mapping will be reversed.
    """

def create_context_internal() -> Context: ...

def destroy_context_internal(arg: Context, /) -> None: ...

def end_aligned_plots() -> None:
    """
    Only call `implot.end_aligned_plots()` if `implot.begin_aligned_plots()` returns `True`!
    """

def end_drag_drop_source() -> None:
    """
    Ends a drag and drop source (currently just an alias for `imgui.end_drag_drop_source()`).
    """

def end_drag_drop_target() -> None:
    """
    Ends a drag and drop target (currently just an alias for `imgui.end_drag_drop_target()`).
    """

def end_legend_popup() -> None:
    """End a popup for a legend entry."""

def end_plot() -> None:
    """
    Only call `implot.end_plot()` if `implot.begin_plot()` returns `True`! Typically called at the end of an if statement conditioned on `implot.begin_plot()`. See example above.
    """

def get_colormap_color(idx: int, cmap: Colormap | int = AUTO) -> tuple[float, float, float, float]:
    """
    Returns a color from a colormap given an index >= 0 (modulo will be performed).
    """

def get_colormap_count() -> int:
    """
    Returns the number of available colormaps (i.e. the built-in + user-added count).
    """

def get_colormap_index(name: str) -> int:
    """
    Returns an index number for a colormap given a valid string name. Returns -1 if name is invalid.
    """

def get_colormap_name(cmap: Colormap) -> str:
    """
    Returns a string name for a colormap given an index. Returns `None` if index is invalid.
    """

def get_colormap_size(cmap: Colormap | int = AUTO) -> int:
    """Returns the size of a colormap."""

def get_last_item_color() -> tuple[float, float, float, float]:
    """Gets the last item primary color (i.e. its legend icon color)"""

def get_marker_name(idx: Marker) -> str:
    """Returns the string name for an ImPlotMarker."""

def get_plot_mouse_pos(x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]:
    """
    Returns the mouse position in x,y coordinates of the current plot. Passing `implot.AUTO` uses the current axes.
    """

def get_plot_pos() -> tuple[float, float]:
    """Get the current Plot position (top-left) in pixels."""

def get_plot_size() -> tuple[float, float]:
    """Get the curent Plot size in pixels."""

def get_style_color_name(idx: Col) -> str:
    """Returns the string name for an `implot.Col`."""

def hide_next_item(hidden: bool = True, cond: Cond = Cond.ONCE) -> None:
    """
    Hides or shows the next plot item (i.e. as if it were toggled from the legend).

    Use `Cond.ALWAYS` if you need to forcefully set this every frame.
    """

def is_axis_hovered(axis: Axis) -> bool:
    """Returns `True` if the axis label area in the current plot is hovered."""

def is_legend_entry_hovered(label_id: str) -> bool:
    """Returns `True` if a plot item legend entry is hovered."""

def is_plot_hovered() -> bool:
    """Returns `True` if the plot area in the current plot is hovered."""

def is_plot_selected() -> bool:
    """Returns `True` if the current plot is being box selected."""

def is_subplots_hovered() -> bool:
    """Returns `True` if the bounding frame of a subplot is hovered."""

@overload
def item_icon(col: tuple[float, float, float, float]) -> None:
    """
    Render icons similar to those that appear in legends (nifty for data lists).
    """

@overload
def item_icon(col: int) -> None: ...

def map_input_default(dst: InputMap | None = None) -> None:
    """
    Default input mapping: pan = LMB drag, box select = RMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll.
    """

def map_input_reverse(dst: InputMap | None = None) -> None:
    """
    Reverse input mapping: pan = RMB drag, box select = LMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll.
    """

def next_colormap_color() -> tuple[float, float, float, float]:
    """
    Returns the next color from the current colormap and advances the colormap for the current plot.

    Can also be used with no return value to skip colors if desired. You need to call this between `implot.begin_plot()`/`implot.end_plot()`!
    """

@overload
def pixels_to_plot(pix: tuple[float, float], x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]:
    """
    Convert pixels to a position in the current plot's coordinate system. Passing `implot.AUTO` uses the current axes.
    """

@overload
def pixels_to_plot(x: float, y: float, x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

def plot_bar_groups(label_ids: Sequence[str], values: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', device='cpu', writable=False)], group_size: float = 0.67, shift: float = 0.0, flags: BarGroupsFlags = BarGroupsFlags.NONE) -> None:
    """
    Plots a group of bars. `values` is a matrix with a shape `(item_count, group_count)`. `label_ids` should have `item_count` elements.
    """

@overload
def plot_bars(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float = 0.67, shift: float = 0.0, flags: BarsFlags = BarFlags.NONE) -> None:
    """
    Plots a bar graph. Vertical by default. `bar_size` and `shift` are in plot units.
    """

@overload
def plot_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float, flags: BarsFlags = BarFlags.NONE) -> None: ...

def plot_digital(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: DigitalFlags = DigitalFlags.NONE) -> None:
    """
    Plots digital data. Digital plots do not respond to y drag or zoom, and are always referenced to the bottom of the plot.
    """

def plot_dummy(label_id: str, flags: DummyFlag = DummyFlag.NONE) -> None:
    """Plots a dummy item (i.e. adds a legend entry colored by `Col.LINE`)."""

@overload
def plot_error_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], err: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ErrorBarsFlags = ErrorBarsFlags.NONE) -> None:
    """
    Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.
    """

@overload
def plot_error_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], neg: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], pos: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ErrorBarsFlags = ErrorBarsFlags.NONE) -> None: ...

def plot_heatmap(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', device='cpu', writable=False)], scale_min: float = 0, scale_max: float = 0.0, label_fmt: str | None = '%.1f', bounds_min: tuple[float, float] = (0.0, 0.0), bounds_max: tuple[float, float] = (1.0, 1.0), flags: HeatmapFlags = HeatmapFlags.NONE) -> None:
    """
    Plots a 2D heatmap chart. `values` is expected to have shape (rows, cols). Leave `scale_min` and `scale_max` both at 0 for automatic color scaling, or set them to a predefined range. `label_fmt` can be set to `None` for no labels.
    """

def plot_image(label_id: str, user_texture_id: int, bounds_min: tuple[float, float], bounds_max: tuple[float, float], uv0: tuple[float, float] = (0,0), uv1: tuple[float, float] = (1,1), tint_col: tuple[float, float, float, float] = (1,1,1,1), flags: ImageFlag = ImageFlag.NONE) -> None:
    """
    Plots an axis-aligned image. `bounds_min`/`bounds_max` are in plot coordinates (y-up) and `uv0`/`uv1` are in texture coordinates (y-down).
    """

def plot_inf_lines(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: InfLinesFlags = InfLinesFlags.NONE) -> None:
    """
    Plots infinite vertical or horizontal lines (e.g. for references or asymptotes).
    """

@overload
def plot_line(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: LineFlags = LineFlags.NONE) -> None:
    """
    Plots a standard 2D line plot. The x values are spaced evenly along the x axis, starting at `xstart` and spaced by `xscale`. The y values are taken from the `values` array.
    """

@overload
def plot_line(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: LineFlags = LineFlags.NONE) -> None:
    """
    Plots a standard 2D line plot. The x values are taken from the `xs` array, and the y values are taken from the `ys` array.
    """

@overload
def plot_scatter(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: ScatterFlags = ScatterFlags.NONE) -> None:
    """Plots a standard 2D scatter plot. Default marker is `Marker.CIRCLE`."""

@overload
def plot_scatter(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ScatterFlags = ScatterFlags.NONE) -> None: ...

@overload
def plot_shaded(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], yref: float = 0, xscale: float = 1.0, xstart: float = 0.0, flags: ShadedFlags = ShadedFlags.NONE) -> None:
    """
    Plots a shaded (filled) region between two lines, or a line and a horizontal reference. Set `yref` to +/-INFINITY for infinite fill extents.
    """

@overload
def plot_shaded(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], yref: float = 0, flags: ShadedFlags = ShadedFlags.NONE) -> None: ...

@overload
def plot_shaded(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys1: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys2: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: ShadedFlags = ShadedFlags.NONE) -> None: ...

@overload
def plot_stairs(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], xscale: float = 1.0, xstart: float = 0.0, flags: StairsFlags = StairsFlags.NONE) -> None:
    """
    Plots a stairstep graph. The y value is continued constantly to the right from every x position, i.e. the interval `[x[i], x[i+1])` has the value `y[i]`
    """

@overload
def plot_stairs(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], flags: StairsFlags = StairsFlags.NONE) -> None: ...

@overload
def plot_stems(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ref: float = 0.0, scale: float = 1.0, start: float = 0.0, flags: StemsFlags = StemsFlags.NONE) -> None: ...

@overload
def plot_stems(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ref: float = 0.0, flags: StemsFlags = StemsFlags.NONE) -> None:
    """Plots stems. Vertical by default."""

def plot_text(text: str, x: float, y: float, pix_offset: tuple[float, float] = (0,0), flags: TextFlag = TextFlag.NONE) -> None:
    """
    Plots a centered text label at point x,y with an optional pixel offset. Text color can be changed with `implot.push_style_color(Col.INLAY_TEXT, ...)`.
    """

@overload
def plot_to_pixels(plt: tuple[float, float], x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]:
    """
    Convert a position in the current plot's coordinate system to pixels. Passing `implot.AUTO` uses the current axes.
    """

@overload
def plot_to_pixels(x: float, y: float, x_axis: Axis | int = AUTO, y_axis: Axis | int = AUTO) -> tuple[float, float]: ...

def pop_colormap(count: int = 1) -> None:
    """
    Undo temporary colormap modification(s). Undo multiple pushes at once by increasing count.
    """

def pop_plot_clip_rect() -> None:
    """
    Pop plot clip rect. Call between `implot.begin_plot()`/`implot.end_plot()`.
    """

def pop_style_color(count: int = 1) -> None:
    """
    Undo temporary style color modification(s). Undo multiple pushes at once by increasing count.
    """

def pop_style_var(count: int = 1) -> None:
    """
    Undo temporary style variable modification(s). Undo multiple pushes at once by increasing count.
    """

@overload
def push_colormap(cmap: Colormap) -> None:
    """
    Temporarily switch to one of the built-in (i.e. ImPlotColormap_XXX) or user-added colormaps (i.e. a return value of `implot.add_colormap()`). Don't forget to call `implot.pop_colormap()`!
    """

@overload
def push_colormap(name: str) -> None:
    """
    Push a colormap by string name. Use built-in names such as "Default", "Deep", "Jet", etc. or a string you provided to `implot.add_colormap(). Don't forget to call `implot.pop_colormap()`!
    """

def push_plot_clip_rect(expand: float = 0) -> None:
    """
    Push clip rect for rendering to current plot area. The rect can be expanded or contracted by #expand pixels. Call between `implot.begin_plot()`/`implot.end_plot()`.
    """

@overload
def push_style_color(idx: Col, col: int) -> None:
    """
    Temporarily modify a style color. Don't forget to call `implot.pop_style_color()`!
    """

@overload
def push_style_color(idx: Col, col: tuple[float, float, float, float]) -> None: ...

@overload
def push_style_var(idx: StyleVar, val: float) -> None:
    """
    Temporarily modify a style variable of float type. Don't forget to call `implot.pop_style_var()`!
    """

@overload
def push_style_var(idx: StyleVar, val: int) -> None:
    """
    Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!
    """

@overload
def push_style_var(idx: StyleVar, val: tuple[float, float]) -> None:
    """
    Temporarily modify a style variable of float 2-tuple. Don't forget to call `implot.pop_style_var()`!
    """

def sample_colormap(t: float, cmap: Colormap | int = AUTO) -> tuple[float, float, float, float]:
    """Sample a color from the current colormap given t between 0 and 1."""

def set_axes(x_axis: Axis, y_axis: Axis) -> None:
    """Select which axis/axes will be used for subsequent plot elements."""

def set_axis(axis: Axis) -> None:
    """Select which axis/axes will be used for subsequent plot elements."""

def set_current_context_internal(arg: Context, /) -> None: ...

def set_next_axes_limits(x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond.ONCE) -> None:
    """
    Sets the upcoming primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`).
    """

def set_next_axes_to_fit() -> None:
    """Sets all upcoming axes to auto fit to their data."""

def set_next_axis_limits(axis: Axis, v_min: float, v_max: float, cond: Cond = Cond.ONCE) -> None:
    """
    Sets an upcoming axis range limits. If ImPlotCond_Always is used, the axes limits will be locked.
    """

def set_next_axis_to_fit(axis: Axis) -> None:
    """Set an upcoming axis to auto fit to its data."""

def set_next_error_bar_style(col: tuple[float, float, float, float] = AUTO_COL, size: float = AUTO, weight: float = AUTO) -> None:
    """Set the error bar style for the next item only."""

def set_next_fill_style(col: tuple[float, float, float, float] = AUTO_COL, alpha_mod: float = AUTO) -> None:
    """Set the fill color for the next item only."""

def set_next_line_style(col: tuple[float, float, float, float] = AUTO_COL, weight: float = AUTO) -> None:
    """Set the line color and weight for the next item only."""

def set_next_marker_style(marker: Marker | int = AUTO, size: float = AUTO, fill: tuple[float, float, float, float] = AUTO_COL, weight: float = AUTO, outline: tuple[float, float, float, float] = AUTO_COL) -> None:
    """Set the marker style for the next item only."""

def setup_axes(x_label: str | None, y_label: str | None, x_flags: AxisFlags = AxisFlags.NONE, y_flags: AxisFlags = AxisFlags.NONE) -> None:
    """
    Sets the label and/or flags for primary X and Y axes (shorthand for two calls to `implot.setup_Axis()`).
    """

def setup_axes_limits(x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond.ONCE) -> None:
    """
    Sets the primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`).
    """

def setup_axis(axis: Axis, label: str | None = None, flags: AxisFlags = AxisFlags.NONE) -> None:
    """
    Enables an axis or sets the label and/or flags for an existing axis. Leave `label=None` for no label.
    """

def setup_axis_format(axis: Axis, fmt: str) -> None:
    """
    Sets the format of numeric axis labels via formater specifier (default="%g"). Formated values will be double (i.e. use %f).  Note that the format string is specified in C printf syntax!
    """

def setup_axis_limits(axis: Axis, v_min: float, v_max: float, cond: Cond = Cond.ONCE) -> None:
    """
    Sets an axis range limits. If `Cond.ALWAYS` is used, the axes limits will be locked. Inversion with `v_min > v_max` is not supported; use `implot.setup_axis_limits` instead.
    """

def setup_axis_limits_constraints(axis: Axis, v_min: float, v_max: float) -> None:
    """Sets an axis' limits constraints."""

def setup_axis_scale(axis: Axis, scale: Scale) -> None:
    """Sets an axis' scale using built-in options."""

@overload
def setup_axis_ticks(axis: int, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], labels: Sequence[str] | None = None, keep_default: bool = False) -> None:
    """
    Sets an axis' ticks and optionally the labels. To keep the default ticks, set `keep_default=True`.
    """

@overload
def setup_axis_ticks(axis: int, v_min: float, v_max: float, n_ticks: int, labels: Sequence[str] | None = None, keep_default: bool = False) -> None: ...

def setup_axis_zoom_constraints(axis: Axis, z_min: float, z_max: float) -> None:
    """Sets an axis' zoom constraints."""

def setup_finish() -> None:
    """
    Explicitly finalize plot setup. Once you call this, you cannot make anymore Setup calls for the current plot!

    Note that calling this function is OPTIONAL; it will be called by the first subsequent setup-locking API call.
    """

def setup_legend(location: Location, flags: LegendFlags = LegendFlags.NONE) -> None:
    """
    Sets up the plot legend. This can also be called immediately after `implot.begin_subplots()` when using `SubplotFlags.SHARE_ITEMS`.
    """

def setup_mouse_text(location: Location, flags: MouseTextFlags = MouseTextFlags.NONE) -> None:
    """
    Set the location of the current plot's mouse position text (default = South|East).
    """

def show_colormap_selector(label: str) -> bool:
    """Shows ImPlot colormap selector dropdown menu."""

def show_demo_window(closable: bool = False) -> bool:
    """Shows the ImPlot demo window."""

def show_input_map_selector(label: str) -> bool:
    """Shows ImPlot input map selector dropdown menu."""

def show_metrics_window(closable: bool = False) -> bool:
    """Shows ImPlot metrics/debug information window."""

def show_style_editor(ref: Style | None = None) -> None:
    """Shows ImPlot style editor block (not a window)."""

def show_style_selector(label: str) -> bool:
    """Shows ImPlot style selector dropdown menu."""

def show_user_guide() -> None:
    """Add basic help/info block for end users (not a window)."""

def style_colors_auto(dst: Style | None = None) -> None:
    """Style plot colors for current ImGui style (default)."""

def style_colors_classic(dst: Style | None = None) -> None:
    """Style plot colors for ImGui "Classic"."""

def style_colors_dark(dst: Style | None = None) -> None:
    """Style plot colors for ImGui "Dark"."""

def style_colors_light(dst: Style | None = None) -> None:
    """Style plot colors for ImGui "Light"."""

@overload
def tag_x(x: float, col: tuple[float, float, float, float], round: bool = False) -> None:
    """Shows a x-axis tag at the specified coordinate value."""

@overload
def tag_x(x: float, col: tuple[float, float, float, float], text: str) -> None: ...

@overload
def tag_y(y: float, col: tuple[float, float, float, float], round: bool = False) -> None:
    """Shows a y-axis tag at the specified coordinate value."""

@overload
def tag_y(y: float, col: tuple[float, float, float, float], text: str) -> None: ...
