from collections.abc import Iterator, Sequence
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike

import slimgui_ext


AUTO: int = -1

AUTO_COL: tuple = (0.0, 0.0, 0.0, -1.0)

class Axis(enum.IntEnum):
    X1 = 0
    """Enabled by default"""

    X2 = 1
    """Disabled by default"""

    X3 = 2
    """Disabled by default"""

    Y1 = 3
    """Enabled by default"""

    Y2 = 4
    """Disabled by default"""

    Y3 = 5
    """Disabled by default"""

    COUNT = 6

class AxisFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_LABEL = 1
    """
    The axis label will not be displayed (axis labels are also hidden if the supplied string name is nullptr)
    """

    NO_GRID_LINES = 2
    """No grid lines will be displayed"""

    NO_TICK_MARKS = 4
    """No tick marks will be displayed"""

    NO_TICK_LABELS = 8
    """No text labels will be displayed"""

    NO_INITIAL_FIT = 16
    """
    Axis will not be initially fit to data extents on the first rendered frame
    """

    NO_MENUS = 32
    """The user will not be able to open context menus with right-click"""

    NO_SIDE_SWITCH = 64
    """The user will not be able to switch the axis side by dragging it"""

    NO_HIGHLIGHT = 128
    """The axis will not have its background highlighted when hovered or held"""

    OPPOSITE = 256
    """
    Axis ticks and labels will be rendered on the conventionally opposite side (i.e, right or top)
    """

    FOREGROUND = 512
    """
    Grid lines will be displayed in the foreground (i.e. on top of data) instead of the background
    """

    INVERT = 1024
    """The axis will be inverted"""

    AUTO_FIT = 2048
    """Axis will be auto-fitting to data extents"""

    RANGE_FIT = 4096
    """
    Axis will only fit points if the point is in the visible range of the **orthogonal** axis
    """

    PAN_STRETCH = 8192
    """
    Panning in a locked or constrained state will cause the axis to stretch if possible
    """

    LOCK_MIN = 16384
    """The axis minimum value will be locked when panning/zooming"""

    LOCK_MAX = 32768
    """The axis maximum value will be locked when panning/zooming"""

    LOCK = 49152

    NO_DECORATIONS = 15

    AUX_DEFAULT = 258

class BarGroupsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """Bar groups will be rendered horizontally on the current y-axis"""

    STACKED = 2048
    """Items in a group will be stacked on top of each other"""

class BarsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """Bars will be rendered horizontally on the current y-axis"""

class Bin(enum.IntEnum):
    SQRT = -1
    """K = sqrt(n)"""

    STURGES = -2
    """K = 1 + log2(n)"""

    RICE = -3
    """K = 2 * cbrt(n)"""

    SCOTT = -4
    """W = 3.49 * sigma / cbrt(n)"""

class Col(enum.IntEnum):
    LINE = 0
    """
    Plot line/outline color (defaults to next unused color in current colormap)
    """

    FILL = 1
    """Plot fill color for bars (defaults to the current line color)"""

    MARKER_OUTLINE = 2
    """Marker outline color (defaults to the current line color)"""

    MARKER_FILL = 3
    """Marker fill color (defaults to the current line color)"""

    ERROR_BAR = 4
    """Error bar color (defaults to `Col.TEXT`)"""

    FRAME_BG = 5
    """Plot frame background color (defaults to `Col.FRAME_BG`)"""

    PLOT_BG = 6
    """Plot area background color (defaults to `Col.WINDOW_BG`)"""

    PLOT_BORDER = 7
    """Plot area border color (defaults to `Col.BORDER`)"""

    LEGEND_BG = 8
    """Legend background color (defaults to `Col.POPUP_BG`)"""

    LEGEND_BORDER = 9
    """Legend border color (defaults to `Col.PLOT_BORDER`)"""

    LEGEND_TEXT = 10
    """Legend text color (defaults to `Col.INLAY_TEXT`)"""

    TITLE_TEXT = 11
    """Plot title text color (defaults to `Col.TEXT`)"""

    INLAY_TEXT = 12
    """Color of text appearing inside of plots (defaults to `Col.TEXT`)"""

    AXIS_TEXT = 13
    """Axis label and tick lables color (defaults to `Col.TEXT`)"""

    AXIS_GRID = 14
    """Axis grid color (defaults to 25% `Col.AXIS_TEXT`)"""

    AXIS_TICK = 15
    """Axis tick color (defaults to AxisGrid)"""

    AXIS_BG = 16
    """Background color of axis hover region (defaults to transparent)"""

    AXIS_BG_HOVERED = 17
    """Axis hover color (defaults to `Col.BUTTON_HOVERED`)"""

    AXIS_BG_ACTIVE = 18
    """Axis active color (defaults to `Col.BUTTON_ACTIVE`)"""

    SELECTION = 19
    """Box-selection color (defaults to yellow)"""

    CROSSHAIRS = 20
    """Crosshairs color (defaults to `Col.PLOT_BORDER`)"""

    COUNT = 21

