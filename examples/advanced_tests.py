"""
Advanced testing examples for WebLens
"""
import asyncio
import json
from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.core.test_runner import weblens_test
from weblens.utils.logger import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="multi_tab_testing",
    description="Test multi-tab functionality",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["multi-tab", "advanced"]
)
async def test_multi_tab_functionality(browser):
    """Test multi-tab operations"""
    # Open first tab
    await browser.go_to("https://example.com")
    original_title = await browser.get_title()
    
    # Open new tab
    await browser.new_tab()
    await browser.go_to("https://httpbin.org")
    
    # Verify we're on the new page
    new_title = await browser.get_title()
    assert "httpbin" in new_title.lower(), f"Expected httpbin in title, got: {new_title}"
    
    # Switch back to first tab
    await browser.switch_to_tab(0)
    current_title = await browser.get_title()
    assert current_title == original_title, "Should be back on original tab"
    
    logger.info("Multi-tab test completed successfully")


@weblens_test(
    name="file_upload_test",
    description="Test file upload functionality",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["upload", "files"]
)
async def test_file_upload(browser):
    """Test file upload functionality"""
    import tempfile
    import os
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test file for WebLens upload testing.")
        temp_file = f.name
    
    try:
        # Navigate to file upload page
        await browser.go_to("https://httpbin.org/forms/post")
        
        # Upload file (if file input exists)
        file_inputs = await browser.find_elements("input[type='file']")
        if file_inputs:
            await browser.upload_file("input[type='file']", temp_file)
            logger.info(f"File uploaded: {temp_file}")
        else:
            logger.info("No file input found, skipping upload test")
    
    finally:
        # Clean up temporary file
        os.unlink(temp_file)
    
    logger.info("File upload test completed")


@weblens_test(
    name="cookie_session_test",
    description="Test cookie and session handling",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["cookies", "session"]
)
async def test_cookie_session_handling(browser):
    """Test cookie and session management"""
    # Navigate to a site that sets cookies
    await browser.go_to("https://httpbin.org/cookies/set/test_cookie/test_value")
    
    # Navigate to cookie display page
    await browser.go_to("https://httpbin.org/cookies")
    
    # Check if cookie was set
    page_content = await browser.get_text("body")
    assert "test_cookie" in page_content, "Test cookie should be present"
    assert "test_value" in page_content, "Test cookie value should be present"
    
    logger.info("Cookie session test completed successfully")


@weblens_test(
    name="iframe_handling",
    description="Test iframe interaction",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["iframe", "frames"]
)
async def test_iframe_handling(browser):
    """Test iframe interactions"""
    # Navigate to a page with iframes
    await browser.go_to("https://www.w3schools.com/html/html_iframe.asp")
    
    # Look for iframes
    iframes = await browser.find_elements("iframe")
    
    if iframes:
        logger.info(f"Found {len(iframes)} iframes")
        
        # Switch to first iframe
        await browser.switch_to_frame(0)
        
        # Interact within iframe
        try:
            iframe_content = await browser.get_text("body")
            logger.info(f"Iframe content preview: {iframe_content[:100]}...")
        except:
            logger.info("Could not read iframe content")
        
        # Switch back to main frame
        await browser.switch_to_default_content()
        
        # Verify we're back in main frame
        main_title = await browser.get_title()
        logger.info(f"Back to main frame: {main_title}")
    else:
        logger.info("No iframes found on the page")
    
    logger.info("Iframe handling test completed")


@weblens_test(
    name="local_storage_test",
    description="Test local storage functionality",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["storage", "javascript"]
)
async def test_local_storage(browser):
    """Test local storage operations"""
    # Navigate to a simple page
    await browser.go_to("https://example.com")
    
    # Set local storage item
    await browser.execute_script("""
        localStorage.setItem('weblens_test', 'test_value');
        localStorage.setItem('weblens_number', '42');
    """)
    
    # Retrieve local storage item
    test_value = await browser.execute_script("return localStorage.getItem('weblens_test');")
    number_value = await browser.execute_script("return localStorage.getItem('weblens_number');")
    
    assert test_value == "test_value", f"Expected 'test_value', got: {test_value}"
    assert number_value == "42", f"Expected '42', got: {number_value}"
    
    # Clear local storage
    await browser.execute_script("localStorage.clear();")
    
    # Verify it's cleared
    cleared_value = await browser.execute_script("return localStorage.getItem('weblens_test');")
    assert cleared_value is None, "Local storage should be cleared"
    
    logger.info("Local storage test completed successfully")


@weblens_test(
    name="geolocation_test",
    description="Test geolocation functionality",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["geolocation", "permissions"]
)
async def test_geolocation(browser):
    """Test geolocation functionality"""
    # Set fake geolocation
    await browser.set_geolocation(latitude=37.7749, longitude=-122.4194)  # San Francisco
    
    # Navigate to a geolocation test page
    await browser.go_to("https://www.w3schools.com/html/html5_geolocation.asp")
    
    # Try to trigger geolocation
    try:
        # Look for geolocation button and click it
        geo_button = await browser.find_element("button")
        if geo_button:
            await browser.click("button")
            
            # Wait a moment for geolocation to be processed
            await asyncio.sleep(3)
            
            logger.info("Geolocation test triggered")
    except:
        logger.info("Could not find geolocation trigger, test completed")
    
    logger.info("Geolocation test completed")


@weblens_test(
    name="cross_browser_comparison",
    description="Compare behavior across different browsers",
    browsers=["chrome", "firefox"],
    profiles=["desktop_chrome", "desktop_firefox"],
    tags=["cross-browser", "comparison"]
)
async def test_cross_browser_comparison(browser):
    """Test cross-browser compatibility"""
    # Navigate to a test page
    await browser.go_to("https://caniuse.com")
    
    # Get page title
    title = await browser.get_title()
    
    # Get user agent
    user_agent = await browser.execute_script("return navigator.userAgent;")
    
    # Check for browser-specific features
    canvas_support = await browser.execute_script("""
        return !!(document.createElement('canvas').getContext);
    """)
    
    webgl_support = await browser.execute_script("""
        try {
            var canvas = document.createElement('canvas');
            return !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
        } catch(e) {
            return false;
        }
    """)
    
    logger.info(f"Browser test results:")
    logger.info(f"  Title: {title}")
    logger.info(f"  User Agent: {user_agent[:50]}...")
    logger.info(f"  Canvas Support: {canvas_support}")
    logger.info(f"  WebGL Support: {webgl_support}")
    
    # Basic assertions
    assert title, "Page should have a title"
    assert "caniuse" in title.lower(), "Should be on caniuse.com"
    
    logger.info("Cross-browser comparison test completed")


async def run_advanced_tests():
    """Run advanced test suite"""
    runner = TestRunner()
    
    # Register advanced test functions
    test_functions = [
        test_multi_tab_functionality,
        test_file_upload,
        test_cookie_session_handling,
        test_iframe_handling,
        test_local_storage,
        test_geolocation,
        test_cross_browser_comparison
    ]
    
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
    logger.info("Starting WebLens advanced tests...")
    results = await runner.run_tests(
        browsers=["chrome"],  # Start with Chrome only
        parallel=False  # Run sequentially for advanced tests
    )
    
    # Print detailed results
    for result in results:
        status_emoji = "✅" if result.status == "passed" else "❌"
        logger.info(f"{status_emoji} {result.name} ({result.duration:.2f}s)")
        if result.error_message:
            logger.error(f"   Error: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(run_advanced_tests())
