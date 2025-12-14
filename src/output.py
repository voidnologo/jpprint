import difflib
from itertools import zip_longest

from .colors import DiffType, apply_line_color, classify_diff_type

BOX_SEPARATOR = '│'
BOX_DIFF_INDICATOR = '◆'


def format_diff_line(
    left_text: str,
    right_text: str,
    diff_type: DiffType,
    diff_ind: str,
    l1width: int,
    l2width: int,
    line_no: int,
    separator: str,
    show_ln: bool,
    use_box_chars: bool,
    use_colors: bool,
) -> str:
    delim = (
        (BOX_SEPARATOR if diff_type == DiffType.EQUAL else BOX_DIFF_INDICATOR)
        if use_box_chars
        else (separator if diff_type == DiffType.EQUAL else diff_ind)
    )

    l1_padded = '{:{width}}'.format(left_text, width=l1width)
    l2_padded = '{:{width}}'.format(right_text, width=l2width)

    l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
    l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

    return '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)


def process_equal_lines(left_lines, right_lines, i1, i2, j1, j2, params, diff_only):
    for l_line, r_line in zip(left_lines[i1:i2], right_lines[j1:j2], strict=False):
        params['line_no'] += 1
        if diff_only:
            continue
        yield format_diff_line(l_line, r_line, DiffType.EQUAL, **params)


def process_delete_lines(left_lines, i1, i2, params):
    for l_line in left_lines[i1:i2]:
        params['line_no'] += 1
        yield format_diff_line(l_line, '', DiffType.DELETED, **params)


def process_insert_lines(right_lines, j1, j2, params):
    for r_line in right_lines[j1:j2]:
        params['line_no'] += 1
        yield format_diff_line('', r_line, DiffType.ADDED, **params)


def process_replace_lines(left_lines, right_lines, i1, i2, j1, j2, params):
    left_block = left_lines[i1:i2]
    right_block = right_lines[j1:j2]
    max_lines = max(len(left_block), len(right_block))

    for idx in range(max_lines):
        params['line_no'] += 1
        l_line = left_block[idx] if idx < len(left_block) else ''
        r_line = right_block[idx] if idx < len(right_block) else ''
        yield format_diff_line(l_line, r_line, DiffType.MODIFIED, **params)


def create_output_aligned(
    f1: str,
    f2: str,
    diff_ind: str,
    separator: str,
    diff_only: bool,
    show_ln: bool,
    l1width: int,
    l2width: int,
    use_colors: bool,
    use_box_chars: bool,
):
    left_lines = f1.splitlines()
    right_lines = f2.splitlines()

    matcher = difflib.SequenceMatcher(None, left_lines, right_lines)
    params = {
        'diff_ind': diff_ind,
        'l1width': l1width,
        'l2width': l2width,
        'line_no': 0,
        'separator': separator,
        'show_ln': show_ln,
        'use_box_chars': use_box_chars,
        'use_colors': use_colors,
    }

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            yield from process_equal_lines(left_lines, right_lines, i1, i2, j1, j2, params, diff_only)
        elif tag == 'delete':
            yield from process_delete_lines(left_lines, i1, i2, params)
        elif tag == 'insert':
            yield from process_insert_lines(right_lines, j1, j2, params)
        elif tag == 'replace':
            yield from process_replace_lines(left_lines, right_lines, i1, i2, j1, j2, params)


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
    use_box_chars: bool = False,
    align_lines: bool = True,
):
    if align_lines:
        yield from create_output_aligned(
            f1, f2, diff_ind, separator, diff_only, show_ln, l1width, l2width, use_colors, use_box_chars
        )
    else:
        # Original zip_longest behavior for backward compatibility
        for line_no, (l1, l2) in enumerate(zip_longest(f1.splitlines(), f2.splitlines(), fillvalue=' '), 1):
            diff_type = classify_diff_type(l1, l2, fillvalue=' ')

            if use_box_chars:
                delim = BOX_DIFF_INDICATOR if l1 != l2 else BOX_SEPARATOR
            else:
                delim = diff_ind if l1 != l2 else separator

            if diff_only and l1 == l2:
                continue

            l1_padded = '{:{width}}'.format(l1, width=l1width)
            l2_padded = '{:{width}}'.format(l2, width=l2width)

            l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
            l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

            yield '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)
