# FAQ

**Does it handle TypeScript well?** Basic regex extraction.

**Can I get machine-readable output?** Yes — `--format json` writes a
structured array of files and symbols, handy for tooling or feeding a map
into another program.

**How do I scan only the top levels?** Pass `--max-depth N`; directories
deeper than N are skipped entirely.
