#!/usr/bin/env python3
"""
Find Files Requiring Internationalization

This script quickly identifies which files contain user-facing strings
that need to be internationalized, generating a prioritized list for Claude to process.

Benefits:
- Pre-scan files to avoid repeated Claude searches
- Prioritize files by string count
- Filter out files that don't need i18n
- Generate actionable work list

Usage:
    python find-i18n-files.py <source_dir> [options]

Options:
    --output, -o     Output file (default: i18n_files.json)
    --format, -f     Output format: json, csv, text (default: json)
    --file-types     Comma-separated file extensions (default: js,jsx,ts,tsx,vue,html)
    --exclude        Directories to exclude (default: node_modules,dist,build)
    --min-strings    Minimum strings to include file (default: 1)
    --workers, -w    Number of parallel workers (default: CPU count)
    --verbose, -v    Show detailed progress

Example:
    python find-i18n-files.py src --format json --output i18n_files.json
"""

import re
import os
import sys
import json
import csv
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import time


# Pre-compiled regex patterns for quick detection
DETECTION_PATTERNS = {
    'jsx_content': re.compile(r'>[A-Z][^<{]{2,}<'),  # Capitalized text in JSX
    'buttons': re.compile(r'<button[^>]*>[A-Z][^<]{2,}</button>', re.IGNORECASE),
    'labels': re.compile(r'<label[^>]*>[A-Z][^<]{2,}</label>', re.IGNORECASE),
    'placeholders': re.compile(r'placeholder=["\'][A-Za-z][^"\']{2,}["\']', re.IGNORECASE),
    'attributes': re.compile(r'(?:title|alt|aria-label)=["\'][A-Za-z][^"\']{2,}["\']', re.IGNORECASE),
    'string_literals': re.compile(r'["\'][A-Z][a-zA-Z\s]{3,}["\']'),  # Capitalized strings
}


def quick_file_scan(filepath: Path) -> Dict[str, any]:
    """
    Quick scan to detect if file contains user-facing strings.

    Returns basic statistics without detailed extraction.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return {
            'path': str(filepath),
            'error': 'Cannot read file',
            'string_count': 0,
            'needs_i18n': False
        }

    # Quick checks for user-facing strings
    indicators = {
        'jsx_text': len(DETECTION_PATTERNS['jsx_content'].findall(content)),
        'buttons': len(DETECTION_PATTERNS['buttons'].findall(content)),
        'labels': len(DETECTION_PATTERNS['labels'].findall(content)),
        'placeholders': len(DETECTION_PATTERNS['placeholders'].findall(content)),
        'attributes': len(DETECTION_PATTERNS['attributes'].findall(content)),
        'string_literals': len(DETECTION_PATTERNS['string_literals'].findall(content)),
    }

    # Estimate total string count (may have overlaps)
    total_strings = sum(indicators.values())

    # File needs i18n if it has any user-facing strings
    needs_i18n = total_strings > 0

    return {
        'path': str(filepath),
        'relative_path': str(filepath.relative_to(Path.cwd())) if filepath.is_absolute() else str(filepath),
        'size_bytes': len(content),
        'string_count': total_strings,
        'indicators': indicators,
        'needs_i18n': needs_i18n
    }


def process_file(filepath: Path) -> Dict[str, any]:
    """Wrapper for parallel processing."""
    return quick_file_scan(filepath)


def find_i18n_files_parallel(
    source_dir: Path,
    file_types: List[str],
    exclude_dirs: List[str],
    min_strings: int = 1,
    workers: int = None,
    verbose: bool = False
) -> Tuple[List[Dict], Dict]:
    """
    Scan directory in parallel to find files needing internationalization.

    Returns:
        Tuple of (files_list, statistics)
    """
    all_files = []

    # Collect all files
    for file_type in file_types:
        pattern = f"**/*.{file_type}"
        for filepath in source_dir.rglob(pattern):
            if any(exclude_dir in filepath.parts for exclude_dir in exclude_dirs):
                continue
            all_files.append(filepath)

    if not all_files:
        return [], {}

    if workers is None:
        workers = min(cpu_count(), len(all_files))

    print(f"[*] Scanning {len(all_files)} files with {workers} workers...")

    # Process files in parallel
    results = []
    needs_i18n_count = 0
    skipped_count = 0

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_file, fp): fp for fp in all_files}

        for future in as_completed(futures):
            result = future.result()

            if result['string_count'] >= min_strings:
                results.append(result)
                if result['needs_i18n']:
                    needs_i18n_count += 1
            else:
                skipped_count += 1

            if verbose and len(results) % 50 == 0:
                print(f"  Processed {len(results)} files...")

    # Sort by string count (descending)
    results.sort(key=lambda x: x['string_count'], reverse=True)

    # Generate statistics
    stats = {
        'total_files_scanned': len(all_files),
        'files_needing_i18n': needs_i18n_count,
        'files_below_threshold': skipped_count,
        'total_strings_found': sum(r['string_count'] for r in results),
        'average_strings_per_file': sum(r['string_count'] for r in results) / len(results) if results else 0,
    }

    return results, stats


def output_json(results: List[Dict], stats: Dict, output_file: str):
    """Output results in JSON format (Claude-friendly)."""
    output = {
        'metadata': {
            'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': stats
        },
        'files': results
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def output_csv(results: List[Dict], stats: Dict, output_file: str):
    """Output results in CSV format."""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Priority',
            'File Path',
            'String Count',
            'Size (bytes)',
            'Buttons',
            'Labels',
            'Placeholders',
            'Attributes',
            'String Literals'
        ])

        # Data rows
        for i, file_data in enumerate(results, 1):
            writer.writerow([
                i,
                file_data['relative_path'],
                file_data['string_count'],
                file_data['size_bytes'],
                file_data['indicators'].get('buttons', 0),
                file_data['indicators'].get('labels', 0),
                file_data['indicators'].get('placeholders', 0),
                file_data['indicators'].get('attributes', 0),
                file_data['indicators'].get('string_literals', 0),
            ])

    # Write stats to separate file
    stats_file = output_file.replace('.csv', '_stats.txt')
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("I18N File Detection Statistics\n")
        f.write("=" * 50 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")


def output_text(results: List[Dict], stats: Dict, output_file: str):
    """Output results in text format (human-readable)."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Files Requiring Internationalization\n")
        f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Statistics\n\n")
        for key, value in stats.items():
            f.write(f"- {key}: {value}\n\n")

        f.write("## Files (Prioritized by String Count)\n\n")

        for i, file_data in enumerate(results, 1):
            f.write(f"{i}. **{file_data['relative_path']}** ({file_data['string_count']} strings)\n")
            f.write(f"   Size: {file_data['size_bytes']:,} bytes\n")
            f.write(f"   Indicators: ")
            f.write(f"buttons={file_data['indicators'].get('buttons', 0)}, ")
            f.write(f"labels={file_data['indicators'].get('labels', 0)}, ")
            f.write(f"placeholders={file_data['indicators'].get('placeholders', 0)}, ")
            f.write(f"attributes={file_data['indicators'].get('attributes', 0)}, ")
            f.write(f"strings={file_data['indicators'].get('string_literals', 0)}\n\n")


