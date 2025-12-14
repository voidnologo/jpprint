from .formatter import formatter, max_len, truncate
from .output import create_output


def set_options(options: dict) -> tuple:
    align_lines = options.get('align_lines', True)
    diff_ind = options.get('diff_ind', '<>')
    diff_only = options.get('diff_only', False)
    indent = options.get('indent', 4)
    max_width = options.get('max_width')
    retr = options.get('retr', False)
    separator = options.get('separator', '|')
    show_ln = options.get('show_ln', False)
    use_box_chars = options.get('use_box_chars', True)
    use_colors = options.get('use_colors', True)
    return (
        align_lines,
        diff_ind,
        diff_only,
        indent,
        max_width,
        retr,
        separator,
        show_ln,
        use_box_chars,
        use_colors,
    )


def jpprint(f1, f2=None, **options):
    (
        align_lines,
        diff_ind,
        diff_only,
        indent,
        max_width,
        retr,
        separator,
        show_ln,
        use_box_chars,
        use_colors,
    ) = set_options(options)
    f1 = formatter(f1, indent)
    if f2 is None:
        print(f1)
        return
    f2 = formatter(f2, indent)
    if max_width:
        f1 = truncate(f1, max_width)
        f2 = truncate(f2, max_width)
    l1width = max_len(f1)
    l2width = max_len(f2)
    output = list(
        create_output(
            f1,
            f2,
            diff_ind,
            separator,
            diff_only,
            show_ln,
            l1width,
            l2width,
            use_colors,
            use_box_chars,
            align_lines,
        )
    )
    if retr:
        return output
    print('\n'.join(output))
