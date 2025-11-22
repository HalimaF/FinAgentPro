# Contributing to FinAgent Pro

Thank you for your interest in contributing to FinAgent Pro! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/finagent-pro.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit: `git commit -m "Add: description of your changes"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-demo.txt
pip install -r requirements-huggingface.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Maximum line length: 100 characters

### TypeScript/React
- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Use Material-UI components

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Guidelines

1. **Title**: Use clear, descriptive titles
   - `Add: New feature description`
   - `Fix: Bug description`
   - `Update: Component/feature description`

2. **Description**: Include:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Screenshots (if UI changes)

3. **Code Quality**:
   - All tests pass
   - No lint errors
   - Code is well-documented
   - No breaking changes (or clearly documented)

## Reporting Issues

When reporting bugs, please include:
- Operating system and version
- Python/Node version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Screenshots (if applicable)

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the problem it solves
- Provide use cases
- Suggest implementation approach (optional)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

For questions about contributing, open an issue with the `question` label or contact the maintainers.

## License

By contributing to FinAgent Pro, you agree that your contributions will be licensed under the MIT License.
