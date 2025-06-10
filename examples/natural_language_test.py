#!/usr/bin/env python3
"""
Example test using WebLens with direct natural language instructions
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path to ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from weblens.core.test_runner import weblens_test
from weblens.core.test_runner import TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="natural_language_test",
    description="Test using natural language instructions",
    tags=["demo", "natural-language"]
)
async def test_with_natural_language(browser):
    """Test using natural language instructions directly"""
    # The browser object is now our Agent that accepts natural language instructions
    
    # Run the task defined in the agent creation (done by TestRunner)
    result = await browser.run()
    logger.info(f"Task completed with result: {result}")
    
    # Take a screenshot (if available)
    screenshot_path = await browser.take_screenshot()
    if screenshot_path:
        logger.info(f"Screenshot saved to {screenshot_path}")
    
    # Execute additional instructions
    additional_result = await browser.execute_natural_language(
        "Go back to the homepage and check if the logo is present"
    )
    logger.info(f"Additional task result: {additional_result}")
    
    # You could make assertions based on the task results
    assert result, "Task should return some result"


@weblens_test(
    name="google_search_test",
    description="Search for WebLens on Google",
    tags=["search", "natural-language"]
)
async def test_google_search(browser):
    """Test Google search with natural language"""
    # Define a complex task with natural language
    result = await browser.execute_natural_language(
        "Go to google.com, search for 'WebLens testing framework', "
        "wait for the search results, and tell me how many results appear on the first page"
    )
    
    logger.info(f"Google search results: {result}")
    
    # You can make assertions based on the returned information
    assert result, "Search should return results"


async def main():
    """Main function to run example tests"""
    logger.info("Starting WebLens natural language tests...")
    
    # Create test runner
    runner = TestRunner()
    
    # Register tests
    runner.register_test(
        name="natural_language_test",
        description="Go to example.com, check the page title, and take a screenshot",
        test_function=test_with_natural_language,
        tags=["demo"]
    )
    
    runner.register_test(
        name="google_search_test",
        description="Go to google.com, search for WebLens, and report the results",
        test_function=test_google_search,
        tags=["search"]
    )
    
    # Run tests
    try:
        results = await runner.run_tests(parallel=False)
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
