from __future__ import annotations

import argparse
import ast
import difflib
import enum
import inspect
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FuncDoc:
    signatures: list[str] = field(default_factory=list)
    docstring: str | None = None


@dataclass
class EnumMemberDoc:
    name: str
    description: str


@dataclass
class EnumDoc:
    members: list[EnumMemberDoc] = field(default_factory=list)


@dataclass
class ClassDoc:
    methods: dict[str, FuncDoc] = field(default_factory=dict)
    properties: dict[str, FuncDoc] = field(default_factory=dict)


@dataclass
class ApiSpec:
    name: str
    doc_path: Path
    pyi_path: Path
    module_name: str


@dataclass
class DocSignature:
    name: str
    signature: str
    line: int
    start: int
    end: int
    docstring: str | None = None


@dataclass
class DocEnum:
    name: str
    members: list[EnumMemberDoc]
    line: int
    start: int
    end: int


@dataclass
class DocClassMethod:
    class_name: str
    method_name: str
    signature: str
    line: int
    start: int
    end: int
    docstring: str | None = None


DEFAULT_SPECS = [
    ApiSpec(
        name="imgui",
        doc_path=Path("docs/api/imgui.md"),
        pyi_path=Path("src/slimgui/slimgui_ext/imgui.pyi"),
        module_name="slimgui.imgui",
    ),
    ApiSpec(
        name="implot",
        doc_path=Path("docs/api/implot.md"),
        pyi_path=Path("src/slimgui/slimgui_ext/implot.pyi"),
        module_name="slimgui.implot",
    ),
]


def _clean_sig(sig: str) -> str:
    sig = " ".join(sig.strip().split())
    if sig.endswith(": ..."):
        sig = sig[: -len(": ...")]
    elif sig.endswith(":"):
        sig = sig[:-1]
    return sig


def _normalize_sig(sig: str) -> str:
    sig = _clean_sig(sig)
    sig = re.sub(r"\(\s+", "(", sig)
    sig = re.sub(r"\s+\)", ")", sig)
    sig = re.sub(r"\s+,", ",", sig)
    sig = re.sub(r",\s*\)", ")", sig)
    return sig


