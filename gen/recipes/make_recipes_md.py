from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recipes.examples import Example, load_examples
else:
    from .examples import Example, load_examples


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _titleize(name: str) -> str:
    if name == "ImPlot":
        return "ImPlot"
    return name.replace("_", " ").strip().title()


def _format_example(example: Example, *, images_subdir: str | None) -> str:
    title = example.title
    parts: list[str] = [f"## {title}", ""]

    if images_subdir:
        parts.append(f"![{title}](./{images_subdir}/{example.name}.png)")
        parts.append("")

    if example.doc:
        parts.append(example.doc)
        parts.append("")

    parts.append("```python")
    parts.append(example.source.rstrip())
    parts.append("```")
    return "\n".join(parts)


def _render_category_page(category: str, examples: list[Example], *, images_subdir: str | None) -> str:
    title = _titleize(category)
    sections = [f"---\ntitle: \"{title}\"\n---", "", f"# {title}", ""]
    for example in examples:
        sections.append(_format_example(example, images_subdir=images_subdir))
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate recipe markdown from doc_examples.")
    parser.add_argument(
        "--output-dir",
        default=Path(__file__).resolve().parents[2] / "docs" / "recipes",
        type=Path,
        help="Output directory for generated recipe markdown files.",
    )
    parser.add_argument(
        "--images-subdir",
        default="images",
        help="Relative subdirectory for screenshots, or empty to omit images.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    repo_root = Path(__file__).resolve().parents[2]
    _, examples = load_examples(repo_root)
    examples_by_category: dict[str, list[Example]] = {}
    for example in examples:
        examples_by_category.setdefault(example.category, []).append(example)

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = repo_root / "docs" / ".vitepress" / "config.ts"
    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    recipe_links = set(re.findall(r'link:\s*"/recipes/([^"]*)"', config_text))

    images_subdir = args.images_subdir.strip() or None

    for category, category_examples in examples_by_category.items():
        slug = _slugify(category)
        if slug not in recipe_links:
            logging.warning('Recipe page "/recipes/%s" is not listed in vitepress sidebar.', slug)
        content = _render_category_page(category, category_examples, images_subdir=images_subdir)
        (output_dir / f"{slug}.md").write_text(content, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
