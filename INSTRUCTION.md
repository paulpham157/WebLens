# WebLens - Hướng Dẫn Sử Dụng

WebLens là framework testing dựa trên AI, cho phép viết test bằng ngôn ngữ tự nhiên thay vì sử dụng các phương thức selector-based truyền thống. Framework kết nối với browser-use cloud API để tự động hóa trình duyệt dựa trên các hướng dẫn viết bằng ngôn ngữ tự nhiên.

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.9+
- Conda (Miniconda hoặc Anaconda)
- macOS, Windows, hoặc Linux

### Cài Đặt với Conda (Khuyến nghị)

```bash
# Clone repository
git clone <repository-url>
cd WebLens

# Tạo conda environment
conda env create -f environment.yml

# Kích hoạt environment
conda activate weblens

# Chạy setup script
./setup.sh

# Hoặc setup thủ công
make setup
```

### Cài Đặt Dependencies Thủ Công

```bash
# Nếu chưa có conda environment
conda create -n weblens python=3.9
conda activate weblens

# Cài đặt dependencies
conda install -c conda-forge pydantic colorama rich pytest pytest-asyncio python-dotenv black flake8 mypy
pip install browser-use>=0.2.0 asyncio-throttle
```

### Cấu Hình Environment

```bash
# Copy file cấu hình mẫu
cp .env.example .env

# Chỉnh sửa file .env với Browser-use API key của bạn
# Cần thiết cho browser-use cloud functionality
```

## 🎯 Cách Sử Dụng

### 1. Sử Dụng CLI

```bash
# Chạy basic tests
python weblens_cli.py run examples/basic_tests.py

# Chạy tests theo tags
python weblens_cli.py run examples/basic_tests.py --tags smoke navigation

# Chạy tests tuần tự (không song song)
python weblens_cli.py run examples/basic_tests.py --sequential

# Xem danh sách profiles
python weblens_cli.py profiles list

# Tạo profile mới
python weblens_cli.py profiles create
```

### 2. Sử Dụng Programmatically

```python
import asyncio
from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.core.test_runner import weblens_test

# Định nghĩa test function
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

### 3. Quản Lý Browser Profiles

```python
from weblens.profiles.profile_manager import ProfileManager

# Tạo profile manager
pm = ProfileManager()

# Tạo custom profile
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

## 📁 Cấu Trúc Dự Án

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
│   ├── basic_tests.py         # Basic test examples
│   ├── advanced_tests.py      # Advanced test scenarios
│   └── cloud_test.py          # Browser-use cloud examples
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

Framework cung cấp sẵn các profiles phổ biến:

- **desktop_chrome**: Desktop Chrome với viewport 1920x1080
- **mobile_chrome**: Mobile Chrome mô phỏng iPhone
- **tablet**: Tablet viewport 768x1024
- **desktop_firefox**: Desktop Firefox
- **high_dpi**: High resolution display
- **privacy**: Privacy-focused profile

## 📊 Test Reports

WebLens tự động tạo reports chi tiết bao gồm:

- **JSON Reports**: Kết quả chi tiết ở format JSON
- **Screenshots**: Captures màn hình khi test fails
- **Videos**: Recording toàn bộ test session (optional)
- **Logs**: Detailed logging với multiple levels

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
    # Test sẽ được retry tối đa 3 lần nếu fail
    result = await browser.execute_natural_language("Navigate to unstable-site.com and verify it loads properly")
```

### Performance Testing

```python
from weblens.utils.helpers import timing

@timing
async def performance_test(browser):
    # Execution time sẽ được log tự động
    result = await browser.execute_natural_language("Go to example.com and measure page load time")
```

## 🔍 Assertions Nâng Cao

WebLens cho phép kết hợp ngôn ngữ tự nhiên với các assertions phức tạp để kiểm tra tính năng và dữ liệu của trang web:

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
    """Kiểm tra và xác thực giá sản phẩm"""
    result = await browser.run()
    
    # Tìm giá trong kết quả bằng biểu thức chính quy
    price_match = re.search(r'\$([0-9]+\.[0-9]+)', result)
    if price_match:
        price = float(price_match.group(1))
        assert 20 <= price <= 50, f"Giá ${price} nằm ngoài khoảng kỳ vọng $20-$50"
    else:
        assert False, "Không tìm thấy thông tin giá trong kết quả"
```

Xem thêm ví dụ phức tạp hơn tại `examples/advanced_natural_assertions.py`.

## Cấu hình API Cloud

WebLens sử dụng browser-use cloud API thay vì Playwright để điều khiển trình duyệt. Để tùy chỉnh:

1. **API Key**: Đặt `BROWSER_USE_API_KEY` trong file `.env` để xác thực với dịch vụ cloud
2. **URL Cơ sở API**: Có thể tùy chỉnh URL API bằng cách đặt biến môi trường `BROWSER_USE_BASE_URL` trong file `.env`

