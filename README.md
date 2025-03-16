# slimgui: Updated ImGui bindings for Python

Work in progress [Dear ImGui](https://github.com/ocornut/imgui) bindings for Python.

Motivation:
- Modernized build process to support Python typings (.pyi files) to allow good IDE support (auto-complete, type checking in VSCode)
- Closely match the Dear ImGui API but adapt for Python as necessary.  Don't invent new API concepts.

Very similar to [https://github.com/pyimgui/pyimgui](pyimgui/pyimugui) except built with Nanobind to better support typings.

## Development

Prerequisites:
- clang-format for generating enums
  - macOS: `brew install clang-format`

MacOS:

```
python3 -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/wjakob/nanobind 'scikit-build-core[pyproject]' click glfw pyopengl numpy requests
pip install --no-build-isolation -ve .
python gen/gen_nb_enums.py > src/im_enums.inl
```

Windows:

```
python3 -m venv .venv
.venv\Scripts\activate.bat
pip install git+https://github.com/wjakob/nanobind scikit-build-core[pyproject] click glfw pyopengl numpy
pip install --no-build-isolation -ve .
python gen\gen_nb_enums.py > src\im_enums.inl
```

### Doc build with filewatching

```
npx nodemon -w gen -w docs/template.html -w docs/apiref.md -x python gen/build_docs.py --pyi-file src/slimgui/slimgui_ext.pyi --output docs/apiref.html docs/apiref.md
```

### Updating cimgui metainfo when upgrading imgui

```
- git clone https://github.com/cimgui/cimgui
- update the imgui folder in the cimgui checkout with an imgui source release
- cd generator && ./generator
- dump the generator/output contents into gen/cimgui
```
