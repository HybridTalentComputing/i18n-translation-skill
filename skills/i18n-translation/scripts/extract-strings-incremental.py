#!/usr/bin/env python3
"""
Incremental String Extraction Script for i18n Internationalization

Optimized version with:
- File modification tracking (only scans changed files)
- Persistent cache database
- Hash-based content change detection
- Fast resume capability

Speed improvement: 10-100x faster for subsequent runs

Usage:
    python extract-strings-incremental.py <source_dir> [options]

Options:
    --output, -o     Output file for extracted strings (default: extracted_strings.txt)
    --format, -f     Output format: text, json, csv (default: text)
    --file-types     Comma-separated list of file extensions (default: js,jsx,ts,tsx,vue,html)
    --exclude        Comma-separated list of directories to exclude (default: node_modules,dist,build)
    --cache-dir      Directory for cache storage (default: .i18n-cache)
    --force, -F      Force full re-scan (ignores cache)
    --verbose, -v    Show detailed progress

Example:
    python extract-strings-incremental.py src --format json --output strings.json
"""

import re
import os
import sys
import json
import csv
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
from datetime import datetime


CACHE_DIR = ".i18n-cache"
CACHE_FILE = "extraction_cache.json"


def calculate_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of file content."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except Exception:
        return ""


def load_cache(cache_dir: str) -> Dict:
    """Load extraction cache from disk."""
    cache_path = Path(cache_dir) / CACHE_FILE
    if not cache_path.exists():
        return {}
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(cache: Dict, cache_dir: str) -> None:
    """Save extraction cache to disk."""
    cache_path = Path(cache_dir) / CACHE_FILE
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)


# Pre-compiled regex patterns (same as fast version)
REGEX_PATTERNS = {
    'jsx_content': re.compile(r'>([^<{]+)<'),
    'buttons': re.compile(r'<button[^>]*>([^<]+)</button>', re.IGNORECASE),
    'labels': re.compile(r'<label[^>]*>([^<]+)</label>', re.IGNORECASE),
    'placeholders': re.compile(r'placeholder=["\']([^"\']+)["\']', re.IGNORECASE),
    'title': re.compile(r'title=["\']([^"\']+)["\']', re.IGNORECASE),
    'alt': re.compile(r'alt=["\']([^"\']+)["\']', re.IGNORECASE),
    'aria_label': re.compile(r'aria-label=["\']([^"\']+)["\']', re.IGNORECASE),
    'message': re.compile(r'message\s*[:=]\s*["\']([^"\']+)["\']'),
    'toast_title': re.compile(r'title\s*[:=]\s*["\']([^"\']+)["\']'),
    'text': re.compile(r'text\s*[:=]\s*["\']([^"\']+)["\']'),
    'ui_literals': re.compile(r'["\']([A-Z][a-zA-Z\s]{2,})["\']'),
}

VALIDATION_KEYWORDS = ['error', 'success', 'warning', 'info', 'confirm',
                       'saved', 'deleted', 'updated', 'login', 'logout']
VALIDATION_PATTERNS = ['required', 'invalid', 'error', 'must', 'cannot', 'please']


def extract_jsx_strings(content: str) -> Set[str]:
    """Extract strings from JSX/Vue template content between tags."""
    matches = REGEX_PATTERNS['jsx_content'].findall(content)
    return {m.strip() for m in matches if m.strip()}


def extract_button_text(content: str) -> Set[str]:
    """Extract button text."""
    matches = REGEX_PATTERNS['buttons'].findall(content)
    return {m.strip() for m in matches if m.strip()}


def extract_label_text(content: str) -> Set[str]:
    """Extract label text."""
    matches = REGEX_PATTERNS['labels'].findall(content)
    return {m.strip() for m in matches if m.strip()}


def extract_placeholders(content: str) -> Set[str]:
    """Extract input placeholder attributes."""
    matches = REGEX_PATTERNS['placeholders'].findall(content)
    return set(matches)


