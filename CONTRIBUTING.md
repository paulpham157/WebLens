# Contributing to WebLens

Thank you for your interest in contributing to WebLens! 🎉

## Development Setup

1. Fork repository
2. Clone your fork:
   ```bash
   git clone https://github.com/paulpham157/WebLens.git
   cd WebLens
   ```

3. Create conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate weblens
   ```

4. Setup development environment:
   ```bash
   ./setup.sh
   # or
   make setup
   ```

5. Run tests to ensure everything works:
   ```bash
   make test-unit
   ```

## Code Style

WebLens follows Python best practices:

- **Formatting**: Use `black` for code formatting
- **Linting**: Use `flake8` for linting
- **Type Hints**: Use type hints where possible
- **Docstrings**: Use Google-style docstrings

Run code quality checks:
```bash
make format  # Format code
make lint    # Check linting
```

## Testing

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests (requires browsers)
make test-integration

# Specific test file
pytest tests/unit/test_core.py -v
```

### Writing Tests

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **E2E tests**: Test complete user workflows

Example test:
```python
import pytest
from weblens import BrowserManager

class TestBrowserManager:
    def test_initialization(self):
        manager = BrowserManager()
        assert manager.browsers == {}
```

## Pull Request Process

1. **Create feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make changes**:
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**:
   ```bash
   make test
   make lint
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push and create PR**:
   ```bash
   git push origin feature/amazing-feature
   ```

## Commit Message Convention

Use conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
- `feat: add mobile profile support`
- `fix: resolve browser launch timeout issue`
- `docs: update README with new examples`

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Include examples in docstrings
- Update type hints

## Reporting Issues

When reporting bugs, please include:

1. **Environment details**:
   - OS and version
   - Python version
   - WebLens version
   - Browser versions

2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Log output** (if available)
5. **Screenshots** (if UI-related)

## Feature Requests

For new features:

1. **Check existing issues** first
2. **Describe the use case** clearly
3. **Provide examples** of how it would work
4. **Consider implementation** complexity

## Questions?

- 💬 Create a GitHub Discussion
- 🐛 Open an Issue for bugs
- 📧 Contact maintainers

Thank you for contributing! 🚀
