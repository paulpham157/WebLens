#!/usr/bin/env python3
"""
WebLens: Ví dụ test đăng nhập cho trang practice test automation
https://practicetestautomation.com/practice-test-login/
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


@weblens_test(
    name="successful_login_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "enter username 'student' and password 'Password123', "
        "click the Submit button, and verify that login was successful "
        "by checking for the 'Logged In Successfully' message"
    ),
    tags=["login", "positive"]
)
async def test_successful_login(browser):
    """Test đăng nhập thành công với thông tin hợp lệ"""
    result = await browser.run()
    logger.info(f"Test result: {result}")
    assert "login was successful" in result.lower() or "logged in successfully" in result.lower()


@weblens_test(
    name="invalid_username_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "enter incorrect username 'incorrectUser' and password 'Password123', "
        "click the Submit button, and verify that proper error message is displayed "
        "indicating 'Your username is invalid'"
    ),
    tags=["login", "negative"]
)
async def test_invalid_username(browser):
    """Test đăng nhập với username không hợp lệ"""
    result = await browser.run()
    logger.info(f"Test result: {result}")
    assert "username is invalid" in result.lower()


@weblens_test(
    name="invalid_password_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "enter correct username 'student' and incorrect password 'InvalidPass', "
        "click the Submit button, and verify that proper error message is displayed "
        "indicating 'Your password is invalid'"
    ),
    tags=["login", "negative"]
)
async def test_invalid_password(browser):
    """Test đăng nhập với password không hợp lệ"""
    result = await browser.run()
    logger.info(f"Test result: {result}")
    assert "password is invalid" in result.lower()


@weblens_test(
    name="logout_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "login with username 'student' and password 'Password123', "
        "verify successful login, then click on the 'Log out' button "
        "and verify that user is successfully logged out and returned to the login page"
    ),
    tags=["login", "logout"]
)
async def test_logout(browser):
    """Test đăng nhập thành công rồi đăng xuất"""
    result = await browser.run()
    logger.info(f"Test result: {result}")
    assert "successfully logged out" in result.lower() or "returned to the login page" in result.lower()


async def main():
    """Run all login tests"""
    logger.info("Starting login tests...")
    
    runner = TestRunner()
    
    # Register all test functions
    for test_func in [
        test_successful_login,
        test_invalid_username,
        test_invalid_password,
        test_logout
    ]:
        info = test_func._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=test_func,
            tags=info["tags"]
        )
    
    try:
        # Run all tests sequentially
        results = await runner.run_tests(parallel=False)
        
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
