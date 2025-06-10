"""
Example test cases for WebLens demonstrating various testing scenarios
"""
import asyncio
from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.core.test_runner import weblens_test
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="basic_navigation",
    description="Test basic navigation functionality",
    browsers=["chrome", "firefox"],
    profiles=["desktop_chrome", "desktop_firefox"],
    tags=["smoke", "navigation"]
)
async def test_basic_navigation(browser):
    """Test basic page navigation"""
    # Navigate to a website
    await browser.go_to("https://example.com")
    
    # Wait for page to load
    await browser.wait_for_element("h1", timeout=10)
    
    # Verify page title
    title = await browser.get_title()
    assert "Example" in title, f"Expected 'Example' in title, got: {title}"
    
    logger.info(f"Successfully navigated to example.com, title: {title}")


@weblens_test(
    name="form_interaction",
    description="Test form filling and submission",
    browsers=["chrome"],
    profiles=["desktop_chrome", "mobile_chrome"],
    tags=["forms", "interaction"]
)
async def test_form_interaction(browser):
    """Test form interactions"""
    # Navigate to a form page
    await browser.go_to("https://httpbin.org/forms/post")
    
    # Fill out form fields
    await browser.fill_input("input[name='custname']", "Test User")
    await browser.fill_input("input[name='custtel']", "123-456-7890")
    await browser.fill_input("input[name='custemail']", "test@example.com")
    
    # Select from dropdown
    await browser.select_option("select[name='size']", "large")
    
    # Submit form
    await browser.click("input[type='submit']")
    
    # Wait for response
    await browser.wait_for_element("pre", timeout=10)
    
    logger.info("Form interaction test completed successfully")


@weblens_test(
    name="responsive_design",
    description="Test responsive design across different viewports",
    browsers=["chrome"],
    profiles=["desktop_chrome", "tablet", "mobile_chrome"],
    tags=["responsive", "ui"]
)
async def test_responsive_design(browser):
    """Test responsive design"""
    # Navigate to a responsive website
    await browser.go_to("https://getbootstrap.com")
    
    # Check if navigation is visible/hidden based on viewport
    try:
        nav_toggle = await browser.find_element(".navbar-toggler")
        if nav_toggle:
            logger.info("Mobile navigation toggle found (mobile/tablet view)")
        else:
            logger.info("No navigation toggle (desktop view)")
    except:
        logger.info("Desktop navigation layout detected")
    
    # Take screenshot for visual verification
    await browser.take_screenshot()
    
    logger.info("Responsive design test completed")


@weblens_test(
    name="javascript_heavy_app",
    description="Test JavaScript-heavy single page application",
    browsers=["chrome", "firefox"],
    profiles=["desktop_chrome", "desktop_firefox"],
    tags=["spa", "javascript"]
)
async def test_javascript_heavy_app(browser):
    """Test JavaScript-heavy application"""
    # Navigate to a React/Vue app
    await browser.go_to("https://react-shopping-cart-67954.firebaseapp.com/")
    
    # Wait for React app to load
    await browser.wait_for_element(".shelf", timeout=15)
    
    # Interact with the app
    products = await browser.find_elements(".shelf-item")
    if products:
        # Click on first product's add to cart button
        await browser.click(".shelf-item:first-child .shelf-item__buy-btn")
        
        # Wait for cart to update
        await asyncio.sleep(2)
        
        # Check cart count
        cart_count = await browser.get_text(".bag__quantity")
        assert cart_count and int(cart_count) > 0, "Cart should have items"
        
        logger.info(f"Successfully added item to cart, count: {cart_count}")
    
    logger.info("JavaScript-heavy app test completed")


@weblens_test(
    name="accessibility_check",
    description="Basic accessibility checks",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["accessibility", "a11y"]
)
async def test_accessibility_check(browser):
    """Test basic accessibility features"""
    # Navigate to a website
    await browser.go_to("https://webaim.org/")
    
    # Check for proper heading structure
    h1_elements = await browser.find_elements("h1")
    assert len(h1_elements) == 1, f"Should have exactly one h1, found {len(h1_elements)}"
    
    # Check for alt text on images
    images = await browser.find_elements("img")
    for i, img in enumerate(images[:5]):  # Check first 5 images
        alt_text = await browser.get_attribute(f"img:nth-of-type({i+1})", "alt")
        if not alt_text:
            logger.warning(f"Image {i+1} missing alt text")
    
    # Check for proper form labels
    inputs = await browser.find_elements("input[type='text'], input[type='email']")
    for i, input_elem in enumerate(inputs[:3]):  # Check first 3 inputs
        label = await browser.find_element(f"label[for='{await browser.get_attribute(f'input:nth-of-type({i+1})', 'id')}']")
        if not label:
            logger.warning(f"Input {i+1} missing associated label")
    
    logger.info("Accessibility check completed")


@weblens_test(
    name="performance_test",
    description="Basic performance testing",
    browsers=["chrome"],
    profiles=["desktop_chrome"],
    tags=["performance"]
)
async def test_performance(browser):
    """Test page load performance"""
    import time
    
    # Measure page load time
    start_time = time.time()
    await browser.go_to("https://www.google.com")
    await browser.wait_for_element("input[name='q']", timeout=10)
    load_time = time.time() - start_time
    
    # Assert reasonable load time (adjust threshold as needed)
    assert load_time < 10, f"Page load took too long: {load_time:.2f}s"
    
    logger.info(f"Page loaded in {load_time:.2f} seconds")
    
    # Test search functionality
    await browser.fill_input("input[name='q']", "WebLens testing framework")
    await browser.press_key("Enter")
    
    # Wait for search results
    await browser.wait_for_element("#search", timeout=10)
    
    logger.info("Performance test completed")


async def main():
    """Main function to run example tests"""
    runner = TestRunner()
    
    # Register all test functions
    test_functions = [
        test_basic_navigation,
        test_form_interaction,
        test_responsive_design,
        test_javascript_heavy_app,
        test_accessibility_check,
        test_performance
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
    try:
        logger.info("Starting WebLens example tests...")
        results = await runner.run_tests(
            browsers=["chrome"],  # Start with Chrome only
            parallel=True
        )
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
        if failed > 0:
            logger.info("Failed tests:")
            for result in results:
                if result.status == "failed":
                    logger.error(f"  - {result.name}: {result.error_message}")
    
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
