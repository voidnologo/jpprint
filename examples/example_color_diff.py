#!/usr/bin/env python
"""
Example demonstrating the color diff functionality in jpprint.

This script shows different diff scenarios:
- MODIFIED lines (yellow): Lines that exist in both but differ
- ADDED lines (green): Lines only in the right column
- DELETED lines (red): Lines only in the left column
- EQUAL lines (no color): Lines that are identical
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jpprint import jpprint

print('=' * 80)
print('Example 1: Modified lines (yellow)')
print('=' * 80)
base = {'name': 'Alice', 'age': 30, 'city': 'New York'}
modified = {'name': 'Alice', 'age': 31, 'city': 'Boston'}
jpprint(base, modified)

print('\n' + '=' * 80)
print('Example 2: Added lines (green on right)')
print('=' * 80)
base = {'name': 'Alice', 'age': 30}
with_additions = {'name': 'Alice', 'age': 30, 'city': 'New York', 'country': 'USA'}
jpprint(base, with_additions)

print('\n' + '=' * 80)
print('Example 3: Deleted lines (red on left)')
print('=' * 80)
full = {'name': 'Alice', 'age': 30, 'city': 'New York', 'country': 'USA'}
partial = {'name': 'Alice', 'age': 30}
jpprint(full, partial)

print('\n' + '=' * 80)
print('Example 4: Mixed changes')
print('=' * 80)
original = {'user': 'alice', 'email': 'alice@old.com', 'role': 'user', 'active': True}
updated = {'user': 'alice', 'email': 'alice@new.com', 'role': 'admin', 'status': 'active'}
jpprint(original, updated)

print('\n' + '=' * 80)
print('Example 5: Same output with colors disabled')
print('=' * 80)
jpprint(original, updated, use_colors=False)