def _split_top_level_commas(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0

    for ch in value:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1

        if ch == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            continue

        current.append(ch)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def _format_signature(sig: str) -> str:
    open_paren = sig.find("(")
    close_paren = sig.rfind(")")
    if open_paren == -1 or close_paren == -1 or close_paren < open_paren:
        return sig

    prefix = sig[:open_paren].strip()
    params = sig[open_paren + 1:close_paren].strip()
    suffix = sig[close_paren + 1:].strip()
    if not params:
        return f"{prefix}(){f' {suffix}' if suffix else ''}"

    lines = [f"{prefix}("]
    for part in _split_top_level_commas(params):
        lines.append(f"    {part},")
    closing = ")"
    if suffix:
        closing += f" {suffix}"
    lines.append(closing)
    return "\n".join(lines)


def _def_sig_from_source(source: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    segment = ast.get_source_segment(source, node)
    if not segment:
        return f"def {node.name}(...)"  # fallback

    header_lines = []
    for line in segment.splitlines():
        header_lines.append(line)
        if line.rstrip().endswith(":"):
            break
    return _clean_sig(" ".join(header_lines))


def _parse_pyi_functions(path: Path) -> dict[str, FuncDoc]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    funcs: dict[str, FuncDoc] = {}

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func = funcs.setdefault(node.name, FuncDoc())
            func.signatures.append(_def_sig_from_source(source, node))
            if func.docstring is None:
                func.docstring = ast.get_docstring(node)

    return funcs


def _clean_enum_description(doc: str | None) -> str:
    if not doc:
        return ""
    return " ".join(line.strip() for line in inspect.cleandoc(doc).splitlines()).strip()


def _is_enum_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        base_text = ast.unparse(base)
        if base_text.endswith(("Enum", "IntEnum", "Flag", "IntFlag")):
            return True
    return False


def _parse_pyi_enums(path: Path) -> dict[str, EnumDoc]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    enums: dict[str, EnumDoc] = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or not _is_enum_class(node):
            continue

        members: list[EnumMemberDoc] = []
        body = node.body
        for idx, item in enumerate(body):
            if not isinstance(item, ast.Assign):
                continue
            if len(item.targets) != 1 or not isinstance(item.targets[0], ast.Name):
                continue
            member_name = item.targets[0].id
            if member_name.startswith("_"):
                continue

            description = ""
            if idx + 1 < len(body):
                next_item = body[idx + 1]
                if (
                    isinstance(next_item, ast.Expr)
                    and isinstance(next_item.value, ast.Constant)
                    and isinstance(next_item.value.value, str)
                ):
                    description = _clean_enum_description(next_item.value.value)

            members.append(EnumMemberDoc(member_name, description))

        enums[node.name] = EnumDoc(members=members)

    return enums


def _parse_pyi_classes(path: Path) -> dict[str, ClassDoc]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    classes: dict[str, ClassDoc] = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or _is_enum_class(node):
            continue

        class_doc = ClassDoc()
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if item.name.startswith("_"):
                continue
            is_property = any(isinstance(dec, ast.Name) and dec.id == "property" for dec in item.decorator_list)
            members = class_doc.properties if is_property else class_doc.methods
            func = members.setdefault(item.name, FuncDoc())
            func.signatures.append(_def_sig_from_source(source, item))
            if func.docstring is None:
                func.docstring = ast.get_docstring(item)

        if class_doc.methods or class_doc.properties:
            classes[node.name] = class_doc

    return classes


def _runtime_docstring(obj: object, signature: str) -> str | None:
    doc = inspect.getdoc(obj)
    if not doc:
        return None

    normalized_doc = " ".join(doc.split())
    normalized_sig = " ".join(_clean_sig(signature).removeprefix("def ").split())
    if normalized_doc == normalized_sig:
        return None

    return doc


def _merge_runtime_functions(module_name: str, funcs: dict[str, FuncDoc]) -> None:
    module = __import__(module_name, fromlist=["*"])
    for name in dir(module):
        if name.startswith("_"):
            continue
        obj = getattr(module, name)
        if not inspect.isfunction(obj):
            continue
        obj_module = getattr(obj, "__module__", "")
        if not obj_module.startswith("slimgui"):
            continue
        try:
            runtime_sig = inspect.signature(obj, eval_str=True, globals=obj.__globals__, locals=obj.__globals__)
        except Exception:
            runtime_sig = inspect.signature(obj)
        sig = _clean_sig(f"def {name}{runtime_sig}")
        already_present = name in funcs
        func = funcs.setdefault(name, FuncDoc())
        if not already_present or not func.signatures:
            func.signatures.append(sig)
        if func.docstring is None:
            func.docstring = _runtime_docstring(obj, sig)


def _merge_runtime_enums(module_name: str, enums: dict[str, EnumDoc]) -> None:
    module = __import__(module_name, fromlist=["*"])
    for name in dir(module):
        if name.startswith("_"):
            continue
        obj = getattr(module, name)
        if not isinstance(obj, type) or not issubclass(obj, enum.Enum):
            continue
        obj_module = getattr(obj, "__module__", "")
        if not obj_module.startswith("slimgui"):
            continue
        if name in enums:
            continue
        enums[name] = EnumDoc(
            members=[
                EnumMemberDoc(member_name, _clean_enum_description(getattr(member, "__doc__", None)))
                for member_name, member in obj.__members__.items()
            ]
        )


def _merge_runtime_classes(module_name: str, classes: dict[str, ClassDoc]) -> None:
    module = __import__(module_name, fromlist=["*"])
    for class_name in dir(module):
        if class_name.startswith("_"):
            continue
        cls = getattr(module, class_name)
        if not isinstance(cls, type):
            continue
        cls_module = getattr(cls, "__module__", "")
        if not cls_module.startswith("slimgui"):
            continue

        class_doc = classes.setdefault(class_name, ClassDoc())
        for method_name in dir(cls):
            if method_name.startswith("_"):
                continue
            obj = inspect.getattr_static(cls, method_name)
            bound = getattr(cls, method_name, None)
            is_property = isinstance(obj, property)
            if is_property:
                bound = obj.fget
            if bound is None or not callable(bound):
                continue
            members = class_doc.properties if is_property else class_doc.methods
            func = members.setdefault(method_name, FuncDoc())
            if func.signatures:
                continue
            try:
                runtime_sig = inspect.signature(bound, eval_str=True, globals=getattr(bound, "__globals__", {}), locals=getattr(bound, "__globals__", {}))
            except Exception:
                try:
                    runtime_sig = inspect.signature(bound)
                except Exception:
                    continue
            sig = _clean_sig(f"def {method_name}{runtime_sig}")
            func.signatures.append(sig)
            if func.docstring is None:
                func.docstring = _runtime_docstring(bound, sig)


def _extract_docstring_from_block(block: str) -> tuple[str, str | None]:
    lines = block.rstrip().splitlines()
    doc_start = None

    for idx, line in enumerate(lines):
        if line.strip() in {'"""', "'''"}:
            doc_start = idx
            break

    if doc_start is None:
        signature = "\n".join(lines).rstrip()
        return signature, None

    signature_lines = lines[:doc_start]
    quote = lines[doc_start].strip()
    doc_lines: list[str] = []
    for idx in range(doc_start + 1, len(lines)):
        if lines[idx].strip() == quote:
            break
        doc_lines.append(lines[idx][4:] if lines[idx].startswith("    ") else lines[idx])

    signature = "\n".join(signature_lines).rstrip()
    docstring = "\n".join(doc_lines).strip()
    return signature, docstring or None


def _parse_doc_signatures(path: Path) -> list[DocSignature]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"::: api-signature\s+```python\s*\n(.*?)\n```\s*:::", re.DOTALL)
    out: list[DocSignature] = []
    class_heading_pattern = re.compile(r"^### Class: ", re.MULTILINE)

    for match in pattern.finditer(text):
        preceding = text[:match.start()]
        last_class_heading = None
        last_section_heading = None
        for heading in re.finditer(r"^### .*", preceding, re.MULTILINE):
            last_section_heading = heading.group(0)
            if class_heading_pattern.match(heading.group(0)):
                last_class_heading = heading.group(0)

        if last_class_heading is not None and last_section_heading == last_class_heading:
            continue

        block = match.group(1)
        signature_block, docstring = _extract_docstring_from_block(block)
        sig = _normalize_sig(signature_block)
        sig_match = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", sig)
        if not sig_match:
            continue
        line = text.count("\n", 0, match.start()) + 1
        out.append(
            DocSignature(
                name=sig_match.group(1),
                signature=sig,
                line=line,
                start=match.start(),
                end=match.end(),
                docstring=docstring,
            )
        )

    return out


def _parse_doc_enums(path: Path) -> list[DocEnum]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line)

    out: list[DocEnum] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("### Enum: "):
            i += 1
            continue

        name = line[len("### Enum: "):].strip()
        if i + 3 >= len(lines):
            i += 1
            continue
        if lines[i + 2].strip() != "| Name | Description |" or lines[i + 3].strip() != "| --- | --- |":
            i += 1
            continue

        members: list[EnumMemberDoc] = []
        j = i + 4
        row_pattern = re.compile(r"^\| (?P<name>[^|]+?) \| ?(?P<description>.*?) ?\|\s*$")
        while j < len(lines):
            stripped = lines[j].strip()
            if not stripped:
                if j + 1 < len(lines) and lines[j + 1].startswith("### "):
                    j += 1
                    break
                if j + 1 < len(lines) and lines[j + 1].startswith("## "):
                    j += 1
                    break
                j += 1
                continue
            if lines[j].startswith("### ") or lines[j].startswith("## "):
                break
            match = row_pattern.match(lines[j])
            if match:
                members.append(
                    EnumMemberDoc(
                        match.group("name").strip(),
                        match.group("description").strip(),
                    )
                )
            j += 1

        out.append(
            DocEnum(
                name=name,
                members=members,
                line=i + 1,
                start=offsets[i],
                end=offsets[j] if j < len(offsets) else len(text),
            )
        )
        i = j

    return out


