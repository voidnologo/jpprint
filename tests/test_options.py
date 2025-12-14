import unittest
from contextlib import redirect_stdout
from io import StringIO

from jpprint import jpprint


class OptionsTests(unittest.TestCase):

    def test_show_line_numbers(self):
        a = {'a': 'b'}
        b = {'b': 'c', 'd': 'e'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, show_ln=True, use_colors=False)
        expected  = '1{               |     {            \n'
        expected += '2    "a": "b"    <>        "b": "c",\n'
        expected += '3}               <>        "d": "e" \n'
        expected += '4                <>    }            \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_separator(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, separator='.', use_colors=False)
        expected  = '{               .     {           \n'
        expected += '    "a": "b"    .         "a": "b"\n'
        expected += '}               .     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_diff_indicator(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, diff_ind='?', use_colors=False)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    ?         "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_diff_only_only_outputs_lines_that_are_different(self):
        a = '{"a": "b", "c": "d"}'
        b = '{"a": "b", "c": "not the same"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, diff_only=True, use_colors=False)
        expected = '    "c": "d"     <>        "c": "not the same"\n'
        self.assertEqual(expected, out.getvalue())

    def test_truncates_line_to_max_width_if_line_is_longer_than_max(self):
        a = '{"a": "1234567890", "b": "b"}'
        b = '{"a": "0987654321", "b": "b"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, max_width=15, use_colors=False)
        expected  = '{                  |     {              \n'
        expected += '    "a": "12...    <>        "a": "09...\n'
        expected += '    "b": "b"       |         "b": "b"   \n'
        expected += '}                  |     }              \n'
        self.assertEqual(expected, out.getvalue())

    def test_retr_option_returns_strings_instead_of_printing(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        expected = [
            '{               |     {           ',
            '    "a": "b"    |         "a": "b"',
            '}               |     }           ',
        ]
        output = jpprint(a, b, retr=True, use_colors=False)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
