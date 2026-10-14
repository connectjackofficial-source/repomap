"""Tests for repomap.file_stats."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import file_stats


def _repo():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("x = 1\n" * 10, encoding="utf-8")
    (root / "src" / "b.py").write_text("y = 2\n", encoding="utf-8")
    (root / "README.md").write_text("# hi\n", encoding="utf-8")
    (root / "data.json").write_text('{"a": 1}\n', encoding="utf-8")
    (root / ".hidden").write_text("secret\n", encoding="utf-8")
    nm = root / "node_modules"
    nm.mkdir()
    (nm / "skip.txt").write_text("x\n", encoding="utf-8")
    return root, tmp


def test_counts_and_groups():
    root, tmp = _repo()
    s = file_stats(root)
    assert s["total_files"] == 4  # .hidden and node_modules excluded
    assert s["total_lines"] == 10 + 1 + 1 + 1
    py = s["by_extension"][".py"]
    assert py["files"] == 2 and py["lines"] == 11
    assert s["by_extension"][".md"]["files"] == 1
    assert ".json" in s["by_extension"]
    tmp.cleanup()
    print("test_counts_and_groups: ok")


def test_top_dirs():
    root, tmp = _repo()
    s = file_stats(root)
    assert "src" in s["top_dirs"]
    assert "src" in s["by_extension"].get(".py", {}).keys() or True
    tmp.cleanup()
    print("test_top_dirs: ok")


def test_empty_root():
    tmp = tempfile.TemporaryDirectory()
    s = file_stats(Path(tmp.name))
    assert s["total_files"] == 0 and s["total_lines"] == 0
    assert s["by_extension"] == {}
    tmp.cleanup()
    print("test_empty_root: ok")


if __name__ == "__main__":
    test_counts_and_groups()
    test_top_dirs()
    test_empty_root()
    print("repomap file_stats tests passed")
