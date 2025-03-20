#!/bin/bash

# Full build that builds the extension, the typing stub slimgui_ext.pyi, and all docs.
# This got a bit more complex so I don't know how to do this in cmake anymore.

# CI builds don't need to run this, as the .pyi file is checked into git.

set -e

# generate the enums
python gen/gen_nb_enums.py > src/im_enums.inl
pip install --no-build-isolation -ve .

python -m nanobind.stubgen -i build/cp312-abi3-macosx_15_0_arm64 -q -m slimgui_ext -o src/slimgui/slimgui_ext.pyi 
python gen/amend_func_docs.py --cimgui-definitions-file gen/cimgui/definitions.json --imgui-h src/c/imgui/imgui.h --pyi-file src/slimgui/slimgui_ext.pyi -o src/slimgui/slimgui_ext.pyi
python gen/build_docs.py --pyi-file src/slimgui/slimgui_ext.pyi --output docs/index.html docs/apiref.md
