"""repomap CLI: scan a repo and write a compact CONTEXT.md."""
import argparse
from pathlib import Path

from .core import scan, render


def main():
    ap = argparse.ArgumentParser(prog="repomap",
                                 description="Generate a compact codebase map for AI agents.")
    ap.add_argument("root", nargs="?", default=".",
                    help="repository root (default: current dir)")
    ap.add_argument("-o", "--output", default="CONTEXT.md",
                    help="output file (default: CONTEXT.md)")
    ap.add_argument("-q", "--quiet", action="store_true",
                    help="suppress summary output")
    args = ap.parse_args()

    root = Path(args.root)
    files = scan(root)
    out = render(files, root_name=root.resolve().name)
    Path(args.output).write_text(out, encoding="utf-8")
    if not args.quiet:
        print(f"repomap: scanned {len(files)} files -> {args.output}")


if __name__ == "__main__":
    main()
