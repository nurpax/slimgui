import gen_utils

def test_docstring_fixer():
    txt = gen_utils.docstring_fixer("set next window background color alpha.")
    assert txt == "Set next window background color alpha."

    txt = gen_utils.docstring_fixer("you may also use ImGuiWindowFlags_NoBackground.")
    assert txt == "You may also use `WindowFlags.NO_BACKGROUND`."

    txt = gen_utils.docstring_fixer("so IsItemActivated() should be a function")
    assert txt == "So `is_item_activated()` should be a function"

    txt = gen_utils.docstring_fixer("so IsItemOomphed() is not known") # not an imgui function, tho looks like one
    assert txt == "So IsItemOomphed() is not known"

    txt = gen_utils.docstring_fixer("InvisibleButton(ImVec2(0.0f, 1.0f))")
    assert txt == "`invisible_button((0.0, 1.0))`"

    # disabled check
    #txt = gen_utils.docstring_fixer("1.0f") # not an imgui function, tho looks like one
    #assert txt == "1.0"

    txt = gen_utils.docstring_fixer("InvisibleButton(\"##label\", ImVec2(0.0f, 1.0f), ImGuiWindowFlags_NoBackground) xyzzy")
    assert txt == "`invisible_button(\"##label\", (0.0, 1.0), WindowFlags.NO_BACKGROUND)` xyzzy"
