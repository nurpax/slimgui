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
python gen/gen_nb.py > src/im_enums.inl
```

Windows:

```
python3 -m venv .venv
.venv\Scripts\activate.bat
pip install git+https://github.com/wjakob/nanobind scikit-build-core[pyproject] click glfw pyopengl numpy
pip install --no-build-isolation -ve .
python gen\gen_nb.py > src\im_enums.inl
```

## Cimgui outputs for some API generation

Switch to v1.90.5 branch for imgui before running generator.bat.
