import datetime
from contextlib import redirect_stdout  # NOTE: redirect_stdout requires python3.4+
from io import StringIO
import json
import unittest
import uuid

from jpprint import jpprint, max_len


class JPPrintTests(unittest.TestCase):

    def test_prints_two_columns(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_show_line_numbers(self):
        a = {'a': 'b'}
        b = {'b': 'c', 'd': 'e'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, show_ln=True)
        expected = '1{               |     {            \n'
        expected += '2    "a": "b"    <>        "b": "c",\n'
        expected += '3}               <>        "d": "e" \n'
        expected += '4                <>    }            \n'
        self.assertEqual(expected, out.getvalue())

    def test_prints_shows_differences(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    <>        "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_separator(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, separator='.')
        expected = '{               .     {           \n'
        expected += '    "a": "b"    .         "a": "b"\n'
        expected += '}               .     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_can_change_diff_indicator(self):
        a = {'a': 'b'}
        b = {'b': 'a'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, diff_ind='?')
        expected = '{               |     {           \n'
        expected += '    "a": "b"    ?         "b": "a"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_dictionaries(self):
        a = {'a': 'b'}
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_two_json(self):
        a = json.dumps({'a': 'b'})
        b = json.dumps({'a': 'b'})
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_json_and_dictionary(self):
        a = json.dumps({'a': 'b'})
        b = {'a': 'b'}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
        expected = '{               |     {           \n'
        expected += '    "a": "b"    |         "a": "b"\n'
        expected += '}               |     }           \n'
        self.assertEqual(expected, out.getvalue())

    def test_compare_byte_encoded_json_and_string_json(self):
        a = b'{"a": "b"}'
        b = '{"a": "b"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b)
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
            jpprint(a, b)
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

    def test_accepts_date_objects(self):
        a = {'date': datetime.date(2017, 12, 31)}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a)
        expected = '{\n'
        expected += '    "date": "2017-12-31"\n'
        expected += '}\n'
        self.assertEqual(expected, out.getvalue())

    def test_accepts_uuid_objects(self):
        uid = uuid.uuid4()
        a = {'uid': uid}
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a)
        expected = '{\n'
        expected += f'    "uid": "{uid}"\n'
        expected += '}\n'
        self.assertEqual(expected, out.getvalue())

    def test_diff_only_only_outputs_lines_that_are_different(self):
        a = '{"a": "b", "c": "d"}'
        b = '{"a": "b", "c": "not the same"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, diff_only=True)
        expected = '    "c": "d"     <>        "c": "not the same"\n'
        self.assertEqual(expected, out.getvalue())

    def test_truncates_line_to_max_width_if_line_is_longer_than_max(self):
        a = '{"a": "1234567890", "b": "b"}'
        b = '{"a": "0987654321", "b": "b"}'
        out = StringIO()
        with redirect_stdout(out):
            jpprint(a, b, max_width=15)
        expected = '{                  |     {              \n'
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
        output = jpprint(a, b, retr=True)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
