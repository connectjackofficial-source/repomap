"""Tests for repomap.todo_scan."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import todo_scan


def test_finds_markers():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "src").mkdir()
        (root / "src" / "a.py").write_text(
            "def f():\n    # TODO handle edge case\n    pass\n")
        (root / "src" / "b.md").write_text("## FIXME broken link\n")
        hits = todo_scan(root)
        assert len(hits) == 2
        assert hits[0]["file"] == "src/a.py"
        assert hits[0]["marker"] == "TODO"
        assert hits[0]["line"] == 2
        assert hits[1]["marker"] == "FIXME"
    print("test_finds_markers: ok")


def test_skips_binary_and_git():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".git").mkdir()
        (root / ".git" / "config").write_text("TODO not scanned\n")
        (root / "blob.bin").write_bytes(b"\x00TODO\xff")
        assert todo_scan(root) == []
    print("test_skips_binary_and_git: ok")


def test_pattern_filter():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "a.py").write_text("x = 1  # TODO later\n")
        (root / "b.py").write_text("y = 2  # HACK around\n")
        hits = todo_scan(root, patterns=("HACK",))
        assert len(hits) == 1
        assert hits[0]["marker"] == "HACK"
    print("test_pattern_filter: ok")


if __name__ == "__main__":
    test_finds_markers()
    test_skips_binary_and_git()
    test_pattern_filter()
    print("repomap todo_scan tests passed")
