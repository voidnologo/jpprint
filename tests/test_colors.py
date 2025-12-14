import unittest
from contextlib import redirect_stdout
from io import StringIO

from jpprint import jpprint
from src.colors import ColorCode, DiffType, apply_line_color, classify_diff_type, strip_color


class ColorTests(unittest.TestCase):
    def test_colors_enabled_by_default(self):
        a = {'a': 'b'}
        b = {'c': 'd'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        # Should contain ANSI codes
        self.assertIn('\033[', out.getvalue())

    def test_colors_can_be_disabled(self):
        a = {'a': 'b'}
        b = {'c': 'd'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False)
        # Should not contain ANSI codes
        self.assertNotIn('\033[', out.getvalue())

    def test_modified_lines_are_yellow(self):
        a = {'a': 'b'}
        b = {'a': 'c'}
        output = jpprint(a, b, retr=True)
        # Both lines should contain yellow color code
        colored_line = output[1]
        self.assertIn(ColorCode.YELLOW.value, colored_line)

    def test_added_lines_are_green_on_right(self):
        # Right has more lines than left
        a = '{"a": "b"}'
        b = '{"a": "b",\n"c": "d"}'
        output = jpprint(a, b, retr=True, align_lines=False)
        # Last line should be fillvalue on left, content on right (green)
        last_line = output[-1]
        self.assertIn(ColorCode.GREEN.value, last_line)

    def test_deleted_lines_are_red_on_left(self):
        # Left has more lines than right
        a = '{"a": "b",\n"c": "d"}'
        b = '{"a": "b"}'
        output = jpprint(a, b, retr=True, align_lines=False)
        # Should have red on left for lines that only exist on left
        has_red = any(ColorCode.RED.value in line for line in output)
        self.assertTrue(has_red)

    def test_equal_lines_have_no_color(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        output = jpprint(a, b, retr=True)
        # Strip colors and compare - should be equal to non-colored version
        stripped = [strip_color(line) for line in output]
        expected = jpprint(a, b, retr=True, use_colors=False)
        self.assertEqual(stripped, expected)

    def test_diff_type_classification(self):
        self.assertEqual(classify_diff_type('a', 'a'), DiffType.EQUAL)
        self.assertEqual(classify_diff_type('a', 'b'), DiffType.MODIFIED)
        self.assertEqual(classify_diff_type(' ', 'b'), DiffType.ADDED)
        self.assertEqual(classify_diff_type('a', ' '), DiffType.DELETED)

    def test_apply_line_color_deleted_left(self):
        result = apply_line_color('test', DiffType.DELETED, is_left=True, use_colors=True)
        self.assertIn(ColorCode.RED.value, result)

    def test_apply_line_color_added_right(self):
        result = apply_line_color('test', DiffType.ADDED, is_left=False, use_colors=True)
        self.assertIn(ColorCode.GREEN.value, result)

    def test_apply_line_color_modified_both(self):
        left_result = apply_line_color('test', DiffType.MODIFIED, is_left=True, use_colors=True)
        right_result = apply_line_color('test', DiffType.MODIFIED, is_left=False, use_colors=True)
        self.assertIn(ColorCode.YELLOW.value, left_result)
        self.assertIn(ColorCode.YELLOW.value, right_result)

    def test_strip_color_removes_ansi_codes(self):
        colored = f'{ColorCode.RED.value}test{ColorCode.RESET.value}'
        stripped = strip_color(colored)
        self.assertEqual(stripped, 'test')
        self.assertNotIn('\033[', stripped)


if __name__ == '__main__':
    unittest.main()
