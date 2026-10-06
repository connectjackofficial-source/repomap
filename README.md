# repomap

> Scan a codebase and generate a compact `CONTEXT.md` so any AI coding agent
> understands your project in 30 seconds, not 30 minutes.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

Every time you point Claude Code / Cursor / Codex at an unfamiliar repo, it
burns hundreds of thousands of tokens re-reading files to figure out where the
entry points are, what the classes do, and how things connect.

`repomap` pre-computes that once: it walks the tree, parses Python with `ast`
and JS/TS with heuristics, and writes a tight map of files, classes, functions,
and exports. Drop `CONTEXT.md` at the root and your agent starts oriented.

## Install

```bash
git clone https://github.com/connectjackofficial-source/repomap.git
cd repomap
python -m repomap.cli /path/to/your/repo
```

## Usage

```bash
# generate CONTEXT.md for the current project
python -m repomap.cli .

# write somewhere else
python -m repomap.cli ~/src/awesome-app -o docs/MAP.md

# skip extra directories
python -m repomap.cli . --ignore generated temp
```

## Example output

```markdown
# my-app - codebase map

**`src/server.py`**
- class Server (methods: listen, route, use)
- def create_app(config)

**`src/db.py`**
- class Pool (methods: query, close)
- const DEFAULT_LIMIT
```

## How it works

| Language | Extraction |
| --- | --- |
| Python | `ast` — classes, methods, functions, constants |
| JS / TS / JSX / TSX | regex — exports, classes, top-level functions |

Skips `.git`, `node_modules`, `__pycache__`, virtualenvs. No network, no
third-party deps.

## Use cases

- Speed up onboarding of new AI coding agents
- Generate a reference doc for contributors
- Spot entry points and public exports before a refactor

## License

[MIT](LICENSE)
