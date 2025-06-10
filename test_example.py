#!/usr/bin/env python3
"""
WebLens Natural Language Test Example
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from weblens.core.test_runner import weblens_test, TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="Test Example",
    description="Go to example.com and check the title",
    tags=["natural-language"]
)
async def test_natural_language(browser):
    """Test using natural language instructions"""
    result = await browser.run()
    logger.info(f"Test result: {result}")
    
    # Add your assertions here
    assert result, "Test should return a result"


async def main():
    """Main function to run tests"""
    runner = TestRunner()
    
    # Register test function
    info = test_natural_language._weblens_test_info
    runner.register_test(
        name=info["name"],
        description=info["description"],
        test_function=test_natural_language,
        tags=info["tags"]
    )
    
    try:
        logger.info(f"Running test: {info['name']}")
        results = await runner.run_tests(
            test_names=[info["name"]],
            parallel=False
        )
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
