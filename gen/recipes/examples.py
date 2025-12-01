from __future__ import annotations

import inspect
import sys
import textwrap
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class Example:
    name: str
    category: str
    title: str
    callable: Callable[..., Any]
    filename: str
    lineno: int

    @property
    def doc(self) -> str:
        return inspect.getdoc(self.callable) or ""

    @property
    def source(self) -> str:
        source = textwrap.dedent(inspect.getsource(self.callable))
        tree = ast.parse(source)
        func = tree.body[0]
        assert isinstance(func, ast.FunctionDef | ast.AsyncFunctionDef)

        lines = source.splitlines()
        rendered_lines = lines[func.lineno - 1 :]

        if (
            func.body
            and isinstance(func.body[0], ast.Expr)
            and isinstance(func.body[0].value, ast.Constant)
            and isinstance(func.body[0].value.value, str)
        ):
            doc = func.body[0]
            doc_start = doc.lineno - func.lineno
            doc_end = doc.end_lineno - func.lineno + 1
            rendered_lines = rendered_lines[:doc_start] + rendered_lines[doc_end:]

            while len(rendered_lines) > 1 and rendered_lines[1].strip() == "":
                del rendered_lines[1]

        return "\n".join(rendered_lines)

    @property
    def state_ctor(self) -> Callable[[], Any] | None:
        return getattr(self.callable, "_example_state_ctor", None)

    @property
    def window_size(self) -> tuple[int, int]:
        return getattr(self.callable, "_example_window_size", None) or (650, 400)


def load_examples(repo_root: Path):
    sys.path.insert(0, str(repo_root / "example"))
    import doc_examples  # noqa: PLC0415

    return doc_examples, _collect_examples(doc_examples)


def _collect_examples(doc_examples_module) -> list[Example]:
    callables: list[tuple[str, int, str, Callable[..., Any]]] = []
    for name, obj in inspect.getmembers(doc_examples_module, inspect.isfunction):
        if not name.startswith("_") and getattr(obj, "_is_example", False):
            filename = obj.__code__.co_filename
            lineno = obj.__code__.co_firstlineno
            callables.append((filename, lineno, name, obj))

    callables.sort(key=lambda item: (item[0], item[1], item[2]))
    examples: list[Example] = []
    for filename, lineno, name, obj in callables:
        examples.append(
            Example(
                name=name,
                category=getattr(obj, "_example_category", "misc"),
                title=getattr(obj, "_example_metadata", {}).get("title", name),
                callable=obj,
                filename=filename,
                lineno=lineno,
            )
        )
    return examples
