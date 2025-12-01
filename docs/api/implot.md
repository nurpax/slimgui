---
title: 'slimgui - ImPlot API reference'
subtitle: 'Python bindings for Dear ImGui'
---

# ImPlot API reference

See [Typing](/guide/typing) for an explanation of the public `imgui` / `implot`
modules and how they relate to the underlying `slimgui.slimgui_ext.*` bindings.

## ImPlot Data Types

Most `implot` plotting functions consume NumPy arrays.

Common accepted shapes include:

- `(N,)` for one-dimensional x/y/value arrays
- `(M, N)` for tabular inputs such as grouped bars or heatmaps
- scalar `np.ndarray` values for interactive tools that modify values in place
- small fixed-shape arrays such as `(2,)` or `(2, 2)` for plot tools

Examples:

```python
xs = np.linspace(0.0, 10.0, 1000)
ys = np.sin(xs)
implot.plot_line("sin(x)", xs, ys)
```

```python
ys = np.random.rand(10)
implot.plot_bars("bars", ys)
```

```python
values = np.random.rand(3, 4)
implot.plot_bar_groups(["A", "B", "C"], values)
```

The bindings generally convert numeric array dtypes automatically where that is safe.
Non-contiguous views are also supported in normal plotting use, for example `data_x[::2]`.

Interactive plot tools use mutable NumPy arrays so the binding can write updated values back
to Python. Examples include: `drag_point`, `drag_line_x`, `drag_line_y`, `drag_rect`.

Those APIs also accept optional scalar `np.ndarray` boolean outputs such as `out_clicked`,
`out_hovered`, and `out_held`.

## ImPlot API functions

### Contexts

::: api-signature
```python
def create_context() -> slimgui.implot.WrappedContext:
    """
    Create an ImPlot context.  Call this after `imgui.create_context()`.
    """
```
:::

::: api-signature
```python
def destroy_context(
    ctx: slimgui.implot.WrappedContext | None,
):
    """
    Destroys an ImPlot context. Call this before `imgui.destroy_context()`. `None` = destroy current context.
    """
```
:::

::: api-signature
```python
def get_current_context() -> slimgui.implot.WrappedContext | None:
    """
    Returns the current ImPlot context. `None` if no context has ben set.
    """
```
:::

::: api-signature
```python
def set_current_context(
    ctx: slimgui.implot.WrappedContext,
) -> None:
    """
    Sets the current ImPlot context.
    """
```
:::

### Begin/End Plot

::: api-signature
```python
def begin_plot(
    title_id: str,
    size: tuple[float, float] = (-1,0),
    flags: PlotFlags = PlotFlags.NONE,
) -> bool:
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
```
:::

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

::: api-signature
```python
def end_plot() -> None:
    """
    Only call `implot.end_plot()` if `implot.begin_plot()` returns `True`! Typically called at the end of an if statement conditioned on `implot.begin_plot()`. See example above.
    """
```
:::

### Subplots

`begin_subplots()` starts a subdivided plotting context.  If the function returns `True`,
`end_subplots()` MUST be called! Call `begin_plot()`/`end_plot()` at most `[rows*cols]`
times in between the begining and end of the subplot context.  Plots are
added in row major order (or use `SubplotFlags.COL_MAJOR` if you want column major).

Example:

```python
if implot.begin_subplots("My Subplot", 2, 3, (800, 400)):
    for i in range(6):
        if implot.begin_plot(...):
            implot.plot_line(...)
            ...
            implot.end_plot()
    implot.end_subplots()
```

Produces:

```
  [0] | [1] | [2]
  ----|-----|----
  [3] | [4] | [5]
```

Important notes:

- `title_id` must be unique to the current ImGui ID scope. If you need to avoid ID
  collisions or don't want to display a title in the plot, use double hashes
  (e.g. `"MySubplot##HiddenIdText"` or `"##NoTitle"`).
- `rows` and `cols` must be greater than 0.
- `size` is the size of the entire grid of subplots, not the individual plots
- `row_ratios` and `col_ratios` must have at exactly `rows` and `cols` elements,
  respectively, or an exception is raised.  These are the sizes of the rows and
  columns expressed in ratios.  If the user adjusts the dimensions, the arrays are
  updated with new ratios.
- The `row/col_ratios` arrays must be created with `dtype=np.float32`, e.g.
  `np.array([0.3, 0.7], dtype=np.float32)`.

Important notes regarding `begin_plot()` from inside of `begin_subplots()`:

- The `title_id` parameter of `begin_plot()` (see above) does NOT have to be
  unique when called inside of a subplot context. Subplot IDs are hashed
  for your convenience so you don't have call `imgui.push_id()` or generate unique title
  strings. Simply pass an empty string to `begin_plot()` unless you want to title
  each subplot.
- The `size` parameter of `begin_plot()` (see above) is ignored when inside of a
  subplot context. The actual size of the subplot will be based on the
  `size` value you pass to `begin_subplots()` and `row_ratios`/`col_ratios` if provided.

::: api-signature
```python
def begin_subplots(
    title_id: str,
    rows: int,
    cols: int,
    size: tuple[float, float],
    flags: SubplotFlags = SubplotFlags.NONE,
    row_ratios: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu')] | None = None,
    col_ratios: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu')] | None = None,
) -> bool:
    """
    See https://nurpax.github.io/slimgui/apiref_implot.html#subplots for details.
    """
```
:::

::: api-signature
```python
def end_subplots() -> None:
```
:::

### Setup

The following API allows you to set up and customize various aspects of the current plot. The functions should be called immediately after `begin_plot()` and before any other API calls. Typical usage is as follows:

```python
if implot.begin_plot(...):                     # 1) begin a new plot
    implot.setup_axis(im_axis_x1, "My X-Axis") # 2) make setup calls
    implot.setup_axis(im_axis_y1, "My Y-Axis")
    implot.setup_legend(im_plot_location_north)
    ...
    implot.setup_finish()                      # 3) [optional] explicitly finish setup
    implot.plot_line(...)                      # 4) plot items
    ...
    implot.end_plot()                          # 5) end the plot
```

**Important Notes**:

- Always call setup code at the top of your `begin_plot()` conditional statement.
- Setup is locked once you start plotting or explicitly call `setup_finish()`.  
  Do **NOT** call setup code after you begin plotting or after you make any non-setup API calls (e.g., utilities like `plot_to_pixels()` also lock setup).
- Calling `setup_finish` is **optional**, but it is probably good practice. If you do not call it yourself, the first subsequent plotting or utility function will call it for you.

::: api-signature
```python
def setup_axis(
    axis: Axis,
    label: str | None = None,
    flags: AxisFlags = AxisFlags.NONE,
) -> None:
    """
    Enables an axis or sets the label and/or flags for an existing axis. Leave `label=None` for no label.
    """
```
:::

::: api-signature
```python
def setup_axis_limits(
    axis: Axis,
    v_min: float,
    v_max: float,
    cond: Cond = Cond.ONCE,
) -> None:
    """
    Sets an axis range limits. If `Cond.ALWAYS` is used, the axes limits will be locked. Inversion with `v_min > v_max` is not supported; use `implot.setup_axis_limits` instead.
    """
```
:::

::: api-signature
```python
def setup_axis_format(
    axis: Axis,
    fmt: str,
) -> None:
    """
    Sets the format of numeric axis labels via formater specifier (default="%g"). Formated values will be double (i.e. use %f).  Note that the format string is specified in C printf syntax!
    """
```
:::

::: api-signature
```python
def setup_axis_ticks(
    axis: int,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    labels: Sequence[str] | None = None,
    keep_default: bool = False,
) -> None:
    """
    Sets an axis' ticks and optionally the labels. To keep the default ticks, set `keep_default=True`.
    """
```
:::

