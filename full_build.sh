#!/bin/bash

# Full build that builds the extension, the typing stub slimgui_ext.pyi, and all docs.
# This got a bit more complex so I don't know how to do this in cmake anymore.

# CI builds don't need to run this, as the .pyi file is checked into git.

set -e

# generate the enums
python gen/gen_nb_enums.py > src/im_enums.inl
pip install --no-build-isolation -ve .

# Get the value of tool.slimgui.imgui_version from pyproject.toml and
# check that slimgui.get_version() returns the same value.  It's to ensure
# pyproject.toml imgui_version field is up to date.
IMGUI_VERSION=$(python -c "import toml; print(toml.load('pyproject.toml')['tool']['slimgui']['imgui_version'])")
python -c "import slimgui; assert slimgui.get_version() == '$IMGUI_VERSION'"

python -m nanobind.stubgen -i build/cp312-abi3-macosx_15_0_arm64 -q -m slimgui_ext -o src/slimgui/slimgui_ext.pyi 
python gen/amend_func_docs.py --cimgui-definitions-file gen/cimgui/definitions.json --imgui-h src/c/imgui/imgui.h --pyi-file src/slimgui/slimgui_ext.pyi -o src/slimgui/slimgui_ext.pyi
python gen/build_docs.py --imgui-version=${IMGUI_VERSION} --pyi-file src/slimgui/slimgui_ext.pyi --output docs/index.html docs/apiref.md