def _parse_doc_class_methods(path: Path) -> list[DocClassMethod]:
    text = path.read_text(encoding="utf-8")
    class_pattern = re.compile(r"^### Class: (?P<name>.+)$", re.MULTILINE)
    block_pattern = re.compile(r"::: api-signature\s+```python\s*\n(.*?)\n```\s*:::", re.DOTALL)
    classes = list(class_pattern.finditer(text))
    out: list[DocClassMethod] = []

    for idx, class_match in enumerate(classes):
        class_name = class_match.group("name").strip()
        start = class_match.end()
        end = classes[idx + 1].start() if idx + 1 < len(classes) else len(text)
        section = text[start:end]

        for block_match in block_pattern.finditer(section):
            block = block_match.group(1)
            signature_block, docstring = _extract_docstring_from_block(block)
            sig = _normalize_sig(signature_block)
            sig_match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)(?:\s*\(|\s+->)", sig)
            method_name = None
            if sig_match:
                rendered_class_name = sig_match.group(1)
                if rendered_class_name != class_name:
                    continue
                method_name = sig_match.group(2)
            else:
                legacy_match = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", sig)
                if legacy_match:
                    method_name = legacy_match.group(1)
            if method_name is None:
                continue
            absolute_start = start + block_match.start()
            line = text.count("\n", 0, absolute_start) + 1
            out.append(
                DocClassMethod(
                    class_name=class_name,
                    method_name=method_name,
                    signature=sig,
                    line=line,
                    start=absolute_start,
                    end=start + block_match.end(),
                    docstring=docstring,
                )
            )

    return out


def _normalize_docstring(doc: str | None) -> str | None:
    if doc is None:
        return None
    normalized = "\n".join(line.rstrip() for line in inspect.cleandoc(doc).strip().splitlines())
    return normalized or None


def _render_python_block(sig: str, docstring: str | None) -> str:
    formatted_sig = _format_signature(sig)
    lines = formatted_sig.splitlines()
    if lines:
        lines[-1] = f"{lines[-1]}:"

    if docstring:
        quote = '"""' if '"""' not in docstring else "'''"
        lines.append("    " + quote)
        lines.extend(f"    {line}" if line else "" for line in _normalize_docstring(docstring).splitlines())
        lines.append("    " + quote)

    return "\n".join(lines)


def _render_api_signature_block(func: FuncDoc, signature: str | None = None) -> str:
    sig = signature or func.signatures[0]
    parts = ["::: api-signature", "```python", _render_python_block(sig, func.docstring), "```", ":::"]
    return "\n".join(parts)


def _render_method_signature(class_name: str, sig: str) -> str:
    sig = _clean_sig(sig)
    match = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)(.*)$", sig)
    if not match:
        return sig

    method_name = match.group(1)
    params = _split_top_level_commas(match.group(2).strip())
    if params:
        first_name = params[0].split(":", 1)[0].split("=", 1)[0].strip()
        if first_name in {"self", "cls"}:
            params = params[1:]

    suffix = match.group(3).strip()
    prefix = f"{class_name}.{method_name}"
    if not params:
        return f"{prefix}(){f' {suffix}' if suffix else ''}"

    lines = [f"{prefix}("]
    for part in params:
        lines.append(f"    {part},")
    closing = ")"
    if suffix:
        closing += f" {suffix}"
    lines.append(closing)
    return "\n".join(lines)