```bash
# Trong file .env
BROWSER_USE_API_KEY=your_api_key_here
BROWSER_USE_BASE_URL=https://api.browser-use.com/api/v1  # URL mặc định
```

### Khi nào cần tùy chỉnh Base URL

Bạn có thể cần tùy chỉnh base URL trong các trường hợp sau:

- Khi sử dụng phiên bản API mới hoặc đặc biệt
- Khi kết nối tới môi trường staging hoặc testing
- Khi dùng proxy để tối ưu hiệu suất từ các khu vực địa lý khác nhau
- Khi triển khai self-hosted browser-use service

### Thiết lập URL và kiểm tra kết nối

```python
import os
from weblens.config import config

# Kiểm tra cấu hình hiện tại
print(f"Base URL: {config.browser_use_base_url}")
print(f"API Key configured: {'Yes' if config.browser_use_api_key else 'No'}")
```

Chi tiết thêm về browser-use cloud API và các tùy chỉnh nâng cao có thể xem tại [tài liệu browser-use cloud API](./docs/browser_use_cloud_api.md).

## 🗣️ Sử Dụng Natural Language

WebLens hiện sử dụng phương pháp ngôn ngữ tự nhiên để điều khiển trình duyệt thay vì các phương thức selector-based truyền thống. Điều này giúp viết test case dễ dàng hơn và ít phụ thuộc vào cấu trúc HTML/CSS cụ thể của trang web.

### 1. Viết Test bằng Ngôn Ngữ Tự Nhiên

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

### 2. Thêm Hướng Dẫn Trong Test

```python
@weblens_test(
    name="complex_flow_test",
    description="Go to example.com"
)
async def test_complex_flow(browser):
    # Thực hiện mô tả ban đầu
    await browser.run()
    
    # Thêm các bước bổ sung
    result1 = await browser.execute_natural_language(
        "Click on the Products link in the navigation menu"
    )
    
    result2 = await browser.execute_natural_language(
        "Sort products by price and select the most expensive item"
    )
    
    result3 = await browser.execute_natural_language(
        "Add the product to cart and proceed to checkout"
    )
    
    # Kiểm tra kết quả
    assert "checkout page" in result3
```

### 3. Kết Hợp Với Assertions

```python
@weblens_test(
    name="search_test",
    description="Go to example.com and search for 'WebLens framework'"
)
async def test_search(browser):
    # Thực hiện tìm kiếm
    result = await browser.run()
    
    # Kiểm tra kết quả tìm kiếm
    search_results = await browser.execute_natural_language(
        "Count the number of search results and return the count"
    )
    
    # Convert kết quả từ chuỗi sang số
    count = int(''.join(filter(str.isdigit, search_results)))
    assert count > 0
```

## 🧪 Ví Dụ Test Đăng Nhập

WebLens cung cấp một ví dụ đầy đủ về cách test chức năng đăng nhập cho một trang web thực tế:

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
    """Test đăng nhập thành công với thông tin hợp lệ"""
    result = await browser.run()
    assert "login was successful" in result.lower()
```

Để chạy ví dụ đầy đủ về test đăng nhập, sử dụng lệnh sau:

```bash
python examples/login_test_example.py
```

Ví dụ này bao gồm các test cases sau:

- Đăng nhập thành công với thông tin hợp lệ
- Đăng nhập với username không hợp lệ
- Đăng nhập với password không hợp lệ
- Đăng nhập thành công và sau đó đăng xuất

Xem mã nguồn đầy đủ tại `examples/login_test_example.py`

## 📚 Tài Liệu Bổ Sung

Ngoài hướng dẫn này, WebLens còn cung cấp các tài liệu chuyên sâu khác:

- [Comprehensive Natural Language Guide](./docs/natural_language_guide_full.md) - Hướng dẫn đầy đủ về cách tiếp cận ngôn ngữ tự nhiên
- [Natural Language Approach](./docs/natural_language_approach.md) - Hướng dẫn chi tiết về cách sử dụng ngôn ngữ tự nhiên trong testing
- [Login Testing Guide](./docs/login_testing_guide.md) - Hướng dẫn kiểm tra chức năng đăng nhập với WebLens
- [Browser Use Cloud API](./docs/browser_use_cloud_api.md) - Tài liệu về API cloud được sử dụng trong WebLens

## 📝 Những Thay Đổi Gần Đây

WebLens đã chuyển sang sử dụng hoàn toàn cách tiếp cận ngôn ngữ tự nhiên thông qua API browser-use. Để biết chi tiết về những thay đổi này, vui lòng tham khảo [tài liệu thay đổi](./docs/THAY_DOI.md).
