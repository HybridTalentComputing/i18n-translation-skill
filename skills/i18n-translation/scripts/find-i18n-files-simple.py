#!/usr/bin/env python3
"""
Simple File List Generator for i18n

Outputs only file paths requiring internationalization.
Minimal output to save Claude context.

Usage:
    python find-i18n-files-simple.py <source_dir> [options]

Options:
    --output, -o     Output file (default: i18n_files.txt)
    --format, -f     Output format: txt, json (default: txt)
    --file-types     Comma-separated file extensions (default: js,jsx,ts,tsx,vue,html)
    --exclude        Directories to exclude (default: node_modules,dist,build)
    --min-strings    Minimum strings to include file (default: 1)
    --workers, -w    Number of parallel workers (default: CPU count)
    --no-filter      Don't filter test files (include all)

Example:
    python find-i18n-files-simple.py src --output i18n_files.txt
    python find-i18n-files-simple.py src --format json --output files.json
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Set
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import time


# Pre-compiled regex patterns for quick detection
DETECTION_PATTERNS = {
    'jsx_content': re.compile(r'>[A-Z][^<{]{2,}<'),
    'buttons': re.compile(r'<button[^>]*>[A-Z][^<]{2,}</button>', re.IGNORECASE),
    'labels': re.compile(r'<label[^>]*>[A-Z][^<]{2,}</label>', re.IGNORECASE),
    'placeholders': re.compile(r'placeholder=["\'][A-Za-z][^"\']{2,}["\']', re.IGNORECASE),
    'attributes': re.compile(r'(?:title|alt|aria-label)=["\'][A-Za-z][^"\']{2,}["\']', re.IGNORECASE),
    'string_literals': re.compile(r'["\'][A-Z][a-zA-Z\s]{3,}["\']'),
}


def quick_file_scan(filepath: Path) -> int:
    """Quick scan to count user-facing strings in file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0

    # Quick checks for user-facing strings
    count = 0
    for pattern in DETECTION_PATTERNS.values():
        count += len(pattern.findall(content))

    return count


def process_file(filepath: Path) -> tuple:
    """Wrapper for parallel processing. Returns (path, string_count)."""
    return str(filepath), quick_file_scan(filepath)


def find_i18n_files(
    source_dir: Path,
    file_types: List[str],
    exclude_dirs: List[str],
    min_strings: int = 1,
    workers: int = None,
    filter_tests: bool = True
) -> List[str]:
    """
    Find files requiring internationalization.

    Returns list of file paths.
    """
    all_files = []

    # Collect all files
    for file_type in file_types:
        pattern = f"**/*.{file_type}"
        for filepath in source_dir.rglob(pattern):
            file_str = str(filepath)

            # Skip excluded directories
            if any(exclude_dir in filepath.parts for exclude_dir in exclude_dirs):
                continue

            # Skip test files if filtering enabled
            if filter_tests:
                if any(pattern in file_str.lower() for pattern in [
                    '.test.', '.spec.', '.stories.', '__tests__', '\\test\\', '/test/',
                    '\\e2e\\', '/e2e/', '\\fixtures\\', '/fixtures/', '\\evals\\', '/evals/'
                ]):
                    continue

            all_files.append(filepath)

    if not all_files:
        return []

    if workers is None:
        workers = min(cpu_count(), len(all_files))

    # Process files in parallel
    results = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_file, fp): fp for fp in all_files}

        for future in as_completed(futures):
            filepath, string_count = future.result()

            if string_count >= min_strings:
                results.append((filepath, string_count))

    # Sort by string count (descending) and extract just paths
    results.sort(key=lambda x: x[1], reverse=True)
    return [path for path, count in results]


def output_text(files: List[str], output_file: str):
    """Output results as simple text file (one path per line)."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for filepath in files:
            f.write(f"{filepath}\n")


def output_json(files: List[str], output_file: str):
    """Output results as simple JSON array."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Find files requiring i18n - Simple output for Claude'
    )
    parser.add_argument(
        'source_dir',
        type=str,
        help='Source directory to scan'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='i18n_files.txt',
        help='Output file (default: i18n_files.txt)'
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['txt', 'json'],
        default='txt',
        help='Output format (default: txt)'
    )
    parser.add_argument(
        '--file-types',
        type=str,
        default='js,jsx,ts,tsx,vue,html',
        help='Comma-separated file extensions to scan'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        default='node_modules,dist,build,.git',
        help='Comma-separated directories to exclude'
    )
    parser.add_argument(
        '--min-strings',
        type=int,
        default=1,
        help='Minimum string count to include file'
    )
    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=None,
        help='Number of parallel workers'
    )
    parser.add_argument(
        '--no-filter',
        action='store_true',
        help='Don\'t filter test files (include all)'
    )

    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    file_types = args.file_types.split(',')
    exclude_dirs = args.exclude.split(',')

    print(f"[*] Scanning {source_dir}...")

    start_time = time.time()

    files = find_i18n_files(
        source_dir,
        file_types,
        exclude_dirs,
        args.min_strings,
        args.workers,
        filter_tests=not args.no_filter
    )

    elapsed = time.time() - start_time

    print(f"[OK] Found {len(files)} files needing i18n (in {elapsed:.2f}s)")

    # Output results
    if args.format == 'txt':
        output_text(files, args.output)
    elif args.format == 'json':
        output_json(files, args.output)

    print(f"[OK] Saved to: {args.output}")

    # Show preview
    if files:
        print(f"\n[*] Preview (first 10 files):")
        for filepath in files[:10]:
            print(f"  - {filepath}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")


if __name__ == '__main__':
    main()
