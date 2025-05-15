import datetime
import json
import uuid


try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


def default_handler(*args):
    if isinstance(args[1], (datetime.datetime, datetime.date)):
        return args[1].isoformat()
    if isinstance(args[1], uuid.UUID):
        return str(args[1])
    return 'Unconvertable Type {} - {}'.format(type(args[1]), args[1])


json.JSONEncoder.default = default_handler


def formatter(data, indent):
    data = data.decode() if isinstance(data, bytes) else data
    try:
        return json.dumps(json.loads(data), indent=indent, sort_keys=True)
    except Exception:
        return json.dumps(data, indent=indent, sort_keys=True)


def max_len(data):
    return max(len(x) for x in data.split('\n'))


def truncate(data, width):
    ellipse = '...'
    return '\n'.join([x[: width - 3] + ellipse if len(x) > width else x for x in data.split('\n')])


def jpprint(f1, f2=None, **options):
    indent, separator, diff_ind, diff_only, max_width, show_ln, retr = set_options(options)
    f1 = formatter(f1, indent)
    if not f2:
        print(f1)
        return
    f2 = formatter(f2, indent)
    if max_width:
        f1 = truncate(f1, max_width)
        f2 = truncate(f2, max_width)
    l1width = max_len(f1)
    l2width = max_len(f2)
    output = list(create_output(f1, f2, diff_ind, separator, diff_only, show_ln, l1width, l2width))
    if retr:
        return output
    print('\n'.join(output))


def set_options(options):
    indent = options.get('indent', 4)
    separator = options.get('separator', '|')
    def_ind = options.get('diff_ind', '<>')
    diff_only = options.get('diff_only', False)
    max_width = options.get('max_width', None)
    show_ln = options.get('show_ln', False)
    retr = options.get('retr', False)
    return indent, separator, def_ind, diff_only, max_width, show_ln, retr


def create_output(f1, f2, diff_ind, separator, diff_only, show_ln, l1width, l2width):
    for line_no, (l1, l2) in enumerate(zip_longest(f1.splitlines(), f2.splitlines(), fillvalue=' '), 1):
        delim = diff_ind if l1 != l2 else separator
        if diff_only and l1 == l2:
            continue
        yield '{}{:{l1width}}{:^10}{:{l2width}}'.format(
            line_no if show_ln else '', l1, delim, l2, l1width=l1width, l2width=l2width
        )
