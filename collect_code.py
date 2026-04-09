#!/usr/bin/env python3
"""Collect code from a directory into a single Markdown file for LLM context."""

import argparse
import json
import os
import sys
from pathlib import Path

# --- DEFAULTS ---

DEFAULTS = {
    "root_dir": ".",
    "output_file": "collected_code.md",
    "ignore_dirs": [
        ".git", "node_modules", "venv", "__pycache__",
        ".vscode", "dist", "build", ".idea"
    ],
    "ignore_files": [
        ".DS_Store", "package-lock.json", ".env"
    ],
    "ignore_extensions": [
        ".pyc", ".log", ".svg", ".png", ".jpg", ".jpeg",
        ".gif", ".ico", ".lock", ".zip", ".gz", ".tif",
        ".npy", ".exe", ".dll", ".so"
    ],
}

SETTINGS_FILE = Path(__file__).parent / "settings_collect_code.json"


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


def collect_code(root_dir: str, output_file: str,
                 ignore_dirs: set, ignore_files: set, ignore_extensions: set) -> None:
    """Walk root_dir and write all source files into a single Markdown file."""
    root_dir = os.path.abspath(root_dir)
    print(f"Collecting code from: '{root_dir}'")

    file_count = 0
    with open(output_file, "w", encoding="utf-8") as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

            for filename in sorted(filenames):
                if filename in ignore_files:
                    continue
                _, ext = os.path.splitext(filename)
                if ext in ignore_extensions:
                    continue
                if filename == os.path.basename(output_file):
                    continue

                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, root_dir).replace("\\", "/")

                lang = ext.lstrip(".")
                outfile.write(f"# {rel_path}\n\n```{lang}\n")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"\n[Could not read file: {e}]\n")
                outfile.write("\n```\n\n")
                file_count += 1
                print(f"  + {rel_path}")

    print(f"Done! {file_count} files -> '{output_file}'")


def main():
    cfg = load_settings()

    parser = argparse.ArgumentParser(
        description="Collect code from a directory into a single Markdown file"
    )
    parser.add_argument("root_dir", nargs="?", default=None,
                        help=f"Root directory to scan (default: {cfg['root_dir']})")
    parser.add_argument("-o", "--output", default=None,
                        help=f"Output .md file (default: {cfg['output_file']})")
    parser.add_argument("--ignore-dirs", nargs="*", default=None,
                        help="Directories to ignore")
    parser.add_argument("--ignore-files", nargs="*", default=None,
                        help="Files to ignore")
    parser.add_argument("--ignore-ext", nargs="*", default=None,
                        help="Extensions to ignore (e.g. .pyc .log)")

    args = parser.parse_args()

    root_dir = args.root_dir or cfg["root_dir"]
    output_file = args.output or cfg["output_file"]
    ignore_dirs = set(args.ignore_dirs if args.ignore_dirs is not None else cfg["ignore_dirs"])
    ignore_files = set(args.ignore_files if args.ignore_files is not None else cfg["ignore_files"])
    ignore_extensions = set(args.ignore_ext if args.ignore_ext is not None else cfg["ignore_extensions"])

    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)

    collect_code(root_dir, output_file, ignore_dirs, ignore_files, ignore_extensions)


if __name__ == "__main__":
    main()
