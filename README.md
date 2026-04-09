# Utils Collection

A collection of useful Python utilities for common tasks. Zero dependencies — only Python stdlib.

## Table of Contents

| Utility | Description |
|---------|-------------|
| [ipynb_to_py](#ipynb_to_py) | Convert Jupyter notebooks to Python scripts (code only) |
| [collect_code](#collect_code) | Collect code from a directory into a single Markdown file |

## Settings

Each script supports an optional JSON settings file: `settings_<script_name>.json` in the same directory. If the file doesn't exist, defaults are used. CLI arguments always override settings.

---

## ipynb_to_py

Convert Jupyter notebooks (`.ipynb`) to Python scripts, extracting only the code without outputs, images, or metadata.

### Features

- Extracts code from all code cells
- Removes cell outputs, images, and execution counts
- Optionally includes markdown cells as comments
- Preserves blank lines between cells for readability
- Simple CLI interface

### Usage

```bash
python ipynb_to_py.py input.ipynb
python ipynb_to_py.py input.ipynb -o output.py
python ipynb_to_py.py input.ipynb --include-markdown
```

### Options

| Flag | Description |
|------|-------------|
| `input` | Input `.ipynb` file (required) |
| `-o, --output` | Output `.py` file (default: same name with `.py`) |
| `--include-markdown` | Include markdown cells as Python comments |

### Settings file: `settings_ipynb_to_py.json`

```json
{
  "include_markdown": false
}
```

---

## collect_code

Collect all source code from a directory into a single Markdown file — useful for feeding code to LLMs.

### Features

- Recursively scans a directory
- Ignores configurable directories, files, and extensions
- Outputs Markdown with syntax-highlighted code blocks
- Auto-detects language from file extension

### Usage

```bash
python collect_code.py                          # scan current dir
python collect_code.py /path/to/project         # scan specific dir
python collect_code.py /path -o context.md      # custom output file
python collect_code.py . --ignore-dirs venv dist
python collect_code.py . --ignore-ext .log .csv
```

### Options

| Flag | Description |
|------|-------------|
| `root_dir` | Directory to scan (default: `.`) |
| `-o, --output` | Output `.md` file (default: `collected_code.md`) |
| `--ignore-dirs` | Directories to skip |
| `--ignore-files` | Files to skip |
| `--ignore-ext` | Extensions to skip (e.g. `.pyc .log`) |

### Settings file: `settings_collect_code.json`

```json
{
  "root_dir": ".",
  "output_file": "collected_code.md",
  "ignore_dirs": [".git", "node_modules", "venv", "__pycache__", ".vscode", "dist", "build", ".idea"],
  "ignore_files": [".DS_Store", "package-lock.json", ".env"],
  "ignore_extensions": [".pyc", ".log", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".lock", ".zip", ".gz"]
}
```

---

## Testing

```bash
python dev-main-test/run_tests.py
```

Tests use mock data in `dev-main-test/mock_data/` and require no external dependencies.

---

## Adding New Utilities

1. Create a new Python script in `dev-main/`
2. Add optional `settings_<name>.json` support (defaults must work without it)
3. Update this README
4. Add tests in `dev-main-test/`

---

## License

MIT
