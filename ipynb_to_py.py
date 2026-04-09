#!/usr/bin/env python3
"""Convert Jupyter notebooks to Python scripts (code only, no outputs)."""

import argparse
import json
import sys
from pathlib import Path

# --- DEFAULTS ---

DEFAULTS = {
    "include_markdown": False,
}

SETTINGS_FILE = Path(__file__).parent / "settings_ipynb_to_py.json"


def load_settings() -> dict:
    """Load settings from JSON file if it exists, merge with defaults."""
    config = dict(DEFAULTS)
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                user = json.load(f)
            config.update(user)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not read settings file: {e}", file=sys.stderr)
    return config


def notebook_to_py(input_path: Path, output_path: Path | None = None,
                   include_markdown: bool = False) -> Path:
    """Convert Jupyter notebook to Python file (code only)."""
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook.get('cells', [])
    code_lines = []

    for cell in cells:
        cell_type = cell.get('cell_type', '')
        if cell_type == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                source = ''.join(source)
            if source.strip():
                code_lines.append(source.rstrip())
                code_lines.append('')
        elif cell_type == 'markdown' and include_markdown:
            source = cell.get('source', [])
            if isinstance(source, list):
                source = ''.join(source)
            if source.strip():
                commented = '\n'.join(f'# {line}' for line in source.strip().splitlines())
                code_lines.append(commented)
                code_lines.append('')

    if output_path is None:
        output_path = input_path.with_suffix('.py')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(code_lines))

    print(f"Converted: {input_path} -> {output_path}")
    return output_path


def main():
    cfg = load_settings()

    parser = argparse.ArgumentParser(description='Convert Jupyter notebook to Python file (code only)')
    parser.add_argument('input', type=Path, help='Input .ipynb file')
    parser.add_argument('-o', '--output', type=Path, help='Output .py file (default: same name with .py)')
    parser.add_argument('--include-markdown', action='store_true',
                        default=None,
                        help='Include markdown cells as comments')

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.input.suffix != '.ipynb':
        print(f"Warning: Expected .ipynb file, got {args.input.suffix}", file=sys.stderr)

    include_md = args.include_markdown if args.include_markdown is not None else cfg["include_markdown"]
    notebook_to_py(args.input, args.output, include_markdown=include_md)


if __name__ == '__main__':
    main()
