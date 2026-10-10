"""repomap CLI: scan a repo and write a compact CONTEXT.md."""
import argparse
import json
from pathlib import Path

from .core import hotspots, language_stats, scan, render, render_json


def main():
    ap = argparse.ArgumentParser(prog="repomap",
                                 description="Generate a compact codebase map for AI agents.")
    ap.add_argument("root", nargs="?", default=".",
                    help="repository root (default: current dir)")
    ap.add_argument("-o", "--output", default="CONTEXT.md",
                    help="output file (default: CONTEXT.md)")
    ap.add_argument("-q", "--quiet", action="store_true",
                    help="suppress summary output")
    ap.add_argument("--ignore", nargs="*", default=[],
                    help="extra directories to skip")
    ap.add_argument("--max-depth", type=int, default=None,
                    help="limit scan to N levels deep")
    ap.add_argument("--min-symbols", type=int, default=1,
                    help="skip files with fewer symbols than this")
    ap.add_argument("--stats", action="store_true",
                    help="print per-language file/symbol counts")
    ap.add_argument("--hotspots", type=int, nargs="?", const=10, default=None,
                    help="print TOP N files by symbol count (refactor targets)")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown",
                    help="output format (default: markdown)")
    args = ap.parse_args()

    root = Path(args.root)
    files = scan(root, extra_ignore=args.ignore, max_depth=args.max_depth,
                 min_symbols=args.min_symbols)
    if args.format == "json":
        out = render_json(files, root_name=root.resolve().name)
    else:
        out = render(files, root_name=root.resolve().name)
    Path(args.output).write_text(out, encoding="utf-8")
    if not args.quiet:
        print(f"repomap: scanned {len(files)} files -> {args.output}")
    if args.stats:
        print(json.dumps(language_stats(files), indent=2))
    if args.hotspots is not None:
        print(json.dumps({"hotspots": hotspots(files, args.hotspots)},
                         indent=2))


if __name__ == "__main__":
    main()
