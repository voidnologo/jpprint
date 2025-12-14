import datetime
import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

from jpprint import jpprint, max_len


class BasicTests(unittest.TestCase):
    def test_prints_two_columns(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_prints_shows_differences(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    <>        "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_dictionaries(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_json(self):
        a = json.dumps({'a': 'b'})
        b = json.dumps({'a': 'b'})
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_json_and_dictionary(self):
        a = json.dumps({'a': 'b'})
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_byte_encoded_json_and_string_json(self):
        a = b'{"a": "b"}'
        b = '{"a": "b"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_accepts_only_one_argument(self):
        a = b'{"a": "b"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a)
        expected = '{\n'
        expected += '    "a": "b"\n'
        expected += '}\n'
        self.assertEqual(expected, out.getvalue())

    def test_expands_based_on_longest_file_length(self):
        a = {'a': 'b'}
        b = {'a': 'b', 'c': 'd'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, use_colors=False, use_box_chars=False, align_lines=False)
        expected = '{               |     {            \n'
        expected += '    "a": "b"    <>        "a": "b",\n'
        expected += '}               <>        "c": "d" \n'
        expected += '                <>    }            \n'
        self.assertEqual(expected, out.getvalue())

    def test_max_length_calculates_longest_line(self):
        a = json.dumps({'a': 'b', 'c': 'def', 'longest!': 'this is the longest!'}, indent=4, sort_keys=True)
        self.assertEqual(max_len(a), 38)

    def test_accepts_datetime_objects(self):
        a = {'datetime': datetime.datetime(2017, 12, 31)}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a)
        expected = '{\n'
        expected += '    "datetime": "2017-12-31T00:00:00"\n'
        expected += '}\n'
        self.assertEqual(expected, out.getvalue())


if __name__ == '__main__':
    unittest.main()
