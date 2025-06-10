# Natural Language Testing with WebLens

WebLens has been updated to use the browser-use API directly with natural language instructions, which aligns with the original design of browser-use.

## What is browser-use?

browser-use is a cloud-based browser automation service that allows you to control web browsers using natural language instructions. Instead of writing code with explicit browser commands, you can describe what you want in plain English.

## The New Natural Language Approach

Instead of using separate methods like `go_to()`, `fill_input()`, or `click()`, WebLens now supports direct natural language instructions:

```python
@weblens_test(
    name="natural_language_test",
    description="Go to example.com, check the page title, and take a screenshot",
    tags=["demo"]
)
async def test_with_natural_language(browser):
    # Execute the task with natural language
    result = await browser.run()
    
    # Add additional instructions if needed
    additional_result = await browser.execute_natural_language(
        "Go back to the homepage and check if the logo is present"
    )
```

**Advantages:**
- No need for complex programmatic APIs
- Tests are written in plain English
- Easy for non-technical users to understand and create tests
- Simpler maintenance
- Better alignment with browser-use's intended usage

**Example:** See `examples/natural_language_test.py` for implementation

### Benefits of the Natural Language Approach

1. **Simplifies Test Cases**: Writing test cases in natural language makes creating tests much easier.
2. **Better Readability**: Natural language test cases are easier to read and understand for both technical and non-technical stakeholders.
3. **Flexibility**: Natural language instructions allow executing complex operations in a single statement.
4. **Leverages AI**: Takes full advantage of browser-use's natural language understanding capabilities.

## Advanced Features

### 1. Data Extraction and Assertions

WebLens now provides helper methods to extract data from natural language test results:

```python
@weblens_test(
    name="product_count",
    description="Go to the demo store and count how many products are available",
    tags=["inventory"]
)
async def test_product_count(browser):
    await browser.run()
    
    # Extract specific data using natural language
    product_count = await browser.get_element_count("products on the page")
    assert product_count > 5, "Should have more than 5 products"
    
    # Check conditions using natural language
    has_discount = await browser.check_condition("there are products with discount badges")
    if has_discount:
        print("Found products with discounts")
```

### 2. Creating Tests via Command Line

You can easily create natural language test templates using the CLI:

```bash
# Interactive mode
weblens generate interactive

# Direct mode
weblens generate template --name "Login Test" \
  --description "Go to example.com/login and test the login form" \
  --output login_test.py
```

## Backward Compatibility

WebLens maintains backward compatibility with the previous API. The following methods still work but now use natural language instructions internally:

- `go_to(url)`
- `click(selector)`
- `fill_input(selector, value)`
- `get_text(selector)`
- `wait_for_element(selector)`

For optimal results, we recommend using direct natural language instructions via the `run()` method.

## Best Practices

1. **Be specific in your instructions**: Provide clear context and expected outcomes
2. **Use natural sentences**: Write instructions as you would explain them to a person
3. **Break complex tasks**: For very complex scenarios, use multiple `execute_natural_language` calls
4. **Validate results**: Use assertions to ensure your test conditions are met
5. **Leverage data extraction**: Use the helper methods to extract specific data from results

## Get Started

To try the new natural language approach:

```bash
python examples/natural_language_test.py
```

To try the advanced assertions with natural language:

```bash
python examples/advanced_assertions_test.py
```
