# WebLens - User Guide

WebLens is an AI-driven testing framework that enables writing tests in natural language instead of using traditional selector-based methods. The framework connects to the browser-use cloud API to automate browsers based on instructions written in natural language.

## 📦 Installation

### System Requirements

- Python 3.9+
- Conda (Miniconda or Anaconda)
- macOS, Windows, or Linux

### Installation with Conda (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd WebLens

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate weblens

# Run setup script
./setup.sh

# Or manual setup
make setup
```

### Manual Dependencies Installation

```bash
# If you don't have a conda environment yet
conda create -n weblens python=3.9
conda activate weblens

# Install dependencies
conda install -c conda-forge pydantic colorama rich pytest pytest-asyncio python-dotenv black flake8 mypy
pip install browser-use>=0.2.0 asyncio-throttle
```

### Environment Configuration

```bash
# Copy example configuration file
cp .env.example .env

# Edit .env file with your Browser-use API key
# Required for browser-use cloud functionality
```

## 🎯 Usage

### 1. Using the CLI

```bash
# Run basic tests
python weblens_cli.py run examples/basic_tests.py

# Run tests by tags
python weblens_cli.py run examples/basic_tests.py --tags smoke navigation

# Run tests sequentially (no parallelism)
python weblens_cli.py run examples/basic_tests.py --sequential

# View list of profiles
python weblens_cli.py profiles list

# Create a new profile
python weblens_cli.py profiles create
```

### 2. Using Programmatically

```python
import asyncio
from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.core.test_runner import weblens_test

# Define test function
@weblens_test(
    name="example_test",
    description="Go to example.com, wait for the page to load, and verify the title contains 'Example'",
    tags=["smoke", "navigation"]
)
async def test_navigation(browser):
    # Execute the natural language instruction
    result = await browser.run()
    assert "Example" in result
    
    # Take screenshot
    await browser.take_screenshot()

# Run tests
async def main():
    runner = TestRunner()
    
    # Register test
    runner.register_test(
        name="example_test",
        description="Go to example.com, wait for the page to load, and verify the title contains 'Example'",
        test_function=test_navigation,
        tags=["smoke", "navigation"]
    )
    
    # Execute tests
    results = await runner.run_tests()
    
    # Print results
    for result in results:
        print(f"{result.name}: {result.status} ({result.duration:.2f}s)")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Profile Management

```python
from weblens.profiles.profile_manager import ProfileManager

# Create profile manager
pm = ProfileManager()

# Create custom profile
profile = pm.create_profile(
    name="my_mobile_profile",
    browser="chrome",
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    viewport={"width": 375, "height": 812},
    locale="vi-VN",
    timezone="Asia/Ho_Chi_Minh"
)

# Clone existing profile
cloned = pm.clone_profile(
    source_name="desktop_chrome",
    new_name="my_desktop_profile",
    user_agent="Custom Desktop Agent"
)

# List profiles
profiles = pm.list_profiles("chrome")
for profile in profiles:
    print(f"{profile.name}: {profile.viewport}")
```

## 📁 Project Structure

```text
WebLens/
├── weblens/                    # Core framework
│   ├── __init__.py
│   ├── config.py              # Configuration management (cloud-based)
│   ├── core/                  # Core components
│   │   ├── browser_manager.py # Browser-use cloud agent manager
│   │   └── test_runner.py     # Test execution engine
│   ├── profiles/              # Profile management
│   │   └── profile_manager.py
│   └── utils/                 # Utilities
│       ├── logger.py          # Logging utilities
│       └── helpers.py         # Helper functions
├── examples/                  # Example test suites
│   ├── natural_language_test.py      # Basic natural language example
│   ├── login_test_example.py         # Login testing example
│   ├── advanced_natural_assertions.py # Advanced assertions using natural language
│   └── direct_browser_use.py  # Direct browser-use API example
├── tests/                     # Framework tests
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── conftest.py            # Pytest configuration
├── config/                    # Configuration files
├── logs/                      # Log files
├── screenshots/               # Test screenshots
├── videos/                    # Test recordings
├── reports/                   # Test reports
├── browser_profiles/          # Browser profile data
├── environment.yml            # Conda environment file
├── weblens_cli.py            # CLI interface
├── requirements.txt           # Python dependencies (backup)
└── pyproject.toml            # Project configuration
```

## 🔧 Available Browser Profiles

The framework provides these common profiles:

- **desktop_chrome**: Desktop Chrome with 1920x1080 viewport
- **mobile_chrome**: Mobile Chrome simulating iPhone
- **tablet**: Tablet viewport 768x1024
- **desktop_firefox**: Desktop Firefox
- **high_dpi**: High resolution display
- **privacy**: Privacy-focused profile

## 📊 Test Reports

WebLens automatically generates detailed reports including:

- **JSON Reports**: Detailed results in JSON format
- **Screenshots**: Screen captures when tests fail
- **Videos**: Recording of the entire test session (optional)
- **Logs**: Detailed logging with multiple levels

## 🎨 Advanced Features

### Custom Test Decorators

```python
@weblens_test(
    name="responsive_test",
    description="Go to example.com and verify the responsive design works correctly across different device sizes",
    tags=["responsive", "ui"]
)
async def test_responsive_design(browser):
    result = await browser.run()
    assert "responsive design works correctly" in result
```

### Error Handling & Retry

