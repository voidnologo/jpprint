import unittest

from jpprint import jpprint


class AlignmentTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
