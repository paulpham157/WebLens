"""
Configuration file for pytest
"""
import pytest
import asyncio
import os


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (may take several seconds)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Skip slow tests by default unless explicitly requested
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run slow tests"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory for testing"""
    config_dir = tmp_path / "weblens_test_config"
    config_dir.mkdir()
    
    # Create subdirectories
    (config_dir / "logs").mkdir()
    (config_dir / "screenshots").mkdir()
    (config_dir / "videos").mkdir()
    (config_dir / "reports").mkdir()
    (config_dir / "browser_profiles").mkdir()
    
    return config_dir


@pytest.fixture
def mock_browser():
    """Create a mock browser for testing using natural language approach"""
    from unittest.mock import AsyncMock
    
    browser = AsyncMock()
    browser.run = AsyncMock(return_value="Mock result")
    browser.execute_natural_language = AsyncMock(return_value="Mock natural language result")
    browser.take_screenshot = AsyncMock(return_value="/path/to/screenshot.png")
    
    return browser
