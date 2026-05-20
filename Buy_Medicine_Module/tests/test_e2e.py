import time
import pytest


from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger

logger = setup_logger()

# Load CSV test data dynamically
login_data = read_csv_data("data/login_data.csv")
medicine_data = read_csv_data("data/medicine_search_data.csv")

# Extract the first row of data to drive the E2E flow
E2E_MOBILE = login_data[0]["mobile"]
E2E_PRODUCT = medicine_data[0]["search_text"]


@pytest.mark.e2e
def test_e2e_user_journey(driver):
    logger.info("Starting End-to-End User Journey Test")

    # Initialize Page Objects
    login = LoginPage(driver)
    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    # --- 1. LAUNCH ---
    assert "Apollo" in driver.title
    logger.info("Apollo 24/7 website launched successfully")

    # --- 2. LOGIN ---
    logger.info("Initiating Login sequence")
    login.click_login_button()

    logger.info(f"Entering Mobile Number from CSV: {E2E_MOBILE}")
    login.enter_mobile_number(E2E_MOBILE)
    login.click_continue_button()

    print(f"\nPlease manually enter OTP for {E2E_MOBILE}...")
    time.sleep(20)  # Waiting for manual OTP

    login.click_verify_button()
    logger.info(f"Login completed successfully for {E2E_MOBILE}")

    # --- 3. SEARCH ---
    logger.info("Checking for and closing promotional popup")
    search.close_promotional_popup()

    logger.info("Navigating to Buy Medicines")
    search.click_buy_medicines()

    logger.info(f"Searching for medicine from CSV: {E2E_PRODUCT}")
    search.search_medicine(E2E_PRODUCT)

    assert search.verify_search_results(), "Search results did not load correctly."

    # --- 4. ADD TO CART & VALIDATE ---
    logger.info("Adding first product from search grid to cart")
    product.add_first_product_to_cart()

    logger.info("Opening cart to verify product")
    cart.open_cart()
    cart_product_name = cart.get_cart_product_name()

    normalized_expected = E2E_PRODUCT.lower().replace(" ", "").replace("-", "")
    normalized_actual = cart_product_name.lower().replace(" ", "").replace("-", "")

    assert normalized_expected in normalized_actual, \
        f"Cart mismatch! Expected '{E2E_PRODUCT}' but found '{cart_product_name}'."

    # --- 5. CHECKOUT ---
    logger.info("Proceeding to payment")
    cart.proceed_to_payment()
    logger.info("E2E Checkout process completed successfully")
