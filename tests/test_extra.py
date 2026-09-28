"""More repomap tests."""
import tempfile
from pathlib import Path

from repomap.core import parse_js, parse_python


def test_parse_js_exports():
    code = """
export function login() {}
export const CONFIG = 1
export class Server {}
"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.js"
        p.write_text(code, encoding="utf-8")
        fm = parse_js(p)
        names = {s.name for s in fm.symbols}
        assert "login" in names
        assert "CONFIG" in names
        assert "Server" in names
    print("test_parse_js_exports: ok")


def test_parse_python_handles_bad_file():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "bad.py"
        p.write_text("def broken(:", encoding="utf-8")
        fm = parse_python(p)
        assert fm is None
    print("test_parse_python_handles_bad_file: ok")


if __name__ == "__main__":
    test_parse_js_exports()
    test_parse_python_handles_bad_file()
    print("extra tests passed")