def _render_property_signature(class_name: str, sig: str) -> str:
    sig = _clean_sig(sig)
    match = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)(.*)$", sig)
    if not match:
        return sig
    property_name = match.group(1)
    suffix = match.group(3).strip()
    return f"{class_name}.{property_name}{f' {suffix}' if suffix else ''}"


def _render_class_member_block(class_name: str, func: FuncDoc, signature: str | None = None, *, is_property: bool) -> str:
    sig = signature or func.signatures[0]
    rendered_sig = _render_property_signature(class_name, sig) if is_property else _render_method_signature(class_name, sig)
    parts = [
        "::: api-signature",
        "```python",
        _render_python_block(rendered_sig, func.docstring),
        "```",
        ":::",
    ]
    return "\n".join(parts)


def _select_matching_member_signature(class_name: str, documented_signature: str, signatures: list[str], *, is_property: bool) -> str:
    render = _render_property_signature if is_property else _render_method_signature
    for sig in signatures:
        if _normalize_sig(render(class_name, sig)) == documented_signature:
            return sig
    for sig in signatures:
        if _normalize_sig(sig) == documented_signature:
            return sig
    return signatures[0]


def _render_enum_block(name: str, enum_doc: EnumDoc) -> str:
    parts = [
        f"### Enum: {name}",
        "",
        "| Name | Description |",
        "| --- | --- |",
    ]
    for member in enum_doc.members:
        description = member.description.replace("|", "\\|")
        parts.append(f"| {member.name} | {description} |")
    return "\n".join(parts) + "\n\n"


