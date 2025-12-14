# jpprint

Side-by-side JSON comparison tool with color-coded diff indicators.

## Features

- **Side-by-side comparison** with intelligent line alignment
- **Color-coded diffs**: Red (deletions), Green (additions), Yellow (modifications)
- **Unicode box-drawing** with beautiful visual separators (│ and ◆)
- **Pure Python** - no external dependencies, stdlib only
- **Python 3.10+** with modern type hints

## Installation

```bash
pip install jpprint
```

## Quick Start

```python
from jpprint import jpprint

base = {"name": "Alice", "age": 30, "city": "NYC"}
updated = {"name": "Alice", "age": 31, "city": "Boston"}

jpprint(base, updated)
```

Output (with colors and Unicode box characters):
```
{                          │     {
    "age": 30,             ◆         "age": 31,
    "city": "NYC",         ◆         "city": "Boston",
    "name": "Alice"        │         "name": "Alice"
}                          │     }
```

## Usage

```python
from jpprint import jpprint

# Compare two JSON objects
left = {"a": "b", "c": "d"}
right = {"a": "b", "c": "changed"}
jpprint(left, right)

# Format single object
jpprint({"user": "alice", "role": "admin"})

# Return as list instead of printing
output = jpprint(left, right, retr=True)

# Show only differences
jpprint(left, right, diff_only=True)

# Disable colors for plain text
jpprint(left, right, use_colors=False)

# Use ASCII characters instead of Unicode
jpprint(left, right, use_box_chars=False)

# Disable intelligent alignment
jpprint(left, right, align_lines=False)
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `align_lines` | bool | `True` | Intelligently align matching lines using difflib |
| `diff_ind` | str | `<>` | Indicator for different lines (ignored if `use_box_chars=True`) |
| `diff_only` | bool | `False` | Show only lines that differ |
| `indent` | int | `4` | JSON indentation spaces |
| `max_width` | int | `None` | Truncate lines to max width |
| `retr` | bool | `False` | Return output instead of printing |
| `separator` | str | `\|` | Column separator for equal lines (ignored if `use_box_chars=True`) |
| `show_ln` | bool | `False` | Display line numbers |
| `use_box_chars` | bool | `True` | Use Unicode box-drawing characters (│, ◆) |
| `use_colors` | bool | `True` | Enable/disable color output |

## Advanced Examples

### Comparing API Responses

```python
import requests
from jpprint import jpprint

v1 = requests.get("https://api.example.com/v1/user/123").json()
v2 = requests.get("https://api.example.com/v2/user/123").json()

jpprint(v1, v2)
```

### Nested JSON Structures

```python
config_old = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"enabled": True}
}

config_new = {
    "database": {"host": "db.example.com", "port": 5432},
    "cache": {"enabled": True, "ttl": 3600}
}

jpprint(config_old, config_new)
```

### Datetime and UUID Support

```python
from datetime import datetime
import uuid

data = {
    "user": "alice",
    "id": uuid.uuid4(),
    "created_at": datetime(2024, 1, 1, 12, 0, 0)
}

jpprint(data)
# Automatically converts datetime to ISO format and UUID to string
```

## How It Works

jpprint uses Python's `difflib.SequenceMatcher` to intelligently align matching lines side-by-side, making it easy to spot additions, deletions, and modifications in JSON data. Color coding and Unicode box characters provide clear visual indicators of changes.

## Development

### Setup

```bash
git clone https://github.com/voidnologo/jpprint.git
cd jpprint
pip install -e ".[dev]"
```

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Code Quality

```bash
ruff format .  # Format code
ruff check .   # Check linting
isort .        # Sort imports
```

## Requirements

- Python 3.10 or higher
- No external runtime dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