::: api-signature
```python
def setup_axis_ticks(
    axis: int,
    v_min: float,
    v_max: float,
    n_ticks: int,
    labels: Sequence[str] | None = None,
    keep_default: bool = False,
) -> None:
    """
    Sets an axis' ticks and optionally the labels. To keep the default ticks, set `keep_default=True`.
    """
```
:::

::: api-signature
```python
def setup_axis_scale(
    axis: Axis,
    scale: Scale,
) -> None:
    """
    Sets an axis' scale using built-in options.
    """
```
:::

::: api-signature
```python
def setup_axis_limits_constraints(
    axis: Axis,
    v_min: float,
    v_max: float,
) -> None:
    """
    Sets an axis' limits constraints.
    """
```
:::

::: api-signature
```python
def setup_axis_zoom_constraints(
    axis: Axis,
    z_min: float,
    z_max: float,
) -> None:
    """
    Sets an axis' zoom constraints.
    """
```
:::

::: api-signature
```python
def setup_axes(
    x_label: str | None,
    y_label: str | None,
    x_flags: AxisFlags = AxisFlags.NONE,
    y_flags: AxisFlags = AxisFlags.NONE,
) -> None:
    """
    Sets the label and/or flags for primary X and Y axes (shorthand for two calls to `implot.setup_Axis()`).
    """
```
:::

::: api-signature
```python
def setup_axes_limits(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    cond: Cond = Cond.ONCE,
) -> None:
    """
    Sets the primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`).
    """
```
:::

::: api-signature
```python
def setup_legend(
    location: Location,
    flags: LegendFlags = LegendFlags.NONE,
) -> None:
    """
    Sets up the plot legend. This can also be called immediately after `implot.begin_subplots()` when using `SubplotFlags.SHARE_ITEMS`.
    """
```
:::

::: api-signature
```python
def setup_mouse_text(
    location: Location,
    flags: MouseTextFlags = MouseTextFlags.NONE,
) -> None:
    """
    Set the location of the current plot's mouse position text (default = South|East).
    """
```
:::

::: api-signature
```python
def setup_finish() -> None:
    """
    Explicitly finalize plot setup. Once you call this, you cannot make anymore Setup calls for the current plot!

    Note that calling this function is OPTIONAL; it will be called by the first subsequent setup-locking API call.
    """
```
:::

Explicitly finalize plot setup. Once you call this, you cannot make anymore Setup calls for the current plot!

Note that calling this function is OPTIONAL; it will be called by the first subsequent setup-locking API call.

### SetNext

Though you should default to the `setup()` API above, there are some scenarios where (re)configuring a plot or axis before `begin_plot()` is needed (e.g., if using a preceding button or slider widget to change the plot limits). In this case, you can use the `set_next_*()` API below. While this is not as feature-rich as the `setup()` API, most common needs are provided. These functions can be called anywhere except inside of `begin_plot`/`end_plot`. For example:

```python
if imgui.button("Center Plot"):
    implot.set_next_axes_limits(-1, 1, -1, 1)
if implot.begin_plot(...):
    ...
    implot.end_plot()
```

**Important Notes**:

- You must still enable non-default axes with `setup_axis` for these functions to work properly.

::: api-signature
```python
def set_next_axis_limits(
    axis: Axis,
    v_min: float,
    v_max: float,
    cond: Cond = Cond.ONCE,
) -> None:
    """
    Sets an upcoming axis range limits. If ImPlotCond_Always is used, the axes limits will be locked.
    """
```
:::

::: api-signature
```python
def set_next_axis_to_fit(
    axis: Axis,
) -> None:
    """
    Set an upcoming axis to auto fit to its data.
    """
```
:::

::: api-signature
```python
def set_next_axes_limits(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    cond: Cond = Cond.ONCE,
) -> None:
    """
    Sets the upcoming primary X and Y axes range limits. If `Cond.ALWAYS` is used, the axes limits will be locked (shorthand for two calls to `implot.setup_axis_limits()`).
    """
```
:::

::: api-signature
```python
def set_next_axes_to_fit() -> None:
    """
    Sets all upcoming axes to auto fit to their data.
    """
```
:::

### Plot Items

The main plotting API is provied below. Call these functions between
Begin/EndPlot and after any Setup API calls. Each plots data on the current
x and y axes, which can be changed with `set_axis()`/`set_axes()`.

NB: All types are converted to double before plotting. You may lose information
if you try plotting extremely large 64-bit integral types. Proceed with caution!

::: api-signature
```python
def plot_line(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: LineFlags = LineFlags.NONE,
) -> None:
    """
    Plots a standard 2D line plot. The x values are taken from the `xs` array, and the y values are taken from the `ys` array.
    """
```
:::

::: api-signature
```python
def plot_line(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    xscale: float = 1.0,
    xstart: float = 0.0,
    flags: LineFlags = LineFlags.NONE,
) -> None:
    """
    Plots a standard 2D line plot. The x values are taken from the `xs` array, and the y values are taken from the `ys` array.
    """
```
:::

Plots a standard 2D line plot. The x values are spaced evenly along the x axis, starting at `xstart` and spaced by `xscale`. The y values are taken from the `values` array.

::: api-signature
```python
def plot_scatter(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: ScatterFlags = ScatterFlags.NONE,
) -> None:
    """
    Plots a standard 2D scatter plot. Default marker is `Marker.CIRCLE`.
    """
```
:::

::: api-signature
```python
def plot_scatter(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    xscale: float = 1.0,
    xstart: float = 0.0,
    flags: ScatterFlags = ScatterFlags.NONE,
) -> None:
    """
    Plots a standard 2D scatter plot. Default marker is `Marker.CIRCLE`.
    """
```
:::

::: api-signature
```python
def plot_stairs(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: StairsFlags = StairsFlags.NONE,
) -> None:
    """
    Plots a stairstep graph. The y value is continued constantly to the right from every x position, i.e. the interval `[x[i], x[i+1])` has the value `y[i]`
    """
```
:::

::: api-signature
```python
def plot_stairs(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    xscale: float = 1.0,
    xstart: float = 0.0,
    flags: StairsFlags = StairsFlags.NONE,
) -> None:
    """
    Plots a stairstep graph. The y value is continued constantly to the right from every x position, i.e. the interval `[x[i], x[i+1])` has the value `y[i]`
    """
```
:::

::: api-signature
```python
def plot_shaded(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys1: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys2: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: ShadedFlags = ShadedFlags.NONE,
) -> None:
    """
    Plots a shaded (filled) region between two lines, or a line and a horizontal reference. Set `yref` to +/-INFINITY for infinite fill extents.
    """
```
:::

::: api-signature
```python
def plot_shaded(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    yref: float = 0,
    flags: ShadedFlags = ShadedFlags.NONE,
) -> None:
    """
    Plots a shaded (filled) region between two lines, or a line and a horizontal reference. Set `yref` to +/-INFINITY for infinite fill extents.
    """
```
:::

::: api-signature
```python
def plot_shaded(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    yref: float = 0,
    xscale: float = 1.0,
    xstart: float = 0.0,
    flags: ShadedFlags = ShadedFlags.NONE,
) -> None:
    """
    Plots a shaded (filled) region between two lines, or a line and a horizontal reference. Set `yref` to +/-INFINITY for infinite fill extents.
    """
```
:::

::: api-signature
```python
def plot_bars(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    bar_size: float,
    flags: BarsFlags = BarsFlags.NONE,
) -> None:
    """
    Plots a bar graph. Vertical by default. `bar_size` and `shift` are in plot units.
    """
```
:::

::: api-signature
```python
def plot_bars(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    bar_size: float = 0.67,
    shift: float = 0.0,
    flags: BarsFlags = BarsFlags.NONE,
) -> None:
    """
    Plots a bar graph. Vertical by default. `bar_size` and `shift` are in plot units.
    """
```
:::

::: api-signature
```python
def plot_bar_groups(
    label_ids: Sequence[str],
    values: Annotated[NDArray[Any], dict(shape=(None, None), order='C', device='cpu', writable=False)],
    group_size: float = 0.67,
    shift: float = 0.0,
    flags: BarGroupsFlags = BarGroupsFlags.NONE,
) -> None:
    """
    Plots a group of bars. `values` is a matrix with a shape `(item_count, group_count)`. `label_ids` should have `item_count` elements.
    """
```
:::

::: api-signature
```python
def plot_error_bars(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    err: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: ErrorBarsFlags = ErrorBarsFlags.NONE,
) -> None:
    """
    Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.
    """
```
:::

::: api-signature
```python
def plot_error_bars(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    neg: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    pos: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: ErrorBarsFlags = ErrorBarsFlags.NONE,
) -> None:
    """
    Plots vertical error bar. The label_id should be the same as the label_id of the associated line or bar plot.
    """
```
:::

::: api-signature
```python
def plot_stems(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ref: float = 0.0,
    flags: StemsFlags = StemsFlags.NONE,
) -> None:
    """
    Plots stems. Vertical by default.
    """
```
:::

::: api-signature
```python
def plot_stems(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ref: float = 0.0,
    scale: float = 1.0,
    start: float = 0.0,
    flags: StemsFlags = StemsFlags.NONE,
) -> None:
    """
    Plots stems. Vertical by default.
    """
```
:::

::: api-signature
```python
def plot_inf_lines(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: InfLinesFlags = InfLinesFlags.NONE,
) -> None:
    """
    Plots infinite vertical or horizontal lines (e.g. for references or asymptotes).
    """
```
:::

::: api-signature
```python
def plot_heatmap(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None, None), order='C', device='cpu', writable=False)],
    scale_min: float = 0,
    scale_max: float = 0.0,
    label_fmt: str | None = '%.1f',
    bounds_min: tuple[float, float] = (0.0, 0.0),
    bounds_max: tuple[float, float] = (1.0, 1.0),
    flags: HeatmapFlags = HeatmapFlags.NONE,
) -> None:
    """
    Plots a 2D heatmap chart. `values` is expected to have shape (rows, cols). Leave `scale_min` and `scale_max` both at 0 for automatic color scaling, or set them to a predefined range. `label_fmt` can be set to `None` for no labels.
    """
```
:::

::: api-signature
```python
def plot_digital(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    flags: DigitalFlags = DigitalFlags.NONE,
) -> None:
    """
    Plots digital data. Digital plots do not respond to y drag or zoom, and are always referenced to the bottom of the plot.
    """
```
:::

::: api-signature
```python
def plot_image(
    label_id: str,
    tex_ref: slimgui_ext.imgui.TextureRef | int,
    bounds_min: tuple[float, float],
    bounds_max: tuple[float, float],
    uv0: tuple[float, float] = (0,0),
    uv1: tuple[float, float] = (1,1),
    tint_col: tuple[float, float, float, float] = (1,1,1,1),
    flags: ImageFlag = ImageFlag.NONE,
) -> None:
    """
    Plots an axis-aligned image. `bounds_min`/`bounds_max` are in plot coordinates (y-up) and `uv0`/`uv1` are in texture coordinates (y-down).
    """
```
:::

::: api-signature
```python
def plot_text(
    text: str,
    x: float,
    y: float,
    pix_offset: tuple[float, float] = (0,0),
    flags: TextFlag = TextFlag.NONE,
) -> None:
    """
    Plots a centered text label at point x,y with an optional pixel offset. Text color can be changed with `implot.push_style_color(Col.INLAY_TEXT, ...)`.
    """
```
:::

::: api-signature
```python
def plot_dummy(
    label_id: str,
    flags: DummyFlag = DummyFlag.NONE,
) -> None:
    """
    Plots a dummy item (i.e. adds a legend entry colored by `Col.LINE`).
    """
```
:::

::: api-signature
```python
def plot_histogram(
    label_id: str,
    values: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    bins: int | Bin = Bin.STURGES,
    bar_scale: float = 1.0,
    range: tuple[float, float] | None = None,
    flags: HistogramFlags = HistogramFlags.NONE,
) -> float:
    """
    Plots a horizontal histogram. `bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `values` will be used as the range.  Otherwise, outlier values outside of the range are not binned. The largest bin count or density is returned.
    """
```
:::

