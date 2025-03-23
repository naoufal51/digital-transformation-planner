# Contributing to Digital Transformation Planner

Thank you for considering contributing to the Digital Transformation Planner! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, browser, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- A clear, descriptive title
- Detailed explanation of the proposed feature
- Any relevant examples or mockups
- Explanation of why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes with clear, descriptive messages
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

Follow these steps to set up the project for development:

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install -r requirements-dev.txt` (if available)

## Coding Standards

- Follow PEP 8 style guidelines
- Write meaningful docstrings using Google or NumPy style
- Include type hints where appropriate
- Write unit tests for new functionality

## Testing

Run the test suite before submitting a PR:

```bash
pytest
```

## Documentation

- Update relevant documentation when changing code
- Document new features thoroughly
- Use clear, concise language

## Review Process

Pull requests will be reviewed by maintainers. You may be asked to make changes before your PR is accepted.

Thank you for contributing! 