def extract_attribute_strings(content: str) -> Set[str]:
    """Extract strings from common attributes (title, alt, aria-label)."""
    strings = set()
    strings.update(REGEX_PATTERNS['title'].findall(content))
    strings.update(REGEX_PATTERNS['alt'].findall(content))
    strings.update(REGEX_PATTERNS['aria_label'].findall(content))
    return strings


def extract_toast_alert_strings(content: str) -> Set[str]:
    """Extract toast and alert message strings."""
    strings = set()
    messages = REGEX_PATTERNS['message'].findall(content)
    titles = REGEX_PATTERNS['toast_title'].findall(content)
    texts = REGEX_PATTERNS['text'].findall(content)

    all_matches = messages + titles + texts
    filtered = [m for m in all_matches if any(
        keyword in m.lower() for keyword in VALIDATION_KEYWORDS
    )]
    strings.update(filtered)
    return strings


def extract_validation_strings(content: str) -> Set[str]:
    """Extract validation and error message strings."""
    pattern_str = '|'.join(VALIDATION_PATTERNS)
    pattern = re.compile(r'["\']([^"\']*(?:{})[^"\']*)["\']'.format(pattern_str), re.IGNORECASE)
    matches = pattern.findall(content)
    return set(matches)


def extract_string_literals(content: str) -> Set[str]:
    """Extract string literals that might be UI text."""
    matches = REGEX_PATTERNS['ui_literals'].findall(content)
    return set(matches)


def extract_from_file(filepath: Path, file_type: str) -> Dict[str, Set[str]]:
    """Extract all user-facing strings from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': {str(e)}}

    results = {}

    if file_type in ['jsx', 'tsx', 'vue', 'html']:
        results['jsx_content'] = extract_jsx_strings(content)
        results['buttons'] = extract_button_text(content)
        results['labels'] = extract_label_text(content)
        results['placeholders'] = extract_placeholders(content)
        results['attributes'] = extract_attribute_strings(content)
        results['toasts_alerts'] = extract_toast_alert_strings(content)

    if file_type in ['js', 'jsx', 'ts', 'tsx', 'vue']:
        results['validation'] = extract_validation_strings(content)
        results['ui_literals'] = extract_string_literals(content)

    return results


def scan_directory_incremental(
    source_dir: Path,
    file_types: List[str],
    exclude_dirs: List[str],
    cache_dir: str = None,
    force_rescan: bool = False,
    verbose: bool = False
) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
    """
    Scan directory with incremental cache support.

    Only processes files that have changed since last run.
    """
    cache_dir = cache_dir or CACHE_DIR
    cache = load_cache(cache_dir)

    all_strings = defaultdict(set)
    file_counts = defaultdict(int)

    # Collect all files
    all_files = []
    for file_type in file_types:
        pattern = f"**/*.{file_type}"
        for filepath in source_dir.rglob(pattern):
            if any(exclude_dir in filepath.parts for exclude_dir in exclude_dirs):
                continue
            all_files.append(filepath)

    if not all_files:
        return dict(all_strings), dict(file_counts)

    # Determine which files need processing
    files_to_process = []
    cached_files = 0

    if force_rescan:
        files_to_process = all_files
        print("[!] Forced full re-scan (cache ignored)")
    else:
        for filepath in all_files:
            file_str = str(filepath)
            current_hash = calculate_file_hash(filepath)

            if file_str in cache and cache[file_str].get('hash') == current_hash:
                # File hasn't changed, use cached results
                cached_data = cache[file_str].get('results', {})
                for category, strings in cached_data.items():
                    all_strings[category].update(set(strings))
                    file_counts[category] += len(strings)
                cached_files += 1
            else:
                # File has changed or is new
                files_to_process.append(filepath)

    total_files = len(all_files)
    new_files = len(files_to_process)

    print(f"[*] Cache Statistics:")
    print(f"  Total files: {total_files}")
    print(f"  Cached files: {cached_files} ({cached_files*100//total_files if total_files else 0}%)")
    print(f"  New/changed files: {new_files}")

    if cached_files > 0:
        print(f"[FAST] Using cached results for {cached_files} files")

    # Process only new/changed files
    if new_files > 0:
        print(f"[>] Processing {new_files} files...")

        for i, filepath in enumerate(files_to_process, 1):
            file_type = filepath.suffix.lstrip('.')

            if verbose:
                print(f"  [{i}/{new_files}] {filepath}")

            results = extract_from_file(filepath, file_type)

            if 'error' not in results:
                # Update cache with new results
                file_str = str(filepath)
                file_hash = calculate_file_hash(filepath)
                cache[file_str] = {
                    'hash': file_hash,
                    'timestamp': datetime.now().isoformat(),
                    'results': {k: list(v) for k, v in results.items()}
                }

                for category, strings in results.items():
                    all_strings[category].update(strings)
                    file_counts[category] += len(strings)

        # Save updated cache
        save_cache(cache, cache_dir)
        print(f"[OK] Cache updated")

    return dict(all_strings), dict(file_counts)


def output_text(strings: Dict[str, Set[str]], output_file: str):
    """Output results in text format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Extracted Strings for i18n (Incremental)\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n\n")

        for category, string_set in sorted(strings.items()):
            f.write(f"\n## {category.upper()} ({len(string_set)} strings)\n\n")
            for s in sorted(string_set):
                f.write(f"- {s}\n")


