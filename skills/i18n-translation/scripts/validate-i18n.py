#!/usr/bin/env python3
"""
Validate i18n translation files for completeness and consistency.

Usage:
    python validate-i18n.py <source_language> <target_languages>

Example:
    python validate-i18n.py en zh-Hans es
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple


def load_json_files(base_dir: str, lang: str) -> Dict[str, Dict]:
    """Load all JSON files for a language."""
    lang_dir = os.path.join(base_dir, lang)
    files = {}

    if not os.path.exists(lang_dir):
        return files

    for file_path in Path(lang_dir).glob('*.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            files[file_path.stem] = json.load(f)

    return files


def compare_keys(source: Dict, target: Dict, path: str = '') -> Tuple[List[str], List[str]]:
    """Compare keys between source and target."""
    missing = []
    extra = []

    for key in source.keys():
        current_path = f"{path}.{key}" if path else key

        if key not in target:
            missing.append(current_path)
        elif isinstance(source[key], dict) and isinstance(target[key], dict):
            sub_missing, sub_extra = compare_keys(source[key], target[key], current_path)
            missing.extend(sub_missing)
            extra.extend(sub_extra)

    for key in target.keys():
        current_path = f"{path}.{key}" if path else key
        if key not in source and not isinstance(target[key], dict):
            extra.append(current_path)

    return missing, extra


def validate_file(source_file: str, target_file: str, source_name: str, target_name: str) -> bool:
    """Validate a single translation file."""
    print(f"\nValidating {source_name} -> {target_name}...")

    with open(source_file, 'r', encoding='utf-8') as f:
        source = json.load(f)

    with open(target_file, 'r', encoding='utf-8') as f:
        target = json.load(f)

    missing, extra = compare_keys(source, target)

    if missing:
        print(f"  ✗ Missing {len(missing)} keys in {target_name}:")
        for key in missing[:10]:  # Show first 10
            print(f"    - {key}")
        if len(missing) > 10:
            print(f"    ... and {len(missing) - 10} more")

    if extra:
        print(f"  ⚠ Extra {len(extra)} keys in {target_name}:")
        for key in extra[:10]:
            print(f"    + {key}")
        if len(extra) > 10:
            print(f"    ... and {len(extra) - 10} more")

    if not missing and not extra:
        source_count = count_keys(source)
        target_count = count_keys(target)
        print(f"  ✓ Perfect match ({source_count} keys)")
        return True

    return False


def count_keys(data: Dict) -> int:
    """Recursively count all keys in a nested structure."""
    count = 0
    for value in data.values():
        count += 1
        if isinstance(value, dict):
            count += count_keys(value) - 1
    return count


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate-i18n.py <locales_dir> <source_lang> <target_lang1> [target_lang2 ...]")
        print("\nExample:")
        print("  python validate-i18n.py locales en zh-Hans es")
        sys.exit(1)

    base_dir = sys.argv[1]
    source_lang = sys.argv[2]
    target_langs = sys.argv[3:]

    print(f"Loading {source_lang} files...")
    source_files = load_json_files(base_dir, source_lang)

    if not source_files:
        print(f"No files found for {source_lang} in {base_dir}/{source_lang}/")
        sys.exit(1)

    print(f"Found {len(source_files)} files: {', '.join(source_files.keys())}")

    all_valid = True

    for target_lang in target_langs:
        print(f"\n{'='*60}")
        print(f"Language: {target_lang}")
        print('='*60)

        target_files = load_json_files(base_dir, target_lang)

        if not target_files:
            print(f"✗ No files found for {target_lang}")
            all_valid = False
            continue

        # Validate each file
        for filename in source_files.keys():
            if filename not in target_files:
                print(f"\n✗ Missing file: {filename}.json")
                all_valid = False
                continue

            source_path = os.path.join(base_dir, source_lang, f"{filename}.json")
            target_path = os.path.join(base_dir, target_lang, f"{filename}.json")

            if not validate_file(source_path, target_path, source_lang, target_lang):
                all_valid = False

    print(f"\n{'='*60}")
    if all_valid:
        print("✓ All validations passed!")
    else:
        print("✗ Some validations failed. Please review the output above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
