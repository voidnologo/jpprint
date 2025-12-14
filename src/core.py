from .formatter import formatter, max_len, truncate
from .output import create_output


def set_options(options: dict) -> tuple:
    indent = options.get('indent', 4)
    separator = options.get('separator', '|')
    def_ind = options.get('diff_ind', '<>')
    diff_only = options.get('diff_only', False)
    max_width = options.get('max_width', None)
    show_ln = options.get('show_ln', False)
    retr = options.get('retr', False)
    use_colors = options.get('use_colors', True)
    use_box_chars = options.get('use_box_chars', False)
    return indent, separator, def_ind, diff_only, max_width, show_ln, retr, use_colors, use_box_chars


def jpprint(f1, f2=None, **options):
    indent, separator, diff_ind, diff_only, max_width, show_ln, retr, use_colors, use_box_chars = set_options(
        options
    )
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
    output = list(
        create_output(f1, f2, diff_ind, separator, diff_only, show_ln, l1width, l2width, use_colors, use_box_chars)
    )
    if retr:
        return output
    print('\n'.join(output))
