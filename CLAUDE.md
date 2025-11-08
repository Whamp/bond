<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal **Python 3.12** project using modern Python packaging standards (`pyproject.toml`). The project is in its initial state with zero dependencies and a single entry point.

## Project Structure

```
/home/will/projects/bond/
├── main.py           # Main entry point (prints "Hello from bond!")
├── pyproject.toml    # Python project configuration
├── README.md         # Project documentation (currently empty)
├── .gitignore        # Git ignore rules for Python
└── .python-version   # Python 3.12 requirement
```

## Architecture

- **Single-module application**: All logic resides in `main.py:1-6`
- **Zero dependencies**: Completely standalone Python script
- **Modern Python packaging**: Uses `pyproject.toml` (PEP 518/621)
- **Package manager**: Uses `uv` for environment management
- **Virtual environment**: Located at `.venv/`

## Development Commands

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the application
python main.py
# or
python -m main

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Lint code
ruff check .

# Format code
ruff format .
black .
isort .
```

## Dependencies

- **Runtime dependencies**: None (empty `dependencies = []` in `pyproject.toml:7`)
- **Development dependencies**: pytest, pytest-cov, ruff, black, isort
- **Python version**: Requires Python 3.12+ (see `pyproject.toml:6` and `.python-version`)

## Entry Points

- **main.py:1-6**: Contains `main()` function that prints "Hello from bond!"
- **Execution**: `python main.py` or `python -m main`

## Configuration Files

- **pyproject.toml:1-8**: Project metadata, Python version requirement, and dependency specification
- **.gitignore:1-11**: Excludes Python build artifacts, `__pycache__/`, `.venv`, etc.
- **README.md**: Currently empty, needs documentation

## Project Status

This is a **starter template** with minimal configuration. Development tools are now installed (pytest, ruff, black, isort). To make it production-ready:
- Add a proper description in `pyproject.toml:4`
- Populate `README.md` with project documentation
- Add dependencies as needed
- Write tests for the application
- Add development scripts to `pyproject.toml`
