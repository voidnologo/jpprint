# NOTE: redirect_stdout requires python3.4+
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from jpprint import jpprint, max_len


class JPPrintTests(unittest.TestCase):

    def test_prints_two_columns(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_prints_shows_differences(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    <>        "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_separator(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, separator='.')
        expected  = '{               .     {           \n'
        expected += '    "a": "b"    .         "a": "b"\n'
        expected += '}               .     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_diff_indicator(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, diff_ind='?')
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    ?         "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_dictionaries(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_json(self):
        a = json.dumps({'a': 'b'})
        b = json.dumps({'a': 'b'})
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_json_and_dictionary(self):
        a = json.dumps({'a': 'b'})
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_expands_based_on_longest_file_length(self):
        a = {'a': 'b'}
        b = {'a': 'b', 'c': 'd'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected  = '{               |     {            \n'
        expected += '    "a": "b"    <>        "a": "b",\n'
        expected += '}               <>        "c": "d" \n'
        expected += '                <>    }            \n'
        self.assertEqual(expected, out.getvalue())

    def test_max_length_calculates_longest_line(self):
        a = json.dumps({'a': 'b', 'c': 'def', 'longest!': 'this is the longest!'}, indent=4, sort_keys=True)
        self.assertEqual(max_len(a), 38)

if __name__ == '__main__':
    unittest.main()
