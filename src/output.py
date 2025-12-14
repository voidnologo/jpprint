try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from .colors import apply_line_color, classify_diff_type


def create_output(
    f1: str,
    f2: str,
    diff_ind: str,
    separator: str,
    diff_only: bool,
    show_ln: bool,
    l1width: int,
    l2width: int,
    use_colors: bool,
):
    for line_no, (l1, l2) in enumerate(
        zip_longest(f1.splitlines(), f2.splitlines(), fillvalue=' '), 1
    ):
        diff_type = classify_diff_type(l1, l2, fillvalue=' ')
        delim = diff_ind if l1 != l2 else separator

        if diff_only and l1 == l2:
            continue

        # Apply colors to each column independently
        l1_colored = apply_line_color(l1, diff_type, is_left=True, use_colors=use_colors)
        l2_colored = apply_line_color(l2, diff_type, is_left=False, use_colors=use_colors)

        yield '{}{:{l1width}}{:^10}{:{l2width}}'.format(
            line_no if show_ln else '', l1_colored, delim, l2_colored, l1width=l1width, l2width=l2width
        )
