# Development

Prerequisites:
- clang-format for generating enums
  - macOS: `brew install clang-format`

MacOS:

```
python3 -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/wjakob/nanobind 'scikit-build-core[pyproject]' click glfw pyopengl numpy requests toml
bash full_build.sh
```

## How to run tests

```
# in project root directory:
pytest
```

## Docs build with filewatching

```
npx nodemon -w gen -w docs/template.html -w docs/apiref.md -x python gen/build_docs.py --pyi-file src/slimgui/slimgui_ext.pyi --output docs/index.html docs/apiref.md
```

## Updating imgui and cimgui metainfo when upgrading imgui

```
cd $ROOT_DIR
python gen/imgui_vendor.py
```

Edit the `imgui_vendor.py` script to pull newer versions.
