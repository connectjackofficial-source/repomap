"""Tests for JSON output and max-depth."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import scan, render_json, render


def _make_tree(root: Path):
    (root / "pkg").mkdir()
    (root / "pkg" / "a.py").write_text("def alpha():\n    pass\n", encoding="utf-8")
    (root / "pkg" / "deep").mkdir()
    (root / "pkg" / "deep" / "b.py").write_text(
        "class Beta:\n    pass\n", encoding="utf-8")


def test_json_output():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _make_tree(root)
        files = scan(root)
        data = render_json(files, root_name=root.name)
        import json
        parsed = json.loads(data)
        assert parsed["root"] == root.name
        assert parsed["files"]
        sym = parsed["files"][0]["symbols"][0]
        assert {"name", "kind", "line"} <= set(sym)
    print("test_json_output: ok")


def test_max_depth():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _make_tree(root)
        # depth 1 = only files directly under root
        files = scan(root, max_depth=1)
        names = [f.path for f in files]
        assert all("/" not in p for p in names), names
    print("test_max_depth: ok")


def test_render_still_works():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _make_tree(root)
        files = scan(root)
        text = render(files, root_name=root.name)
        assert text.startswith("#")
    print("test_render_still_works: ok")


if __name__ == "__main__":
    test_json_output()
    test_max_depth()
    test_render_still_works()
    print("repomap json/depth tests passed")
