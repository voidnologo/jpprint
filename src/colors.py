import re
from enum import Enum, auto


class ColorCode(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'


class DiffType(Enum):
    EQUAL = auto()
    ADDED = auto()
    DELETED = auto()
    MODIFIED = auto()


def colorize(text: str, color: ColorCode) -> str:
    return f'{color.value}{text}{ColorCode.RESET.value}'


def strip_color(text: str) -> str:
    ansi_escape = re.compile(r'\033\[[0-9;]+m')
    return ansi_escape.sub('', text)


def classify_diff_type(l1: str, l2: str, fillvalue: str = ' ') -> DiffType:
    if l1 == l2:
        return DiffType.EQUAL
    elif l1 == fillvalue:
        return DiffType.ADDED
    elif l2 == fillvalue:
        return DiffType.DELETED
    else:
        return DiffType.MODIFIED


def apply_line_color(text: str, diff_type: DiffType, is_left: bool, use_colors: bool) -> str:
    if not use_colors or diff_type == DiffType.EQUAL:
        return text

    if diff_type == DiffType.DELETED and is_left:
        return colorize(text, ColorCode.RED)
    elif diff_type == DiffType.ADDED and not is_left:
        return colorize(text, ColorCode.GREEN)
    elif diff_type == DiffType.MODIFIED:
        return colorize(text, ColorCode.YELLOW)

    return text
