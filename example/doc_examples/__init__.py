from .buttons import button_simple, button_colors
from .implot import (
    plot_bar_groups_basic,
    plot_bars_basic,
    plot_line_basic,
    plot_line_values_only,
    plot_spec_marker_color_arrays,
    plot_scatter_basic,
)
from .layout import (
    layout_group_sizing,
    layout_item_width_patterns,
    layout_master_detail_tabs,
    layout_same_line_basics,
    layout_tabs_basic,
    layout_text_baseline_alignment,
)
from .styles import (
    styles_color_palette_popup,
    styles_edit_style_object,
    styles_preset_with_overrides,
    styles_scoped_push_pop,
)

font_url = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"
__all__ = ["font_url"]
__all__ += ["button_simple", "button_colors"]
__all__ += [
    "plot_line_basic",
    "plot_line_values_only",
    "plot_bars_basic",
    "plot_bar_groups_basic",
    "plot_scatter_basic",
    "plot_spec_marker_color_arrays",
]
__all__ += [
    "layout_master_detail_tabs",
    "layout_item_width_patterns",
    "layout_group_sizing",
    "layout_same_line_basics",
    "layout_text_baseline_alignment",
    "layout_tabs_basic",
]
__all__ += [
    "styles_edit_style_object",
    "styles_scoped_push_pop",
    "styles_preset_with_overrides",
    "styles_color_palette_popup",
]
