# Sử dụng WebLens với Hướng Dẫn Ngôn Ngữ Tự Nhiên

WebLens sử dụng API browser-use với hướng dẫn ngôn ngữ tự nhiên, cho phép tạo các test case mạnh mẽ mà không cần sử dụng các selector.

## Cách Tiếp Cận Ngôn Ngữ Tự Nhiên

WebLens cung cấp hai phương thức chính để làm việc với ngôn ngữ tự nhiên:

```python
@weblens_test(
    name="natural_language_test",
    description="Test using natural language instructions",
    tags=["demo"]
)
async def test_with_natural_language(browser):
    # Thực thi tác vụ bằng ngôn ngữ tự nhiên từ mô tả của test
    result = await browser.run()
    
    # Thêm hướng dẫn bổ sung
    additional_result = await browser.execute_natural_language(
        "Go back to the homepage and check if the logo is present"
    )
```

## Lợi Ích Của Cách Tiếp Cận Ngôn Ngữ Tự Nhiên

1. **Đơn giản hóa các test case**: Viết test case bằng ngôn ngữ tự nhiên giúp đơn giản hóa quá trình tạo test.
2. **Dễ đọc hơn**: Các test case bằng ngôn ngữ tự nhiên dễ đọc và hiểu hơn cho cả người kỹ thuật và không kỹ thuật.
3. **Linh hoạt**: Hướng dẫn bằng ngôn ngữ tự nhiên cho phép thực hiện nhiều thao tác phức tạp trong một câu lệnh duy nhất.
4. **Tận dụng tối đa AI**: Tận dụng khả năng hiểu ngôn ngữ tự nhiên của browser-use.
5. **Thích ứng với thay đổi UI**: Test không bị vỡ khi UI thay đổi vì không phụ thuộc vào các selector cụ thể.

## Hướng Dẫn Sử Dụng

### 1. Tạo Test Case Đơn Giản

```python
@weblens_test(
    name="example_test",
    description="Go to example.com and check the title",
    tags=["demo"]
)
async def test_example(browser):
    result = await browser.run()
    assert result, "Task should return some result"
```

### 2. Thực Hiện Nhiều Hành Động

Bạn có thể mô tả nhiều hành động trong một hướng dẫn duy nhất:

```python
@weblens_test(
    name="multi_step_test",
    description="Go to an e-commerce site, search for a product, add it to cart, and verify the cart",
    tags=["e-commerce"]
)
async def test_ecommerce(browser):
    result = await browser.run()
    assert "added to cart" in result.lower(), "Product should be added to cart"
```

### 3. Thực Hiện Các Hướng Dẫn Bổ Sung

```python
@weblens_test(
    name="multi_instruction_test",
    description="Go to example.com",
    tags=["demo"]
)
async def test_multiple_instructions(browser):
    # Thực hiện tác vụ ban đầu
    await browser.run()
    
    # Thêm hướng dẫn bổ sung
    result1 = await browser.execute_natural_language("Click on the About link and tell me the company's founding year")
    result2 = await browser.execute_natural_language("Go back to the homepage and check if there's a contact form")
```

## Ví Dụ Hoàn Chỉnh

Xem tệp ví dụ đầy đủ tại `examples/natural_language_test.py`:

```bash
python examples/natural_language_test.py
```

## Best Practices Khi Viết Hướng Dẫn Ngôn Ngữ Tự Nhiên

1. **Cụ thể và rõ ràng**: "Go to example.com and check if the page title contains 'Example Domain'"
2. **Mô tả từng bước**: "Navigate to the login page, enter username 'test@example.com' and password 'password123', then click the login button"
3. **Chỉ định các yếu tố quan trọng**: "Find the button with text 'Submit' and click it"
4. **Xác định thời gian chờ khi cần**: "Wait for the loading spinner to disappear, then check the results"
5. **Yêu cầu trích xuất dữ liệu**: "Extract the price of the first product and check if it's less than $100"

## Các Phương Thức API

WebLens hiện tại sử dụng chỉ hai phương thức chính cho tất cả các tương tác với trình duyệt:

1. **`run()`**: Thực thi hướng dẫn ngôn ngữ tự nhiên từ mô tả của test
2. **`execute_natural_language(instructions)`**: Thực thi hướng dẫn ngôn ngữ tự nhiên được chỉ định
3. **`take_screenshot(path)`**: Chụp ảnh màn hình hiện tại của trình duyệt

## Kết Luận

Cách tiếp cận mới này cho phép WebLens tận dụng đầy đủ khả năng hiểu ngôn ngữ tự nhiên của browser-use, giúp việc viết và bảo trì test case trở nên đơn giản và hiệu quả hơn. Bằng cách loại bỏ sự phụ thuộc vào các selector, các test trở nên linh hoạt hơn và ít bị vỡ hơn khi giao diện thay đổi.
