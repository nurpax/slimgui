#!/bin/bash

# Full build that builds the extension, the typing stub slimgui_ext.pyi, and all docs.
# This got a bit more complex so I don't know how to do this in cmake anymore.

# CI builds don't need to run this, as the .pyi file is checked into git.

set -e

# generate the enums
python gen/gen_nb_enums.py --cimgui-defs-dir gen/cimgui > src/imgui_enums.inl
python gen/gen_nb_enums.py --cimgui-defs-dir gen/cimplot > src/implot_enums.inl
python gen/gen_nb_funcs.py --cimgui-defs-dir gen/cimplot > src/implot_funcs.inl
pip install --no-build-isolation -v .

# Get the value of tool.slimgui.imgui_version from pyproject.toml and
# check that slimgui.imgui.get_version() returns the same value.  It's to ensure
# pyproject.toml imgui_version field is up to date.
IMGUI_VERSION=$(python -c "import toml; print(toml.load('pyproject.toml')['tool']['slimgui']['imgui_version'])")
python -c "from slimgui import imgui; assert imgui.get_version() == '$IMGUI_VERSION'"

python -m nanobind.stubgen -i build/cp312-abi3-macosx_15_0_arm64 -q -m slimgui_ext -r -O src/slimgui/slimgui_ext
mv src/slimgui/slimgui_ext/slimgui_ext.pyi src/slimgui/slimgui_ext/__init__.pyi
python gen/amend_func_docs.py --cimgui-definitions-file gen/cimgui/definitions.json --imgui-h src/c/imgui/imgui.h --pyi-file src/slimgui/slimgui_ext/imgui/__init__.pyi -o src/slimgui/slimgui_ext/imgui/__init__.pyi
python gen/build_docs.py --imgui-version=${IMGUI_VERSION} --pyi-file src/slimgui/slimgui_ext/imgui/__init__.pyi --output docs/index.html docs/apiref.md
