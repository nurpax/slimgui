
import slimgui as imgui

refcol = (0.1, 0.2, 0.4, 1)
editing_col = (0.5, 0.5, 0.5, 1)
col3 = (0.1, 0.5, 0.5)

def show():
    global editing_col, col3

    expanded, _ = imgui.collapsing_header("Widgets 2")
    if not expanded:
        return

    imgui.text("Random selection of widgets")
    _c, editing_col = imgui.color_picker4("##picker4", editing_col, imgui.ColorEditFlags.NO_SMALL_PREVIEW, refcol)
    imgui.text('Color btn'); imgui.same_line(); imgui.color_button("##color_button", editing_col)
    _c, col3 = imgui.color_picker3("##picker3", col3)

    # Text links & open URL
    imgui.text_link("Link##link"); imgui.same_line(); imgui.text_link_open_url("URL##url", "https://github.com/nurpax/slimgui")
