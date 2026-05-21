import time
import pytest
import allure
from allure_commons.types import AttachmentType

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

# Extract the mobile number
E2E_MOBILE = login_data[0]["mobile"]


@allure.epic("Apollo 24/7 E2E Automation")
@allure.feature("End-to-End Journey")
@allure.story("Multi-Product Purchase Flow")
@allure.title("E2E: Login, Add Multiple Items, and Checkout")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.e2e
def test_e2e_multiple_items_journey(driver):
    logger.info("Starting Multi-Item End-to-End Test")

    # Initialize Page Objects
    login = LoginPage(driver)
    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    with allure.step("1. Launch Apollo 24/7 Website"):
        assert "Apollo" in driver.title
        logger.info("Apollo 24/7 website launched successfully")
        allure.attach(driver.get_screenshot_as_png(), name="1_Launch", attachment_type=AttachmentType.PNG)

    with allure.step(f"2. Login with mobile number: {E2E_MOBILE}"):
        logger.info("Initiating Login sequence")
        login.click_login_button()
        login.enter_mobile_number(E2E_MOBILE)
        login.click_continue_button()

        print(f"\nPlease manually enter OTP for {E2E_MOBILE}...")
        time.sleep(20)  # Waiting for manual OTP

        login.click_verify_button()
        logger.info("Login completed successfully")
        allure.attach(driver.get_screenshot_as_png(), name="2_Login", attachment_type=AttachmentType.PNG)

    # <-- THE LOOP STARTS HERE -->
    # We take the first 3 products from the CSV and add them one by one
    for index, row in enumerate(medicine_data[:3], start=1):
        medicine_name = row["search_text"]

        # Allure will create a sub-step for each item (e.g., 3.1, 3.2, 3.3)
        with allure.step(f"3.{index} Search and Add to Cart: {medicine_name}"):
            logger.info(f"Processing item {index}: {medicine_name}")

            # Only check for the promotional popup on the very first item
            if index == 1:
                search.close_promotional_popup()

            # Navigate to Buy Medicines to reset the page state for the new search
            search.click_buy_medicines()
            search.search_medicine(medicine_name)

            assert search.verify_search_results(), f"Search failed for {medicine_name}"

            # Add to cart
            product.add_first_product_to_cart()

            # Take a screenshot for each item added
            allure.attach(driver.get_screenshot_as_png(), name=f"Added_{medicine_name}",
                          attachment_type=AttachmentType.PNG)
    # <-- THE LOOP ENDS HERE -->

    with allure.step("4. Open Cart and Proceed to Checkout"):
        logger.info("Opening cart to verify and checkout")
        cart.open_cart()

        # Click checkout with all 3 items in the cart
        cart.proceed_to_payment()
        logger.info("Multi-item Checkout process initiated")

        # Final screenshot showing the checkout screen with multiple items
        allure.attach(driver.get_screenshot_as_png(), name="5_Multi_Checkout", attachment_type=AttachmentType.PNG)