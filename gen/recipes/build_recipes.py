from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recipes.examples import load_examples
else:
    from .examples import load_examples


def _run(command: list[str]) -> None:
    logging.info("Running: %s", " ".join(command))
    subprocess.run(command, check=True)


def _find_orphaned_images(images_dir: Path, example_names: set[str]) -> list[Path]:
    if not images_dir.exists():
        return []
    return sorted(path for path in images_dir.glob("*.png") if path.stem not in example_names)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build recipe markdown and screenshots.")
    parser.add_argument(
        "--recipes-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "docs" / "recipes",
        help="Output directory for recipe markdown files.",
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=None,
        help="Output directory for screenshots (default: recipes-dir/images).",
    )
    parser.add_argument(
        "--example",
        action="append",
        default=[],
        help="Limit to specific example(s). Can be passed multiple times.",
    )
    parser.add_argument("--skip-md", action="store_true", help="Skip markdown generation.")
    parser.add_argument("--skip-images", action="store_true", help="Skip screenshot generation.")
    parser.add_argument(
        "--clean-orphaned-images",
        action="store_true",
        help="Delete recipe screenshots that no longer correspond to any example.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    repo_root = Path(__file__).resolve().parents[2]
    _, examples = load_examples(repo_root)

    if args.example:
        selected = [ex for ex in examples if ex.name in set(args.example)]
    else:
        selected = examples

    if not selected:
        logging.warning("No examples selected.")
        return 0

    recipes_dir = args.recipes_dir
    images_dir = args.images_dir or (recipes_dir / "images")

    if not args.skip_md:
        _run(
            [
                sys.executable,
                str(repo_root / "gen" / "recipes" / "make_recipes_md.py"),
                "--output-dir",
                str(recipes_dir),
                "--images-subdir",
                "images",
            ]
        )

    if not args.skip_images:
        images_dir.mkdir(parents=True, exist_ok=True)
        for example in selected:
            _run(
                [
                    sys.executable,
                    str(repo_root / "gen" / "recipes" / "screenshot_render.py"),
                    "--example",
                    example.name,
                    "--output",
                    str(images_dir / f"{example.name}.png"),
                ]
            )

    example_names = {example.name for example in examples}
    orphaned_images = _find_orphaned_images(images_dir, example_names)
    if orphaned_images:
        if args.clean_orphaned_images:
            for path in orphaned_images:
                path.unlink()
                logging.info("Deleted orphaned recipe image: %s", path)
        else:
            logging.warning("Orphaned recipe images:")
            for path in orphaned_images:
                logging.warning("  %s", path)
            logging.warning("Use --clean-orphaned-images to delete them.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
