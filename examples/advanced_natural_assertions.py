#!/usr/bin/env python3
"""
WebLens: Natural Language Testing với Assertions Phức Tạp
--------------------------------------------------------

Ví dụ này minh họa cách sử dụng ngôn ngữ tự nhiên kết hợp với assertions 
để kiểm tra các chức năng phức tạp hơn trên trang web
"""
import asyncio
import sys
import json
from pathlib import Path
import re

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from weblens.core.test_runner import weblens_test, TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="product_price_assertion",
    description=(
        "Go to https://www.saucedemo.com/, "
        "login with username 'standard_user' and password 'secret_sauce', "
        "check the price of the 'Sauce Labs Backpack', "
        "and return the price value"
    ),
    tags=["ecommerce", "price-checking"]
)
async def test_product_price(browser):
    """Kiểm tra và xác thực giá sản phẩm"""
    result = await browser.run()
    
    # Tìm giá trong kết quả bằng biểu thức chính quy
    price_match = re.search(r'\$([0-9]+\.[0-9]+)', result)
    if price_match:
        price = float(price_match.group(1))
        logger.info(f"Sản phẩm có giá: ${price}")
        
        # Kiểm tra giá có hợp lý không
        assert 20 <= price <= 50, f"Giá ${price} nằm ngoài khoảng kỳ vọng $20-$50"
        return price
    else:
        assert False, "Không tìm thấy thông tin giá trong kết quả"


@weblens_test(
    name="product_sorting_test",
    description=(
        "Go to https://www.saucedemo.com/, "
        "login with username 'standard_user' and password 'secret_sauce', "
        "sort products by price low to high, "
        "and check if the first product's price is lower than the last product"
    ),
    tags=["ecommerce", "sorting"]
)
async def test_product_sorting(browser):
    """Kiểm tra chức năng sắp xếp sản phẩm theo giá"""
    # Thực hiện sắp xếp
    result = await browser.run()
    
    # Lấy giá sản phẩm đầu tiên
    first_product = await browser.execute_natural_language(
        "Get the name and price of the first product in the sorted list"
    )
    logger.info(f"Sản phẩm đầu tiên: {first_product}")
    
    # Lấy giá sản phẩm cuối cùng
    last_product = await browser.execute_natural_language(
        "Get the name and price of the last product in the sorted list"
    )
    logger.info(f"Sản phẩm cuối cùng: {last_product}")
    
    # Trích xuất giá từ kết quả
    first_price = extract_price(first_product)
    last_price = extract_price(last_product)
    
    # Kiểm tra sắp xếp
    assert first_price < last_price, "Sản phẩm không được sắp xếp đúng theo giá tăng dần"


@weblens_test(
    name="shopping_cart_test",
    description=(
        "Go to https://www.saucedemo.com/, "
        "login with username 'standard_user' and password 'secret_sauce', "
        "add 'Sauce Labs Backpack' to cart, "
        "navigate to the cart, "
        "check that the item is in the cart, "
        "and verify the total price is correct"
    ),
    tags=["ecommerce", "cart"]
)
async def test_shopping_cart(browser):
    """Kiểm tra chức năng giỏ hàng"""
    # Thực hiện các bước chính
    result = await browser.run()
    logger.info(f"Kết quả: {result}")
    
    # Kiểm tra sản phẩm có trong giỏ hàng không
    assert "Sauce Labs Backpack" in result, "Sản phẩm không có trong giỏ hàng"
    
    # Kiểm tra tổng giá
    if "total" in result.lower():
        total_match = re.search(r'total.*\$([0-9]+\.[0-9]+)', result, re.IGNORECASE)
        if total_match:
            total = float(total_match.group(1))
            logger.info(f"Tổng giá: ${total}")
            assert total > 0, "Tổng giá không hợp lệ"
        else:
            assert False, "Không tìm thấy thông tin tổng giá"


def extract_price(text):
    """Trích xuất giá từ một chuỗi văn bản"""
    price_match = re.search(r'\$([0-9]+\.[0-9]+)', text)
    if price_match:
        return float(price_match.group(1))
    return 0


async def main():
    """Hàm main để chạy tất cả các tests"""
    logger.info("Starting advanced tests with natural language assertions...")
    
    runner = TestRunner()
    
    # Đăng ký các test functions
    for test_func in [test_product_price, test_product_sorting, test_shopping_cart]:
        info = test_func._weblens_test_info
        runner.register_test(
            name=info["name"],
            description=info["description"],
            test_function=test_func,
            tags=info["tags"]
        )
    
    try:
        # Chạy tests một cách tuần tự
        results = await runner.run_tests(parallel=False)
        
        # In tóm tắt
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
        if failed > 0:
            for result in results:
                if result.status == "failed":
                    logger.error(f"Failed test: {result.name}")
                    logger.error(f"Error: {result.error_message}")
    
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