def _check_spec(spec: ApiSpec) -> list[str]:
    errors: list[str] = []
    funcs = _parse_pyi_functions(spec.pyi_path)
    _merge_runtime_functions(spec.module_name, funcs)
    enums = _parse_pyi_enums(spec.pyi_path)
    _merge_runtime_enums(spec.module_name, enums)
    classes = _parse_pyi_classes(spec.pyi_path)
    _merge_runtime_classes(spec.module_name, classes)

    documented = _parse_doc_signatures(spec.doc_path)
    documented_names = {entry.name for entry in documented}
    documented_enums = _parse_doc_enums(spec.doc_path)
    documented_enum_names = {entry.name for entry in documented_enums}
    documented_class_methods = _parse_doc_class_methods(spec.doc_path)

    for entry in documented:
        expected = funcs.get(entry.name)
        if expected is None:
            errors.append(
                f"{spec.doc_path}:{entry.line}: documented symbol `{entry.name}` not found in {spec.pyi_path} or {spec.module_name}"
            )
            continue
        expected_signatures = [_normalize_sig(sig) for sig in expected.signatures]
        if entry.signature not in expected_signatures:
            expected_list = "; ".join(expected.signatures)
            errors.append(
                f"{spec.doc_path}:{entry.line}: signature mismatch for `{entry.name}`\n"
                f"  documented: {entry.signature}\n"
                f"  expected:   {expected_list}"
            )
        expected_docstring = _normalize_docstring(expected.docstring)
        documented_docstring = _normalize_docstring(entry.docstring)
        if documented_docstring != expected_docstring:
            errors.append(
                f"{spec.doc_path}:{entry.line}: docstring mismatch for `{entry.name}`\n"
                f"  documented: {documented_docstring or '<missing>'}\n"
                f"  expected:   {expected_docstring or '<missing>'}"
            )

    undocumented = sorted(
        name for name in funcs if name not in documented_names and not name.endswith("_internal")
    )
    for name in undocumented:
        errors.append(f"{spec.doc_path}: undocumented public function `{name}`")

    for entry in documented_enums:
        expected = enums.get(entry.name)
        if expected is None:
            errors.append(
                f"{spec.doc_path}:{entry.line}: documented enum `{entry.name}` not found in {spec.pyi_path} or {spec.module_name}"
            )
            continue
        if entry.members != expected.members:
            errors.append(
                f"{spec.doc_path}:{entry.line}: enum block mismatch for `{entry.name}`"
            )

    undocumented_enums = sorted(name for name in enums if name not in documented_enum_names)
    for name in undocumented_enums:
        errors.append(f"{spec.doc_path}: undocumented public enum `{name}`")

    documented_methods_by_class: dict[str, set[str]] = {}
    for entry in documented_class_methods:
        class_doc = classes.get(entry.class_name)
        if class_doc is None:
            errors.append(f"{spec.doc_path}:{entry.line}: documented class `{entry.class_name}` not found in {spec.pyi_path} or {spec.module_name}")
            continue
        method_doc = class_doc.methods.get(entry.method_name)
        property_doc = class_doc.properties.get(entry.method_name)
        member_doc = method_doc or property_doc
        is_property = property_doc is not None
        if member_doc is None:
            errors.append(
                f"{spec.doc_path}:{entry.line}: documented method `{entry.class_name}.{entry.method_name}` not found in {spec.pyi_path} or {spec.module_name}"
            )
            continue

        render = _render_property_signature if is_property else _render_method_signature
        expected_signatures = [_normalize_sig(render(entry.class_name, sig)) for sig in member_doc.signatures]
        if entry.signature not in expected_signatures:
            expected_list = "; ".join(render(entry.class_name, sig) for sig in member_doc.signatures)
            errors.append(
                f"{spec.doc_path}:{entry.line}: signature mismatch for `{entry.class_name}.{entry.method_name}`\n"
                f"  documented: {entry.signature}\n"
                f"  expected:   {expected_list}"
            )

        expected_docstring = _normalize_docstring(member_doc.docstring)
        documented_docstring = _normalize_docstring(entry.docstring)
        if documented_docstring != expected_docstring:
            errors.append(
                f"{spec.doc_path}:{entry.line}: docstring mismatch for `{entry.class_name}.{entry.method_name}`\n"
                f"  documented: {documented_docstring or '<missing>'}\n"
                f"  expected:   {expected_docstring or '<missing>'}"
            )

        documented_methods_by_class.setdefault(entry.class_name, set()).add(entry.method_name)

    for class_name, method_names in documented_methods_by_class.items():
        class_doc = classes.get(class_name)
        if class_doc is None:
            continue
        undocumented_methods = sorted(
            name
            for name in {**class_doc.methods, **class_doc.properties}
            if name not in method_names and not name.endswith("_internal")
        )
        for method_name in undocumented_methods:
            errors.append(f"{spec.doc_path}: undocumented public method `{class_name}.{method_name}`")

    return errors


