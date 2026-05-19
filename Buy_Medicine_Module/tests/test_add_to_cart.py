import pytest

from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger

logger = setup_logger()

test_data = read_csv_data(
    "data/product_validation_data.csv"
)

@pytest.mark.order(4)
@pytest.mark.parametrize("data", test_data)
def test_add_medicine_to_cart(driver, data):
    logger.info("Starting Add to Cart Test")

    search = SearchMedicinePage(driver)
    product = ProductPage(driver)

    medicine_name = data["product_name"]

    # ADD THIS STEP: Navigate to the Buy Medicines section first
    logger.info("Clicking Buy Medicines")
    search.click_buy_medicines()

    logger.info(f"Searching medicine: {medicine_name}")
    search.search_medicine(medicine_name)

    logger.info("Adding medicine to cart from the search grid")
    product.add_first_product_to_cart()

    logger.info("Verifying cart update")
    assert product.verify_cart_updated(), "Cart count was not updated successfully!"

    logger.info("Add to Cart Test Passed Successfully")