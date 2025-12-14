from jpprint import jpprint

from . import BaseTestCase


class AlignmentTests(BaseTestCase):
    def test_alignment_matches_common_lines(self):
        # Lines that exist in both should align
        a = {'a': 'b', 'x': 'delete_me', 'z': 'end'}
        b = {'a': 'b', 'z': 'end'}
        output = jpprint(a, b, retr=True, use_colors=False, align_lines=True)

        # Should have diff indicator for deleted line
        has_diff = any('◆' in line or '<>' in line for line in output)
        self.assertTrue(has_diff)

        # Common lines should align (a and z should be side by side)
        output_str = '\n'.join(output)
        self.assertIn('"a": "b"', output_str)
        self.assertIn('"z": "end"', output_str)

    def test_alignment_shows_additions_correctly(self):
        # Lines only in right should show empty left
        a = {'a': 'b'}
        b = {'a': 'b', 'new': 'field'}
        output = jpprint(a, b, retr=True, use_colors=False, align_lines=True)

        # Should have a line with empty left side and content on right
        has_empty_left = any('◆' in line or '<>' in line for line in output)
        self.assertTrue(has_empty_left)

    def test_alignment_shows_deletions_correctly(self):
        # Lines only in left should show empty right
        a = {'a': 'b', 'old': 'field'}
        b = {'a': 'b'}
        output = jpprint(a, b, retr=True, use_colors=False, align_lines=True)

        # Should have deleted content
        output_str = '\n'.join(output)
        self.assertIn('"old": "field"', output_str)

    def test_alignment_with_colors_added_lines(self):
        # Empty left, content right - should show colored diff
        a = {}
        b = {'new': 'field'}
        output = jpprint(a, b, retr=True, align_lines=True)

        # Should have colored diff output (yellow for modifications)
        has_color = any('\033[9' in line for line in output)
        self.assertTrue(has_color)

        # Should show the new field
        output_str = '\n'.join(output)
        self.assertIn('"new": "field"', output_str)

    def test_alignment_with_colors_deleted_lines(self):
        # Content left, empty right - should show colored diff
        a = {'old': 'field'}
        b = {}
        output = jpprint(a, b, retr=True, align_lines=True)

        # Should have colored diff output (yellow for modifications)
        has_color = any('\033[9' in line for line in output)
        self.assertTrue(has_color)

        # Should show the old field
        output_str = '\n'.join(output)
        self.assertIn('"old": "field"', output_str)

    def test_alignment_default_enabled(self):
        # Alignment should be enabled by default
        a = {'a': 'b', 'x': 'y', 'z': 'end'}
        b = {'a': 'b', 'z': 'end'}

        aligned = jpprint(a, b, retr=True, use_colors=False)
        unaligned = jpprint(a, b, retr=True, use_colors=False, align_lines=False)

        # They should be different (aligned is better)
        self.assertNotEqual(aligned, unaligned)

    def test_alignment_complex_case(self):
        # More complex alignment scenario
        a = {'status': 'ok', 'removed': 'field', 'user': 'alice', 'value': 1}
        b = {'added': 'field', 'status': 'ok', 'user': 'alice', 'value': 1}
        output = jpprint(a, b, retr=True, use_colors=False, align_lines=True)

        # status, user, and value should align
        # removed should show on left only (red)
        # added should show on right only (green)
        output_str = '\n'.join(output)

        self.assertIn('"status": "ok"', output_str)
        self.assertIn('"user": "alice"', output_str)
        self.assertIn('"value": 1', output_str)

    def test_complex_alignment_with_key_matching(self):
        # Comprehensive test: matches, modifications, deletes, and adds
        first = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'f': 5, 'g': 6}
        second = {'a': 1, 'b': 3, 'd': 4, 'e': 5, 'g': 6}

        output = jpprint(first, second, retr=True, use_colors=False, use_box_chars=False)
        output_str = '\n'.join(output)

        # Check that equal keys are aligned with |
        self.assertIn('"a": 1,    |         "a": 1,', output_str)
        self.assertIn('"d": 4,    |         "d": 4,', output_str)
        self.assertIn('"g": 6     |         "g": 6', output_str)

        # Check that modified key 'b' shows on both sides (same key, different value)
        lines = output_str.split('\n')
        b_lines = [line for line in lines if '"b"' in line]
        self.assertEqual(len(b_lines), 1)  # Should be one line with both sides
        self.assertIn('"b": 2,', b_lines[0])
        self.assertIn('"b": 3,', b_lines[0])
        self.assertIn('<>', b_lines[0])

        # Check that deleted keys show on left only
        c_lines = [line for line in lines if '"c": 3' in line]
        self.assertEqual(len(c_lines), 1)
        self.assertIn('"c": 3,    <>   ', c_lines[0])  # Left side only

        f_lines = [line for line in lines if '"f": 5' in line]
        self.assertEqual(len(f_lines), 1)
        self.assertIn('"f": 5,    <>   ', f_lines[0])  # Left side only

        # Check that added key shows on right only
        e_lines = [line for line in lines if '"e": 5' in line]
        self.assertEqual(len(e_lines), 1)
        self.assertIn('    <>        "e": 5,', e_lines[0])  # Right side only
