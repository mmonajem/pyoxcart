# Contributing to PyCCAPT

Thank you for your interest in contributing to PyCCAPT! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Types of Contributions](#types-of-contributions)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style Guidelines](#code-style-guidelines)
- [Documentation](#documentation)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please report unacceptable behavior to mehrpad.monajem@fau.de.

## Types of Contributions

### Reporting Bugs
- Before creating a bug report, please check the [existing issues](https://github.com/mmonajem/pyccapt/issues)
- Use the bug report template when creating a new issue
- Include as much relevant information as possible:
  - Operating system and version
  - Python version
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Screenshots or error messages
  - Relevant code snippets

### Suggesting Enhancements
- Use the feature request template
- Provide a clear use case and motivation
- Include examples of how the feature would work
- Consider potential impacts on existing functionality

### Pull Requests
- Fill out the pull request template
- Include tests for new features
- Update documentation as needed
- Follow the code style guidelines

## Getting Started

1. Fork the [PyCCAPT repository](https://github.com/mmonajem/pyccapt)
2. Clone your fork:
   ```bash
   git clone https://github.com/YourUsername/pyccapt.git
   cd pyccapt
   ```
3. Set up your development environment:
   ```bash
   # Create and activate conda environment
   conda env create -f environment.yml
   conda activate pyccapt

   # Install development dependencies
   pip install -e ".[dev]"
   ```

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- Conda (recommended)
- A code editor (VS Code, PyCharm, etc.)

### Environment Setup
1. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

2. Configure your editor:
   - Install Python extensions
   - Set up linting and formatting
   - Configure test runners

### Development Tools
- Black for code formatting
- Flake8 for linting
- MyPy for type checking
- Pytest for testing

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```

2. Make your changes following our [code style guidelines](#code-style-guidelines)

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names
- Add comments for complex logic

### Documentation Style
- Use clear and concise language
- Include code examples
- Update both docstrings and user documentation
- Follow Google style for docstrings

### Git Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 🚱 `:non-potable_water:` when plugging memory leaks
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - 💚 `:green_heart:` when fixing the CI build
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies

## Documentation

### Code Documentation
- Add docstrings to all public functions and classes
- Include type hints
- Provide examples in docstrings
- Keep documentation up to date

### User Documentation
- Update README.md when adding new features
- Add new documentation files in the `docs` directory
- Include screenshots and examples
- Keep the documentation organized and searchable

## Testing

### Writing Tests
- Write tests for new features
- Include both unit and integration tests
- Use pytest fixtures when appropriate
- Mock external dependencies

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific.py

# Run with coverage report
pytest --cov=pyccapt
```

## Submitting Changes

1. Push your changes to your fork
2. Create a Pull Request:
   - Use the PR template
   - Link related issues
   - Add a clear description
   - Include screenshots for UI changes

2. Ensure your PR:
   - Passes all tests
   - Follows code style guidelines
   - Includes updated documentation
   - Has no merge conflicts

## Review Process

1. All PRs require at least one review
2. Address review comments promptly
3. Keep the PR focused and manageable
4. Update the PR based on feedback
5. Request re-review when ready

## Getting Help

- Open an issue for questions
- Join our discussions
- Contact the maintainers at mehrpad.monajem@fau.de

Thank you for contributing to PyCCAPT!


