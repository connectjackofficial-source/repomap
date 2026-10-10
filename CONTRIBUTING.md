## Contributing

PRs welcome. Keep the scanner dependency-free (stdlib only: `ast`, `os`, `re`).

## Development

Run the test suite from the repository root:

```bash
python tests/test_core.py
python tests/test_stats.py
python tests/test_ignore.py
python tests/test_json_depth.py
```

## Scanner additions

Adding a new language = adding one parser function and registering it in
`PARSERS` in `repomap/core.py`. Parsers must return a `FileMap` or `None`.