def _missing_doc_entries(spec: ApiSpec) -> dict[str, FuncDoc]:
    funcs = _parse_pyi_functions(spec.pyi_path)
    _merge_runtime_functions(spec.module_name, funcs)
    documented_names = {entry.name for entry in _parse_doc_signatures(spec.doc_path)}

    return {
        name: funcs[name]
        for name in sorted(funcs)
        if name not in documented_names and not name.endswith("_internal")
    }


def _missing_doc_enums(spec: ApiSpec) -> dict[str, EnumDoc]:
    enums = _parse_pyi_enums(spec.pyi_path)
    _merge_runtime_enums(spec.module_name, enums)
    documented_names = {entry.name for entry in _parse_doc_enums(spec.doc_path)}

    return {
        name: enums[name]
        for name in sorted(enums)
        if name not in documented_names
    }


def _render_missing_md(spec: ApiSpec) -> str:
    missing = _missing_doc_entries(spec)
    parts = [f"<!-- Missing API docs for {spec.name} -->", ""]

    for name, func in missing.items():
        for sig in func.signatures:
            parts.append(_render_api_signature_block(func, sig))
            parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def _render_missing_enum_md(spec: ApiSpec) -> str:
    missing = _missing_doc_enums(spec)
    parts = [f"<!-- Missing enum docs for {spec.name} -->", ""]

    for name, enum_doc in missing.items():
        parts.append(_render_enum_block(name, enum_doc).rstrip())
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def _sync_spec(spec: ApiSpec) -> bool:
    funcs = _parse_pyi_functions(spec.pyi_path)
    _merge_runtime_functions(spec.module_name, funcs)
    enums = _parse_pyi_enums(spec.pyi_path)
    _merge_runtime_enums(spec.module_name, enums)
    classes = _parse_pyi_classes(spec.pyi_path)
    _merge_runtime_classes(spec.module_name, classes)

    path = spec.doc_path
    text = path.read_text(encoding="utf-8")
    documented = _parse_doc_signatures(path)
    documented_enums = _parse_doc_enums(path)
    documented_class_methods = _parse_doc_class_methods(path)
    updated = text
    changed = False

    for entry in reversed(documented_class_methods):
        class_doc = classes.get(entry.class_name)
        if class_doc is None:
            continue
        method_doc = class_doc.methods.get(entry.method_name)
        property_doc = class_doc.properties.get(entry.method_name)
        member_doc = method_doc or property_doc
        is_property = property_doc is not None
        if member_doc is None:
            continue
        matching_signature = _select_matching_member_signature(entry.class_name, entry.signature, member_doc.signatures, is_property=is_property)
        replacement = _render_class_member_block(entry.class_name, member_doc, matching_signature, is_property=is_property)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    for entry in reversed(documented_enums):
        enum_doc = enums.get(entry.name)
        if enum_doc is None:
            continue
        replacement = _render_enum_block(entry.name, enum_doc)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    for entry in reversed(documented):
        func = funcs.get(entry.name)
        if func is None:
            continue
        replacement = _render_api_signature_block(func, entry.signature)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def _sync_spec_preview(spec: ApiSpec) -> tuple[bool, str]:
    funcs = _parse_pyi_functions(spec.pyi_path)
    _merge_runtime_functions(spec.module_name, funcs)
    enums = _parse_pyi_enums(spec.pyi_path)
    _merge_runtime_enums(spec.module_name, enums)
    classes = _parse_pyi_classes(spec.pyi_path)
    _merge_runtime_classes(spec.module_name, classes)

    path = spec.doc_path
    original = path.read_text(encoding="utf-8")
    documented = _parse_doc_signatures(path)
    documented_enums = _parse_doc_enums(path)
    documented_class_methods = _parse_doc_class_methods(path)
    updated = original
    changed = False

    for entry in reversed(documented_class_methods):
        class_doc = classes.get(entry.class_name)
        if class_doc is None:
            continue
        method_doc = class_doc.methods.get(entry.method_name)
        property_doc = class_doc.properties.get(entry.method_name)
        member_doc = method_doc or property_doc
        is_property = property_doc is not None
        if member_doc is None:
            continue
        matching_signature = _select_matching_member_signature(entry.class_name, entry.signature, member_doc.signatures, is_property=is_property)
        replacement = _render_class_member_block(entry.class_name, member_doc, matching_signature, is_property=is_property)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    for entry in reversed(documented_enums):
        enum_doc = enums.get(entry.name)
        if enum_doc is None:
            continue
        replacement = _render_enum_block(entry.name, enum_doc)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    for entry in reversed(documented):
        func = funcs.get(entry.name)
        if func is None:
            continue
        replacement = _render_api_signature_block(func, entry.signature)
        if updated[entry.start:entry.end] != replacement:
            updated = updated[:entry.start] + replacement + updated[entry.end:]
            changed = True

    if not changed:
        return False, ""

    diff = "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path),
        )
    )
    return True, diff


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API markdown against .pyi and runtime modules.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_spec_arg(cmd: argparse.ArgumentParser) -> None:
        cmd.add_argument(
            "--spec",
            action="append",
            default=[],
            help="Override defaults with NAME:DOC_PATH:PYI_PATH:MODULE",
        )

    check_parser = subparsers.add_parser(
        "check",
        help="Validate authored API markdown against .pyi files and runtime modules.",
    )
    add_spec_arg(check_parser)

    sync_parser = subparsers.add_parser(
        "sync",
        help="Rewrite existing api-signature and enum blocks in place from canonical API data.",
    )
    add_spec_arg(sync_parser)
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show a unified diff of the changes that sync would make without writing files.",
    )

    print_missing_parser = subparsers.add_parser(
        "print-missing",
        help="Print undocumented top-level functions as copy-pasteable api-signature markdown blocks.",
    )
    add_spec_arg(print_missing_parser)

    print_missing_enums_parser = subparsers.add_parser(
        "print-missing-enums",
        help="Print undocumented enums as copy-pasteable markdown enum sections.",
    )
    add_spec_arg(print_missing_enums_parser)

    args = parser.parse_args()

    specs = DEFAULT_SPECS
    if args.spec:
        specs = []
        for raw in args.spec:
            name, doc_path, pyi_path, module_name = raw.split(":", 3)
            specs.append(ApiSpec(name, Path(doc_path), Path(pyi_path), module_name))

    if args.command == "print-missing":
        for idx, spec in enumerate(specs):
            if idx:
                print()
            print(_render_missing_md(spec), end="")
        return 0

    if args.command == "print-missing-enums":
        for idx, spec in enumerate(specs):
            if idx:
                print()
            print(_render_missing_enum_md(spec), end="")
        return 0

    if args.command == "sync":
        if args.dry_run:
            any_changes = False
            for spec in specs:
                changed, diff = _sync_spec_preview(spec)
                if not changed:
                    continue
                any_changes = True
                print(diff, end="")
            if any_changes:
                return 1
            print("check_apiref_docs.py: already up to date")
            return 0

        changed = False
        for spec in specs:
            changed = _sync_spec(spec) or changed
        print("check_apiref_docs.py: synced" if changed else "check_apiref_docs.py: already up to date")
        return 0

    all_errors: list[str] = []
    for spec in specs:
        all_errors.extend(_check_spec(spec))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        print(f"\ncheck_apiref_docs.py: {len(all_errors)} issue(s) found", file=sys.stderr)
        return 1

    print("check_apiref_docs.py: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
