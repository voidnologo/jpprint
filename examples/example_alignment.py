#!/usr/bin/env python
"""
Example demonstrating intelligent line alignment in jpprint.

Shows how jpprint uses difflib.SequenceMatcher to align matching lines
for much clearer diffs, especially when data is added or removed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jpprint import jpprint

print('=' * 80)
print('Example 1: WITHOUT alignment (align_lines=False)')
print('=' * 80)
print("Notice how matching lines don't align - harder to read")
print()

left = {
    'age': 30,
    'city': 'New York',
    'country': 'USA',
    'name': 'Alice',
}

right = {
    'age': 30,
    'name': 'Alice',
}

jpprint(left, right, use_box_chars=True, align_lines=False)

print('\n' + '=' * 80)
print('Example 2: WITH intelligent alignment (align_lines=True, DEFAULT)')
print('=' * 80)
print('Matching lines align perfectly - much clearer!')
print()

jpprint(left, right, use_box_chars=True)

print('\n' + '=' * 80)
print('Example 3: Real-world API version comparison')
print('=' * 80)

v1_api = {
    'status': 'success',
    'data': {
        'user_id': 123,
        'username': 'alice',
        'email': 'alice@old.com',
        'role': 'user',
        'created': '2024-01-01',
    },
    'deprecated_field': 'will_be_removed',
    'version': '1.0',
}

v2_api = {
    'status': 'success',
    'data': {
        'user_id': 123,
        'username': 'alice',
        'email': 'alice@new.com',
        'premium_user': True,
        'created': '2024-01-01',
    },
    'version': '2.0',
    'new_feature': 'enabled',
}

jpprint(v1_api, v2_api, use_box_chars=True)

print('\n' + '=' * 80)
print('Example 4: Empty dict handling')
print('=' * 80)

print('Empty left, content right:')
jpprint({}, {'new_field': 'value'}, use_box_chars=True)

print('\nContent left, empty right:')
jpprint({'old_field': 'value'}, {}, use_box_chars=True)

print('\nBoth empty:')
jpprint({}, {}, use_box_chars=True)
