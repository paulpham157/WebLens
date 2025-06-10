# Kiểm Tra Chức Năng Đăng Nhập Với WebLens

Tài liệu này hướng dẫn cách sử dụng WebLens để kiểm tra chức năng đăng nhập của một trang web, sử dụng ngôn ngữ tự nhiên thay vì các phương thức selector-based truyền thống.

## Khái Quát

Test chức năng đăng nhập là một trong những test cơ bản nhất khi kiểm tra một trang web. Với WebLens, bạn có thể viết các test case đơn giản bằng ngôn ngữ tự nhiên, giúp giảm thời gian phát triển và bảo trì test.

## Các Test Case Điển Hình

### 1. Đăng nhập thành công

```python
@weblens_test(
    name="successful_login_test",
    description=(
        "Go to https://example.com/login, "
        "enter username 'validuser' and password 'validpass', "
        "click the login button, and verify that login was successful"
    )
)
async def test_successful_login(browser):
    result = await browser.run()
    assert "login was successful" in result.lower()
```

### 2. Đăng nhập với thông tin không hợp lệ

```python
@weblens_test(
    name="invalid_credentials_test",
    description=(
        "Go to https://example.com/login, "
        "enter username 'invaliduser' and password 'invalidpass', "
        "click the login button, and check for error message"
    )
)
async def test_invalid_credentials(browser):
    result = await browser.run()
    assert "invalid username or password" in result.lower()
```

### 3. Kiểm tra chức năng đăng xuất

```python
@weblens_test(
    name="logout_test",
    description=(
        "Go to https://example.com/login, "
        "login with valid credentials, "
        "then click logout button and verify user is logged out"
    )
)
async def test_logout(browser):
    result = await browser.run()
    assert "logged out successfully" in result.lower()
```

### 4. Kiểm tra nhớ đăng nhập (Remember Me)

```python
@weblens_test(
    name="remember_me_test",
    description=(
        "Go to https://example.com/login, "
        "enter valid credentials, check the remember me checkbox, "
        "log in, then close the browser, reopen it, "
        "navigate to the site again and verify user is still logged in"
    )
)
async def test_remember_me(browser):
    result = await browser.run()
    assert "still logged in" in result.lower()
```

## Lợi Ích Của Cách Tiếp Cận Ngôn Ngữ Tự Nhiên

1. **Dễ đọc và hiểu**: Các test case được viết bằng ngôn ngữ tự nhiên dễ dàng cho mọi người đọc và hiểu, kể cả những người không có kiến thức kỹ thuật.

2. **Ít phụ thuộc vào cấu trúc HTML**: Không cần phải tìm kiếm và sử dụng các CSS selector hoặc XPath, giảm thiểu việc phải cập nhật test khi UI thay đổi.

3. **Tập trung vào hành vi**: Test tập trung vào hành vi của ứng dụng thay vì chi tiết kỹ thuật.

4. **Dễ bảo trì**: Khi UI thay đổi, các test không cần phải được cập nhật nhiều vì không phụ thuộc vào các selector cụ thể.

## Ví Dụ Thực Tế

Xem ví dụ đầy đủ về test đăng nhập tại `examples/login_test_example.py`.
