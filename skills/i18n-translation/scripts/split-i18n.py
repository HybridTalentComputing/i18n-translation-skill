#!/usr/bin/env python3
"""
Split large i18n JSON files into smaller, feature-based files.

Usage:
    python split-i18n.py <source_file> <output_dir> [--by-feature] [--by-prefix]

Example:
    python split-i18n.py locales/en/common.json locales/en/ --by-prefix
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict


def load_json(file_path: str) -> Dict:
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, file_path: str) -> None:
    """Save JSON file with proper formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def split_by_prefix(data: Dict, prefix: str) -> Dict:
    """Extract keys that start with given prefix."""
    result = {}
    prefix_len = len(prefix)

    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[prefix_len:]  # Remove prefix
            result[new_key] = value

    return result


def split_by_feature(data: Dict, features: list) -> Dict[str, Dict]:
    """Split data by feature prefixes."""
    result = {}
    remaining = {}

    for feature in features:
        feature_data = split_by_prefix(data, f"{feature}.")
        if feature_data:
            result[feature] = feature_data

    # Add remaining keys without prefix
    for key, value in data.items():
        if not any(key.startswith(f"{f}.") for f in features):
            remaining[key] = value

    if remaining:
        result['common'] = remaining

    return result


def analyze_keys(data: Dict) -> Dict[str, int]:
    """Analyze key prefixes to suggest features."""
    prefixes = defaultdict(int)

    for key in data.keys():
        if '.' in key:
            prefix = key.split('.')[0]
            prefixes[prefix] += 1

    return dict(prefixes)


def main():
    if len(sys.argv) < 3:
        print("Usage: python split-i18n.py <source_file> <output_dir> [--by-feature] [--by-prefix]")
        print("\nExample:")
        print("  python split-i18n.py locales/en/common.json locales/en/ --by-prefix")
        sys.exit(1)

    source_file = sys.argv[1]
    output_dir = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else '--by-prefix'

    # Load source file
    print(f"Loading {source_file}...")
    data = load_json(source_file)
    total_keys = len(data)
    print(f"Total keys: {total_keys}")

    # Analyze keys
    print("\nAnalyzing key prefixes...")
    prefixes = analyze_keys(data)
    print("Key distribution by prefix:")
    for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True):
        print(f"  {prefix}: {count} keys")

    # Determine split strategy
    if mode == '--by-prefix' and prefixes:
        # Split by detected prefixes
        features = list(prefixes.keys())
        print(f"\nSplitting into {len(features)} feature files...")

        split_data = split_by_feature(data, features)

        for feature, feature_data in split_data.items():
            output_file = os.path.join(output_dir, f"{feature}.json")
            save_json(feature_data, output_file)
            print(f"  ✓ Created {feature}.json ({len(feature_data)} keys)")

    else:
        print("\nNo automatic split performed. Manual splitting required.")
        print("\nSuggested features based on key prefixes:")
        for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True):
            if count >= 10:  # Only show features with 10+ keys
                print(f"  - {prefix}.json ({count} keys)")

    print(f"\nTotal: {total_keys} keys processed")


if __name__ == '__main__':
    main()
