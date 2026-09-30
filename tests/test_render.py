"""More repomap tests."""
from repomap.core import render, FileMap, Symbol


def test_render_groups_by_dir():
    files = [
        FileMap(path="src/a.py", symbols=[Symbol("Foo", "class", 1)]),
        FileMap(path="src/b.py", symbols=[Symbol("bar", "function", 1)]),
        FileMap(path="tests/t.py", symbols=[Symbol("test_x", "function", 1)]),
    ]
    out = render(files, "demo")
    assert "src/" in out
    assert "tests/" in out
    print("test_render_groups_by_dir: ok")


if __name__ == "__main__":
    test_render_groups_by_dir()
    print("extra repomap tests passed")
