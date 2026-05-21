import time
import pytest
import allure

# Page Objects
from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# Utils
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger

# Initialize logger and load all CSV data at the module level
logger = setup_logger()
login_data = read_csv_data("data/login_data.csv")
medicine_search_data = read_csv_data("data/medicine_search_data.csv")
product_validation_data = read_csv_data("data/product_validation_data.csv")


@allure.epic("Apollo 24/7 E2E Automation")  # <-- ALLURE: Highest level grouping
@allure.feature("Environment Setup")  # <-- ALLURE: Module grouping
@allure.story("Website Launch")  # <-- ALLURE: Specific test story
@allure.title("Verify application launches successfully")  # <-- ALLURE: Readable test name
@pytest.mark.order(1)
def test_website_launch(driver):
    with allure.step("Validate page title contains 'Apollo'"):  # <-- ALLURE: Logs steps inside the report
        logger.info("Starting Website Launch Test")
        assert "Apollo" in driver.title
        logger.info("Apollo 24/7 website launched successfully")


@allure.epic("Apollo 24/7 E2E Automation")
@allure.feature("Authentication")
@allure.story("User Login Process")
@allure.severity(allure.severity_level.CRITICAL)  # <-- ALLURE: Sets priority
@pytest.mark.order(2)
@pytest.mark.parametrize("data", login_data)
def test_login_page(driver, data):
    # ALLURE: Dynamically update the test title based on parameterized data
    allure.dynamic.title(f"Login Test: Mobile {data['mobile']} (Expected: {data['expected']})")

    logger.info("Starting Login Test")
    login = LoginPage(driver)

    with allure.step("Navigate to Login and enter credentials"):
        login.click_login_button()
        logger.info("Clicked Login Button")

        login.enter_mobile_number(data["mobile"])
        logger.info(f"Entered Mobile Number: {data['mobile']}")

        login.click_continue_button()
        logger.info("Clicked Continue Button")

    # Handle Positive & Negative Login Test
    with allure.step(f"Validate OTP process for {data['expected']} scenario"):
        if data["expected"] == "pass":
            print(f"\nPlease manually enter OTP for {data['mobile']}...")
            logger.info(f"Waiting for manual OTP entry for {data['mobile']}")
            time.sleep(20)

            login.click_verify_button()
            logger.info("Clicked Verify Button")
            logger.info(f"Login completed successfully for {data['mobile']}")
        else:
            logger.info(f"Negative test executed for {data['mobile']}. OTP wait skipped.")


@allure.epic("Apollo 24/7 E2E Automation")
@allure.feature("Medicine Search")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.order(3)
@pytest.mark.parametrize("data", medicine_search_data)
def test_search_medicine(driver, data):
    medicine_name = data["search_text"]
    allure.dynamic.title(f"Search for medicine: {medicine_name}")

    logger.info("Starting Search Medicine Test")
    search = SearchMedicinePage(driver)

    with allure.step("Close promotional popups"):
        logger.info("Checking for and closing promotional popup")
        search.close_promotional_popup()

    with allure.step(f"Execute search for '{medicine_name}'"):
        logger.info("Clicking Buy Medicines")
        search.click_buy_medicines()
        logger.info(f"Searching medicine: {medicine_name}")
        search.search_medicine(medicine_name)

    with allure.step("Validate search results"):
        logger.info("Validating search results")
        result = search.verify_search_results()

        # Handle Positive vs Negative Search Test
        if data["expected"] == "success":
            logger.info("Positive test case passed")
            assert result, f"Expected successful search for {medicine_name} but it failed."
        else:
            logger.info("Negative test case executed")
            assert not result, f"Expected search for {medicine_name} to fail, but it succeeded."


@allure.epic("Apollo 24/7 E2E Automation")
@allure.feature("Checkout Process")
@allure.story("Add Medicine to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.order(4)
@pytest.mark.parametrize("data", product_validation_data)
def test_add_medicine_to_cart(driver, data):
    medicine_name = data["product_name"]
    allure.dynamic.title(f"Add {medicine_name} to cart and proceed to checkout")

    logger.info("Starting Add to Cart and Checkout Test")

    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    with allure.step(f"Search and select {medicine_name}"):
        search.click_buy_medicines()
        search.search_medicine(medicine_name)
        product.add_first_product_to_cart()

    with allure.step("Open cart and validate contents"):
        cart.open_cart()
        cart_product_name = cart.get_cart_product_name()
        logger.info(f"Product found in cart: {cart_product_name}")

        normalized_expected = medicine_name.lower().replace(" ", "").replace("-", "")
        normalized_actual = cart_product_name.lower().replace(" ", "").replace("-", "")

        assert normalized_expected in normalized_actual, \
            f"Correct product was not added to cart! Expected '{medicine_name}' but found '{cart_product_name}'."

    with allure.step("Initiate payment process"):
        cart.proceed_to_payment()
        logger.info("Checkout process initiated successfully")