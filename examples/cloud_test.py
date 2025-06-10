"""
Simple example using WebLens with browser-use cloud API
"""
import asyncio
import os
from weblens import BrowserManager, TestRunner
from weblens.core.test_runner import weblens_test
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="simple_navigation_test",
    description="Test basic navigation with browser-use cloud",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["smoke", "cloud"]
)
async def test_simple_navigation(browser):
    """Simple navigation test using browser-use cloud API"""
    try:
        # Navigate to a website
        logger.info("Navigating to example.com...")
        await browser.go_to("https://example.com")
        
        # Get page title
        title = await browser.get_title()
        logger.info(f"Page title: {title}")
        
        # Verify title contains "Example"
        assert "Example" in title, f"Expected 'Example' in title, got: {title}"
        
        # Take a screenshot
        logger.info("Taking screenshot...")
        await browser.take_screenshot()
        
        logger.info("Test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise


@weblens_test(
    name="google_search_test",
    description="Test Google search functionality",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["search", "cloud"]
)
async def test_google_search(browser):
    """Test Google search functionality"""
    try:
        # Navigate to Google
        logger.info("Navigating to Google...")
        await browser.go_to("https://www.google.com")
        
        # Search for WebLens
        logger.info("Performing search...")
        search_box = await browser.find_element("textarea[name='q']")
        if search_box:
            await browser.fill_input("textarea[name='q']", "WebLens testing framework")
            await browser.click("input[name='btnK']")
            
            # Wait for results
            await asyncio.sleep(3)
            
            # Check if we have search results
            title = await browser.get_title()
            logger.info(f"Search results page title: {title}")
            
            assert "WebLens" in title, f"Expected 'WebLens' in title, got: {title}"
        else:
            logger.warning("Could not find search box")
        
        logger.info("Google search test completed!")
        
    except Exception as e:
        logger.error(f"Google search test failed: {e}")
        raise


async def main():
    """Main function to run simple tests"""
    # Check if API key is configured
    api_key = os.getenv("BROWSER_USE_API_KEY")
    if not api_key or api_key == "your_browser_use_api_key_here":
        logger.warning("Browser-use API key not configured!")
        logger.info("Please set BROWSER_USE_API_KEY in your .env file")
        logger.info("Tests will run with mock browser functionality")
    
    # Create test runner
    runner = TestRunner()
    
    # Register tests
    test_functions = [test_simple_navigation, test_google_search]
    
    for test_func in test_functions:
        if hasattr(test_func, '_weblens_test_info'):
            info = test_func._weblens_test_info
            runner.register_test(
                name=info['name'],
                description=info['description'],
                test_function=test_func,
                browsers=info['browsers'],
                profiles=info['profiles'],
                tags=info['tags']
            )
    
    # Run tests
    try:
        logger.info("Starting WebLens simple cloud tests...")
        results = await runner.run_tests(
            browsers=["chrome"],
            parallel=False  # Run sequentially for better debugging
        )
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        
        logger.info("=" * 50)
        logger.info("TEST SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total tests: {len(results)}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        
        if failed > 0:
            logger.info("\nFailed tests:")
            for result in results:
                if result.status == "failed":
                    logger.error(f"  ❌ {result.name}: {result.error_message}")
        
        if passed > 0:
            logger.info("\nPassed tests:")
            for result in results:
                if result.status == "passed":
                    logger.info(f"  ✅ {result.name} ({result.duration:.2f}s)")
    
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
