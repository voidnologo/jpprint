# jpprint

Side-by-side JSON comparison tool with color-coded diff indicators.

## Features

- **Side-by-side comparison**: View two JSON objects in parallel columns
- **Color-coded diffs**: Instantly identify changes with visual color indicators
  - 🔴 **Red**: Deletions (content only in left/base)
  - 🟢 **Green**: Additions (content only in right/comparison)
  - 🟡 **Yellow**: Modifications (different content in both)
- **Flexible formatting**: Configurable indent, separators, and display options
- **Pure Python**: No external dependencies, stdlib only
- **Python 3.10+**: Modern type hints and clean code

## Installation

```bash
pip install jpprint
```

## Quick Start

```python
from jpprint import jpprint

# Simple comparison
base = {"name": "Alice", "age": 30, "city": "NYC"}
updated = {"name": "Alice", "age": 31, "city": "Boston"}

jpprint(base, updated)
```

Output:
```
{                          |     {
    "age": 30,             <>        "age": 31,
    "city": "NYC",         <>        "city": "Boston",
    "name": "Alice"        |         "name": "Alice"
}                          |     }
```

## Usage Examples

### Basic Comparison

```python
from jpprint import jpprint

left = {"a": "b", "c": "d"}
right = {"a": "b", "c": "changed"}

jpprint(left, right)
# Shows side-by-side with yellow highlighting on modified lines
```

### Single Object Formatting

```python
data = {"user": "alice", "role": "admin"}
jpprint(data)
# Prints formatted JSON (no comparison)
```

### Disable Colors

```python
jpprint(left, right, use_colors=False)
# Plain text output without ANSI color codes
```

### Show Line Numbers

```python
jpprint(left, right, show_ln=True)
# Adds line numbers to output
```

### Show Only Differences

```python
jpprint(left, right, diff_only=True)
# Only display lines that differ
```

### Custom Separators

```python
jpprint(left, right, separator='│', diff_ind='║')
# Use custom characters for separators
```

### Return as List

```python
output = jpprint(left, right, retr=True)
# Returns list of strings instead of printing
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `use_colors` | bool | `True` | Enable/disable color output |
| `indent` | int | `4` | JSON indentation spaces |
| `separator` | str | `\|` | Column separator for equal lines |
| `diff_ind` | str | `<>` | Indicator for different lines |
| `diff_only` | bool | `False` | Show only lines that differ |
| `show_ln` | bool | `False` | Display line numbers |
| `max_width` | int | `None` | Truncate lines to max width |
| `retr` | bool | `False` | Return output instead of printing |

## Color Diff Logic

jpprint intelligently categorizes each line:

- **EQUAL**: Identical content in both → No color
- **MODIFIED**: Different content in both → Yellow on both sides
- **ADDED**: Content only on right → Green on right side
- **DELETED**: Content only on left → Red on left side

## Advanced Examples

### Comparing API Responses

```python
import requests
from jpprint import jpprint

v1_response = requests.get("https://api.example.com/v1/user/123").json()
v2_response = requests.get("https://api.example.com/v2/user/123").json()

jpprint(v1_response, v2_response)
```

### Nested JSON Structures

```python
config_old = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "cache": {"enabled": True}
}

config_new = {
    "database": {
        "host": "db.example.com",
        "port": 5432,
        "name": "mydb"
    },
    "cache": {"enabled": True, "ttl": 3600}
}

jpprint(config_old, config_new)
```

### With Datetime Objects

```python
from datetime import datetime

data = {
    "user": "alice",
    "created_at": datetime(2024, 1, 1, 12, 0, 0)
}

jpprint(data)
# Automatically converts datetime to ISO format
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/jpprint.git
cd jpprint

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python -m unittest tests.test_colors
```

### Code Quality

```bash
# Format code
ruff format .

# Check linting
ruff check .

# Sort imports
isort .
```

## Project Structure

```
jpprint/
├── src/
│   ├── __init__.py      # Public API exports
│   ├── colors.py        # Color codes and diff classification
│   ├── formatter.py     # JSON formatting utilities
│   ├── output.py        # Output generation
│   └── core.py          # Main jpprint function
├── tests/
│   ├── test_basic.py    # Core functionality tests
│   ├── test_options.py  # Configuration tests
│   └── test_colors.py   # Color diff tests
└── pyproject.toml       # Project configuration
```

## Requirements

- Python 3.10 or higher
- No external runtime dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