def output_json(strings: Dict[str, Set[str]], output_file: str):
    """Output results in JSON format."""
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'total_strings': sum(len(s) for s in strings.values()),
            'categories': len(strings)
        },
        'strings': {
            category: sorted(list(string_set))
            for category, string_set in sorted(strings.items())
        }
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def output_csv(strings: Dict[str, Set[str]], output_file: str):
    """Output results in CSV format."""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'String', 'Suggested Key'])

        for category, string_set in sorted(strings.items()):
            for s in sorted(string_set):
                key = s.lower().replace(' ', '_').replace('-', '_').strip()
                key = re.sub(r'[^a-z0-9_]', '', key)
                writer.writerow([category, s, key])


def main():
    parser = argparse.ArgumentParser(
        description='Incremental extraction of user-facing strings for i18n internationalization.'
    )
    parser.add_argument(
        'source_dir',
        type=str,
        help='Source directory to scan'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='extracted_strings.txt',
        help='Output file (default: extracted_strings.txt)'
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
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
        '--cache-dir',
        type=str,
        default=CACHE_DIR,
        help=f'Cache directory (default: {CACHE_DIR})'
    )
    parser.add_argument(
        '--force', '-F',
        action='store_true',
        help='Force full re-scan (ignore cache)'
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

    print(f"[FAST] Incremental String Extraction")
    print(f"Scanning {source_dir}...")
    print(f"File types: {', '.join(file_types)}")
    print(f"Excluding: {', '.join(exclude_dirs)}")
    print(f"Cache dir: {args.cache_dir}")
    print()

    import time
    start_time = time.time()

    strings, file_counts = scan_directory_incremental(
        source_dir,
        file_types,
        exclude_dirs,
        args.cache_dir,
        args.force,
        args.verbose
    )

    elapsed = time.time() - start_time

    # Print summary
    total_strings = sum(len(s) for s in strings.values())
    print(f"\n[OK] Extraction Complete (in {elapsed:.2f}s)")
    print(f"Total unique strings found: {total_strings}")
    print(f"Categories: {len(strings)}")
    print()

    for category, string_set in sorted(strings.items()):
        print(f"  {category}: {len(string_set)} strings")

    # Output results
    print(f"\nWriting output to: {args.output}")

    if args.format == 'text':
        output_text(strings, args.output)
    elif args.format == 'json':
        output_json(strings, args.output)
    elif args.format == 'csv':
        output_csv(strings, args.output)

    print(f"[OK] Done!")


if __name__ == '__main__':
    main()