class Colormap(enum.IntEnum):
    DEEP = 0
    """A.k.a. seaborn deep             (qual=true,  n=10) (default)"""

    DARK = 1
    """A.k.a. matplotlib "Set1"        (qual=true,  n=9 )"""

    PASTEL = 2
    """A.k.a. matplotlib "Pastel1"     (qual=true,  n=9 )"""

    PAIRED = 3
    """A.k.a. matplotlib "Paired"      (qual=true,  n=12)"""

    VIRIDIS = 4
    """A.k.a. matplotlib "viridis"     (qual=false, n=11)"""

    PLASMA = 5
    """A.k.a. matplotlib "plasma"      (qual=false, n=11)"""

    HOT = 6
    """A.k.a. matplotlib/MATLAB "hot"  (qual=false, n=11)"""

    COOL = 7
    """A.k.a. matplotlib/MATLAB "cool" (qual=false, n=11)"""

    PINK = 8
    """A.k.a. matplotlib/MATLAB "pink" (qual=false, n=11)"""

    JET = 9
    """A.k.a. MATLAB "jet"             (qual=false, n=11)"""

    TWILIGHT = 10
    """A.k.a. matplotlib "twilight"    (qual=false, n=11)"""

    RD_BU = 11
    """Red/blue, Color Brewer          (qual=false, n=11)"""

    BR_BG = 12
    """Brown/blue-green, Color Brewer  (qual=false, n=11)"""

    PI_YG = 13
    """Pink/yellow-green, Color Brewer (qual=false, n=11)"""

    SPECTRAL = 14
    """Color spectrum, Color Brewer    (qual=false, n=11)"""

    GREYS = 15
    """White/black                     (qual=false, n=2 )"""

class ColormapScaleFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_LABEL = 1
    """The colormap axis label will not be displayed"""

    OPPOSITE = 2
    """Render the colormap label and tick labels on the opposite side"""

    INVERT = 4
    """
    Invert the colormap bar and axis scale (this only affects rendering; if you only want to reverse the scale mapping, make scale_min > scale_max)
    """

class ColorsArray:
    def __getitem__(self, arg: Col, /) -> tuple[float, float, float, float]: ...

    def __setitem__(self, arg0: Col, arg1: tuple[float, float, float, float], /) -> None: ...

    def __iter__(self) -> Iterator[tuple[float, float, float, float]]: ...

    def __len__(self) -> int: ...

class Cond(enum.IntEnum):
    NONE = 0
    """No condition (always set the variable), same as _Always"""

    ALWAYS = 1
    """No condition (always set the variable)"""

    ONCE = 2
    """
    Set the variable once per runtime session (only the first call will succeed)
    """

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
    """Default"""

class DragToolFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_CURSORS = 1
    """Drag tools won't change cursor icons when hovered or held"""

    NO_FIT = 2
    """The drag tool won't be considered for plot fits"""

    NO_INPUTS = 4
    """Lock the tool from user inputs"""

    DELAYED = 8
    """
    Tool rendering will be delayed one frame; useful when applying position-constraints
    """

class DummyFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

class ErrorBarsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """Error bars will be rendered horizontally on the current y-axis"""

class HeatmapFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    COL_MAJOR = 1024
    """Data will be read in column major order"""

class HistogramFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """
    Histogram bars will be rendered horizontally (not supported by PlotHistogram2D)
    """

    CUMULATIVE = 2048
    """
    Each bin will contain its count plus the counts of all previous bins (not supported by PlotHistogram2D)
    """

    DENSITY = 4096
    """
    Counts will be normalized, i.e. the PDF will be visualized, or the CDF will be visualized if Cumulative is also set
    """

    NO_OUTLIERS = 8192
    """
    Exclude values outside the specifed histogram range from the count toward normalizing and cumulative counts
    """

    COL_MAJOR = 16384
    """
    Data will be read in column major order (not supported by `plot_histogram`)
    """

class ImageFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

class InfLinesFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """Lines will be rendered horizontally on the current y-axis"""

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
    """The item won't have a legend entry displayed"""

    NO_FIT = 2
    """The item won't be considered for plot fits"""

class LegendFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_BUTTONS = 1
    """Legend icons will not function as hide/show buttons"""

    NO_HIGHLIGHT_ITEM = 2
    """Plot items will not be highlighted when their legend entry is hovered"""

    NO_HIGHLIGHT_AXIS = 4
    """
    Axes will not be highlighted when legend entries are hovered (only relevant if x/y-axis count > 1)
    """

    NO_MENUS = 8
    """The user will not be able to open context menus with right-click"""

    OUTSIDE = 16
    """Legend will be rendered outside of the plot area"""

    HORIZONTAL = 32
    """Legend entries will be displayed horizontally"""

    SORT = 64
    """Legend entries will be displayed in alphabetical order"""

class LineFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    SEGMENTS = 1024
    """A line segment will be rendered from every two consecutive points"""

    LOOP = 2048
    """The last and first point will be connected to form a closed loop"""

    SKIP_NA_N = 4096
    """NaNs values will be skipped instead of rendered as missing data"""

    NO_CLIP = 8192
    """Markers (if displayed) on the edge of a plot will not be clipped"""

    SHADED = 16384
    """
    A filled region between the line and horizontal origin will be rendered; use PlotShaded for more advanced cases
    """

class Location(enum.IntEnum):
    CENTER = 0
    """Center-center"""

    NORTH = 1
    """Top-center"""

    SOUTH = 2
    """Bottom-center"""

    WEST = 4
    """Center-left"""

    EAST = 8
    """Center-right"""

    NORTH_WEST = 5
    """Top-left"""

    NORTH_EAST = 9
    """Top-right"""

    SOUTH_WEST = 6
    """Bottom-left"""

    SOUTH_EAST = 10
    """Bottom-right"""

class Marker(enum.IntEnum):
    NONE = -1
    """No marker"""

    CIRCLE = 0
    """A circle marker (default)"""

    SQUARE = 1
    """A square maker"""

    DIAMOND = 2
    """A diamond marker"""

    UP = 3
    """An upward-pointing triangle marker"""

    DOWN = 4
    """An downward-pointing triangle marker"""

    LEFT = 5
    """An leftward-pointing triangle marker"""

    RIGHT = 6
    """An rightward-pointing triangle marker"""

    CROSS = 7
    """A cross marker (not fillable)"""

    PLUS = 8
    """A plus marker (not fillable)"""

    ASTERISK = 9
    """A asterisk marker (not fillable)"""

    COUNT = 10

class MouseTextFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_AUX_AXES = 1
    """Only show the mouse position for primary axes"""

    NO_FORMAT = 2
    """Axes label formatters won't be used to render text"""

    SHOW_ALWAYS = 4
    """Always display mouse position even if plot not hovered"""

class PieChartFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NORMALIZE = 1024
    """
    Force normalization of pie chart values (i.e. always make a full circle if sum < 0)
    """

    IGNORE_HIDDEN = 2048
    """
    Ignore hidden slices when drawing the pie chart (as if they were not there)
    """

    EXPLODING = 4096
    """Explode legend-hovered slice"""

class PlotFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_TITLE = 1
    """
    The plot title will not be displayed (titles are also hidden if preceeded by double hashes, e.g. "##MyPlot")
    """

    NO_LEGEND = 2
    """The legend will not be displayed"""

    NO_MOUSE_TEXT = 4
    """
    The mouse position, in plot coordinates, will not be displayed inside of the plot
    """

    NO_INPUTS = 8
    """The user will not be able to interact with the plot"""

    NO_MENUS = 16
    """The user will not be able to open context menus"""

    NO_BOX_SELECT = 32
    """The user will not be able to box-select"""

    NO_FRAME = 64
    """The ImGui frame will not be rendered"""

    EQUAL = 128
    """X and y axes pairs will be constrained to have the same units/pixel"""

    CROSSHAIRS = 256
    """
    The default mouse cursor will be replaced with a crosshair when hovered
    """

    CANVAS_ONLY = 55

class Scale(enum.IntEnum):
    LINEAR = 0
    """Default linear scale"""

    TIME = 1
    """Date/time scale"""

    LOG10 = 2
    """Base 10 logartithmic scale"""

    SYM_LOG = 3
    """Symmetric log scale"""

class ScatterFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_CLIP = 1024
    """Markers on the edge of a plot will not be clipped"""

class ShadedFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

class StairsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    PRE_STEP = 1024
    """
    The y value is continued constantly to the left from every x position, i.e. the interval (x[i-1], x[i]] has the value y[i]
    """

    SHADED = 2048
    """
    A filled region between the stairs and horizontal origin will be rendered; use PlotShaded for more advanced cases
    """

class StemsFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    HORIZONTAL = 1024
    """Stems will be rendered horizontally on the current y-axis"""

