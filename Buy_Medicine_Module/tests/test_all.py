import time
import pytest

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


@pytest.mark.order(1)
def test_website_launch(driver):
    logger.info("Starting Website Launch Test")
    assert "Apollo" in driver.title
    logger.info("Apollo 24/7 website launched successfully")


@pytest.mark.order(2)
@pytest.mark.parametrize("data", login_data)
def test_login_page(driver, data):
    logger.info("Starting Login Test")
    login = LoginPage(driver)

    login.click_login_button()
    logger.info("Clicked Login Button")

    login.enter_mobile_number(data["mobile"])
    logger.info(f"Entered Mobile Number: {data['mobile']}")

    login.click_continue_button()
    logger.info("Clicked Continue Button")

    # Handle Positive vs Negative Login Test
    if data["expected"] == "pass":
        print(f"\nPlease manually enter OTP for {data['mobile']}...")
        logger.info(f"Waiting for manual OTP entry for {data['mobile']}")
        time.sleep(20)

        login.click_verify_button()
        logger.info("Clicked Verify Button")
        logger.info(f"Login completed successfully for {data['mobile']}")
    else:
        logger.info(f"Negative test executed for {data['mobile']}. OTP wait skipped.")


@pytest.mark.order(3)
@pytest.mark.parametrize("data", medicine_search_data)
def test_search_medicine(driver, data):
    logger.info("Starting Search Medicine Test")
    search = SearchMedicinePage(driver)

    logger.info("Checking for and closing promotional popup")
    search.close_promotional_popup()

    logger.info("Clicking Buy Medicines")
    search.click_buy_medicines()

    medicine_name = data["search_text"]
    logger.info(f"Searching medicine: {medicine_name}")
    search.search_medicine(medicine_name)

    logger.info("Validating search results")
    result = search.verify_search_results()

    # Handle Positive vs Negative Search Test
    if data["expected"] == "success":
        logger.info("Positive test case passed")
        assert result, f"Expected successful search for {medicine_name} but it failed."
    else:
        logger.info("Negative test case executed")
        assert not result, f"Expected search for {medicine_name} to fail, but it succeeded."


@pytest.mark.order(4)
@pytest.mark.parametrize("data", product_validation_data)
def test_add_medicine_to_cart(driver, data):
    logger.info("Starting Add to Cart and Checkout Test")

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

    logger.info("Opening cart")
    cart.open_cart()

    logger.info("Fetching product name from cart")
    cart_product_name = cart.get_cart_product_name()
    logger.info(f"Product found in cart: {cart_product_name}")

    normalized_expected = medicine_name.lower().replace(" ", "").replace("-", "")
    normalized_actual = cart_product_name.lower().replace(" ", "").replace("-", "")

    assert normalized_expected in normalized_actual, \
        f"Correct product was not added to cart! Expected '{medicine_name}' but found '{cart_product_name}'."

    logger.info("Clicking Proceed to Payment")
    cart.proceed_to_payment()
    logger.info("Checkout process initiated successfully")

    @pytest.mark.skip(reason="Skipping duplicate product validation logic for now")
    @pytest.mark.parametrize("data", product_validation_data)
    def test_product_validation(driver, data):
        search = SearchMedicinePage(driver)
        product = ProductPage(driver)
        medicine_name = data["product_name"]

        search.click_buy_medicines()
        search.search_medicine(medicine_name)

        actual_title = product.get_product_title()
        product.add_first_product_to_cart()

        assert medicine_name.lower() in actual_title.lower()


