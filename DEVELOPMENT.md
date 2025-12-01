# Development

Prerequisites:
- clang-format for generating enums
  - macOS: `brew install clang-format`

MacOS:

```
python3 -m venv .venv
. .venv/bin/activate
pip install nanobind==2.9.2 scikit-build-core click glfw pyopengl numpy requests toml
bash full_build.sh
```

## How to run tests

```
# in project root directory:
pytest
```

## API docs workflow

The VitePress API reference markdown under `docs/api/` is the authored source.
Function signatures and docstrings inside `::: api-signature` blocks are synced from `.pyi`
files with runtime fallback for Python-defined functions. Enum tables are synced as whole
blocks, and class members use class-qualified signatures such as `DrawList.add_line(...) -> None`.

Check that authored API docs still match the exposed API:

```bash
python3 gen/check_apiref_docs.py check
```

Rewrite existing `api-signature` blocks and enum sections in place from canonical API data:

```bash
python3 gen/check_apiref_docs.py sync
```

Preview what `sync` would change without writing files:

```bash
python3 gen/check_apiref_docs.py sync --dry-run
```

Print missing top-level API entries as copy-pasteable markdown blocks:

```bash
python3 gen/check_apiref_docs.py print-missing
```

Recommended workflow when editing API docs:
- add or move sections manually in `docs/api/imgui.md` or `docs/api/implot.md`
- paste new missing entries with `print-missing`
- run `sync --dry-run` to preview changes
- run `sync` to refresh signatures and embedded docstrings
- run `check` to verify there is no drift

## Building and deploying docs

Recipe markdown is generated into `docs/recipes/`. Recipe screenshots are also generated locally,
but the `docs/recipes/images/*.png` files are intentionally ignored by git. Rebuild them whenever
you want to refresh the docs locally or before publishing.

Regenerate recipe markdown and screenshots:

```bash
python3 gen/recipes/build_recipes.py
```

Regenerate only markdown:

```bash
python3 gen/recipes/build_recipes.py --skip-images
```

Regenerate only screenshots:

```bash
python3 gen/recipes/build_recipes.py --skip-md
```

Build the VitePress site:

```bash
rm -rf dist
npm run docs:build
```

Preview the built site:

```bash
npm run docs:preview
```

Deploy to `gh-pages`:

```bash
bash deploy_docs.sh
```

To compare the current local build against what is already published on `gh-pages`:

```bash
git clone --branch gh-pages --single-branch git@github.com:nurpax/slimgui.git /tmp/slimgui-gh-pages
rm -rf docs/dist
npm run docs:build
diff -ru /tmp/slimgui-gh-pages docs/dist
```

Use `diff -rq` if you only want a summary of changed files.

Recommended manual publish flow:
- first run any binding/stub maintenance you need, such as `bash full_build.sh`
- run `python3 gen/check_apiref_docs.py sync` and `python3 gen/check_apiref_docs.py check` when API docs changed
- run `python3 gen/recipes/build_recipes.py`
- run `bash deploy_docs.sh`

## Updating imgui and cimgui metainfo when upgrading imgui

Edit the `imgui_vendor.py` script to pull newer versions and then:

```
cd $ROOT_DIR
python gen/imgui_vendor.py
```

You need to also git cherry-pick imconfig related changes + do a `full_rebuild.sh` to update enums.  See git log for reference.