def print_summary(results: List[Dict], stats: Dict, top_n: int = 20):
    """Print summary to console."""
    print(f"\n[*] Scan Results Summary")
    print("=" * 60)
    print(f"Total files scanned: {stats['total_files_scanned']}")
    print(f"Files needing i18n: {stats['files_needing_i18n']}")
    print(f"Files below threshold: {stats['files_below_threshold']}")
    print(f"Total strings found: {stats['total_strings_found']}")
    print(f"Average strings per file: {stats['average_strings_per_file']:.1f}")
    print()

    # Show top files
    top_files = results[:top_n]
    if top_files:
        print(f"[*] Top {len(top_files)} Files by String Count:")
        print("-" * 60)

        for i, file_data in enumerate(top_files, 1):
            print(f"{i:2d}. {file_data['string_count']:3d} strings - {file_data['relative_path']}")

        if len(results) > top_n:
            print(f"\n... and {len(results) - top_n} more files")


def main():
    parser = argparse.ArgumentParser(
        description='Find files requiring internationalization (i18n).'
    )
    parser.add_argument(
        'source_dir',
        type=str,
        help='Source directory to scan'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='i18n_files.json',
        help='Output file (default: i18n_files.json)'
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['json', 'csv', 'text'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--file-types',
        type=str,
        default='js,jsx,ts,tsx,vue,html',
        help='Comma-separated file extensions to scan (default: js,jsx,ts,tsx,vue,html)'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        default='node_modules,dist,build,.git',
        help='Comma-separated directories to exclude (default: node_modules,dist,build,.git)'
    )
    parser.add_argument(
        '--min-strings',
        type=int,
        default=1,
        help='Minimum string count to include file (default: 1)'
    )
    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=None,
        help=f'Number of parallel workers (default: CPU count)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    file_types = args.file_types.split(',')
    exclude_dirs = args.exclude.split(',')

    print("[*] Finding Files Requiring Internationalization")
    print(f"[*] Scanning: {source_dir}")
    print(f"[*] File types: {', '.join(file_types)}")
    print(f"[*] Excluding: {', '.join(exclude_dirs)}")
    print(f"[*] Minimum strings: {args.min_strings}")
    print()

    start_time = time.time()

    results, stats = find_i18n_files_parallel(
        source_dir,
        file_types,
        exclude_dirs,
        args.min_strings,
        args.workers,
        args.verbose
    )

    elapsed = time.time() - start_time

    print(f"\n[OK] Scan Complete (in {elapsed:.2f}s)")

    # Print summary
    print_summary(results, stats, top_n=20)

    # Output results
    print(f"\n[*] Writing output to: {args.output}")

    if args.format == 'json':
        output_json(results, stats, args.output)
    elif args.format == 'csv':
        output_csv(results, stats, args.output)
    elif args.format == 'text':
        output_text(results, stats, args.output)

    print("[OK] Done!")
    print()
    print("[TIP] Claude can now read this file to know exactly which files to process!")
    if args.format == 'json':
        print("[TIP] Use: i18n_files.json contains prioritized file list with string counts")


if __name__ == '__main__':
    main()
