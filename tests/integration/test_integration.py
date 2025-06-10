"""
Integration tests for WebLens
"""
import pytest
import asyncio
import tempfile
from pathlib import Path

from weblens import BrowserManager, TestRunner, ProfileManager
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
            
            # Launch browser
            browser = await manager.launch_browser("chrome")
            assert browser is not None
            
            # Navigate to a page
            await browser.go_to("https://example.com")
            
            # Get page title
            title = await browser.get_title()
            assert "Example" in title
            
            # Close browser
            await manager.close_browser("chrome")
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_profile_based_testing(self):
        """Test browser launch with different profiles"""
        manager = BrowserManager()
        profile_manager = ProfileManager()
        
        try:
            await manager.start()
            
            # Get available profiles
            chrome_profiles = profile_manager.get_profiles_by_browser("chrome")
            if chrome_profiles:
                profile_name = chrome_profiles[0].name
                
                # Launch browser with profile
                browser = await manager.launch_browser("chrome", profile_name)
                assert browser is not None
                
                # Test navigation
                await browser.go_to("https://httpbin.org/user-agent")
                
                # Close browser
                await manager.close_browser("chrome", profile_name)
        
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_test_execution(self):
        """Test full test execution pipeline"""
        runner = TestRunner()
        
        # Define a simple test
        async def simple_test(browser):
            await browser.go_to("https://example.com")
            title = await browser.get_title()
            assert "Example" in title
        
        # Register test
        runner.register_test(
            name="simple_integration_test",
            description="Simple integration test",
            test_function=simple_test,
            browsers=["chrome"],
            profiles=[None]
        )
        
        # Run tests
        results = await runner.run_tests(parallel=False)
        
        # Verify results
        assert len(results) == 1
        assert results[0].status == "passed"
        assert results[0].name == "simple_integration_test_chrome_default"
    
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
        async def failing_test(browser):
            await browser.go_to("https://example.com")
            # This should fail
            await browser.click("#non-existent-element")
        
        # Register test
        runner.register_test(
            name="failing_integration_test",
            description="Test that should fail",
            test_function=failing_test,
            browsers=["chrome"],
            profiles=[None]
        )
        
        # Run tests
        results = await runner.run_tests(parallel=False)
        
        # Verify results
        assert len(results) == 1
        assert results[0].status == "failed"
        assert results[0].error_message is not None
        
        # Check if screenshot was taken (if enabled)
        if config.test_config.screenshot_on_failure and results[0].screenshot_path:
            screenshot_path = Path(results[0].screenshot_path)
            assert screenshot_path.exists()
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_multiple_browser_sessions(self):
        """Test managing multiple browser sessions"""
        manager = BrowserManager()
        
        try:
            await manager.start()
            
            # Launch multiple browsers
            chrome_browser = await manager.launch_browser("chrome", "profile1")
            firefox_browser = await manager.launch_browser("firefox", "profile2")
            
            # Test both browsers
            await chrome_browser.go_to("https://example.com")
            await firefox_browser.go_to("https://httpbin.org")
            
            # Get titles
            chrome_title = await chrome_browser.get_title()
            firefox_title = await firefox_browser.get_title()
            
            assert "Example" in chrome_title
            assert "httpbin" in firefox_title.lower()
            
            # Verify browser instances are tracked
            active_browsers = manager.list_active_browsers()
            assert "chrome_profile1" in active_browsers
            assert "firefox_profile2" in active_browsers
            
            # Close browsers
            await manager.close_browser("chrome", "profile1")
            await manager.close_browser("firefox", "profile2")
            
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
        
        async def user_journey_test(browser):
            # Step 1: Navigate to a form page
            await browser.go_to("https://httpbin.org/forms/post")
            
            # Step 2: Fill out the form
            await browser.fill_input("input[name='custname']", "Integration Test User")
            await browser.fill_input("input[name='custtel']", "555-0123")
            await browser.fill_input("input[name='custemail']", "test@weblens.com")
            
            # Step 3: Select dropdown option
            await browser.select_option("select[name='size']", "medium")
            
            # Step 4: Submit form
            await browser.click("input[type='submit']")
            
            # Step 5: Verify submission
            await browser.wait_for_element("pre", timeout=10)
            
            # Step 6: Navigate to another page
            await browser.go_to("https://httpbin.org/json")
            
            # Step 7: Verify JSON response
            content = await browser.get_text("body")
            assert "slideshow" in content
        
        # Register and run test
        runner.register_test(
            name="user_journey_e2e",
            description="Complete user journey test",
            test_function=user_journey_test,
            browsers=["chrome"]
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
        profile_manager = ProfileManager()
        
        async def responsive_test(browser):
            # Navigate to a responsive site
            await browser.go_to("https://getbootstrap.com/docs/5.3/examples/")
            
            # Take screenshot for current viewport
            await browser.take_screenshot()
            
            # Check for responsive elements
            try:
                # Try to find mobile menu toggle (present on mobile/tablet)
                mobile_toggle = await browser.find_element(".navbar-toggler")
                if mobile_toggle:
                    await browser.click(".navbar-toggler")
            except:
                # Likely desktop view, no mobile toggle
                pass
            
            # Verify page loaded correctly
            title = await browser.get_title()
            assert "Bootstrap" in title
        
        # Register test for different profiles
        runner.register_test(
            name="responsive_e2e",
            description="Responsive design E2E test",
            test_function=responsive_test,
            browsers=["chrome"],
            profiles=["desktop_chrome", "tablet", "mobile_chrome"]
        )
        
        results = await runner.run_tests(parallel=False)
        
        # Should have 3 results (one for each profile)
        assert len(results) == 3
        assert all(r.status == "passed" for r in results)


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