class Style:
    """Plot style structure"""

    @property
    def line_weight(self) -> float: ...

    @line_weight.setter
    def line_weight(self, arg: float, /) -> None: ...

    @property
    def marker(self) -> int: ...

    @marker.setter
    def marker(self, arg: int, /) -> None: ...

    @property
    def marker_size(self) -> float: ...

    @marker_size.setter
    def marker_size(self, arg: float, /) -> None: ...

    @property
    def marker_weight(self) -> float: ...

    @marker_weight.setter
    def marker_weight(self, arg: float, /) -> None: ...

    @property
    def fill_alpha(self) -> float: ...

    @fill_alpha.setter
    def fill_alpha(self, arg: float, /) -> None: ...

    @property
    def error_bar_size(self) -> float: ...

    @error_bar_size.setter
    def error_bar_size(self, arg: float, /) -> None: ...

    @property
    def error_bar_weight(self) -> float: ...

    @error_bar_weight.setter
    def error_bar_weight(self, arg: float, /) -> None: ...

    @property
    def digital_bit_height(self) -> float: ...

    @digital_bit_height.setter
    def digital_bit_height(self, arg: float, /) -> None: ...

    @property
    def digital_bit_gap(self) -> float: ...

    @digital_bit_gap.setter
    def digital_bit_gap(self, arg: float, /) -> None: ...

    @property
    def plot_border_size(self) -> float: ...

    @plot_border_size.setter
    def plot_border_size(self, arg: float, /) -> None: ...

    @property
    def minor_alpha(self) -> float: ...

    @minor_alpha.setter
    def minor_alpha(self, arg: float, /) -> None: ...

    @property
    def major_tick_len(self) -> tuple[float, float]: ...

    @major_tick_len.setter
    def major_tick_len(self, arg: tuple[float, float], /) -> None: ...

    @property
    def minor_tick_len(self) -> tuple[float, float]: ...

    @minor_tick_len.setter
    def minor_tick_len(self, arg: tuple[float, float], /) -> None: ...

    @property
    def major_tick_size(self) -> tuple[float, float]: ...

    @major_tick_size.setter
    def major_tick_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def minor_tick_size(self) -> tuple[float, float]: ...

    @minor_tick_size.setter
    def minor_tick_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def major_grid_size(self) -> tuple[float, float]: ...

    @major_grid_size.setter
    def major_grid_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def minor_grid_size(self) -> tuple[float, float]: ...

    @minor_grid_size.setter
    def minor_grid_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def plot_padding(self) -> tuple[float, float]: ...

    @plot_padding.setter
    def plot_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def label_padding(self) -> tuple[float, float]: ...

    @label_padding.setter
    def label_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def legend_padding(self) -> tuple[float, float]: ...

    @legend_padding.setter
    def legend_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def legend_inner_padding(self) -> tuple[float, float]: ...

    @legend_inner_padding.setter
    def legend_inner_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def legend_spacing(self) -> tuple[float, float]: ...

    @legend_spacing.setter
    def legend_spacing(self, arg: tuple[float, float], /) -> None: ...

    @property
    def mouse_pos_padding(self) -> tuple[float, float]: ...

    @mouse_pos_padding.setter
    def mouse_pos_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def annotation_padding(self) -> tuple[float, float]: ...

    @annotation_padding.setter
    def annotation_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def fit_padding(self) -> tuple[float, float]: ...

    @fit_padding.setter
    def fit_padding(self, arg: tuple[float, float], /) -> None: ...

    @property
    def plot_default_size(self) -> tuple[float, float]: ...

    @plot_default_size.setter
    def plot_default_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def plot_min_size(self) -> tuple[float, float]: ...

    @plot_min_size.setter
    def plot_min_size(self, arg: tuple[float, float], /) -> None: ...

    @property
    def colors(self) -> ColorsArray: ...

    @property
    def colormap(self) -> int: ...

    @colormap.setter
    def colormap(self, arg: int, /) -> None: ...

    @property
    def use_local_time(self) -> bool: ...

    @use_local_time.setter
    def use_local_time(self, arg: bool, /) -> None: ...

    @property
    def use_iso8601(self) -> bool: ...

    @use_iso8601.setter
    def use_iso8601(self, arg: bool, /) -> None: ...

    @property
    def use_24hour_clock(self) -> bool: ...

    @use_24hour_clock.setter
    def use_24hour_clock(self, arg: bool, /) -> None: ...

class StyleVar(enum.IntEnum):
    LINE_WEIGHT = 0
    """Float,  plot item line weight in pixels"""

    MARKER = 1
    """Int,    marker specification"""

    MARKER_SIZE = 2
    """Float,  marker size in pixels (roughly the marker's "radius")"""

    MARKER_WEIGHT = 3
    """Float,  plot outline weight of markers in pixels"""

    FILL_ALPHA = 4
    """Float,  alpha modifier applied to all plot item fills"""

    ERROR_BAR_SIZE = 5
    """Float,  error bar whisker width in pixels"""

    ERROR_BAR_WEIGHT = 6
    """Float,  error bar whisker weight in pixels"""

    DIGITAL_BIT_HEIGHT = 7
    """Float,  digital channels bit height (at 1) in pixels"""

    DIGITAL_BIT_GAP = 8
    """Float,  digital channels bit padding gap in pixels"""

    PLOT_BORDER_SIZE = 9
    """Float,  thickness of border around plot area"""

    MINOR_ALPHA = 10
    """Float,  alpha multiplier applied to minor axis grid lines"""

    MAJOR_TICK_LEN = 11
    """ImVec2, major tick lengths for X and Y axes"""

    MINOR_TICK_LEN = 12
    """ImVec2, minor tick lengths for X and Y axes"""

    MAJOR_TICK_SIZE = 13
    """ImVec2, line thickness of major ticks"""

    MINOR_TICK_SIZE = 14
    """ImVec2, line thickness of minor ticks"""

    MAJOR_GRID_SIZE = 15
    """ImVec2, line thickness of major grid lines"""

    MINOR_GRID_SIZE = 16
    """ImVec2, line thickness of minor grid lines"""

    PLOT_PADDING = 17
    """
    ImVec2, padding between widget frame and plot area, labels, or outside legends (i.e. main padding)
    """

    LABEL_PADDING = 18
    """ImVec2, padding between axes labels, tick labels, and plot edge"""

    LEGEND_PADDING = 19
    """ImVec2, legend padding from plot edges"""

    LEGEND_INNER_PADDING = 20
    """ImVec2, legend inner padding from legend edges"""

    LEGEND_SPACING = 21
    """ImVec2, spacing between legend entries"""

    MOUSE_POS_PADDING = 22
    """ImVec2, padding between plot edge and interior info text"""

    ANNOTATION_PADDING = 23
    """ImVec2, text padding around annotation labels"""

    FIT_PADDING = 24
    """
    ImVec2, additional fit padding as a percentage of the fit extents (e.g. ImVec2(0.1f,0.1f) adds 10% to the fit extents of X and Y)
    """

    PLOT_DEFAULT_SIZE = 25
    """ImVec2, default size used when ImVec2(0,0) is passed to BeginPlot"""

    PLOT_MIN_SIZE = 26
    """ImVec2, minimum size plot frame can be when shrunk"""

    COUNT = 27

