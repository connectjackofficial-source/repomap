"""Tests for language stats and min_symbols filtering."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import language_stats, scan


def test_language_stats():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "proj"
        (root / "pkg").mkdir(parents=True)
        (root / "pkg" / "a.py").write_text(
            "def one(): pass\nclass Two:\n    pass\n", encoding="utf-8")
        (root / "pkg" / "b.py").write_text("def three(): pass\n", encoding="utf-8")
        (root / "pkg" / "c.js").write_text(
            "export function ui() {}\n", encoding="utf-8")
        files = scan(root)
        stats = language_stats(files)
        assert stats[".py"]["files"] == 2
        assert stats[".py"]["symbols"] == 3
        assert stats[".js"]["files"] == 1
    print("test_language_stats: ok")


def test_min_symbols_filter():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "proj"
        (root / "pkg").mkdir(parents=True)
        (root / "pkg" / "a.py").write_text(
            "def one(): pass\nclass Two:\n    pass\n", encoding="utf-8")
        (root / "pkg" / "b.py").write_text("X = 1\n", encoding="utf-8")
        all_files = scan(root, min_symbols=1)
        # b.py has one constant -> included
        assert len(all_files) == 2
        only_big = scan(root, min_symbols=2)
        # only a.py qualifies
        assert len(only_big) == 1
        assert only_big[0].path == "pkg/a.py"
    print("test_min_symbols_filter: ok")


if __name__ == "__main__":
    test_language_stats()
    test_min_symbols_filter()
    print("repomap stats tests passed")
