#!/usr/bin/env python3
"""
Simple test to verify WebLens framework
"""
import asyncio
import os
from weblens.core.test_runner import TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


async def simple_test_function(agent):
    """Simple test function"""
    logger.info("Running simple test...")
    # Just a simple assertion
    assert True, "This should pass"
    logger.info("Simple test completed!")


async def main():
    """Main function to run simple test"""
    logger.info("Starting simple WebLens test...")
    
    # Create test runner
    runner = TestRunner()
    
    # Register test manually
    runner.register_test(
        name="simple_test",
        description="A simple test to verify framework",
        test_function=simple_test_function,
        tags=["smoke"]
    )
    
    # Run tests
    try:
        logger.info("Executing test...")
        results = await runner.run_tests(parallel=False)
        
        # Print results
        logger.info("=" * 50)
        logger.info("TEST RESULTS")
        logger.info("=" * 50)
        
        for result in results:
            status_icon = "✅" if result.status == "passed" else "❌"
            logger.info(f"{status_icon} {result.name}: {result.status} ({result.duration:.2f}s)")
            if result.error_message:
                logger.error(f"   Error: {result.error_message}")
        
        return len([r for r in results if r.status == "failed"]) == 0
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
