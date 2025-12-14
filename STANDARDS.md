# Development Standards

This document outlines the coding standards and practices for the jpprint project.

## Python Version Support

- **Minimum**: Python 3.10
- **Tested versions**: 3.10, 3.11, 3.12, 3.13
- No Python 2 compatibility code or legacy workarounds

## Code Style

### Type Hints

- Use modern type hints for all functions and methods
- Required for all function parameters and return types
- Example:
  ```python
  def format_diff_line(left_text: str, right_text: str) -> str:
      ...
  ```

### Documentation

- **No Google-style docstrings** - rely on clear function names and type annotations
- Use comments only to explain **why**, not **how**
- Code should be self-documenting through clear naming

### Code Quality Tools

All code must pass these checks:

```bash
ruff format .      # Code formatting (single quotes, consistent indentation)
ruff check .       # Linting (see pyproject.toml for rules)
isort .            # Import sorting
```

### Linting Rules

- **Maximum complexity**: 6 (McCabe)
- **Line length**: 110 characters
- **Quote style**: Single quotes
- **Import style**: Alphabetically sorted, grouped by stdlib/local
- See `pyproject.toml` for complete ruff configuration

### Code Organization

- **Extract helper functions** when complexity exceeds limits
- **Alphabetize parameters** in function definitions (since we use keyword arguments)
- **Alphabetize dictionary keys** where order doesn't matter semantically
- **Keep functions focused** - each function should do one thing well

## Project Structure

```
jpprint/
├── src/              # Source code
│   ├── __init__.py   # Public API exports
│   ├── colors.py     # Color codes and diff classification
│   ├── formatter.py  # JSON formatting utilities
│   ├── output.py     # Output generation
│   └── core.py       # Main jpprint function
├── tests/            # Unit tests
├── examples/         # Example scripts
├── .github/          # GitHub Actions workflows
└── pyproject.toml    # Project configuration
```

## Dependencies

- **Runtime**: None - stdlib only
- **Development**: ruff, isort (specified in pyproject.toml)
- **No external runtime dependencies** - keep the library lightweight

## Testing

### Test Framework

- Use `unittest` (stdlib) - no pytest
- Test files: `tests/test_*.py`
- Run tests: `python -m unittest discover -s tests -p "test_*.py" -v`

### Test Coverage

- All new features must include tests
- Test both happy path and edge cases
- Maintain 100% of current test pass rate

### Test Organization

- `test_basic.py` - Core functionality
- `test_options.py` - Configuration options
- `test_colors.py` - Color diff features
- `test_alignment.py` - Line alignment features

## Git Workflow

### Branch Protection

- Main branch requires:
  - All status checks passing (lint + tests on all Python versions)
  - 1 approval before merge
  - Squash merge preferred
  - Admins can bypass rules

### GitHub Actions

- **Separate workflows** for linting and testing
- `lint.yml` - Runs ruff format, ruff check, isort on Python 3.12
- `test.yml` - Runs tests on Python 3.10, 3.11, 3.12, 3.13

## Design Principles

### SOLID Principles

- **Single Responsibility**: Each module/function has one clear purpose
- **Open/Closed**: Extend behavior through configuration, not modification
- **Dependency Inversion**: Depend on abstractions (type hints), not concrete implementations

### DRY (Don't Repeat Yourself)

- Extract common patterns into helper functions
- Use configuration over duplication
- Maintain single source of truth

### Simplicity

- Avoid over-engineering
- No premature optimization
- No unnecessary abstractions
- Make the simple case simple

## API Design

### Configuration

- Use keyword arguments for all options
- Provide sensible defaults
- Document all options in README table (alphabetically)
- Keep backward compatibility where possible

### Function Signatures

- Alphabetize parameters for easy scanning
- Use clear, descriptive parameter names
- Type hint all parameters and return values
- Example:
  ```python
  def jpprint(
      f1,
      f2=None,
      align_lines: bool = True,
      diff_ind: str = '<>',
      diff_only: bool = False,
      ...
  ):
  ```

## Documentation

### README

- Keep succinct and scannable
- Show Unicode box characters in examples (default behavior)
- Configuration table should be alphabetically ordered
- Minimize redundant explanations - rely on clear examples and table

### Code Comments

- Explain **why** decisions were made
- Don't explain **what** the code does (use clear names instead)
- Keep comments up-to-date with code changes

## Error Handling

- Validate at system boundaries (user input, external APIs)
- Trust internal code and framework guarantees
- Provide clear, actionable error messages
- Don't add error handling for impossible scenarios

## Performance

- Don't optimize prematurely
- Focus on algorithmic efficiency (e.g., difflib for alignment)
- Keep memory usage reasonable for typical use cases
- Simple code is often fast enough

## Backwards Compatibility

- Maintain compatibility when possible
- Use deprecation warnings before removal
- Document breaking changes clearly
- Version bumps follow semantic versioning
