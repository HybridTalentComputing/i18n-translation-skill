#!/usr/bin/env python3
"""
String Extraction Script for i18n Internationalization

This script extracts user-facing strings from source code files to help
with creating i18n translation files.

Usage:
    python extract-strings.py <source_dir> [options]

Options:
    --output, -o     Output file for extracted strings (default: extracted_strings.txt)
    --format, -f     Output format: text, json, csv (default: text)
    --file-types     Comma-separated list of file extensions (default: js,jsx,ts,tsx,vue,html)
    --exclude        Comma-separated list of directories to exclude (default: node_modules,dist,build)
    --verbose, -v    Show detailed progress

Example:
    python extract-strings.py src --format json --output strings.json
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


def extract_jsx_strings(content: str) -> Set[str]:
    """Extract strings from JSX/Vue template content between tags."""
    # Match text between > and < (JSX/Vue templates)
    pattern = r'>([^<{]+)<'
    matches = re.findall(pattern, content)
    # Filter out whitespace-only strings
    strings = {m.strip() for m in matches if m.strip()}
    return strings


def extract_button_text(content: str) -> Set[str]:
    """Extract button text."""
    pattern = r'<button[^>]*>([^<]+)</button>'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return {m.strip() for m in matches if m.strip()}


def extract_label_text(content: str) -> Set[str]:
    """Extract label text."""
    pattern = r'<label[^>]*>([^<]+)</label>'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return {m.strip() for m in matches if m.strip()}


def extract_placeholders(content: str) -> Set[str]:
    """Extract input placeholder attributes."""
    pattern = r'placeholder=["\']([^"\']+)["\']'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return set(matches)


def extract_attribute_strings(content: str) -> Set[str]:
    """Extract strings from common attributes (title, alt, aria-label)."""
    patterns = [
        r'title=["\']([^"\']+)["\']',
        r'alt=["\']([^"\']+)["\']',
        r'aria-label=["\']([^"\']+)["\']',
    ]
    strings = set()
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        strings.update(matches)
    return strings


def extract_toast_alert_strings(content: str) -> Set[str]:
    """Extract toast and alert message strings."""
    patterns = [
        r'message\s*[:=]\s*["\']([^"\']+)["\']',
        r'title\s*[:=]\s*["\']([^"\']+)["\']',
        r'text\s*[:=]\s*["\']([^"\']+)["\']',
    ]
    strings = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        # Filter for common toast/alert keywords
        filtered = [m for m in matches if any(
            keyword in m.lower()
            for keyword in ['error', 'success', 'warning', 'info', 'confirm',
                          'saved', 'deleted', 'updated', 'login', 'logout']
        )]
        strings.update(filtered)
    return strings


def extract_validation_strings(content: str) -> Set[str]:
    """Extract validation and error message strings."""
    keywords = ['required', 'invalid', 'error', 'must', 'cannot', 'please']
    patterns = [
        r'["\']([^"\']*(?:{})[^"\']*)["\']'.format('|'.join(keywords)),
    ]
    strings = set()
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        strings.update(matches)
    return strings


def extract_string_literals(content: str) -> Set[str]:
    """Extract string literals that might be UI text."""
    # Single and double quoted strings
    pattern = r'["\']([A-Z][a-zA-Z\s]{2,})["\']'
    # Match strings starting with capital letter (likely UI text)
    matches = re.findall(pattern, content)
    return set(matches)


def extract_from_file(filepath: Path, file_type: str) -> Dict[str, Set[str]]:
    """Extract all user-facing strings from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return {}

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


def categorize_string(s: str) -> str:
    """Categorize a string into a logical group."""
    s_lower = s.lower()

    # Check for common patterns
    if any(word in s_lower for word in ['save', 'cancel', 'delete', 'edit', 'submit', 'close']):
        return 'actions'
    elif any(word in s_lower for word in ['login', 'signup', 'logout', 'password', 'email']):
        return 'auth'
    elif any(word in s_lower for word in ['dashboard', 'settings', 'profile']):
        return 'navigation'
    elif any(word in s_lower for word in ['loading', 'success', 'error', 'warning']):
        return 'status'
    elif any(word in s_lower for word in ['required', 'invalid', 'must']):
        return 'validation'
    elif any(word in s_lower for word in ['network', 'server', 'not found']):
        return 'errors'
    else:
        return 'common'


def scan_directory(
    source_dir: Path,
    file_types: List[str],
    exclude_dirs: List[str],
    verbose: bool = False
) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
    """
    Scan directory and extract all strings.

    Returns:
        Tuple of (categorized_strings, file_counts)
    """
    all_strings = defaultdict(set)
    file_counts = defaultdict(int)

    for file_type in file_types:
        pattern = f"**/*.{file_type}"
        for filepath in source_dir.rglob(pattern):
            # Skip excluded directories
            if any(exclude_dir in filepath.parts for exclude_dir in exclude_dirs):
                continue

            if verbose:
                print(f"Scanning: {filepath}")

            results = extract_from_file(filepath, file_type)

            for category, strings in results.items():
                all_strings[category].update(strings)
                file_counts[category] += len(strings)

    return dict(all_strings), dict(file_counts)


def output_text(strings: Dict[str, Set[str]], output_file: str):
    """Output results in text format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Extracted Strings for i18n\n")
        f.write("# Generated by extract-strings.py\n\n")

        for category, string_set in sorted(strings.items()):
            f.write(f"\n## {category.upper()} ({len(string_set)} strings)\n\n")
            for s in sorted(string_set):
                f.write(f"- {s}\n")


def output_json(strings: Dict[str, Set[str]], output_file: str):
    """Output results in JSON format."""
    # Convert sets to lists for JSON serialization
    output = {
        category: sorted(list(string_set))
        for category, string_set in sorted(strings.items())
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
                # Generate a suggested key
                key = s.lower().replace(' ', '_').replace('-', '_').strip()
                # Remove non-alphanumeric chars
                key = re.sub(r'[^a-z0-9_]', '', key)
                writer.writerow([category, s, key])


def main():
    parser = argparse.ArgumentParser(
        description='Extract user-facing strings from source code for i18n internationalization.'
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

    print(f"Scanning {source_dir}...")
    print(f"File types: {', '.join(file_types)}")
    print(f"Excluding: {', '.join(exclude_dirs)}")
    print()

    strings, file_counts = scan_directory(
        source_dir,
        file_types,
        exclude_dirs,
        args.verbose
    )

    # Print summary
    total_strings = sum(len(s) for s in strings.values())
    print(f"\n✓ Extraction Complete")
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

    print(f"✓ Done!")


if __name__ == '__main__':
    main()
