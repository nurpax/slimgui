nb::enum_<ImAxis_>(m, "Axis", nb::is_arithmetic())
    .value("X1", ImAxis_X1, "Enabled by default")
    .value("X2", ImAxis_X2, "Disabled by default")
    .value("X3", ImAxis_X3, "Disabled by default")
    .value("Y1", ImAxis_Y1, "Enabled by default")
    .value("Y2", ImAxis_Y2, "Disabled by default")
    .value("Y3", ImAxis_Y3, "Disabled by default")
    .value("COUNT", ImAxis_COUNT);
nb::enum_<ImPlotFlags_>(m, "PlotFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotFlags_None, "Default")
    .value("NO_TITLE", ImPlotFlags_NoTitle,
           "The plot title will not be displayed (titles are also hidden if "
           "preceeded by double hashes, e.g. \"##MyPlot\")")
    .value("NO_LEGEND", ImPlotFlags_NoLegend,
           "The legend will not be displayed")
    .value("NO_MOUSE_TEXT", ImPlotFlags_NoMouseText,
           "The mouse position, in plot coordinates, will not be displayed "
           "inside of the plot")
    .value("NO_INPUTS", ImPlotFlags_NoInputs,
           "The user will not be able to interact with the plot")
    .value("NO_MENUS", ImPlotFlags_NoMenus,
           "The user will not be able to open context menus")
    .value("NO_BOX_SELECT", ImPlotFlags_NoBoxSelect,
           "The user will not be able to box-select")
    .value("NO_FRAME", ImPlotFlags_NoFrame,
           "The ImGui frame will not be rendered")
    .value(
        "EQUAL", ImPlotFlags_Equal,
        "X and y axes pairs will be constrained to have the same units/pixel")
    .value("CROSSHAIRS", ImPlotFlags_Crosshairs,
           "The default mouse cursor will be replaced with a crosshair when "
           "hovered")
    .value("CANVAS_ONLY", ImPlotFlags_CanvasOnly);
nb::enum_<ImPlotAxisFlags_>(m, "AxisFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotAxisFlags_None, "Default")
    .value("NO_LABEL", ImPlotAxisFlags_NoLabel,
           "The axis label will not be displayed (axis labels are also hidden "
           "if the supplied string name is nullptr)")
    .value("NO_GRID_LINES", ImPlotAxisFlags_NoGridLines,
           "No grid lines will be displayed")
    .value("NO_TICK_MARKS", ImPlotAxisFlags_NoTickMarks,
           "No tick marks will be displayed")
    .value("NO_TICK_LABELS", ImPlotAxisFlags_NoTickLabels,
           "No text labels will be displayed")
    .value("NO_INITIAL_FIT", ImPlotAxisFlags_NoInitialFit,
           "Axis will not be initially fit to data extents on the first "
           "rendered frame")
    .value("NO_MENUS", ImPlotAxisFlags_NoMenus,
           "The user will not be able to open context menus with right-click")
    .value("NO_SIDE_SWITCH", ImPlotAxisFlags_NoSideSwitch,
           "The user will not be able to switch the axis side by dragging it")
    .value("NO_HIGHLIGHT", ImPlotAxisFlags_NoHighlight,
           "The axis will not have its background highlighted when hovered or "
           "held")
    .value("OPPOSITE", ImPlotAxisFlags_Opposite,
           "Axis ticks and labels will be rendered on the conventionally "
           "opposite side (i.e, right or top)")
    .value("FOREGROUND", ImPlotAxisFlags_Foreground,
           "Grid lines will be displayed in the foreground (i.e. on top of "
           "data) instead of the background")
    .value("INVERT", ImPlotAxisFlags_Invert, "The axis will be inverted")
    .value("AUTO_FIT", ImPlotAxisFlags_AutoFit,
           "Axis will be auto-fitting to data extents")
    .value("RANGE_FIT", ImPlotAxisFlags_RangeFit,
           "Axis will only fit points if the point is in the visible range of "
           "the **orthogonal** axis")
    .value("PAN_STRETCH", ImPlotAxisFlags_PanStretch,
           "Panning in a locked or constrained state will cause the axis to "
           "stretch if possible")
    .value("LOCK_MIN", ImPlotAxisFlags_LockMin,
           "The axis minimum value will be locked when panning/zooming")
    .value("LOCK_MAX", ImPlotAxisFlags_LockMax,
           "The axis maximum value will be locked when panning/zooming")
    .value("LOCK", ImPlotAxisFlags_Lock)
    .value("NO_DECORATIONS", ImPlotAxisFlags_NoDecorations)
    .value("AUX_DEFAULT", ImPlotAxisFlags_AuxDefault);
nb::enum_<ImPlotSubplotFlags_>(m, "SubplotFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImPlotSubplotFlags_None, "Default")
    .value("NO_TITLE", ImPlotSubplotFlags_NoTitle,
           "The subplot title will not be displayed (titles are also hidden if "
           "preceeded by double hashes, e.g. \"##MySubplot\")")
    .value("NO_LEGEND", ImPlotSubplotFlags_NoLegend,
           "The legend will not be displayed (only applicable if "
           "`SubplotFlags.SHARE_ITEMS` is enabled)")
    .value("NO_MENUS", ImPlotSubplotFlags_NoMenus,
           "The user will not be able to open context menus with right-click")
    .value("NO_RESIZE", ImPlotSubplotFlags_NoResize,
           "Resize splitters between subplot cells will be not be provided")
    .value("NO_ALIGN", ImPlotSubplotFlags_NoAlign,
           "Subplot edges will not be aligned vertically or horizontally")
    .value("SHARE_ITEMS", ImPlotSubplotFlags_ShareItems,
           "Items across all subplots will be shared and rendered into a "
           "single legend entry")
    .value("LINK_ROWS", ImPlotSubplotFlags_LinkRows,
           "Link the y-axis limits of all plots in each row (does not apply to "
           "auxiliary axes)")
    .value("LINK_COLS", ImPlotSubplotFlags_LinkCols,
           "Link the x-axis limits of all plots in each column (does not apply "
           "to auxiliary axes)")
    .value("LINK_ALL_X", ImPlotSubplotFlags_LinkAllX,
           "Link the x-axis limits in every plot in the subplot (does not "
           "apply to auxiliary axes)")
    .value("LINK_ALL_Y", ImPlotSubplotFlags_LinkAllY,
           "Link the y-axis limits in every plot in the subplot (does not "
           "apply to auxiliary axes)")
    .value("COL_MAJOR", ImPlotSubplotFlags_ColMajor,
           "Subplots are added in column major order instead of the default "
           "row major order");
nb::enum_<ImPlotLegendFlags_>(m, "LegendFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImPlotLegendFlags_None, "Default")
    .value("NO_BUTTONS", ImPlotLegendFlags_NoButtons,
           "Legend icons will not function as hide/show buttons")
    .value(
        "NO_HIGHLIGHT_ITEM", ImPlotLegendFlags_NoHighlightItem,
        "Plot items will not be highlighted when their legend entry is hovered")
    .value("NO_HIGHLIGHT_AXIS", ImPlotLegendFlags_NoHighlightAxis,
           "Axes will not be highlighted when legend entries are hovered (only "
           "relevant if x/y-axis count > 1)")
    .value("NO_MENUS", ImPlotLegendFlags_NoMenus,
           "The user will not be able to open context menus with right-click")
    .value("OUTSIDE", ImPlotLegendFlags_Outside,
           "Legend will be rendered outside of the plot area")
    .value("HORIZONTAL", ImPlotLegendFlags_Horizontal,
           "Legend entries will be displayed horizontally")
    .value("SORT", ImPlotLegendFlags_Sort,
           "Legend entries will be displayed in alphabetical order");
nb::enum_<ImPlotMouseTextFlags_>(m, "MouseTextFlags", nb::is_flag(),
                                 nb::is_arithmetic())
    .value("NONE", ImPlotMouseTextFlags_None, "Default")
    .value("NO_AUX_AXES", ImPlotMouseTextFlags_NoAuxAxes,
           "Only show the mouse position for primary axes")
    .value("NO_FORMAT", ImPlotMouseTextFlags_NoFormat,
           "Axes label formatters won't be used to render text")
    .value("SHOW_ALWAYS", ImPlotMouseTextFlags_ShowAlways,
           "Always display mouse position even if plot not hovered");
nb::enum_<ImPlotDragToolFlags_>(m, "DragToolFlags", nb::is_flag(),
                                nb::is_arithmetic())
    .value("NONE", ImPlotDragToolFlags_None, "Default")
    .value("NO_CURSORS", ImPlotDragToolFlags_NoCursors,
           "Drag tools won't change cursor icons when hovered or held")
    .value("NO_FIT", ImPlotDragToolFlags_NoFit,
           "The drag tool won't be considered for plot fits")
    .value("NO_INPUTS", ImPlotDragToolFlags_NoInputs,
           "Lock the tool from user inputs")
    .value("DELAYED", ImPlotDragToolFlags_Delayed,
           "Tool rendering will be delayed one frame; useful when applying "
           "position-constraints");
nb::enum_<ImPlotColormapScaleFlags_>(m, "ColormapScaleFlags", nb::is_flag(),
                                     nb::is_arithmetic())
    .value("NONE", ImPlotColormapScaleFlags_None, "Default")
    .value("NO_LABEL", ImPlotColormapScaleFlags_NoLabel,
           "The colormap axis label will not be displayed")
    .value("OPPOSITE", ImPlotColormapScaleFlags_Opposite,
           "Render the colormap label and tick labels on the opposite side")
    .value("INVERT", ImPlotColormapScaleFlags_Invert,
           "Invert the colormap bar and axis scale (this only affects "
           "rendering; if you only want to reverse the scale mapping, make "
           "scale_min > scale_max)");
nb::enum_<ImPlotItemFlags_>(m, "ItemFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotItemFlags_None)
    .value("NO_LEGEND", ImPlotItemFlags_NoLegend,
           "The item won't have a legend entry displayed")
    .value("NO_FIT", ImPlotItemFlags_NoFit,
           "The item won't be considered for plot fits");
nb::enum_<ImPlotLineFlags_>(m, "LineFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotLineFlags_None, "Default")
    .value("SEGMENTS", ImPlotLineFlags_Segments,
           "A line segment will be rendered from every two consecutive points")
    .value("LOOP", ImPlotLineFlags_Loop,
           "The last and first point will be connected to form a closed loop")
    .value("SKIP_NA_N", ImPlotLineFlags_SkipNaN,
           "NaNs values will be skipped instead of rendered as missing data")
    .value("NO_CLIP", ImPlotLineFlags_NoClip,
           "Markers (if displayed) on the edge of a plot will not be clipped")
    .value("SHADED", ImPlotLineFlags_Shaded,
           "A filled region between the line and horizontal origin will be "
           "rendered; use PlotShaded for more advanced cases");
nb::enum_<ImPlotScatterFlags_>(m, "ScatterFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImPlotScatterFlags_None, "Default")
    .value("NO_CLIP", ImPlotScatterFlags_NoClip,
           "Markers on the edge of a plot will not be clipped");
nb::enum_<ImPlotStairsFlags_>(m, "StairsFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImPlotStairsFlags_None, "Default")
    .value("PRE_STEP", ImPlotStairsFlags_PreStep,
           "The y value is continued constantly to the left from every x "
           "position, i.e. the interval (x[i-1], x[i]] has the value y[i]")
    .value("SHADED", ImPlotStairsFlags_Shaded,
           "A filled region between the stairs and horizontal origin will be "
           "rendered; use PlotShaded for more advanced cases");
nb::enum_<ImPlotShadedFlags_>(m, "ShadedFlags", nb::is_flag(),
                              nb::is_arithmetic())
    .value("NONE", ImPlotShadedFlags_None, "Default");
nb::enum_<ImPlotBarsFlags_>(m, "BarsFlags", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotBarsFlags_None, "Default")
    .value("HORIZONTAL", ImPlotBarsFlags_Horizontal,
           "Bars will be rendered horizontally on the current y-axis");
nb::enum_<ImPlotBarGroupsFlags_>(m, "BarGroupsFlags", nb::is_flag(),
                                 nb::is_arithmetic())
    .value("NONE", ImPlotBarGroupsFlags_None, "Default")
    .value("HORIZONTAL", ImPlotBarGroupsFlags_Horizontal,
           "Bar groups will be rendered horizontally on the current y-axis")
    .value("STACKED", ImPlotBarGroupsFlags_Stacked,
           "Items in a group will be stacked on top of each other");
nb::enum_<ImPlotErrorBarsFlags_>(m, "ErrorBarsFlags", nb::is_flag(),
                                 nb::is_arithmetic())
    .value("NONE", ImPlotErrorBarsFlags_None, "Default")
    .value("HORIZONTAL", ImPlotErrorBarsFlags_Horizontal,
           "Error bars will be rendered horizontally on the current y-axis");
nb::enum_<ImPlotStemsFlags_>(m, "StemsFlags", nb::is_flag(),
                             nb::is_arithmetic())
    .value("NONE", ImPlotStemsFlags_None, "Default")
    .value("HORIZONTAL", ImPlotStemsFlags_Horizontal,
           "Stems will be rendered horizontally on the current y-axis");
nb::enum_<ImPlotInfLinesFlags_>(m, "InfLinesFlags", nb::is_flag(),
                                nb::is_arithmetic())
    .value("NONE", ImPlotInfLinesFlags_None, "Default")
    .value("HORIZONTAL", ImPlotInfLinesFlags_Horizontal,
           "Lines will be rendered horizontally on the current y-axis");
nb::enum_<ImPlotPieChartFlags_>(m, "PieChartFlags", nb::is_flag(),
                                nb::is_arithmetic())
    .value("NONE", ImPlotPieChartFlags_None, "Default")
    .value("NORMALIZE", ImPlotPieChartFlags_Normalize,
           "Force normalization of pie chart values (i.e. always make a full "
           "circle if sum < 0)")
    .value("IGNORE_HIDDEN", ImPlotPieChartFlags_IgnoreHidden,
           "Ignore hidden slices when drawing the pie chart (as if they were "
           "not there)")
    .value("EXPLODING", ImPlotPieChartFlags_Exploding,
           "Explode legend-hovered slice");
nb::enum_<ImPlotHeatmapFlags_>(m, "HeatmapFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImPlotHeatmapFlags_None, "Default")
    .value("COL_MAJOR", ImPlotHeatmapFlags_ColMajor,
           "Data will be read in column major order");
nb::enum_<ImPlotHistogramFlags_>(m, "HistogramFlags", nb::is_flag(),
                                 nb::is_arithmetic())
    .value("NONE", ImPlotHistogramFlags_None, "Default")
    .value("HORIZONTAL", ImPlotHistogramFlags_Horizontal,
           "Histogram bars will be rendered horizontally (not supported by "
           "PlotHistogram2D)")
    .value("CUMULATIVE", ImPlotHistogramFlags_Cumulative,
           "Each bin will contain its count plus the counts of all previous "
           "bins (not supported by PlotHistogram2D)")
    .value("DENSITY", ImPlotHistogramFlags_Density,
           "Counts will be normalized, i.e. the PDF will be visualized, or the "
           "CDF will be visualized if Cumulative is also set")
    .value("NO_OUTLIERS", ImPlotHistogramFlags_NoOutliers,
           "Exclude values outside the specifed histogram range from the count "
           "toward normalizing and cumulative counts")
    .value("COL_MAJOR", ImPlotHistogramFlags_ColMajor,
           "Data will be read in column major order (not supported by "
           "`plot_histogram`)");
nb::enum_<ImPlotDigitalFlags_>(m, "DigitalFlags", nb::is_flag(),
                               nb::is_arithmetic())
    .value("NONE", ImPlotDigitalFlags_None, "Default");
nb::enum_<ImPlotImageFlags_>(m, "ImageFlag", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotImageFlags_None, "Default");
nb::enum_<ImPlotTextFlags_>(m, "TextFlag", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotTextFlags_None, "Default")
    .value("VERTICAL", ImPlotTextFlags_Vertical,
           "Text will be rendered vertically");
nb::enum_<ImPlotDummyFlags_>(m, "DummyFlag", nb::is_flag(), nb::is_arithmetic())
    .value("NONE", ImPlotDummyFlags_None, "Default");
nb::enum_<ImPlotCond_>(m, "Cond", nb::is_arithmetic())
    .value("NONE", ImPlotCond_None,
           "No condition (always set the variable), same as _Always")
    .value("ALWAYS", ImPlotCond_Always,
           "No condition (always set the variable)")
    .value("ONCE", ImPlotCond_Once,
           "Set the variable once per runtime session (only the first call "
           "will succeed)");
nb::enum_<ImPlotCol_>(m, "Col", nb::is_arithmetic())
    .value("LINE", ImPlotCol_Line,
           "Plot line/outline color (defaults to next unused color in current "
           "colormap)")
    .value("FILL", ImPlotCol_Fill,
           "Plot fill color for bars (defaults to the current line color)")
    .value("MARKER_OUTLINE", ImPlotCol_MarkerOutline,
           "Marker outline color (defaults to the current line color)")
    .value("MARKER_FILL", ImPlotCol_MarkerFill,
           "Marker fill color (defaults to the current line color)")
    .value("ERROR_BAR", ImPlotCol_ErrorBar,
           "Error bar color (defaults to `Col.TEXT`)")
    .value("FRAME_BG", ImPlotCol_FrameBg,
           "Plot frame background color (defaults to `Col.FRAME_BG`)")
    .value("PLOT_BG", ImPlotCol_PlotBg,
           "Plot area background color (defaults to `Col.WINDOW_BG`)")
    .value("PLOT_BORDER", ImPlotCol_PlotBorder,
           "Plot area border color (defaults to `Col.BORDER`)")
    .value("LEGEND_BG", ImPlotCol_LegendBg,
           "Legend background color (defaults to `Col.POPUP_BG`)")
    .value("LEGEND_BORDER", ImPlotCol_LegendBorder,
           "Legend border color (defaults to `Col.PLOT_BORDER`)")
    .value("LEGEND_TEXT", ImPlotCol_LegendText,
           "Legend text color (defaults to `Col.INLAY_TEXT`)")
    .value("TITLE_TEXT", ImPlotCol_TitleText,
           "Plot title text color (defaults to `Col.TEXT`)")
    .value("INLAY_TEXT", ImPlotCol_InlayText,
           "Color of text appearing inside of plots (defaults to `Col.TEXT`)")
    .value("AXIS_TEXT", ImPlotCol_AxisText,
           "Axis label and tick lables color (defaults to `Col.TEXT`)")
    .value("AXIS_GRID", ImPlotCol_AxisGrid,
           "Axis grid color (defaults to 25% `Col.AXIS_TEXT`)")
    .value("AXIS_TICK", ImPlotCol_AxisTick,
           "Axis tick color (defaults to AxisGrid)")
    .value("AXIS_BG", ImPlotCol_AxisBg,
           "Background color of axis hover region (defaults to transparent)")
    .value("AXIS_BG_HOVERED", ImPlotCol_AxisBgHovered,
           "Axis hover color (defaults to `Col.BUTTON_HOVERED`)")
    .value("AXIS_BG_ACTIVE", ImPlotCol_AxisBgActive,
           "Axis active color (defaults to `Col.BUTTON_ACTIVE`)")
    .value("SELECTION", ImPlotCol_Selection,
           "Box-selection color (defaults to yellow)")
    .value("CROSSHAIRS", ImPlotCol_Crosshairs,
           "Crosshairs color (defaults to `Col.PLOT_BORDER`)")
    .value("COUNT", ImPlotCol_COUNT);
nb::enum_<ImPlotStyleVar_>(m, "StyleVar", nb::is_arithmetic())
    .value("LINE_WEIGHT", ImPlotStyleVar_LineWeight,
           "Float,  plot item line weight in pixels")
    .value("MARKER", ImPlotStyleVar_Marker, "Int,    marker specification")
    .value("MARKER_SIZE", ImPlotStyleVar_MarkerSize,
           "Float,  marker size in pixels (roughly the marker's \"radius\")")
    .value("MARKER_WEIGHT", ImPlotStyleVar_MarkerWeight,
           "Float,  plot outline weight of markers in pixels")
    .value("FILL_ALPHA", ImPlotStyleVar_FillAlpha,
           "Float,  alpha modifier applied to all plot item fills")
    .value("ERROR_BAR_SIZE", ImPlotStyleVar_ErrorBarSize,
           "Float,  error bar whisker width in pixels")
    .value("ERROR_BAR_WEIGHT", ImPlotStyleVar_ErrorBarWeight,
           "Float,  error bar whisker weight in pixels")
    .value("DIGITAL_BIT_HEIGHT", ImPlotStyleVar_DigitalBitHeight,
           "Float,  digital channels bit height (at 1) in pixels")
    .value("DIGITAL_BIT_GAP", ImPlotStyleVar_DigitalBitGap,
           "Float,  digital channels bit padding gap in pixels")
    .value("PLOT_BORDER_SIZE", ImPlotStyleVar_PlotBorderSize,
           "Float,  thickness of border around plot area")
    .value("MINOR_ALPHA", ImPlotStyleVar_MinorAlpha,
           "Float,  alpha multiplier applied to minor axis grid lines")
    .value("MAJOR_TICK_LEN", ImPlotStyleVar_MajorTickLen,
           "ImVec2, major tick lengths for X and Y axes")
    .value("MINOR_TICK_LEN", ImPlotStyleVar_MinorTickLen,
           "ImVec2, minor tick lengths for X and Y axes")
    .value("MAJOR_TICK_SIZE", ImPlotStyleVar_MajorTickSize,
           "ImVec2, line thickness of major ticks")
    .value("MINOR_TICK_SIZE", ImPlotStyleVar_MinorTickSize,
           "ImVec2, line thickness of minor ticks")
    .value("MAJOR_GRID_SIZE", ImPlotStyleVar_MajorGridSize,
           "ImVec2, line thickness of major grid lines")
    .value("MINOR_GRID_SIZE", ImPlotStyleVar_MinorGridSize,
           "ImVec2, line thickness of minor grid lines")
    .value("PLOT_PADDING", ImPlotStyleVar_PlotPadding,
           "ImVec2, padding between widget frame and plot area, labels, or "
           "outside legends (i.e. main padding)")
    .value("LABEL_PADDING", ImPlotStyleVar_LabelPadding,
           "ImVec2, padding between axes labels, tick labels, and plot edge")
    .value("LEGEND_PADDING", ImPlotStyleVar_LegendPadding,
           "ImVec2, legend padding from plot edges")
    .value("LEGEND_INNER_PADDING", ImPlotStyleVar_LegendInnerPadding,
           "ImVec2, legend inner padding from legend edges")
    .value("LEGEND_SPACING", ImPlotStyleVar_LegendSpacing,
           "ImVec2, spacing between legend entries")
    .value("MOUSE_POS_PADDING", ImPlotStyleVar_MousePosPadding,
           "ImVec2, padding between plot edge and interior info text")
    .value("ANNOTATION_PADDING", ImPlotStyleVar_AnnotationPadding,
           "ImVec2, text padding around annotation labels")
    .value("FIT_PADDING", ImPlotStyleVar_FitPadding,
           "ImVec2, additional fit padding as a percentage of the fit extents "
           "(e.g. ImVec2(0.1f,0.1f) adds 10% to the fit extents of X and Y)")
    .value("PLOT_DEFAULT_SIZE", ImPlotStyleVar_PlotDefaultSize,
           "ImVec2, default size used when ImVec2(0,0) is passed to BeginPlot")
    .value("PLOT_MIN_SIZE", ImPlotStyleVar_PlotMinSize,
           "ImVec2, minimum size plot frame can be when shrunk")
    .value("COUNT", ImPlotStyleVar_COUNT);
nb::enum_<ImPlotScale_>(m, "Scale", nb::is_arithmetic())
    .value("LINEAR", ImPlotScale_Linear, "Default linear scale")
    .value("TIME", ImPlotScale_Time, "Date/time scale")
    .value("LOG10", ImPlotScale_Log10, "Base 10 logartithmic scale")
    .value("SYM_LOG", ImPlotScale_SymLog, "Symmetric log scale");
nb::enum_<ImPlotMarker_>(m, "Marker", nb::is_arithmetic())
    .value("NONE", ImPlotMarker_None, "No marker")
    .value("CIRCLE", ImPlotMarker_Circle, "A circle marker (default)")
    .value("SQUARE", ImPlotMarker_Square, "A square maker")
    .value("DIAMOND", ImPlotMarker_Diamond, "A diamond marker")
    .value("UP", ImPlotMarker_Up, "An upward-pointing triangle marker")
    .value("DOWN", ImPlotMarker_Down, "An downward-pointing triangle marker")
    .value("LEFT", ImPlotMarker_Left, "An leftward-pointing triangle marker")
    .value("RIGHT", ImPlotMarker_Right, "An rightward-pointing triangle marker")
    .value("CROSS", ImPlotMarker_Cross, "A cross marker (not fillable)")
    .value("PLUS", ImPlotMarker_Plus, "A plus marker (not fillable)")
    .value("ASTERISK", ImPlotMarker_Asterisk,
           "A asterisk marker (not fillable)")
    .value("COUNT", ImPlotMarker_COUNT);
nb::enum_<ImPlotColormap_>(m, "Colormap", nb::is_arithmetic())
    .value("DEEP", ImPlotColormap_Deep,
           "A.k.a. seaborn deep             (qual=true,  n=10) (default)")
    .value("DARK", ImPlotColormap_Dark,
           "A.k.a. matplotlib \"Set1\"        (qual=true,  n=9 )")
    .value("PASTEL", ImPlotColormap_Pastel,
           "A.k.a. matplotlib \"Pastel1\"     (qual=true,  n=9 )")
    .value("PAIRED", ImPlotColormap_Paired,
           "A.k.a. matplotlib \"Paired\"      (qual=true,  n=12)")
    .value("VIRIDIS", ImPlotColormap_Viridis,
           "A.k.a. matplotlib \"viridis\"     (qual=false, n=11)")
    .value("PLASMA", ImPlotColormap_Plasma,
           "A.k.a. matplotlib \"plasma\"      (qual=false, n=11)")
    .value("HOT", ImPlotColormap_Hot,
           "A.k.a. matplotlib/MATLAB \"hot\"  (qual=false, n=11)")
    .value("COOL", ImPlotColormap_Cool,
           "A.k.a. matplotlib/MATLAB \"cool\" (qual=false, n=11)")
    .value("PINK", ImPlotColormap_Pink,
           "A.k.a. matplotlib/MATLAB \"pink\" (qual=false, n=11)")
    .value("JET", ImPlotColormap_Jet,
           "A.k.a. MATLAB \"jet\"             (qual=false, n=11)")
    .value("TWILIGHT", ImPlotColormap_Twilight,
           "A.k.a. matplotlib \"twilight\"    (qual=false, n=11)")
    .value("RD_BU", ImPlotColormap_RdBu,
           "Red/blue, Color Brewer          (qual=false, n=11)")
    .value("BR_BG", ImPlotColormap_BrBG,
           "Brown/blue-green, Color Brewer  (qual=false, n=11)")
    .value("PI_YG", ImPlotColormap_PiYG,
           "Pink/yellow-green, Color Brewer (qual=false, n=11)")
    .value("SPECTRAL", ImPlotColormap_Spectral,
           "Color spectrum, Color Brewer    (qual=false, n=11)")
    .value("GREYS", ImPlotColormap_Greys,
           "White/black                     (qual=false, n=2 )");
nb::enum_<ImPlotLocation_>(m, "Location", nb::is_arithmetic())
    .value("CENTER", ImPlotLocation_Center, "Center-center")
    .value("NORTH", ImPlotLocation_North, "Top-center")
    .value("SOUTH", ImPlotLocation_South, "Bottom-center")
    .value("WEST", ImPlotLocation_West, "Center-left")
    .value("EAST", ImPlotLocation_East, "Center-right")
    .value("NORTH_WEST", ImPlotLocation_NorthWest, "Top-left")
    .value("NORTH_EAST", ImPlotLocation_NorthEast, "Top-right")
    .value("SOUTH_WEST", ImPlotLocation_SouthWest, "Bottom-left")
    .value("SOUTH_EAST", ImPlotLocation_SouthEast, "Bottom-right");
nb::enum_<ImPlotBin_>(m, "Bin", nb::is_arithmetic())
    .value("SQRT", ImPlotBin_Sqrt, "K = sqrt(n)")
    .value("STURGES", ImPlotBin_Sturges, "K = 1 + log2(n)")
    .value("RICE", ImPlotBin_Rice, "K = 2 * cbrt(n)")
    .value("SCOTT", ImPlotBin_Scott, "W = 3.49 * sigma / cbrt(n)");
