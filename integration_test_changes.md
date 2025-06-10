# Thay Đổi Cần Thiết Cho Test Integration

Sau khi loại bỏ các phương thức selector-based không còn sử dụng, các test integration cần được cập nhật để sử dụng cách tiếp cận ngôn ngữ tự nhiên. Dưới đây là danh sách các thay đổi cần thực hiện:

## File: tests/integration/test_integration.py

### 1. Phương thức `test_browser_launch_and_navigation`

Thay:
```python
# Launch browser
browser = await manager.launch_browser("chrome")
assert browser is not None

# Navigate to a page
await browser.go_to("https://example.com")

# Get page title
title = await browser.get_title()
assert "Example" in title
```

Bằng:
```python
# Create agent
agent = await manager.create_agent("Go to example.com and check the title", "test_agent")
assert agent is not None

# Run natural language task
result = await agent.run()
assert result
```

### 2. Phương thức `test_profile_based_testing`

Thay:
```python
# Launch browser with profile
browser = await manager.launch_browser("chrome", profile_name)
assert browser is not None

# Test navigation
await browser.go_to("https://httpbin.org/user-agent")

# Close browser
await manager.close_browser("chrome", profile_name)
```

Bằng:
```python
# Create agent with task
agent = await manager.create_agent(f"Go to https://httpbin.org/user-agent", "test_agent")
assert agent is not None

# Run natural language task
result = await agent.run()
assert result
```

### 3. Phương thức `test_full_test_execution`

Cập nhật để sử dụng cách tiếp cận ngôn ngữ tự nhiên thông qua TestRunner và các weblens_test với natural language description.

### 4. Phương thức `test_error_handling_and_screenshots`

Thay đổi để sử dụng cách tiếp cận ngôn ngữ tự nhiên cho việc xử lý lỗi và chụp ảnh màn hình.

### 5. Phương thức `test_multiple_browser_sessions`

Sử dụng nhiều agent với các task khác nhau thay vì nhiều browser.

## File: tests/conftest.py

Cập nhật `mock_browser` fixture để mô phỏng các phương thức dựa trên ngôn ngữ tự nhiên:
- `run()`
- `execute_natural_language()`
- `take_screenshot()`

## Kế Hoạch

1. Tạo một branch riêng để cập nhật các test
2. Cập nhật các test integration theo danh sách trên
3. Kiểm tra tất cả các test để đảm bảo chúng vẫn hoạt động đúng
4. Merge các thay đổi vào branch chính

Lưu ý: Một số test có thể cần được vô hiệu hóa tạm thời cho đến khi API mới được triển khai đầy đủ.
