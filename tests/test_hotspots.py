"""Tests for hotspot ranking."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from repomap.core import FileMap, Symbol, hotspots


def _fm(path, n_symbols):
    fm = FileMap(path=path)
    for i in range(n_symbols):
        fm.symbols.append(Symbol(f"s{i}", "function", i))
    return fm


def test_hotspots_ranks_descending():
    files = [_fm("a.py", 2), _fm("b.py", 9), _fm("c.py", 5)]
    top = hotspots(files, n=3)
    assert top[0] == ("b.py", 9)
    assert top[1] == ("c.py", 5)
    assert top[2] == ("a.py", 2)
    print("test_hotspots_ranks_descending: ok")


def test_hotspots_limit():
    files = [_fm("a.py", 2), _fm("b.py", 9), _fm("c.py", 5)]
    assert len(hotspots(files, n=2)) == 2
    assert len(hotspots(files, n=99)) == 3
    print("test_hotspots_limit: ok")


def test_hotspots_empty():
    assert hotspots([]) == []
    print("test_hotspots_empty: ok")


if __name__ == "__main__":
    test_hotspots_ranks_descending()
    test_hotspots_limit()
    test_hotspots_empty()
    print("repomap hotspots tests passed")
