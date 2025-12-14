import difflib

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from .colors import DiffType, apply_line_color, classify_diff_type

BOX_SEPARATOR = '│'
BOX_DIFF_INDICATOR = '◆'


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
    line_no = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Lines match - show side by side
            for l_line, r_line in zip(left_lines[i1:i2], right_lines[j1:j2]):
                line_no += 1
                if diff_only:
                    continue

                diff_type = DiffType.EQUAL
                delim = BOX_SEPARATOR if use_box_chars else separator

                l1_padded = '{:{width}}'.format(l_line, width=l1width)
                l2_padded = '{:{width}}'.format(r_line, width=l2width)

                l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
                l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

                yield '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)

        elif tag == 'delete':
            # Lines only in left (deleted)
            for l_line in left_lines[i1:i2]:
                line_no += 1
                diff_type = DiffType.DELETED
                delim = BOX_DIFF_INDICATOR if use_box_chars else diff_ind

                l1_padded = '{:{width}}'.format(l_line, width=l1width)
                l2_padded = '{:{width}}'.format('', width=l2width)

                l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
                l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

                yield '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)

        elif tag == 'insert':
            # Lines only in right (added)
            for r_line in right_lines[j1:j2]:
                line_no += 1
                diff_type = DiffType.ADDED
                delim = BOX_DIFF_INDICATOR if use_box_chars else diff_ind

                l1_padded = '{:{width}}'.format('', width=l1width)
                l2_padded = '{:{width}}'.format(r_line, width=l2width)

                l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
                l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

                yield '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)

        elif tag == 'replace':
            # Lines differ - show both sides
            left_block = left_lines[i1:i2]
            right_block = right_lines[j1:j2]
            max_lines = max(len(left_block), len(right_block))

            for idx in range(max_lines):
                line_no += 1
                l_line = left_block[idx] if idx < len(left_block) else ''
                r_line = right_block[idx] if idx < len(right_block) else ''

                diff_type = DiffType.MODIFIED
                delim = BOX_DIFF_INDICATOR if use_box_chars else diff_ind

                l1_padded = '{:{width}}'.format(l_line, width=l1width)
                l2_padded = '{:{width}}'.format(r_line, width=l2width)

                l1_colored = apply_line_color(l1_padded, diff_type, is_left=True, use_colors=use_colors)
                l2_colored = apply_line_color(l2_padded, diff_type, is_left=False, use_colors=use_colors)

                yield '{}{}{:^10}{}'.format(line_no if show_ln else '', l1_colored, delim, l2_colored)


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