::: api-signature
```python
def plot_histogram2d(
    label_id: str,
    xs: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    ys: Annotated[NDArray[Any], dict(shape=(None), order='C', device='cpu', writable=False)],
    x_bins: int | Bin = Bin.STURGES,
    y_bins: int | Bin = Bin.STURGES,
    range: tuple[tuple[float, float], tuple[float, float]] | None = None,
    flags: HistogramFlags = HistogramFlags.NONE,
) -> float:
    """
    Plots two dimensional, bivariate histogram as a heatmap. `x_bins` and `y_bins` can be a positive integer or a method specified with the `implot.Bin` enum. If `range` is left unspecified, the min/max of `xs` an `ys` will be used as the ranges. Otherwise, outlier values outside of range are not binned. The largest bin count or density is returned.
    """
```
:::

The `range` parameter in `plot_histogram2d` is typed as a pair of float 2-tuples.  The first element is the range `(min,max)` for `xs`, the second for `ys`.

### Plot Tools

The following can be used to render interactive elements and/or annotations.
Like the item plotting functions above, they apply to the current x and y
axes, which can be changed with `set_axis()`/`set_axes()`. These functions return `True`
when user interaction causes the provided coordinates to change. Additional
user interactions can be retrieved through the optional output parameters.

Functions such as `drag_point`, `drag_line_x/y` and `drag_rect` use `np.array`s to pass in a mutable reference to float and bool values.

