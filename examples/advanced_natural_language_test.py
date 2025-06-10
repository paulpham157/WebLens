#!/usr/bin/env python3
"""
WebLens: Natural Language Testing Example
----------------------------------------

This example demonstrates testing a web application using natural language instructions.
This approach is much simpler than traditional programmatic testing approaches.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from weblens.core.test_runner import weblens_test, TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)

# -------------------------------------------------------------------------
# Test functions using natural language instructions
# -------------------------------------------------------------------------

@weblens_test(
    name="e_commerce_test",
    description=(
        "Go to https://react-shopping-cart-67954.firebaseapp.com/, "
        "find the first product, add it to cart, verify the cart has 1 item, "
        "then take a screenshot of the cart"
    ),
    tags=["e-commerce", "natural-language"]
)
async def test_e_commerce(browser):
    """Test e-commerce functionality using natural language"""
    # Run the task defined in the description
    result = await browser.run()
    logger.info(f"Test result: {result}")


@weblens_test(
    name="responsive_test",
    description=(
        "Go to https://getbootstrap.com, check if the site is responsive "
        "by resizing the window to mobile size (375x667), and verify "
        "that the mobile menu button appears"
    ),
    tags=["responsive", "natural-language"]
)
async def test_responsive(browser):
    """Test responsive design using natural language"""
    result = await browser.run()
    logger.info(f"Test result: {result}")


@weblens_test(
    name="form_validation_test",
    description=(
        "Go to https://getbootstrap.com/docs/5.3/forms/validation/, "
        "find the validation example form, try to submit it without "
        "filling any fields, and verify validation errors appear"
    ),
    tags=["forms", "validation", "natural-language"]
)
async def test_form_validation(browser):
    """Test form validation using natural language"""
    result = await browser.run()
    logger.info(f"Test result: {result}")


async def main():
    """Main function to run tests"""
    runner = TestRunner()
    
    # Register test functions
    for test_func in [test_e_commerce, test_responsive, test_form_validation]:
        info = test_func._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=test_func,
            tags=info["tags"]
        )
    
    # Run single test (for faster demo)
    test_to_run = "form_validation_test"  # Change this to run different tests
    
    try:
        logger.info(f"Running test: {test_to_run}")
        results = await runner.run_tests(
            test_names=[test_to_run],
            parallel=False
        )
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
        if failed > 0:
            for result in results:
                if result.status == "failed":
                    logger.error(f"Failed test: {result.name}")
                    logger.error(f"Error: {result.error_message}")
    
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
