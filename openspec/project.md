# Project Context

## Purpose
A minimal Python 3.12 starter template with modern packaging standards. Currently contains a simple "Hello from bond!" application and serves as a foundation for Python projects with zero runtime dependencies.

## Tech Stack
- **Runtime**: Python 3.12+
- **Packaging**: pyproject.toml (PEP 518/621)
- **Package Manager**: uv
- **Testing**: pytest, pytest-cov
- **Code Quality**: ruff, black, isort

## Project Conventions

### Code Style
- **Formatter**: black (line length 88)
- **Import Sorter**: isort
- **Linter**: ruff with default settings
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Line Length**: 88 characters (black default)
- **Docstrings**: Follow PEP 257

### Architecture Patterns
- **Single-module application**: Main logic in `main.py`
- **Modular design**: Can be expanded into package structure
- **Zero dependencies**: Keep runtime dependencies minimal
- **Entry point**: `main()` function in `main.py`

### Testing Strategy
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Test files**: `tests/` directory (to be created)
- **Test naming**: `test_*.py` pattern
- **Coverage target**: Aim for >80% coverage

### Git Workflow
- **Main branch**: master
- **Branching**: Feature branches (feature/feature-name)
- **Commits**: Conventional commits (feat, fix, docs, etc.)
- **Hooks**: Pre-commit hooks recommended (ruff, black, pytest)

## Domain Context
This is a starter template project. The actual application logic will be developed based on requirements. AI assistants should suggest modern Python best practices and keep the project structure minimal unless additional complexity is needed.

## Important Constraints
- **Python Version**: Requires Python 3.12 or higher
- **Dependencies**: Zero runtime dependencies (keep it that way unless absolutely necessary)
- **Licensing**: None specified
- **Python Standards**: Follow PEP 8, PEP 257, PEP 621

## External Dependencies
- **Package Manager**: uv (for development environment)
- **Virtual Environment**: .venv/ (excluded from git)
- **CI/CD**: None configured yet
- **Build System**: Built-in (no setuptools/pybuild needed for single module)