```python
from weblens.utils.helpers import retry_async

@retry_async(max_retries=3, delay=1.0)
async def flaky_test(browser):
    # Test will be retried up to 3 times if it fails
    result = await browser.execute_natural_language("Navigate to unstable-site.com and verify it loads properly")
```

### Performance Testing

```python
from weblens.utils.helpers import timing

@timing
async def performance_test(browser):
    # Execution time will be logged automatically
    result = await browser.execute_natural_language("Go to example.com and measure page load time")
```

## 🔍 Advanced Assertions

WebLens allows combining natural language with complex assertions to test website features and data:

```python
@weblens_test(
    name="product_price_assertion",
    description=(
        "Go to https://www.saucedemo.com/, "
        "login with username 'standard_user' and password 'secret_sauce', "
        "check the price of the 'Sauce Labs Backpack', "
        "and return the price value"
    )
)
async def test_product_price(browser):
    """Check and validate product price"""
    result = await browser.run()
    
    # Find price in the result using regex
    price_match = re.search(r'\$([0-9]+\.[0-9]+)', result)
    if price_match:
        price = float(price_match.group(1))
        assert 20 <= price <= 50, f"Price ${price} is outside the expected range $20-$50"
    else:
        assert False, "Price information not found in the result"
```

See more complex examples in `examples/advanced_natural_assertions.py`.

## Cloud API Configuration

WebLens uses the browser-use cloud API instead of Playwright to control browsers. To customize:

1. **API Key**: Set `BROWSER_USE_API_KEY` in the `.env` file to authenticate with the cloud service
2. **API Base URL**: You can customize the API URL by setting the `BROWSER_USE_BASE_URL` environment variable in the `.env` file

```bash
# In .env file
BROWSER_USE_API_KEY=your_api_key_here
BROWSER_USE_BASE_URL=https://api.browser-use.com/api/v1  # default URL
```

### When to customize Base URL

You may need to customize the base URL in the following cases:

- When using a new or special API version
- When connecting to staging or testing environments
- When using proxies to optimize performance from different geographical regions
- When deploying a self-hosted browser-use service

### Setting up URL and checking connection

```python
import os
from weblens.config import config

# Check current configuration
print(f"Base URL: {config.browser_use_base_url}")
print(f"API Key configured: {'Yes' if config.browser_use_api_key else 'No'}")
```

Chi tiết thêm về browser-use cloud API và các tùy chỉnh nâng cao có thể xem tại [tài liệu browser-use cloud API](./docs/browser_use_cloud_api.md).

## 🗣️ Using Natural Language

WebLens now uses a natural language approach to control browsers instead of traditional selector-based methods. This makes writing test cases easier and less dependent on specific HTML/CSS structure of web pages.

### 1. Writing Tests in Natural Language

```python
@weblens_test(
    name="login_test",
    description=(
        "Go to example.com/login, "
        "enter 'testuser' into username field, "
        "enter 'password123' into password field, "
        "click on login button, and "
        "verify that the welcome message appears"
    )
)
async def test_login(browser):
    result = await browser.run()
    assert "welcome message appears" in result
```

### 2. Adding Instructions in Tests

```python
@weblens_test(
    name="complex_flow_test",
    description="Go to example.com"
)
async def test_complex_flow(browser):
    # Execute initial description
    await browser.run()
    
    # Add additional steps
    result1 = await browser.execute_natural_language(
        "Click on the Products link in the navigation menu"
    )
    
    result2 = await browser.execute_natural_language(
        "Sort products by price and select the most expensive item"
    )
    
    result3 = await browser.execute_natural_language(
        "Add the product to cart and proceed to checkout"
    )
    
    # Check results
    assert "checkout page" in result3
```

### 3. Combining with Assertions

```python
@weblens_test(
    name="search_test",
    description="Go to example.com and search for 'WebLens framework'"
)
async def test_search(browser):
    # Perform search
    result = await browser.run()
    
    # Check search results
    search_results = await browser.execute_natural_language(
        "Count the number of search results and return the count"
    )
    
    # Convert result from string to number
    count = int(''.join(filter(str.isdigit, search_results)))
    assert count > 0
```

## 🧪 Login Test Example

WebLens provides a complete example of how to test login functionality for a real website:

```python
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
    """Test successful login with valid credentials"""
    result = await browser.run()
    assert "login was successful" in result.lower()
```

To run the complete login testing example, use the following command:

```bash
python examples/login_test_example.py
```

This example includes the following test cases:

- Successful login with valid credentials
- Login with an invalid username
- Login with an invalid password
- Successful login followed by logout

For the complete source code, see `examples/login_test_example.py`

## 📚 Additional Documentation

Besides this guide, WebLens provides other in-depth documentation:

- [Comprehensive Natural Language Guide](./docs/natural_language_guide_full.md) - Complete guide to the natural language approach
- [Natural Language Approach](./docs/natural_language_approach.md) - Detailed guide on using natural language in testing
- [Login Testing Guide](./docs/login_testing_guide.md) - Guide for testing login functionality with WebLens
- [Browser Use Cloud API](./docs/browser_use_cloud_api.md) - Documentation about the cloud API used in WebLens

## 📝 Recent Changes

WebLens has transitioned to using a fully natural language approach through the browser-use API. For details about these changes, please refer to the [change log document](../../CHANGELOG.md).
