"""
Integration tests for WebLens
"""
import pytest
import asyncio
import tempfile
from pathlib import Path

from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.core.test_runner import weblens_test
from weblens.config import config


class TestIntegration:
    """Integration tests for WebLens components"""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_browser_launch_and_navigation(self):
        """Test actual browser launch and navigation"""
        manager = BrowserManager()
        
        try:
            await manager.start()
            
            # Create agent with natural language task
            agent = await manager.create_agent("Navigate to example.com and check the page title", "test_agent")
            assert agent is not None
            
            # Run natural language task
            result = await agent.run()
            assert result
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_profile_based_testing(self):
        """Test browser launch with different profiles"""
        manager = BrowserManager()
        
        try:
            await manager.start()
            
            # Create agent with task
            agent = await manager.create_agent("Access https://httpbin.org/user-agent and check the user-agent information", "test_profile_agent")
            assert agent is not None
            
            # Run task
            result = await agent.run()
            assert result
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_test_execution(self):
        """Test full test execution pipeline"""
        runner = TestRunner()
        
        # Define a simple test with natural language instructions
        @weblens_test(
            name="simple_integration_test",
            description="Navigate to example.com and verify the title contains 'Example'"
        )
        async def simple_test(browser):
            result = await browser.run()
            assert result
        
        # Register the test
        info = simple_test._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=simple_test
        )
        
        # Run tests
        results = await runner.run_tests(parallel=False)
        
        # Verify results
        assert len(results) == 1
        assert results[0].status == "passed"
        assert results[0].name == "simple_integration_test"
    
    @pytest.mark.asyncio
    async def test_profile_creation_and_usage(self):
        """Test creating and using custom profiles"""
        profile_manager = ProfileManager()
        
        # Create custom profile
        custom_profile = profile_manager.create_profile(
            name="test_integration_profile",
            browser="chrome",
            user_agent="WebLens Integration Test Agent",
            viewport={"width": 800, "height": 600}
        )
        
        assert custom_profile.name == "test_integration_profile"
        assert custom_profile.browser == "chrome"
        assert custom_profile.user_agent == "WebLens Integration Test Agent"
        assert custom_profile.viewport == {"width": 800, "height": 600}
        
        # Verify profile is saved
        retrieved_profile = profile_manager.get_profile("test_integration_profile")
        assert retrieved_profile is not None
        assert retrieved_profile.name == custom_profile.name
        
        # Clean up
        profile_manager.delete_profile("test_integration_profile")
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_error_handling_and_screenshots(self):
        """Test error handling and screenshot capture"""
        runner = TestRunner()
        
        # Define a test that will fail
        @weblens_test(
            name="failing_integration_test",
            description="Click on a non-existent element on example.com"
        )
        async def failing_test(browser):
            # Natural language instruction likely to fail
            await browser.execute_natural_language("Click on the non-existent-button that doesn't exist on example.com")
            # This should fail
        
        # Register test
        info = failing_test._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=failing_test
        )
        
        # Run tests
        results = await runner.run_tests(parallel=False)
        
        # Verify results
        assert len(results) == 1
        assert results[0].status == "failed"
        assert results[0].error_message is not None
        
        # Check if screenshot was taken
        if results[0].screenshot_path:
            screenshot_path = Path(results[0].screenshot_path)
            assert screenshot_path.exists()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_multiple_browser_sessions(self):
        """Test managing multiple browser sessions"""
        manager = BrowserManager()
        
        try:
            await manager.start()
            
            # Create multiple agents with different tasks
            agent1 = await manager.create_agent("Navigate to example.com and check the title", "agent1")
            agent2 = await manager.create_agent("Go to httpbin.org and check the title", "agent2")
            
            # Run tasks
            result1 = await agent1.run()
            result2 = await agent2.run()
            
            # Verify results
            assert result1
            assert result2
            
        finally:
            await manager.stop()


class TestE2EScenarios:
    """End-to-end testing scenarios"""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    @pytest.mark.e2e
    async def test_complete_user_journey(self):
        """Test a complete user journey"""
        runner = TestRunner()
        
        @weblens_test(
            name="user_journey_e2e",
            description=(
                "Navigate to https://httpbin.org/forms/post, fill out the form with name 'Integration Test User', "
                "phone '555-0123', and email 'test@weblens.com'. Select 'medium' from the size dropdown. "
                "Submit the form and verify it was successful. Then navigate to https://httpbin.org/json "
                "and verify the page contains 'slideshow'."
            ),
            tags=["e2e", "user-journey"]
        )
        async def user_journey_test(browser):
            # Use natural language approach
            result = await browser.run()
            assert result
        
        # Register and run test
        info = user_journey_test._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=user_journey_test,
            tags=info["tags"]
        )
        
        results = await runner.run_tests(parallel=False)
        
        assert len(results) == 1
        assert results[0].status == "passed"
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    @pytest.mark.e2e
    async def test_responsive_testing_workflow(self):
        """Test responsive design testing workflow"""
        runner = TestRunner()
        
        @weblens_test(
            name="responsive_e2e",
            description=(
                "Navigate to https://getbootstrap.com/docs/5.3/examples/. "
                "Take a screenshot of the page. "
                "If there is a mobile menu toggle button visible, click on it. "
                "Verify that the page title contains 'Bootstrap'"
            ),
            tags=["e2e", "responsive"]
        )
        async def responsive_test(browser):
            # Use natural language approach
            result = await browser.run()
            assert result
            
            # Take screenshot
            screenshot_path = await browser.take_screenshot()
            assert screenshot_path
        
        # Register test
        info = responsive_test._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=responsive_test,
            tags=info["tags"]
        )
        
        results = await runner.run_tests(parallel=False)
        
        # Should have 1 result
        assert len(results) == 1
        assert results[0].status == "passed"


# Markers for different test categories
pytestmark = [
    pytest.mark.integration,
]


# Configuration for integration tests
def pytest_configure(config):
    """Configure pytest for integration tests"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (may take several seconds)"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not slow"])
