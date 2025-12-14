#!/usr/bin/env python
"""
Example demonstrating box-drawing characters in jpprint.

Shows the difference between standard ASCII separators and Unicode box-drawing characters.
Uses │ (vertical line) for equal lines and ◆ (diamond) for differing lines.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jpprint import jpprint

base = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York',
    'role': 'developer',
}

updated = {
    'name': 'Alice',
    'age': 31,
    'city': 'Boston',
    'role': 'senior developer',
}

print('=' * 80)
print('Standard Mode (default)')
print('=' * 80)
jpprint(base, updated, use_colors=False)

print('\n' + '=' * 80)
print('Box-Drawing Mode (use_box_chars=True)')
print('=' * 80)
jpprint(base, updated, use_colors=False, use_box_chars=True)

print('\n' + '=' * 80)
print('Box-Drawing + Colors (recommended)')
print('=' * 80)
jpprint(base, updated, use_box_chars=True)

print('\n' + '=' * 80)
print('Complex Example: API Response Comparison')
print('=' * 80)

v1_response = {
    'status': 'success',
    'data': {
        'user_id': 12345,
        'username': 'alice_dev',
        'email': 'alice@oldcompany.com',
        'premium': False,
    },
    'version': '1.0',
}

v2_response = {
    'status': 'success',
    'data': {
        'user_id': 12345,
        'username': 'alice_dev',
        'email': 'alice@newcompany.com',
        'premium': True,
        'tier': 'gold',
    },
    'version': '2.0',
}

jpprint(v1_response, v2_response, use_box_chars=True)
