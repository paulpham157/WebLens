# WebLens: Tích hợp API browser-use với hướng dẫn ngôn ngữ tự nhiên

## Tổng quan về thay đổi

WebLens đã được cập nhật để tận dụng đầy đủ khả năng xử lý ngôn ngữ tự nhiên của browser-use API. Thay vì sử dụng các phương thức lập trình tường minh (như `go_to()`, `click()`, `fill_input()`), framework giờ đây hỗ trợ việc gửi hướng dẫn bằng ngôn ngữ tự nhiên trực tiếp đến API browser-use.

## Kiến trúc mới

### BrowserManager

`BrowserManager` giờ đây tạo ra các đối tượng `Agent` có khả năng:
- Xử lý hướng dẫn ngôn ngữ tự nhiên
- Giao tiếp trực tiếp với browser-use REST API
- Theo dõi và báo cáo các bước thực thi
- Lấy kết quả đầu ra và ảnh chụp màn hình

### Agent class

Lớp `Agent` đã được cài đặt lại để:
- Khởi tạo với một mô tả nhiệm vụ bằng ngôn ngữ tự nhiên
- Tạo và theo dõi các tác vụ browser-use qua REST API
- Cung cấp phương thức `execute_natural_language()` để thực hiện các hướng dẫn bổ sung
- Duy trì các phương thức tương thích ngược cho các test hiện có (như `go_to()`, `click()`)

## Cách sử dụng

### 1. Sử dụng WebLens với hướng dẫn ngôn ngữ tự nhiên

```python
@weblens_test(
    name="search_test",
    description="Go to google.com, search for WebLens framework, and check the results"
)
async def test_search(browser):
    # Thực thi mô tả nhiệm vụ được cung cấp trong decorator
    result = await browser.run()
    assert "WebLens" in result
```

### 2. Thực hiện các hướng dẫn bổ sung

```python
@weblens_test(
    name="multi_step_test",
    description="Go to example.com"
)
async def test_multi_step(browser):
    # Thực hiện mô tả ban đầu
    await browser.run()
    
    # Thêm hướng dẫn bổ sung
    result = await browser.execute_natural_language(
        "Click on the About link and check if there is contact information"
    )
```

### 3. Tương thích ngược với code hiện có

```python
@weblens_test(
    name="legacy_test",
    description="Test with legacy API"
)
async def test_legacy(browser):
    # Các phương thức này vẫn hoạt động nhưng được chuyển đổi
    # thành hướng dẫn ngôn ngữ tự nhiên trong nội bộ
    await browser.go_to("https://example.com")
    title = await browser.get_title()
    assert "Example" in title
```

## Ví dụ mới

Trong thư mục `/examples` có các ví dụ minh họa phương pháp mới:

1. `natural_language_test.py` - Ví dụ cơ bản với hướng dẫn ngôn ngữ tự nhiên
2. `advanced_natural_language_test.py` - Ví dụ nâng cao với nhiều tình huống test
3. `direct_browser_use.py` - Ví dụ sử dụng API browser-use trực tiếp không qua WebLens

## So sánh cách tiếp cận

### Cách cũ (Programmatic API):
```python
# Nhiều dòng code cho một tác vụ đơn giản
await browser.go_to("https://example.com")
await browser.wait_for_element("h1")
title = await browser.get_title()
await browser.click("a[href='/about']")
await browser.wait_for_element("h2")
```

### Cách mới (Natural Language):
```python
# Một dòng đơn giản với hướng dẫn ngôn ngữ tự nhiên
await browser.execute_natural_language(
    "Go to example.com, wait for the page to load, verify the title, "
    "click on the About link, and wait for the heading to appear"
)
```

## Kết luận

Phương pháp mới này cho phép WebLens tận dụng đầy đủ khả năng hiểu ngôn ngữ tự nhiên của browser-use, giúp việc viết và bảo trì test case trở nên đơn giản và hiệu quả hơn. Đồng thời, WebLens vẫn duy trì khả năng tương thích với các test hiện có.

## Tài liệu tham khảo

- [Browser-use Cloud API Documentation](docs/browser_use_cloud_api.md)
- [Natural Language Testing Approach](docs/natural_language_approach.md)
- [Examples](examples/)
