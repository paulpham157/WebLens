"""
Unit tests for WebLens core functionality
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path

from weblens.core.browser_manager import BrowserManager
from weblens.core.test_runner import TestRunner, TestCase, TestResult
from weblens.profiles.profile_manager import ProfileManager, ProfileSettings
from weblens.config import Config


class TestBrowserManager:
    """Test cases for BrowserManager"""
    
    @pytest.mark.asyncio
    async def test_browser_manager_initialization(self):
        """Test browser manager initialization"""
        manager = BrowserManager()
        assert manager.agents == {}
        assert manager.is_started == False
    
    @pytest.mark.asyncio
    async def test_browser_manager_start_stop(self):
        """Test browser manager start and stop"""
        manager = BrowserManager()
        
        # Test start
        await manager.start()
        assert manager.is_started == True
        
        # Test stop
        await manager.stop()
        assert manager.is_started == False


class TestTestRunner:
    """Test cases for TestRunner"""
    
    def test_test_runner_initialization(self):
        """Test test runner initialization"""
        runner = TestRunner()
        assert isinstance(runner.browser_manager, BrowserManager)
        assert runner.test_cases == []
        assert runner.results == []
    
    def test_register_test(self):
        """Test test registration"""
        runner = TestRunner()
        
        async def dummy_test(browser):
            pass
        
        runner.register_test(
            name="test1",
            description="Test description",
            test_function=dummy_test,
            tags=["smoke"]
        )
        
        assert len(runner.test_cases) == 1
        test_case = runner.test_cases[0]
        assert test_case.name == "test1"
        assert test_case.description == "Test description"
        assert test_case.tags == ["smoke"]
    
    def test_filter_tests(self):
        """Test test filtering"""
        runner = TestRunner()
        
        async def test1(browser):
            pass
        
        async def test2(browser):
            pass
        
        # Register tests
        runner.register_test(
            name="test1", 
            description="Description 1", 
            test_function=test1,
            tags=["smoke"]
        )
        runner.register_test(
            name="test2", 
            description="Description 2", 
            test_function=test2,
            tags=["regression"]
        )
        
        # Test filtering by tags
        filtered = runner._filter_tests(tags=["smoke"])
        assert len(filtered) == 1
        assert filtered[0].name == "test1"


class TestProfileManager:
    """Test cases for ProfileManager"""
    
    def test_profile_manager_initialization(self):
        """Test profile manager initialization"""
        manager = ProfileManager()
        assert isinstance(manager.profiles, dict)
        assert len(manager.profiles) > 0  # Should have default profiles
    
    def test_create_profile(self):
        """Test profile creation"""
        manager = ProfileManager()
        
        profile = manager.create_profile(
            name="test_profile",
            browser="chrome",
            user_agent="Test User Agent",
            viewport={"width": 1280, "height": 720}
        )
        
        assert profile.name == "test_profile"
        assert profile.browser == "chrome"
        assert profile.user_agent == "Test User Agent"
        assert profile.viewport == {"width": 1280, "height": 720}
        assert "test_profile" in manager.profiles
    
    def test_get_profile(self):
        """Test profile retrieval"""
        manager = ProfileManager()
        
        # Create a test profile
        manager.create_profile("test_get", "chrome")
        
        # Get existing profile
        profile = manager.get_profile("test_get")
        assert profile is not None
        assert profile.name == "test_get"
        
        # Get non-existing profile
        profile = manager.get_profile("non_existing")
        assert profile is None
    
    def test_list_profiles(self):
        """Test profile listing"""
        manager = ProfileManager()
        
        # List all profiles
        all_profiles = manager.list_profiles()
        assert len(all_profiles) > 0
        
        # List chrome profiles only
        chrome_profiles = manager.list_profiles("chrome")
        assert all(p.browser == "chrome" for p in chrome_profiles)
    
    def test_clone_profile(self):
        """Test profile cloning"""
        manager = ProfileManager()
        
        # Create original profile
        original = manager.create_profile(
            "original",
            "chrome",
            user_agent="Original UA",
            viewport={"width": 1920, "height": 1080}
        )
        
        # Clone profile with overrides
        cloned = manager.clone_profile(
            "original",
            "cloned",
            user_agent="Cloned UA"
        )
        
        assert cloned is not None
        assert cloned.name == "cloned"
        assert cloned.browser == "chrome"  # Inherited
        assert cloned.user_agent == "Cloned UA"  # Overridden
        assert cloned.viewport == {"width": 1920, "height": 1080}  # Inherited


class TestConfig:
    """Test cases for Config"""
    
    def test_config_initialization(self):
        """Test config initialization"""
        config = Config()
        assert config.project_root.exists()
        assert config.logs_dir.exists()
        assert config.screenshots_dir.exists()
        assert config.videos_dir.exists()
        assert config.reports_dir.exists()
    
    def test_config_values(self):
        """Test config values"""
        config = Config()
        
        # Basic properties should be present
        assert hasattr(config, "api_key")
        assert hasattr(config, "base_url")
        assert hasattr(config, "timeout")
        assert hasattr(config, "screenshot_on_failure")
        assert hasattr(config, "parallel_workers")


class TestProfileSettings:
    """Test cases for ProfileSettings"""
    
    def test_profile_settings_creation(self):
        """Test profile settings creation"""
        settings = ProfileSettings(
            name="test",
            browser="chrome",
            user_agent="Test UA",
            viewport={"width": 1024, "height": 768}
        )
        
        assert settings.name == "test"
        assert settings.browser == "chrome"
        assert settings.user_agent == "Test UA"
        assert settings.viewport == {"width": 1024, "height": 768}
        assert settings.locale == "en-US"  # Default value
        assert settings.permissions == []  # Default value
    
    def test_profile_settings_defaults(self):
        """Test profile settings default values"""
        settings = ProfileSettings(name="test", browser="chrome")
        
        assert settings.viewport == {"width": 1920, "height": 1080}
        assert settings.permissions == []
        assert settings.cookies == []
        assert settings.local_storage == {}
        assert settings.session_storage == {}
        assert settings.extensions == []


class TestTestResult:
    """Test cases for TestResult"""
    
    def test_test_result_creation(self):
        """Test test result creation"""
        result = TestResult(
            name="test_example",
            status="passed",
            duration=1.5
        )
        
        assert result.name == "test_example"
        assert result.status == "passed"
        assert result.duration == 1.5
        assert result.error_message is None
        assert result.screenshot_path is None


class TestTestCase:
    """Test cases for TestCase"""
    
    def test_test_case_creation(self):
        """Test test case creation"""
        async def dummy_test(browser):
            pass
        
        test_case = TestCase(
            name="test_example",
            description="Example test",
            test_function=dummy_test,
            tags=["smoke", "regression"]
        )
        
        assert test_case.name == "test_example"
        assert test_case.description == "Example test"
        assert test_case.test_function == dummy_test
        assert test_case.tags == ["smoke", "regression"]


# Fixtures for testing
@pytest.fixture
def sample_profile_manager():
    """Create a sample profile manager for testing"""
    manager = ProfileManager()
    manager.profiles.clear()  # Clear default profiles for clean testing
    return manager


@pytest.fixture
def sample_test_runner():
    """Create a sample test runner for testing"""
    return TestRunner()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
