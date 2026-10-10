"""Core: scan a repo and build a structured, compact map.

No third-party deps. Python files are parsed with `ast`; JS/TS files use
heuristic regex extraction.
"""
from __future__ import annotations

import ast
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
               "dist", "build", ".idea", ".vscode", "env"}


@dataclass
class Symbol:
    name: str
    kind: str          # class | function | export
    line: int
    signature: str = ""


@dataclass
class FileMap:
    path: str
    symbols: list = field(default_factory=list)


def parse_python(path: Path) -> Optional[FileMap]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except (SyntaxError, ValueError):
        return None
    fm = FileMap(path=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            sig = f"class {node.name}"
            if methods:
                sig += f"  (methods: {', '.join(methods[:8])})"
            fm.symbols.append(Symbol(node.name, "class", node.lineno, sig))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = ", ".join(a.arg for a in node.args.args)
            fm.symbols.append(
                Symbol(node.name, "function", node.lineno,
                       f"def {node.name}({args})"))
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper() and len(t.id) > 2:
                    fm.symbols.append(Symbol(t.id, "constant", node.lineno))
    return fm


# Minimal JS/TS heuristics
RE_EXPORT = re.compile(r"^export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|let)\s+(\w+)")
RE_EXPORT_FROM = re.compile(r"^export\s+\{([^}]+)\}")
RE_CLASS = re.compile(r"^class\s+(\w+)")
RE_FUNC = re.compile(r"^(?:async\s+)?function\s+(\w+)\s*\(")


def parse_js(path: Path) -> Optional[FileMap]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    fm = FileMap(path=str(path))
    for i, line in enumerate(lines, 1):
        s = line.strip()
        for rx, kind in [(RE_EXPORT, "export"), (RE_CLASS, "class"),
                         (RE_FUNC, "function")]:
            m = rx.match(s)
            if m:
                fm.symbols.append(Symbol(m.group(1), kind, i))
                break
        else:
            m = RE_EXPORT_FROM.match(s)
            if m:
                for name in m.group(1).split(","):
                    name = name.strip().split(" as ")[-1].strip()
                    if name:
                        fm.symbols.append(Symbol(name, "export", i))
    return fm


PARSERS = {".py": parse_python, ".js": parse_js, ".ts": parse_js,
           ".jsx": parse_js, ".tsx": parse_js}


def scan(root: str | Path, max_files: int = 400,
         extra_ignore: Optional[list] = None,
         max_depth: Optional[int] = None,
         min_symbols: int = 1) -> list[FileMap]:
    root = Path(root).resolve()
    ignore = IGNORE_DIRS | set(extra_ignore or [])
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_depth = len(Path(dirpath).relative_to(root).parts)
        if max_depth is not None and rel_depth >= max_depth:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in ignore]
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            parser = PARSERS.get(ext)
            if not parser:
                continue
            p = Path(dirpath) / fn
            rel = p.relative_to(root)
            fm = parser(p)
            if fm and len(fm.symbols) >= min_symbols:
                fm.path = str(rel).replace("\\", "/")
                out.append(fm)
            if len(out) >= max_files:
                return out
    return out


def language_stats(files: list[FileMap]) -> dict:
    """Count files and symbols per language (by extension)."""
    stats: dict[str, dict] = {}
    for fm in files:
        ext = Path(fm.path).suffix or "(none)"
        entry = stats.setdefault(ext, {"files": 0, "symbols": 0})
        entry["files"] += 1
        entry["symbols"] += len(fm.symbols)
    return dict(sorted(stats.items(), key=lambda kv: -kv[1]["files"]))


def render(files: list[FileMap], root_name: str) -> str:
    total_symbols = sum(len(f.symbols) for f in files)
    lines = [f"# {root_name} - codebase map",
             "",
             f"_Files: {len(files)}  |  Symbols: {total_symbols}_",
             ""]
    # group by top-level directory
    by_dir: dict[str, list[FileMap]] = {}
    for fm in files:
        top = fm.path.split("/")[0] if "/" in fm.path else "."
        by_dir.setdefault(top, []).append(fm)
    for d in sorted(by_dir):
        lines.append(f"## {d}/")
        for fm in by_dir[d]:
            lines.append(f"\n**`{fm.path}`**")
            for s in fm.symbols:
                lines.append(f"- {s.signature or s.name}")
        lines.append("")
    return "\n".join(lines)


def render_json(files: list[FileMap], root_name: str) -> str:
    """Machine-readable output: one object per file, symbols as arrays."""
    import json
    payload = {
        "root": root_name,
        "files": [
            {
                "path": fm.path,
                "symbols": [
                    {"name": s.name, "kind": s.kind, "line": s.line}
                    for s in fm.symbols
                ],
            }
            for fm in files
        ],
    }
    return json.dumps(payload, indent=2)
