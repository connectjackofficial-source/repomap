"""Tests for repomap largest_files."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import largest_files


def _tree():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "src").mkdir()
    (root / "data").mkdir()
    (root / "src" / "app.py").write_text("print('x')\n")
    (root / "data" / "model.bin").write_bytes(b"\x00" * 5000)
    (root / "data" / "cache.log").write_bytes(b"1" * 300)
    (root / "vendor").mkdir()
    (root / "vendor" / "big.bin").write_bytes(b"\x01" * 9000)
    return root, tmp


def test_biggest_first():
    root, tmp = _tree()
    top = largest_files(str(root), n=3)
    assert top[0]["path"] == "vendor/big.bin"
    assert top[0]["bytes"] == 9000
    assert top[1]["path"] == "data/model.bin"
    assert top[2]["path"] == "data/cache.log"
    tmp.cleanup()
    print("test_biggest_first: ok")


def test_ignore_dirs():
    root, tmp = _tree()
    top = largest_files(str(root), n=3, extra_ignore=["vendor"])
    assert all("vendor" not in t["path"] for t in top)
    assert top[0]["path"] == "data/model.bin"
    tmp.cleanup()
    print("test_ignore_dirs: ok")


def test_n_limit():
    root, tmp = _tree()
    top = largest_files(str(root), n=1)
    assert len(top) == 1
    tmp.cleanup()
    print("test_n_limit: ok")


def test_empty_tree():
    tmp = tempfile.TemporaryDirectory()
    assert largest_files(tmp.name) == []
    tmp.cleanup()
    print("test_empty_tree: ok")


if __name__ == "__main__":
    test_biggest_first()
    test_ignore_dirs()
    test_n_limit()
    test_empty_tree()
    print("repomap largest_files tests passed")
