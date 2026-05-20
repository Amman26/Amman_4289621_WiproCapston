import pytest

from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger

logger = setup_logger()
test_data = read_csv_data("data/product_validation_data.csv")


@pytest.mark.order(4)
@pytest.mark.parametrize("data", test_data)
def test_add_medicine_to_cart(driver, data):
    logger.info("Starting Add to Cart and Checkout Test")

    # Initialize all required Page Objects
    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    medicine_name = data["product_name"]

    logger.info("Clicking Buy Medicines")
    search.click_buy_medicines()

    logger.info(f"Searching medicine: {medicine_name}")
    search.search_medicine(medicine_name)

    logger.info("Adding medicine to cart from the search grid")
    product.add_first_product_to_cart()

    # --- TRANSITION TO CART PAGE ---

    logger.info("Opening cart")
    cart.open_cart()

    logger.info("Fetching product name from cart")
    cart_product_name = cart.get_cart_product_name()

    logger.info(f"Product found in cart: {cart_product_name}")

    # Normalize both strings by removing spaces and hyphens to prevent false failures
    normalized_expected = medicine_name.lower().replace(" ", "").replace("-", "")
    normalized_actual = cart_product_name.lower().replace(" ", "").replace("-", "")

    # Assert using the normalized strings
    assert normalized_expected in normalized_actual, \
        f"Correct product was not added to cart! Expected '{medicine_name}' but found '{cart_product_name}'."

    # --- PROCEED TO PAYMENT ---
    logger.info("Clicking Proceed to Payment")
    cart.proceed_to_payment()

    logger.info("Checkout process initiated successfully")