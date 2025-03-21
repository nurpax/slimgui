# Development

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

## Docs build with filewatching

```
npx nodemon -w gen -w docs/template.html -w docs/apiref.md -x python gen/build_docs.py --pyi-file src/slimgui/slimgui_ext.pyi --output docs/index.html docs/apiref.md
```

## Updating imgui and cimgui metainfo when upgrading imgui

NOTE NOTE! imconfig.h contains slimgui changes!  Review after updating imgui.

```
- git clone https://github.com/cimgui/cimgui
- update the imgui folder in the cimgui checkout with an imgui source release
- cd generator && ./generator
- dump the generator/output contents into gen/cimgui
```
