"""Tests for repomap core scanning."""
import tempfile
from pathlib import Path

from repomap.core import scan, render, parse_python


def test_parse_python_extracts_classes_and_funcs():
    code = '''
class Server:
    def listen(self): pass
    def route(self): pass
    CONSTANT = 42

def handle(req):
    return "ok"
'''
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "srv.py"
        p.write_text(code, encoding="utf-8")
        fm = parse_python(p)
        kinds = {s.kind for s in fm.symbols}
        names = {s.name for s in fm.symbols}
        assert "class" in kinds
        assert "Server" in names
        assert "handle" in names
    print("test_parse_python_extracts_classes_and_funcs: ok")


def test_scan_skips_ignored_dirs():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "good.py").write_text("class A: pass\n", encoding="utf-8")
        (root / "node_modules").mkdir()
        (root / "node_modules" / "bad.js").write_text("export function x(){}", encoding="utf-8")
        files = scan(root)
        paths = [f.path for f in files]
        assert "good.py" in paths
        assert not any("node_modules" in p for p in paths)
    print("test_scan_skips_ignored_dirs: ok")


def test_render_produces_markdown():
    from repomap.core import FileMap, Symbol
    fm = FileMap(path="a.py")
    fm.symbols.append(Symbol("Foo", "class", 1, "class Foo"))
    out = render([fm], "demo")
    assert "# demo" in out
    assert "class Foo" in out
    print("test_render_produces_markdown: ok")


if __name__ == "__main__":
    test_parse_python_extracts_classes_and_funcs()
    test_scan_skips_ignored_dirs()
    test_render_produces_markdown()
    print("all repomap tests passed")