class SubplotFlags(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    NO_TITLE = 1
    """
    The subplot title will not be displayed (titles are also hidden if preceeded by double hashes, e.g. "##MySubplot")
    """

    NO_LEGEND = 2
    """
    The legend will not be displayed (only applicable if `SubplotFlags.SHARE_ITEMS` is enabled)
    """

    NO_MENUS = 4
    """The user will not be able to open context menus with right-click"""

    NO_RESIZE = 8
    """Resize splitters between subplot cells will be not be provided"""

    NO_ALIGN = 16
    """Subplot edges will not be aligned vertically or horizontally"""

    SHARE_ITEMS = 32
    """
    Items across all subplots will be shared and rendered into a single legend entry
    """

    LINK_ROWS = 64
    """
    Link the y-axis limits of all plots in each row (does not apply to auxiliary axes)
    """

    LINK_COLS = 128
    """
    Link the x-axis limits of all plots in each column (does not apply to auxiliary axes)
    """

    LINK_ALL_X = 256
    """
    Link the x-axis limits in every plot in the subplot (does not apply to auxiliary axes)
    """

    LINK_ALL_Y = 512
    """
    Link the y-axis limits in every plot in the subplot (does not apply to auxiliary axes)
    """

    COL_MAJOR = 1024
    """
    Subplots are added in column major order instead of the default row major order
    """

class TextFlag(enum.IntFlag):
    __str__ = __repr__

    def __repr__(self, /):
        """Return repr(self)."""

    NONE = 0
    """Default"""

    VERTICAL = 1024
    """Text will be rendered vertically"""

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

    ```
    if implot.begin_plot(...):
        implot.plot_line(...)
        ...
        implot.end_plot()
    ```

    Important notes:

    - `title_id` must be unique to the current ImGui ID scope. If you need to avoid ID
      collisions or don't want to display a title in the plot, use double hashes
      (e.g. `"MyPlot##HiddenIdText"` or `"##NoTitle"`).

    - `size` is the **frame** size of the plot widget, not the plot area. The default
      size of plots (i.e. when `(0,0)`) can be modified in your `implot.Style`.
    """

def begin_subplots(title_id: str, rows: int, cols: int, size: tuple[float, float], flags: SubplotFlags = SubplotFlags.NONE, row_ratios: Annotated[ArrayLike, dict(dtype='float32', shape=(None), order='C', device='cpu')] | None = None, col_ratios: Annotated[ArrayLike, dict(dtype='float32', shape=(None), order='C', device='cpu')] | None = None) -> bool:
    """
    See https://nurpax.github.io/slimgui/apiref_implot.html#subplots for details.
    """

def bust_color_cache(plot_title_id: str | None = None) -> None:
    """
    When items in a plot sample their color from a colormap, the color is cached and does not change
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

def drag_line_x(id: int, x: Annotated[ArrayLike, dict(dtype='float64', shape=(), order='C', device='cpu')], col: tuple[float, float, float, float], thickness: float = 1, flags: DragToolFlags = DragToolFlags.NONE, out_clicked: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_hovered: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_held: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None) -> bool:
    """
    Shows a draggable vertical guide line at an x-value. The updated drag position will be written to the `x` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the line was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """

def drag_line_y(id: int, y: Annotated[ArrayLike, dict(dtype='float64', shape=(), order='C', device='cpu')], col: tuple[float, float, float, float], thickness: float = 1, flags: DragToolFlags = DragToolFlags.NONE, out_clicked: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_hovered: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_held: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None) -> bool:
    """
    Shows a draggable horizontal guide line at a y-value. The updated drag position will be written to the `y` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the line is clicked, hovered, or held, respectively.
    Returns `True` if the line was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """

def drag_point(id: int, point: Annotated[ArrayLike, dict(dtype='float64', shape=(2), order='C', device='cpu')], col: tuple[float, float, float, float], size: float = 4.0, flags: DragToolFlags = DragToolFlags.NONE, out_clicked: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_hovered: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_held: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None) -> bool:
    """
    Shows a draggable point at `point`.  The updated drag position will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the point was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """

def drag_rect(id: int, rect: Annotated[ArrayLike, dict(dtype='float64', shape=(2, 2), order='C', device='cpu')], col: tuple[float, float, float, float], flags: DragToolFlags = DragToolFlags.NONE, out_clicked: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_hovered: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None, out_held: Annotated[ArrayLike, dict(dtype='bool', shape=(), order='C', device='cpu')] | None = None) -> bool:
    """
    Shows a draggable rectangle at `[[x0, y0], [x1, y1]` coordinates, loaded from `rect`.  The updated drag rectangle will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the rectangle was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """

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

def end_subplots() -> None: ...

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
def plot_bars(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float = 0.67, shift: float = 0.0, flags: BarsFlags = BarsFlags.NONE) -> None:
    """
    Plots a bar graph. Vertical by default. `bar_size` and `shift` are in plot units.
    """

@overload
def plot_bars(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bar_size: float, flags: BarsFlags = BarsFlags.NONE) -> None: ...

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

def plot_histogram(label_id: str, values: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], bins: int | Bin = Bin.STURGES, bar_scale: float = 1.0, range: tuple[float, float] | None = None, flags: HistogramFlags = HistogramFlags.NONE) -> float:
    """
    Plots a horizontal histogram. `bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `values` will be used as the range.  Otherwise, outlier values outside of the range are not binned. The largest bin count or density is returned.
    """

def plot_histogram2d(label_id: str, xs: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], ys: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C', device='cpu', writable=False)], x_bins: int | Bin = Bin.STURGES, y_bins: int | Bin = Bin.STURGES, range: tuple[tuple[float, float], tuple[float, float]] | None = None, flags: HistogramFlags = HistogramFlags.NONE) -> float:
    """
    Plots two dimensional, bivariate histogram as a heatmap. `x_bins` and `y_bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `xs` an `ys` will be used as the ranges. Otherwise, outlier values outside of range are not binned. The largest bin count or density is returned.
    """

def plot_image(label_id: str, tex_ref: slimgui_ext.imgui.TextureRef, bounds_min: tuple[float, float], bounds_max: tuple[float, float], uv0: tuple[float, float] = (0,0), uv1: tuple[float, float] = (1,1), tint_col: tuple[float, float, float, float] = (1,1,1,1), flags: ImageFlag = ImageFlag.NONE) -> None:
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
def push_style_var(idx: StyleVar, val: int) -> None:
    """
    Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!
    """

@overload
def push_style_var(idx: StyleVar, val: float) -> None:
    """
    Temporarily modify a style variable of float type. Don't forget to call `implot.pop_style_var()`!
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
