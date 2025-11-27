# Code Quality & Linting Guide

This project uses multiple tools to ensure high code quality standards:

## Tools Used

### 1. **Ruff** - Fast Python Linter & Formatter
- **Purpose**: Primary linter and formatter (replaces flake8, isort, pyupgrade, and more)
- **Configuration**: `pyproject.toml` under `[tool.ruff]`
- **Enabled Rules**:
  - `E/F` - Pyflakes and PyCodeStyle errors
  - `W` - PyCodeStyle warnings
  - `UP` - PyUpgrade (automatic Python syntax upgrades)
  - `I` - Import sorting
  - `B` - Bugbear (common bugs and design problems)
  - `C4` - Comprehensions
  - `C90` - McCabe complexity (max: 10)
  - `DJ` - Django-specific checks
  - `N` - PEP8 naming conventions
  - `PLE/PLW` - Pylint errors and warnings
  - `S` - Security (Bandit)
  - `SIM` - Code simplification
  - `T10/T20` - Debugger and print statements
  - `RUF` - Ruff-specific rules
  - And more...

### 2. **Black** - Code Formatter
- **Purpose**: Opinionated code formatter for consistent style
- **Line Length**: 88 characters
- **Configuration**: `pyproject.toml` under `[tool.black]`

### 3. **mypy** - Static Type Checker
- **Purpose**: Optional static type checking
- **Configuration**: `pyproject.toml` under `[tool.mypy]`
- **Django Plugin**: Enabled via `django-stubs`

### 4. **Pre-commit** - Git Hook Manager
- **Purpose**: Automatically run checks before each commit
- **Configuration**: `.pre-commit-config.yaml`
- **Hooks Include**: Ruff, Black, mypy, Django-upgrade, Bandit, and more

## Quick Commands

### Using Make (Recommended)

```bash
# Auto-format code
make format

# Run linter with auto-fix
make lint

# Check linting (no auto-fix)
make check-lint

# Run type checking
make check-types

# Run all checks
make check-all

# Install pre-commit hooks
make pre-commit-install

# Run pre-commit on all files
make pre-commit-run

# Update pre-commit hooks
make pre-commit-update

# CI-style checks (no auto-fix)
make ci-lint
```

### Using Commands Directly

```bash
# Ruff
ruff check .                  # Check for issues
ruff check --fix .            # Check and auto-fix
ruff format .                 # Format code

# Black
black .                       # Format code
black --check .               # Check formatting (CI mode)

# mypy
mypy .                        # Type check

# Pre-commit
pre-commit run --all-files    # Run all hooks
pre-commit run ruff          # Run specific hook
```

## Pre-commit Setup

1. **Install pre-commit hooks** (one-time setup):
   ```bash
   make pre-commit-install
   # or
   pre-commit install
   ```

2. **Pre-commit will now run automatically** on `git commit`

3. **To skip pre-commit** (not recommended):
   ```bash
   git commit --no-verify
   ```

## Configuration Files

- `pyproject.toml` - Main configuration for Ruff, Black, mypy, pytest, coverage
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `Makefile` - Convenient command shortcuts

## IDE Integration

### VS Code
Install these extensions:
- `charliermarsh.ruff` - Ruff linter and formatter
- `ms-python.mypy-type-checker` - mypy integration
- `ms-python.black-formatter` - Black formatter

Add to `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "ruff.lint.run": "onSave"
}
```

### PyCharm
1. Enable Ruff: Settings → Tools → Ruff
2. Enable Black: Settings → Tools → Black
3. Enable mypy: Settings → Tools → External Tools

## CI/CD Integration

Add to your CI pipeline (GitHub Actions, GitLab CI, etc.):

```yaml
# Example GitHub Actions
- name: Lint with Ruff
  run: make ci-lint

# Or individually
- name: Check formatting
  run: black --check .

- name: Lint
  run: ruff check .

- name: Type check
  run: mypy .
```

## Ignoring Rules

### File-level ignores
```python
# ruff: noqa  # Ignore entire file

import os  # noqa: F401  # Ignore specific rule on this line
```

### Configuration-based ignores
Add to `pyproject.toml`:
```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
```

## Gradually Increasing Strictness

The current configuration is balanced for productivity. To increase strictness:

1. **Enable more Ruff rules** in `pyproject.toml`:
   - Uncomment rules like `ANN` (annotations), `D` (docstrings), etc.

2. **Increase mypy strictness**:
   ```toml
   [tool.mypy]
   strict = true
   disallow_untyped_calls = true
   disallow_untyped_defs = true
   ```

3. **Decrease complexity limit**:
   ```toml
   [tool.ruff.lint.mccabe]
   max-complexity = 8  # Lower is stricter
   ```

## Troubleshooting

### "Command not found: ruff/black/mypy"
Install dependencies:
```bash
pip install -e .
# or
pip install ruff black mypy django-stubs
```

### Pre-commit hooks not running
```bash
pre-commit install
```

### Too many linting errors
Start with auto-fix:
```bash
make format  # Auto-format first
make lint    # Then auto-fix linting issues
```

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)
