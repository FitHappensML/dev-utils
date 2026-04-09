# Utils Collection

A collection of useful Python utilities for common tasks.

[![Open WhisperTranscribe in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/FitHappensML/dev-utils/blob/main/WhisperTranscribe_v1.ipynb)

## Table of Contents

### Scripts (stdlib-only)

| Utility | Description |
|---------|-------------|
| [ipynb_to_py](#ipynb_to_py) | Convert Jupyter notebooks to Python scripts (code only) |
| [collect_code](#collect_code) | Collect code from a directory into a single Markdown file |

### Colab Notebooks

| Notebook | Description |
|----------|-------------|
| [WhisperTranscribe](#whispertranscribe) | Audio transcription with OpenAI Whisper (3 presets, auto language detection) |

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

## WhisperTranscribe

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/FitHappensML/dev-utils/blob/main/WhisperTranscribe_v1.ipynb)

Google Colab notebook for audio-to-text transcription using OpenAI's Whisper model (via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) engine).

### Features

- Three presets: **small** (fast), **medium** (balanced), **high** (best quality)
- 99 languages with automatic detection
- Output: plain text (.txt), markdown (.md), SRT subtitles (.srt)
- Export audio with silence removed (.mp3)
- Runs on free Colab T4 GPU (all presets)

### Presets

| Preset | Model | Beam size | VRAM | Speed |
|--------|-------|-----------|------|-------|
| **small** | `small` | 1 | ~1 GB | ~30x realtime |
| **medium** | `medium` | 3 | ~2.5 GB | ~15x realtime |
| **high** | `large-v3` | 5 | ~5 GB | ~5x realtime |

### How to use

1. Open the notebook in Google Colab (click the badge above)
2. Set runtime to GPU: **Runtime → Change runtime type → GPU (T4)**
3. Run all setup cells (Section 1)
4. Select preset and options (Section 2)
5. Upload audio file (Section 3)
6. Run transcription (Section 4)
7. Download results (Section 5)

**Location:** `WhisperTranscribe_v1.ipynb`

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
