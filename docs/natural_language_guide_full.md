# Tổng Quan về Cách Tiếp Cận Ngôn Ngữ Tự Nhiên trong WebLens

## Giới Thiệu

WebLens đã chuyển sang một mô hình hoàn toàn mới sử dụng ngôn ngữ tự nhiên để điều khiển trình duyệt. Tài liệu này cung cấp tổng quan đầy đủ về cách tiếp cận này và hướng dẫn thực hành chi tiết.

## Lý Do Chuyển Đổi

Trong các framework testing truyền thống, việc tương tác với trình duyệt thường dựa vào các selector để tìm và tương tác với các phần tử trên trang web:

```python
# Cách cũ (không còn được WebLens hỗ trợ)
await browser.go_to("https://example.com")
await browser.click("button.login")
await browser.fill_input("#username", "test_user")
await browser.fill_input("#password", "password123")
await browser.click("button[type='submit']")
```

Cách tiếp cận này có nhiều nhược điểm:
- Phụ thuộc vào cấu trúc HTML/CSS cụ thể
- Dễ bị lỗi khi UI thay đổi
- Yêu cầu kiến thức kỹ thuật về CSS selectors và DOM
- Khó bảo trì và cập nhật

Với cách tiếp cận ngôn ngữ tự nhiên mới, toàn bộ test case trên có thể được viết lại một cách đơn giản:

```python
@weblens_test(
    name="login_test",
    description=(
        "Go to example.com, click the login button, enter 'test_user' as username, "
        "enter 'password123' as password, click submit, and verify login is successful"
    )
)
async def test_login(browser):
    result = await browser.run()
    assert "login is successful" in result.lower()
```

## Các Phương Thức Chính

WebLens hiện chỉ sử dụng hai phương thức chính cho tất cả các tương tác với trình duyệt:

1. **`browser.run()`**: Thực thi mô tả nhiệm vụ được cung cấp trong decorator `@weblens_test`.
2. **`browser.execute_natural_language(instructions)`**: Thực thi hướng dẫn bổ sung được cung cấp dưới dạng chuỗi.

## Ví Dụ Thực Tế

### 1. Test Đăng Nhập Cơ Bản

```python
@weblens_test(
    name="login_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "enter username 'student' and password 'Password123', "
        "click the Submit button, and verify that login was successful"
    ),
    tags=["login", "positive"]
)
async def test_successful_login(browser):
    result = await browser.run()
    assert "login was successful" in result.lower()
```

### 2. Test Đăng Nhập Thất Bại

```python
@weblens_test(
    name="invalid_username_test",
    description=(
        "Go to https://practicetestautomation.com/practice-test-login/, "
        "enter incorrect username 'incorrectUser' and password 'Password123', "
        "click the Submit button, and verify that an error message is displayed"
    ),
    tags=["login", "negative"]
)
async def test_invalid_username(browser):
    result = await browser.run()
    assert "error message is displayed" in result.lower()
```

### 3. Test Nhiều Bước

```python
@weblens_test(
    name="multi_step_test",
    description="Go to example.com"
)
async def test_multi_step(browser):
    # Thực hiện bước đầu tiên
    await browser.run()
    
    # Thực hiện các bước bổ sung
    result1 = await browser.execute_natural_language("Click on the About link")
    result2 = await browser.execute_natural_language("Verify the About page contains company information")
    
    assert "company information" in result2.lower()
```

## Hướng Dẫn Viết Mô Tả Hiệu Quả

Để đảm bảo browser-use API hiểu đúng ý định của bạn, hãy tuân thủ các nguyên tắc sau khi viết mô tả:

1. **Rõ ràng và Cụ thể**: Mô tả chính xác từng hành động cần thực hiện.
   ```python
   "Go to example.com, find the login button in the top right corner, and click on it"
   ```

2. **Sử dụng Cụm Động Từ Mệnh Lệnh**: Sử dụng các động từ mệnh lệnh như "go to", "click", "enter", "verify".
   ```python
   "Enter 'testuser@example.com' in the email field, enter 'password123' in the password field"
   ```

3. **Chỉ Định Giá Trị Cụ Thể**: Luôn đặt các giá trị cần nhập trong dấu nháy đơn.
   ```python
   "Enter 'John Doe' in the name field and '1990-01-01' in the date of birth field"
   ```

4. **Mô Tả Phần Tử UI**: Mô tả phần tử UI theo nội dung thay vì các chi tiết kỹ thuật.
   ```python
   "Click on the button labeled 'Submit Application'"
   ```

5. **Bao Gồm Các Bước Xác Thực**: Cuối cùng, thêm bước để xác thực kết quả mong đợi.
   ```python
   "Verify that a success message appears saying 'Your application has been submitted'"
   ```

## Trích Xuất và Xử Lý Dữ Liệu

Trong nhiều trường hợp, bạn sẽ cần trích xuất dữ liệu từ kết quả của một tác vụ ngôn ngữ tự nhiên để thực hiện các kiểm tra phức tạp hơn.

```python
import re

@weblens_test(
    name="price_check_test",
    description="Go to the product page for item XYZ and find its current price"
)
async def test_price(browser):
    result = await browser.run()
    
    # Trích xuất giá từ kết quả bằng regex
    price_match = re.search(r'\$([0-9]+\.[0-9]+)', result)
    if price_match:
        price = float(price_match.group(1))
        assert 10.0 <= price <= 20.0, f"Giá ${price} nằm ngoài phạm vi mong đợi"
```

## So Sánh và Phân Tích Dữ Liệu

Ngôn ngữ tự nhiên cũng có thể được sử dụng để thu thập thông tin so sánh:

```python
@weblens_test(
    name="product_comparison_test",
    description="Go to the comparison page and get the prices of Product A and Product B"
)
async def test_product_comparison(browser):
    # Get prices
    await browser.run()
    
    # Get specific details about each product
    product_a_info = await browser.execute_natural_language(
        "Find Product A and return its price, rating, and available colors"
    )
    
    product_b_info = await browser.execute_natural_language(
        "Find Product B and return its price, rating, and available colors"
    )
    
    # Make assertions based on the information
    assert "price" in product_a_info.lower() and "price" in product_b_info.lower()
```

## Kết Luận

Cách tiếp cận ngôn ngữ tự nhiên giúp WebLens trở nên mạnh mẽ hơn, dễ sử dụng hơn và ít bị ảnh hưởng bởi các thay đổi UI. Bằng cách loại bỏ sự phụ thuộc vào các selector, các test trở nên linh hoạt và dễ bảo trì hơn nhiều so với các framework testing truyền thống.

Để xem các ví dụ thực tế, hãy tham khảo các tệp mẫu trong thư mục `examples/`:

- `natural_language_test.py`: Các ví dụ cơ bản
- `advanced_natural_assertions.py`: Các ví dụ với assertions nâng cao
- `login_test_example.py`: Ví dụ kiểm tra đăng nhập
