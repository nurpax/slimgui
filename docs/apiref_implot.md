---
title: 'slimgui - ImPlot API'
subtitle: 'Python bindings for Dear ImGui'
---

# slimgui - ImPlot API reference

## Overview

The Slimgui package provides modern Python bindings for the following libraries:

 - [Dear ImGui](https://github.com/ocornut/imgui)
 - [ImPlot](https://github.com/epezent/implot)

The Python bindings documentation has been split into several parts:

- [Dear ImGui bindings reference](./index.html)
- ImPlot bindings API reference -- you're reading it.

The project source code is hosted on [github.com/nurpax/slimgui](https://github.com/nurpax/slimgui).

## Module naming

The below reference assumes the Python bindings are imported as:

```
from slimgui import imgui
from slimgui import implot
```

For example, a symbol like `slimgui_ext.imgui.MouseButton` will be written as `imgui.MouseButton`.

## Binding considerations for ImPlot

* TODO `np.ndarray` usage

## ImPlot Enums

A detailed enum and class reference can be found here: [Enum Reference](#enum-reference)

## ImPlot API functions

### Contexts

<div class="raw-html-insert" data-apirefs="create_context, destroy_context, get_current_context, set_current_context"></div>

### Begin/End Plot

<div class="raw-html-insert" data-apirefs="begin_plot, end_plot"></div>

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

<div class="raw-html-insert" data-apirefs="begin_subplots, end_subplots"></div>

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

<div class="raw-html-insert" data-apirefs="setup_axis,setup_axis_limits,setup_axis_links,setup_axis_format,setup_axis_ticks,setup_axis_scale,setup_axis_limits_constraints,setup_axis_zoom_constraints,setup_axes,setup_axes_limits,setup_legend,setup_mouse_text,setup_finish"></div>

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

<div class="raw-html-insert" data-apirefs="set_next_axis_limits,set_next_axis_links,set_next_axis_to_fit,set_next_axes_limits,set_next_axes_to_fit"></div>

### Plot Items

The main plotting API is provied below. Call these functions between
Begin/EndPlot and after any Setup API calls. Each plots data on the current
x and y axes, which can be changed with `set_axis()`/`set_axes()`.

NB: All types are converted to double before plotting. You may lose information
if you try plotting extremely large 64-bit integral types. Proceed with caution!

<div class="raw-html-insert" data-apirefs="plot_line,plot_scatter,plot_stairs,plot_shaded,plot_bars,plot_bar_groups,plot_error_bars,plot_pie_chart,plot_heatmap,plot_digital,plot_image,plot_text,plot_dummy"></div>

<div class="raw-html-insert" data-apirefs="plot_histogram,plot_histogram2d">

The `range` parameter in `plot_histogram2d` is typed as a pair of float 2-tuples.  The first element is the range `(min,max)` for `xs`, the second for `ys`.
</div>

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

<div class="raw-html-insert" data-apirefs="drag_point,drag_line_x,drag_line_y,drag_rect,annotation,tag_x,tag_y"></div>

### Plot Utils

<div class="raw-html-insert" data-apirefs="set_axis,set_axes,pixels_to_plot,plot_to_pixels,get_plot_pos,get_plot_size,get_plot_mouse_pos,get_plot_limits,is_plot_hovered,is_axis_hovered,is_subplots_hovered,is_plot_selected,get_plot_selection,cancel_plot_selection,hide_next_item"></div>

Use the following around calls to `begin_plot()`/`end_plot()` to align l/r/t/b padding.
Consider using `begin_subplots()`/`end_subplots()` first. They are more feature rich and
accomplish the same behaviour by default. The functions below offer lower
level control of plot alignment.

<div class="raw-html-insert" data-apirefs="begin_aligned_plots,end_aligned_plots"></div>

### Legend Utils

<div class="raw-html-insert" data-apirefs="begin_legend_popup,end_legend_popup,is_legend_entry_hovered"></div>

### Drag and Drop

<div class="raw-html-insert" data-apirefs="begin_drag_drop_target_plot,begin_drag_drop_target_axis,begin_drag_drop_target_legend,end_drag_drop_target"></div>

NB: By default, plot and axes drag and drop *sources* require holding the Ctrl modifier to initiate the drag.
You can change the modifier if desired. If `imgui.Key.MOD_NONE` is provided, the axes will be locked from panning.

<div class="raw-html-insert" data-apirefs="begin_drag_drop_source_plot,begin_drag_drop_source_axis,begin_drag_drop_source_item,end_drag_drop_source"></div>

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

<div class="raw-html-insert" data-apirefs="get_style,style_colors_auto,style_colors_classic,style_colors_dark,style_colors_light"></div>

Use `push_style_*` to temporarily modify your `implot.Style`. The modification
will last until the matching call to `pop_style_*`. You MUST call a pop for
every push, otherwise you will leak memory! This behaves just like ImGui.

<div class="raw-html-insert" data-apirefs="push_style_color,pop_style_color,push_style_var,pop_style_var"></div>

The following can be used to modify the style of the next plot item ONLY. They do
NOT require calls to `pop_style_*`. Leave style attributes you don't want modified to
`implot.AUTO` or `implot.AUTO_COL`. Automatic styles will be deduced from the current
values in your `implot.Style` or from Colormap data.

<div class="raw-html-insert" data-apirefs="set_next_line_style,set_next_fill_style,set_next_marker_style,set_next_error_bar_style,get_last_item_color,get_style_color_name,get_marker_name"></div>

### Colormaps

Item styling is based on colormaps when the relevant `implot.Col.*` is set to
`implot.AUTO_COL` (default). Several built-in colormaps are available. You can
add and then push/pop your own colormaps as well. To permanently set a colormap,
modify the Colormap index member of your `implot.Style`.

Colormap data will be ignored and a custom color will be used if you have done one of the following:

1. Modified an item style color in your `implot.Style` to anything other than `implot.AUTO_COL`.
2. Pushed an item style color using `push_style_color()`.
3. Set the next item style with a `set_next_*_style()` function.

<div class="raw-html-insert" data-apirefs="add_colormap,get_colormap_count,get_colormap_name,get_colormap_index,push_colormap,pop_colormap,next_colormap_color"></div>

Colormap utils. If cmap = `implot.AUTO_COL` (default), the current colormap is assumed.
Pass an explicit colormap index (built-in or user-added) to specify otherwise.

<div class="raw-html-insert" data-apirefs="get_colormap_size,get_colormap_color,sample_colormap,colormap_scale,colormap_slider,colormap_button,bust_color_cache"></div>

### Input Mapping

<div class="raw-html-insert" data-apirefs="get_input_map,map_input_default,map_input_reverse"></div>

### Miscellaneous

<div class="raw-html-insert" data-apirefs="item_icon,colormap_icon,get_plot_draw_list,push_plot_clip_rect,pop_plot_clip_rect,show_style_selector,show_colormap_selector,show_input_map_selector,show_style_editor,show_user_guide,show_metrics_window"></div>

### Demo

<div class="raw-html-insert" data-apirefs="show_demo_window"></div>

## Enum Reference

<div class="raw-html-insert" data-apirefs="Axis,Bin,Col,Colormap,Cond,Location,Marker,Scale,StyleVar,AxisFlags,BarGroupsFlags,BarsFlags,ColormapScaleFlags,DigitalFlags,DragToolFlags,DummyFlag,ErrorBarsFlags,HeatmapFlags,HistogramFlags,ImageFlag,InfLinesFlags,ItemFlags,LegendFlags,LineFlags,MouseTextFlags,PieChartFlags,PlotFlags,ScatterFlags,ShadedFlags,StairsFlags,StemsFlags,SubplotFlags,TextFlag"></div>