Be careful to use the right `dtype` for the input `np.arrays`: use `dtype=np.float64` for floats and `dtype=np.bool_` for bools.
For example, to specify a point for `drag_point`, you could create the array like so: `np.array([x, y], dtype=np.float64)`.
Search for `drag_line_x` in [example/implot_demo_window/implot.py](https://github.com/nurpax/slimgui/blob/main/example/implot_demo_window/implot.py) for more examples.

::: api-signature
```python
def drag_point(
    id: int,
    point: Annotated[NDArray[Any], dict(shape=(2), order='C', device='cpu')],
    col: tuple[float, float, float, float],
    size: float = 4.0,
    flags: DragToolFlags = DragToolFlags.NONE,
    out_clicked: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_hovered: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_held: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
) -> bool:
    """
    Shows a draggable point at `point`.  The updated drag position will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the point was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """
```
:::

Shows a draggable point at `point`.  The updated drag position will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
Returns `True` if the point was dragged.

The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.

::: api-signature
```python
def drag_line_x(
    id: int,
    x: Annotated[NDArray[Any], dict(shape=(), order='C', device='cpu')],
    col: tuple[float, float, float, float],
    thickness: float = 1,
    flags: DragToolFlags = DragToolFlags.NONE,
    out_clicked: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_hovered: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_held: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
) -> bool:
    """
    Shows a draggable vertical guide line at an x-value. The updated drag position will be written to the `x` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the line was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """
```
:::

Shows a draggable vertical guide line at an x-value. The updated drag position will be written to the `x` array.  Color `col` defaults to `imgui.Col.TEXT`.
`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
Returns `True` if the line was dragged.

The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.

::: api-signature
```python
def drag_line_y(
    id: int,
    y: Annotated[NDArray[Any], dict(shape=(), order='C', device='cpu')],
    col: tuple[float, float, float, float],
    thickness: float = 1,
    flags: DragToolFlags = DragToolFlags.NONE,
    out_clicked: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_hovered: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_held: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
) -> bool:
    """
    Shows a draggable horizontal guide line at a y-value. The updated drag position will be written to the `y` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the line is clicked, hovered, or held, respectively.
    Returns `True` if the line was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """
```
:::

Shows a draggable horizontal guide line at a y-value. The updated drag position will be written to the `y` array.  Color `col` defaults to `imgui.Col.TEXT`.
`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the line is clicked, hovered, or held, respectively.
Returns `True` if the line was dragged.

The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.

::: api-signature
```python
def drag_rect(
    id: int,
    rect: Annotated[NDArray[Any], dict(shape=(2, 2), order='C', device='cpu')],
    col: tuple[float, float, float, float],
    flags: DragToolFlags = DragToolFlags.NONE,
    out_clicked: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_hovered: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
    out_held: Annotated[NDArray[numpy.bool], dict(shape=(), order='C', device='cpu')] | None = None,
) -> bool:
    """
    Shows a draggable rectangle at `[[x0, y0], [x1, y1]` coordinates, loaded from `rect`.  The updated drag rectangle will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
    `out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
    Returns `True` if the rectangle was dragged.

    The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.
    """
```
:::

Shows a draggable rectangle at `[[x0, y0], [x1, y1]` coordinates, loaded from `rect`.  The updated drag rectangle will be written to the `point` array.  Color `col` defaults to `imgui.Col.TEXT`.
`out_clicked`, `out_hovered`, and `out_held` are optional single bool np.arrays that will be set to `True` if the point is clicked, hovered, or held, respectively.
Returns `True` if the rectangle was dragged.

The input `np.array` arguments are motivated by being able to pass in a mutable reference value that the bound API functions can write to.  See [https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools](https://nurpax.github.io/slimgui/apiref_implot.html#plot-tools) for details.

::: api-signature
```python
def annotation(
    x: float,
    y: float,
    col: tuple[float, float, float, float],
    pix_offset: tuple[float, float],
    clamp: bool,
    round: bool = False,
) -> None:
    """
    Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.
    """
```
:::

::: api-signature
```python
def annotation(
    x: float,
    y: float,
    col: tuple[float, float, float, float],
    pix_offset: tuple[float, float],
    clamp: bool,
    text: str,
) -> None:
    """
    Shows an annotation callout at a chosen point. Clamping keeps annotations in the plot area. Annotations are always rendered on top.
    """
```
:::

::: api-signature
```python
def tag_x(
    x: float,
    col: tuple[float, float, float, float],
    round: bool = False,
) -> None:
    """
    Shows a x-axis tag at the specified coordinate value.
    """
```
:::

::: api-signature
```python
def tag_x(
    x: float,
    col: tuple[float, float, float, float],
    text: str,
) -> None:
    """
    Shows a x-axis tag at the specified coordinate value.
    """
```
:::

::: api-signature
```python
def tag_y(
    y: float,
    col: tuple[float, float, float, float],
    round: bool = False,
) -> None:
    """
    Shows a y-axis tag at the specified coordinate value.
    """
```
:::

::: api-signature
```python
def tag_y(
    y: float,
    col: tuple[float, float, float, float],
    text: str,
) -> None:
    """
    Shows a y-axis tag at the specified coordinate value.
    """
```
:::

### Plot Utils

::: api-signature
```python
def set_axis(
    axis: Axis,
) -> None:
    """
    Select which axis/axes will be used for subsequent plot elements.
    """
```
:::

::: api-signature
```python
def set_axes(
    x_axis: Axis,
    y_axis: Axis,
) -> None:
    """
    Select which axis/axes will be used for subsequent plot elements.
    """
```
:::

::: api-signature
```python
def pixels_to_plot(
    pix: tuple[float, float],
    x_axis: Axis | int = AUTO,
    y_axis: Axis | int = AUTO,
) -> tuple[float, float]:
    """
    Convert pixels to a position in the current plot's coordinate system. Passing `implot.AUTO` uses the current axes.
    """
```
:::

::: api-signature
```python
def pixels_to_plot(
    x: float,
    y: float,
    x_axis: Axis | int = AUTO,
    y_axis: Axis | int = AUTO,
) -> tuple[float, float]:
    """
    Convert pixels to a position in the current plot's coordinate system. Passing `implot.AUTO` uses the current axes.
    """
```
:::

::: api-signature
```python
def plot_to_pixels(
    plt: tuple[float, float],
    x_axis: Axis | int = AUTO,
    y_axis: Axis | int = AUTO,
) -> tuple[float, float]:
    """
    Convert a position in the current plot's coordinate system to pixels. Passing `implot.AUTO` uses the current axes.
    """
```
:::

::: api-signature
```python
def plot_to_pixels(
    x: float,
    y: float,
    x_axis: Axis | int = AUTO,
    y_axis: Axis | int = AUTO,
) -> tuple[float, float]:
    """
    Convert a position in the current plot's coordinate system to pixels. Passing `implot.AUTO` uses the current axes.
    """
```
:::

::: api-signature
```python
def get_plot_pos() -> tuple[float, float]:
    """
    Get the current Plot position (top-left) in pixels.
    """
```
:::

::: api-signature
```python
def get_plot_size() -> tuple[float, float]:
    """
    Get the curent Plot size in pixels.
    """
```
:::

::: api-signature
```python
def get_plot_mouse_pos(
    x_axis: Axis | int = AUTO,
    y_axis: Axis | int = AUTO,
) -> tuple[float, float]:
    """
    Returns the mouse position in x,y coordinates of the current plot. Passing `implot.AUTO` uses the current axes.
    """
```
:::

::: api-signature
```python
def is_plot_hovered() -> bool:
    """
    Returns `True` if the plot area in the current plot is hovered.
    """
```
:::

::: api-signature
```python
def is_axis_hovered(
    axis: Axis,
) -> bool:
    """
    Returns `True` if the axis label area in the current plot is hovered.
    """
```
:::

::: api-signature
```python
def is_subplots_hovered() -> bool:
    """
    Returns `True` if the bounding frame of a subplot is hovered.
    """
```
:::

::: api-signature
```python
def is_plot_selected() -> bool:
    """
    Returns `True` if the current plot is being box selected.
    """
```
:::

::: api-signature
```python
def cancel_plot_selection() -> None:
    """
    Cancels a the current plot box selection.
    """
```
:::

::: api-signature
```python
def hide_next_item(
    hidden: bool = True,
    cond: Cond = Cond.ONCE,
) -> None:
    """
    Hides or shows the next plot item (i.e. as if it were toggled from the legend).

    Use `Cond.ALWAYS` if you need to forcefully set this every frame.
    """
```
:::

Hides or shows the next plot item (i.e. as if it were toggled from the legend).

Use `Cond.ALWAYS` if you need to forcefully set this every frame.

Use the following around calls to `begin_plot()`/`end_plot()` to align l/r/t/b padding.
Consider using `begin_subplots()`/`end_subplots()` first. They are more feature rich and
accomplish the same behaviour by default. The functions below offer lower
level control of plot alignment.

::: api-signature
```python
def begin_aligned_plots(
    group_id: str,
    vertical: bool = True,
) -> bool:
    """
    Align axis padding over multiple plots in a single row or column. `group_id` must
    be unique. If this function returns `True`, `implot.end_aligned_plots()` must be called.
    """
```
:::

::: api-signature
```python
def end_aligned_plots() -> None:
    """
    Only call `implot.end_aligned_plots()` if `implot.begin_aligned_plots()` returns `True`!
    """
```
:::

### Legend Utils

::: api-signature
```python
def begin_legend_popup(
    label_id: str,
    mouse_button: slimgui_ext.imgui.MouseButton = slimgui_ext.imgui.MouseButton.RIGHT,
) -> bool:
    """
    Begin a popup for a legend entry.
    """
```
:::

::: api-signature
```python
def end_legend_popup() -> None:
    """
    End a popup for a legend entry.
    """
```
:::

::: api-signature
```python
def is_legend_entry_hovered(
    label_id: str,
) -> bool:
    """
    Returns `True` if a plot item legend entry is hovered.
    """
```
:::

### Drag and Drop

::: api-signature
```python
def begin_drag_drop_target_plot() -> bool:
    """
    Turns the current plot's plotting area into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """
```
:::

::: api-signature
```python
def begin_drag_drop_target_axis(
    axis: Axis,
) -> bool:
    """
    Turns the current plot's X-axis into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """
```
:::

::: api-signature
```python
def begin_drag_drop_target_legend() -> bool:
    """
    Turns the current plot's legend into a drag and drop target. Don't forget to call `implot.end_drag_drop_target()`!
    """
```
:::

::: api-signature
```python
def end_drag_drop_target() -> None:
    """
    Ends a drag and drop target (currently just an alias for `imgui.end_drag_drop_target()`).
    """
```
:::

NB: By default, plot and axes drag and drop *sources* require holding the Ctrl modifier to initiate the drag.
You can change the modifier if desired. If `imgui.Key.MOD_NONE` is provided, the axes will be locked from panning.

::: api-signature
```python
def begin_drag_drop_source_plot(
    flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE,
) -> bool:
    """
    Turns the current plot's plotting area into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!
    """
```
:::

::: api-signature
```python
def begin_drag_drop_source_axis(
    axis: Axis,
    flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE,
) -> bool:
    """
    Turns the current plot's X-axis into a drag and drop source. You must hold Ctrl. Don't forget to call `implot.end_drag_drop_source()`!
    """
```
:::

::: api-signature
```python
def begin_drag_drop_source_item(
    label_id: str,
    flags: slimgui_ext.imgui.DragDropFlags = slimgui_ext.imgui.DragDropFlags.NONE,
) -> bool:
    """
    Turns an item in the current plot's legend into drag and drop source. Don't forget to call `implot.end_drag_drop_source()`!
    """
```
:::

::: api-signature
```python
def end_drag_drop_source() -> None:
    """
    Ends a drag and drop source (currently just an alias for `imgui.end_drag_drop_source()`).
    """
```
:::

### Styling

Styling colors in ImPlot works similarly to styling colors in ImGui, but
with one important difference. Like ImGui, all style colors are stored in an
indexable array in ImPlotStyle. You can permanently modify these values through
GetStyle().Colors, or temporarily modify them with Push/Pop functions below.
However, by default all style colors in ImPlot default to a special color
IMPLOT_AUTO_COL. The behavior of this color depends upon the style color to
which it as applied:

1. For style colors associated with plot items (e.g. `Col.LINE`),
`implot.AUTO_COL` tells ImPlot to color the item with the next unused
color in the current colormap. Thus, every item will have a different
color up to the number of colors in the colormap, at which point the
colormap will roll over. For most use cases, you should not need to
set these style colors to anything but `implot.AUTO_COL`; you are
probably better off changing the current colormap. However, if you
need to explicitly color a particular item you may either Push/Pop
the style color around the item in question, or use the `set_next_*_style()`
API below. If you permanently set one of these style colors to a specific
color, or forget to call Pop, then all subsequent items will be styled
with the color you set.

2. For style colors associated with plot styling (e.g. `Col.PLOT_BG`),
`implot.AUTO_COL` tells ImPlot to set that color from color data in your
`imgui.Style`. The `imgui.Col` that these style colors default to are
detailed above, and in general have been mapped to produce plots visually
consistent with your current ImGui style. Of course, you are free to
manually set these colors to whatever you like, and further can Push/Pop
them around individual plots for plot-specific styling (e.g. coloring axes).

::: api-signature
```python
def get_style() -> slimgui.slimgui_ext.implot.Style:
    """
    Provides access to plot style structure for permanant modifications to colors, sizes, etc.
    """
```
:::

::: api-signature
```python
def style_colors_auto(
    dst: Style | None = None,
) -> None:
    """
    Style plot colors for current ImGui style (default).
    """
```
:::

::: api-signature
```python
def style_colors_classic(
    dst: Style | None = None,
) -> None:
    """
    Style plot colors for ImGui "Classic".
    """
```
:::

::: api-signature
```python
def style_colors_dark(
    dst: Style | None = None,
) -> None:
    """
    Style plot colors for ImGui "Dark".
    """
```
:::

::: api-signature
```python
def style_colors_light(
    dst: Style | None = None,
) -> None:
    """
    Style plot colors for ImGui "Light".
    """
```
:::

Use `push_style_*` to temporarily modify your `implot.Style`. The modification
will last until the matching call to `pop_style_*`. You MUST call a pop for
every push, otherwise you will leak memory! This behaves just like ImGui.

::: api-signature
```python
def push_style_color(
    idx: Col,
    col: int,
) -> None:
    """
    Temporarily modify a style color. Don't forget to call `implot.pop_style_color()`!
    """
```
:::

::: api-signature
```python
def push_style_color(
    idx: Col,
    col: tuple[float, float, float, float],
) -> None:
    """
    Temporarily modify a style color. Don't forget to call `implot.pop_style_color()`!
    """
```
:::

::: api-signature
```python
def pop_style_color(
    count: int = 1,
) -> None:
    """
    Undo temporary style color modification(s). Undo multiple pushes at once by increasing count.
    """
```
:::

::: api-signature
```python
def push_style_var(
    idx: StyleVar,
    val: int,
) -> None:
    """
    Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!
    """
```
:::

::: api-signature
```python
def push_style_var(
    idx: StyleVar,
    val: float,
) -> None:
    """
    Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!
    """
```
:::

::: api-signature
```python
def push_style_var(
    idx: StyleVar,
    val: tuple[float, float],
) -> None:
    """
    Temporarily modify a style variable of int type. Don't forget to call `implot.pop_style_var()`!
    """
```
:::

Temporarily modify a style variable of float 2-tuple. Don't forget to call `implot.pop_style_var()`!

::: api-signature
```python
def pop_style_var(
    count: int = 1,
) -> None:
    """
    Undo temporary style variable modification(s). Undo multiple pushes at once by increasing count.
    """
```
:::

The following can be used to modify the style of the next plot item ONLY. They do
NOT require calls to `pop_style_*`. Leave style attributes you don't want modified to
`implot.AUTO` or `implot.AUTO_COL`. Automatic styles will be deduced from the current
values in your `implot.Style` or from Colormap data.

::: api-signature
```python
def set_next_line_style(
    col: tuple[float, float, float, float] = AUTO_COL,
    weight: float = AUTO,
) -> None:
    """
    Set the line color and weight for the next item only.
    """
```
:::

::: api-signature
```python
def set_next_fill_style(
    col: tuple[float, float, float, float] = AUTO_COL,
    alpha_mod: float = AUTO,
) -> None:
    """
    Set the fill color for the next item only.
    """
```
:::

::: api-signature
```python
def set_next_marker_style(
    marker: Marker | int = AUTO,
    size: float = AUTO,
    fill: tuple[float, float, float, float] = AUTO_COL,
    weight: float = AUTO,
    outline: tuple[float, float, float, float] = AUTO_COL,
) -> None:
    """
    Set the marker style for the next item only.
    """
```
:::

::: api-signature
```python
def set_next_error_bar_style(
    col: tuple[float, float, float, float] = AUTO_COL,
    size: float = AUTO,
    weight: float = AUTO,
) -> None:
    """
    Set the error bar style for the next item only.
    """
```
:::

::: api-signature
```python
def get_last_item_color() -> tuple[float, float, float, float]:
    """
    Gets the last item primary color (i.e. its legend icon color)
    """
```
:::

::: api-signature
```python
def get_style_color_name(
    idx: Col,
) -> str:
    """
    Returns the string name for an `implot.Col`.
    """
```
:::

::: api-signature
```python
def get_marker_name(
    idx: Marker,
) -> str:
    """
    Returns the string name for an ImPlotMarker.
    """
```
:::

### Colormaps

Item styling is based on colormaps when the relevant `implot.Col.*` is set to
`implot.AUTO_COL` (default). Several built-in colormaps are available. You can
add and then push/pop your own colormaps as well. To permanently set a colormap,
modify the Colormap index member of your `implot.Style`.

Colormap data will be ignored and a custom color will be used if you have done one of the following:

1. Modified an item style color in your `implot.Style` to anything other than `implot.AUTO_COL`.
2. Pushed an item style color using `push_style_color()`.
3. Set the next item style with a `set_next_*_style()` function.

::: api-signature
```python
def get_colormap_count() -> int:
    """
    Returns the number of available colormaps (i.e. the built-in + user-added count).
    """
```
:::

::: api-signature
```python
def get_colormap_name(
    cmap: Colormap,
) -> str:
    """
    Returns a string name for a colormap given an index. Returns `None` if index is invalid.
    """
```
:::

::: api-signature
```python
def get_colormap_index(
    name: str,
) -> int:
    """
    Returns an index number for a colormap given a valid string name. Returns -1 if name is invalid.
    """
```
:::

::: api-signature
```python
def push_colormap(
    cmap: Colormap,
) -> None:
    """
    Temporarily switch to one of the built-in (i.e. ImPlotColormap_XXX) or user-added colormaps (i.e. a return value of `implot.add_colormap()`). Don't forget to call `implot.pop_colormap()`!
    """
```
:::

::: api-signature
```python
def push_colormap(
    name: str,
) -> None:
    """
    Temporarily switch to one of the built-in (i.e. ImPlotColormap_XXX) or user-added colormaps (i.e. a return value of `implot.add_colormap()`). Don't forget to call `implot.pop_colormap()`!
    """
```
:::

Push a colormap by string name. Use built-in names such as "Default", "Deep", "Jet", etc. or a string you provided to `implot.add_colormap(). Don't forget to call `implot.pop_colormap()`!

::: api-signature
```python
def pop_colormap(
    count: int = 1,
) -> None:
    """
    Undo temporary colormap modification(s). Undo multiple pushes at once by increasing count.
    """
```
:::

::: api-signature
```python
def next_colormap_color() -> tuple[float, float, float, float]:
    """
    Returns the next color from the current colormap and advances the colormap for the current plot.

    Can also be used with no return value to skip colors if desired. You need to call this between `implot.begin_plot()`/`implot.end_plot()`!
    """
```
:::

Returns the next color from the current colormap and advances the colormap for the current plot.

Can also be used with no return value to skip colors if desired. You need to call this between `implot.begin_plot()`/`implot.end_plot()`!

Colormap utils. If cmap = `implot.AUTO_COL` (default), the current colormap is assumed.
Pass an explicit colormap index (built-in or user-added) to specify otherwise.

::: api-signature
```python
def get_colormap_size(
    cmap: Colormap | int = AUTO,
) -> int:
    """
    Returns the size of a colormap.
    """
```
:::

::: api-signature
```python
def get_colormap_color(
    idx: int,
    cmap: Colormap | int = AUTO,
) -> tuple[float, float, float, float]:
    """
    Returns a color from a colormap given an index >= 0 (modulo will be performed).
    """
```
:::

::: api-signature
```python
def sample_colormap(
    t: float,
    cmap: Colormap | int = AUTO,
) -> tuple[float, float, float, float]:
    """
    Sample a color from the current colormap given t between 0 and 1.
    """
```
:::

::: api-signature
```python
def colormap_scale(
    label: str,
    scale_min: float,
    scale_max: float,
    size: tuple[float, float] = (0,0),
    format: str = '%g',
    flags: ColormapScaleFlags = ColormapScaleFlags.NONE,
    cmap: Colormap | int = AUTO,
) -> None:
    """
    Shows a vertical color scale with linear spaced ticks using the specified color map. Use double hashes to hide label (e.g. "##NoLabel"). If `scale_min > scale_max`, the scale to color mapping will be reversed.
    """
```
:::

::: api-signature
```python
def colormap_button(
    label: str,
    size: tuple[float, float] = (0,0),
    cmap: Colormap | int = AUTO,
) -> bool:
    """
    Shows a button with a colormap gradient brackground.
    """
```
:::

::: api-signature
```python
def bust_color_cache(
    plot_title_id: str | None = None,
) -> None:
    """
    When items in a plot sample their color from a colormap, the color is cached and does not change
    unless explicitly overriden. Therefore, if you change the colormap after the item has already been plotted,
    item colors will NOT update. If you need item colors to resample the new colormap, then use this
    function to bust the cached colors. If #plot_title_id is nullptr, then every item in EVERY existing plot
    will be cache busted. Otherwise only the plot specified by #plot_title_id will be busted. For the
    latter, this function must be called in the same ImGui ID scope that the plot is in. You should rarely if ever
    need this function, but it is available for applications that require runtime colormap swaps (e.g. Heatmaps demo).
    """
```
:::

### Input Mapping

::: api-signature
```python
def get_input_map() -> slimgui.slimgui_ext.implot.InputMap:
    """
    Provides access to input mapping structure for permanant modifications to controls for pan, select, etc.
    """
```
:::

::: api-signature
```python
def map_input_default(
    dst: InputMap | None = None,
) -> None:
    """
    Default input mapping: pan = LMB drag, box select = RMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll.
    """
```
:::

::: api-signature
```python
def map_input_reverse(
    dst: InputMap | None = None,
) -> None:
    """
    Reverse input mapping: pan = RMB drag, box select = LMB drag, fit = LMB double click, context menu = RMB click, zoom = scroll.
    """
```
:::

### Miscellaneous

::: api-signature
```python
def item_icon(
    col: tuple[float, float, float, float],
) -> None:
    """
    Render icons similar to those that appear in legends (nifty for data lists).
    """
```
:::

::: api-signature
```python
def item_icon(
    col: int,
) -> None:
    """
    Render icons similar to those that appear in legends (nifty for data lists).
    """
```
:::

::: api-signature
```python
def colormap_icon(
    cmap: Colormap,
) -> None:
    """
    Render icons similar to those that appear in legends (nifty for data lists).
    """
```
:::

::: api-signature
```python
def get_plot_draw_list() -> slimgui.slimgui_ext.imgui.DrawList:
    """
    Get the plot draw list for custom rendering to the current plot area. Call between Begin/EndPlot.
    """
```
:::

::: api-signature
```python
def push_plot_clip_rect(
    expand: float = 0,
) -> None:
    """
    Push clip rect for rendering to current plot area. The rect can be expanded or contracted by #expand pixels. Call between `implot.begin_plot()`/`implot.end_plot()`.
    """
```
:::

::: api-signature
```python
def pop_plot_clip_rect() -> None:
    """
    Pop plot clip rect. Call between `implot.begin_plot()`/`implot.end_plot()`.
    """
```
:::

::: api-signature
```python
def show_style_selector(
    label: str,
) -> bool:
    """
    Shows ImPlot style selector dropdown menu.
    """
```
:::

::: api-signature
```python
def show_colormap_selector(
    label: str,
) -> bool:
    """
    Shows ImPlot colormap selector dropdown menu.
    """
```
:::

::: api-signature
```python
def show_input_map_selector(
    label: str,
) -> bool:
    """
    Shows ImPlot input map selector dropdown menu.
    """
```
:::

::: api-signature
```python
def show_style_editor(
    ref: Style | None = None,
) -> None:
    """
    Shows ImPlot style editor block (not a window).
    """
```
:::

::: api-signature
```python
def show_user_guide() -> None:
    """
    Add basic help/info block for end users (not a window).
    """
```
:::

::: api-signature
```python
def show_metrics_window(
    closable: bool = False,
) -> bool:
    """
    Shows ImPlot metrics/debug information window.
    """
```
:::

### Demo

::: api-signature
```python
def show_demo_window(
    closable: bool = False,
) -> bool:
    """
    Shows the ImPlot demo window.
    """
```
:::

## Enum Reference

### Enum: Axis

| Name | Description |
| --- | --- |
| X1 | Enabled by default |
| X2 | Disabled by default |
| X3 | Disabled by default |
| Y1 | Enabled by default |
| Y2 | Disabled by default |
| Y3 | Disabled by default |
| COUNT |  |

### Enum: Bin

| Name | Description |
| --- | --- |
| SQRT | K = sqrt(n) |
| STURGES | K = 1 + log2(n) |
| RICE | K = 2 * cbrt(n) |
| SCOTT | W = 3.49 * sigma / cbrt(n) |

### Enum: Col

| Name | Description |
| --- | --- |
| LINE | Plot line/outline color (defaults to next unused color in current colormap) |
| FILL | Plot fill color for bars (defaults to the current line color) |
| MARKER_OUTLINE | Marker outline color (defaults to the current line color) |
| MARKER_FILL | Marker fill color (defaults to the current line color) |
| ERROR_BAR | Error bar color (defaults to `Col.TEXT`) |
| FRAME_BG | Plot frame background color (defaults to `Col.FRAME_BG`) |
| PLOT_BG | Plot area background color (defaults to `Col.WINDOW_BG`) |
| PLOT_BORDER | Plot area border color (defaults to `Col.BORDER`) |
| LEGEND_BG | Legend background color (defaults to `Col.POPUP_BG`) |
| LEGEND_BORDER | Legend border color (defaults to `Col.PLOT_BORDER`) |
| LEGEND_TEXT | Legend text color (defaults to `Col.INLAY_TEXT`) |
| TITLE_TEXT | Plot title text color (defaults to `Col.TEXT`) |
| INLAY_TEXT | Color of text appearing inside of plots (defaults to `Col.TEXT`) |
| AXIS_TEXT | Axis label and tick lables color (defaults to `Col.TEXT`) |
| AXIS_GRID | Axis grid color (defaults to 25% `Col.AXIS_TEXT`) |
| AXIS_TICK | Axis tick color (defaults to AxisGrid) |
| AXIS_BG | Background color of axis hover region (defaults to transparent) |
| AXIS_BG_HOVERED | Axis hover color (defaults to `Col.BUTTON_HOVERED`) |
| AXIS_BG_ACTIVE | Axis active color (defaults to `Col.BUTTON_ACTIVE`) |
| SELECTION | Box-selection color (defaults to yellow) |
| CROSSHAIRS | Crosshairs color (defaults to `Col.PLOT_BORDER`) |
| COUNT |  |

### Enum: Colormap

| Name | Description |
| --- | --- |
| DEEP | A.k.a. seaborn deep             (qual=true,  n=10) (default) |
| DARK | A.k.a. matplotlib "Set1"        (qual=true,  n=9 ) |
| PASTEL | A.k.a. matplotlib "Pastel1"     (qual=true,  n=9 ) |
| PAIRED | A.k.a. matplotlib "Paired"      (qual=true,  n=12) |
| VIRIDIS | A.k.a. matplotlib "viridis"     (qual=false, n=11) |
| PLASMA | A.k.a. matplotlib "plasma"      (qual=false, n=11) |
| HOT | A.k.a. matplotlib/MATLAB "hot"  (qual=false, n=11) |
| COOL | A.k.a. matplotlib/MATLAB "cool" (qual=false, n=11) |
| PINK | A.k.a. matplotlib/MATLAB "pink" (qual=false, n=11) |
| JET | A.k.a. MATLAB "jet"             (qual=false, n=11) |
| TWILIGHT | A.k.a. matplotlib "twilight"    (qual=false, n=11) |
| RD_BU | Red/blue, Color Brewer          (qual=false, n=11) |
| BR_BG | Brown/blue-green, Color Brewer  (qual=false, n=11) |
| PI_YG | Pink/yellow-green, Color Brewer (qual=false, n=11) |
| SPECTRAL | Color spectrum, Color Brewer    (qual=false, n=11) |
| GREYS | White/black                     (qual=false, n=2 ) |

### Enum: Cond

| Name | Description |
| --- | --- |
| NONE | No condition (always set the variable), same as _Always |
| ALWAYS | No condition (always set the variable) |
| ONCE | Set the variable once per runtime session (only the first call will succeed) |

### Enum: Location

| Name | Description |
| --- | --- |
| CENTER | Center-center |
| NORTH | Top-center |
| SOUTH | Bottom-center |
| WEST | Center-left |
| EAST | Center-right |
| NORTH_WEST | Top-left |
| NORTH_EAST | Top-right |
| SOUTH_WEST | Bottom-left |
| SOUTH_EAST | Bottom-right |

### Enum: Marker

| Name | Description |
| --- | --- |
| NONE | No marker |
| CIRCLE | A circle marker (default) |
| SQUARE | A square maker |
| DIAMOND | A diamond marker |
| UP | An upward-pointing triangle marker |
| DOWN | An downward-pointing triangle marker |
| LEFT | An leftward-pointing triangle marker |
| RIGHT | An rightward-pointing triangle marker |
| CROSS | A cross marker (not fillable) |
| PLUS | A plus marker (not fillable) |
| ASTERISK | A asterisk marker (not fillable) |
| COUNT |  |

### Enum: Scale

| Name | Description |
| --- | --- |
| LINEAR | Default linear scale |
| TIME | Date/time scale |
| LOG10 | Base 10 logartithmic scale |
| SYM_LOG | Symmetric log scale |

### Enum: StyleVar

| Name | Description |
| --- | --- |
| LINE_WEIGHT | Float,  plot item line weight in pixels |
| MARKER | Int,    marker specification |
| MARKER_SIZE | Float,  marker size in pixels (roughly the marker's "radius") |
| MARKER_WEIGHT | Float,  plot outline weight of markers in pixels |
| FILL_ALPHA | Float,  alpha modifier applied to all plot item fills |
| ERROR_BAR_SIZE | Float,  error bar whisker width in pixels |
| ERROR_BAR_WEIGHT | Float,  error bar whisker weight in pixels |
| DIGITAL_BIT_HEIGHT | Float,  digital channels bit height (at 1) in pixels |
| DIGITAL_BIT_GAP | Float,  digital channels bit padding gap in pixels |
| PLOT_BORDER_SIZE | Float,  thickness of border around plot area |
| MINOR_ALPHA | Float,  alpha multiplier applied to minor axis grid lines |
| MAJOR_TICK_LEN | ImVec2, major tick lengths for X and Y axes |
| MINOR_TICK_LEN | ImVec2, minor tick lengths for X and Y axes |
| MAJOR_TICK_SIZE | ImVec2, line thickness of major ticks |
| MINOR_TICK_SIZE | ImVec2, line thickness of minor ticks |
| MAJOR_GRID_SIZE | ImVec2, line thickness of major grid lines |
| MINOR_GRID_SIZE | ImVec2, line thickness of minor grid lines |
| PLOT_PADDING | ImVec2, padding between widget frame and plot area, labels, or outside legends (i.e. main padding) |
| LABEL_PADDING | ImVec2, padding between axes labels, tick labels, and plot edge |
| LEGEND_PADDING | ImVec2, legend padding from plot edges |
| LEGEND_INNER_PADDING | ImVec2, legend inner padding from legend edges |
| LEGEND_SPACING | ImVec2, spacing between legend entries |
| MOUSE_POS_PADDING | ImVec2, padding between plot edge and interior info text |
| ANNOTATION_PADDING | ImVec2, text padding around annotation labels |
| FIT_PADDING | ImVec2, additional fit padding as a percentage of the fit extents (e.g. ImVec2(0.1f,0.1f) adds 10% to the fit extents of X and Y) |
| PLOT_DEFAULT_SIZE | ImVec2, default size used when ImVec2(0,0) is passed to BeginPlot |
| PLOT_MIN_SIZE | ImVec2, minimum size plot frame can be when shrunk |
| COUNT |  |

### Enum: AxisFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_LABEL | The axis label will not be displayed (axis labels are also hidden if the supplied string name is nullptr) |
| NO_GRID_LINES | No grid lines will be displayed |
| NO_TICK_MARKS | No tick marks will be displayed |
| NO_TICK_LABELS | No text labels will be displayed |
| NO_INITIAL_FIT | Axis will not be initially fit to data extents on the first rendered frame |
| NO_MENUS | The user will not be able to open context menus with right-click |
| NO_SIDE_SWITCH | The user will not be able to switch the axis side by dragging it |
| NO_HIGHLIGHT | The axis will not have its background highlighted when hovered or held |
| OPPOSITE | Axis ticks and labels will be rendered on the conventionally opposite side (i.e, right or top) |
| FOREGROUND | Grid lines will be displayed in the foreground (i.e. on top of data) instead of the background |
| INVERT | The axis will be inverted |
| AUTO_FIT | Axis will be auto-fitting to data extents |
| RANGE_FIT | Axis will only fit points if the point is in the visible range of the **orthogonal** axis |
| PAN_STRETCH | Panning in a locked or constrained state will cause the axis to stretch if possible |
| LOCK_MIN | The axis minimum value will be locked when panning/zooming |
| LOCK_MAX | The axis maximum value will be locked when panning/zooming |
| LOCK |  |
| NO_DECORATIONS |  |
| AUX_DEFAULT |  |

### Enum: BarGroupsFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Bar groups will be rendered horizontally on the current y-axis |
| STACKED | Items in a group will be stacked on top of each other |

### Enum: BarsFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Bars will be rendered horizontally on the current y-axis |

### Enum: ColormapScaleFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_LABEL | The colormap axis label will not be displayed |
| OPPOSITE | Render the colormap label and tick labels on the opposite side |
| INVERT | Invert the colormap bar and axis scale (this only affects rendering; if you only want to reverse the scale mapping, make scale_min > scale_max) |

### Enum: DigitalFlags

| Name | Description |
| --- | --- |
| NONE | Default |

### Enum: DragToolFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_CURSORS | Drag tools won't change cursor icons when hovered or held |
| NO_FIT | The drag tool won't be considered for plot fits |
| NO_INPUTS | Lock the tool from user inputs |
| DELAYED | Tool rendering will be delayed one frame; useful when applying position-constraints |

### Enum: DummyFlag

| Name | Description |
| --- | --- |
| NONE | Default |

### Enum: ErrorBarsFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Error bars will be rendered horizontally on the current y-axis |

### Enum: HeatmapFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| COL_MAJOR | Data will be read in column major order |

### Enum: HistogramFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Histogram bars will be rendered horizontally (not supported by PlotHistogram2D) |
| CUMULATIVE | Each bin will contain its count plus the counts of all previous bins (not supported by PlotHistogram2D) |
| DENSITY | Counts will be normalized, i.e. the PDF will be visualized, or the CDF will be visualized if Cumulative is also set |
| NO_OUTLIERS | Exclude values outside the specifed histogram range from the count toward normalizing and cumulative counts |
| COL_MAJOR | Data will be read in column major order (not supported by `plot_histogram`) |

### Enum: ImageFlag

| Name | Description |
| --- | --- |
| NONE | Default |

### Enum: InfLinesFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Lines will be rendered horizontally on the current y-axis |

### Enum: ItemFlags

| Name | Description |
| --- | --- |
| NONE |  |
| NO_LEGEND | The item won't have a legend entry displayed |
| NO_FIT | The item won't be considered for plot fits |

### Enum: LegendFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_BUTTONS | Legend icons will not function as hide/show buttons |
| NO_HIGHLIGHT_ITEM | Plot items will not be highlighted when their legend entry is hovered |
| NO_HIGHLIGHT_AXIS | Axes will not be highlighted when legend entries are hovered (only relevant if x/y-axis count > 1) |
| NO_MENUS | The user will not be able to open context menus with right-click |
| OUTSIDE | Legend will be rendered outside of the plot area |
| HORIZONTAL | Legend entries will be displayed horizontally |
| SORT | Legend entries will be displayed in alphabetical order |

### Enum: LineFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| SEGMENTS | A line segment will be rendered from every two consecutive points |
| LOOP | The last and first point will be connected to form a closed loop |
| SKIP_NA_N | NaNs values will be skipped instead of rendered as missing data |
| NO_CLIP | Markers (if displayed) on the edge of a plot will not be clipped |
| SHADED | A filled region between the line and horizontal origin will be rendered; use PlotShaded for more advanced cases |

### Enum: MouseTextFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_AUX_AXES | Only show the mouse position for primary axes |
| NO_FORMAT | Axes label formatters won't be used to render text |
| SHOW_ALWAYS | Always display mouse position even if plot not hovered |

### Enum: PieChartFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NORMALIZE | Force normalization of pie chart values (i.e. always make a full circle if sum < 0) |
| IGNORE_HIDDEN | Ignore hidden slices when drawing the pie chart (as if they were not there) |
| EXPLODING | Explode legend-hovered slice |

### Enum: PlotFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_TITLE | The plot title will not be displayed (titles are also hidden if preceeded by double hashes, e.g. "##MyPlot") |
| NO_LEGEND | The legend will not be displayed |
| NO_MOUSE_TEXT | The mouse position, in plot coordinates, will not be displayed inside of the plot |
| NO_INPUTS | The user will not be able to interact with the plot |
| NO_MENUS | The user will not be able to open context menus |
| NO_BOX_SELECT | The user will not be able to box-select |
| NO_FRAME | The ImGui frame will not be rendered |
| EQUAL | X and y axes pairs will be constrained to have the same units/pixel |
| CROSSHAIRS | The default mouse cursor will be replaced with a crosshair when hovered |
| CANVAS_ONLY |  |

### Enum: ScatterFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_CLIP | Markers on the edge of a plot will not be clipped |

### Enum: ShadedFlags

| Name | Description |
| --- | --- |
| NONE | Default |

### Enum: StairsFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| PRE_STEP | The y value is continued constantly to the left from every x position, i.e. the interval (x[i-1], x[i]] has the value y[i] |
| SHADED | A filled region between the stairs and horizontal origin will be rendered; use PlotShaded for more advanced cases |

### Enum: StemsFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| HORIZONTAL | Stems will be rendered horizontally on the current y-axis |

### Enum: SubplotFlags

| Name | Description |
| --- | --- |
| NONE | Default |
| NO_TITLE | The subplot title will not be displayed (titles are also hidden if preceeded by double hashes, e.g. "##MySubplot") |
| NO_LEGEND | The legend will not be displayed (only applicable if `SubplotFlags.SHARE_ITEMS` is enabled) |
| NO_MENUS | The user will not be able to open context menus with right-click |
| NO_RESIZE | Resize splitters between subplot cells will be not be provided |
| NO_ALIGN | Subplot edges will not be aligned vertically or horizontally |
| SHARE_ITEMS | Items across all subplots will be shared and rendered into a single legend entry |
| LINK_ROWS | Link the y-axis limits of all plots in each row (does not apply to auxiliary axes) |
| LINK_COLS | Link the x-axis limits of all plots in each column (does not apply to auxiliary axes) |
| LINK_ALL_X | Link the x-axis limits in every plot in the subplot (does not apply to auxiliary axes) |
| LINK_ALL_Y | Link the y-axis limits in every plot in the subplot (does not apply to auxiliary axes) |
| COL_MAJOR | Subplots are added in column major order instead of the default row major order |

### Enum: TextFlag

| Name | Description |
| --- | --- |
| NONE | Default |
| VERTICAL | Text will be rendered vertically |

