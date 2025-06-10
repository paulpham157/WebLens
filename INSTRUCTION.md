# WebLens - Hướng Dẫn Sử Dụng

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

# Chạy tests với browsers cụ thể
python weblens_cli.py run examples/basic_tests.py --browsers chrome firefox

# Chạy tests với profiles cụ thể
python weblens_cli.py run examples/basic_tests.py --profiles desktop_chrome mobile_chrome

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
    description="Test basic navigation",
    browsers=["chrome", "firefox"],
    profiles=["desktop_chrome", "mobile_chrome"],
    tags=["smoke", "navigation"]
)
async def test_navigation(browser):
    # Navigate to website
    await browser.go_to("https://example.com")
    
    # Wait for element
    await browser.wait_for_element("h1", timeout=10)
    
    # Get page title
    title = await browser.get_title()
    assert "Example" in title
    
    # Take screenshot
    await browser.take_screenshot()

# Run tests
async def main():
    runner = TestRunner()
    
    # Register test
    runner.register_test(
        name="example_test",
        description="Test basic navigation",
        test_function=test_navigation,
        browsers=["chrome"],
        profiles=["desktop_chrome"]
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
    description="Test responsive design",
    browsers=["chrome"],
    profiles=["desktop_chrome", "tablet", "mobile_chrome"],
    tags=["responsive", "ui"]
)
async def test_responsive_design(browser):
    await browser.go_to("https://example.com")
    # Test sẽ chạy trên 3 profiles khác nhau
```

### Error Handling & Retry

```python
from weblens.utils.helpers import retry_async

@retry_async(max_retries=3, delay=1.0)
async def flaky_test(browser):
    # Test sẽ được retry tối đa 3 lần nếu fail
    await browser.go_to("https://unstable-site.com")
```

### Performance Testing

```python
from weblens.utils.helpers import timing

@timing
async def performance_test(browser):
    # Execution time sẽ được log tự động
    await browser.go_to("https://example.com")
```

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
