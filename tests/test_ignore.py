"""Test extra_ignore."""
import tempfile
from pathlib import Path

from repomap.core import scan


def test_extra_ignore_dirs():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "a.py").write_text("class A: pass\n", encoding="utf-8")
        (root / "generated").mkdir()
        (root / "generated" / "g.py").write_text("class G: pass\n", encoding="utf-8")
        files = scan(root, extra_ignore=["generated"])
        paths = [f.path for f in files]
        assert "a.py" in paths
        assert not any("generated" in p for p in paths)
    print("test_extra_ignore_dirs: ok")


if __name__ == "__main__":
    test_extra_ignore_dirs()
    print("ignore test passed")
