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
from utils.screenshot_utils import capture_screenshot

logger = setup_logger()

# =====================================================
# LOAD CSV DATA
# =====================================================

login_data = read_csv_data(
    "data/login_data.csv"
)

medicine_search_data = read_csv_data(
    "data/medicine_search_data.csv"
)

product_validation_data = read_csv_data(
    "data/product_validation_data.csv"
)

# =====================================================
# COMMON LOGIN FLOW
# =====================================================

@allure.step("Execute Common Login Flow")
def login_flow(driver, mobile_number):

    login = LoginPage(driver)

    login.click_login_button()

    logger.info("Clicked Login Button")

    login.enter_mobile_number(mobile_number)

    logger.info(
        f"Entered Mobile Number : {mobile_number}"
    )

    login.click_continue_button()

    logger.info("Clicked Continue Button")


# =====================================================
# POSITIVE TEST CASE 1
# VERIFY WEBSITE LAUNCH
# =====================================================

@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.order(1)

@allure.title(
    "Verify Apollo Website Launch"
)

@allure.description(
    "Tests if Apollo 24/7 website launches successfully."
)

def test_website_launch(driver):

    logger.info(
        "========== WEBSITE LAUNCH TEST =========="
    )

    capture_screenshot(
        driver,
        "website_launch"
    )

    assert "Apollo" in driver.title

    logger.info(
        "Apollo Website Launch Test Passed"
    )


# =====================================================
# POSITIVE LOGIN TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.order(2)

@allure.feature("Authentication")
@allure.story("Positive Login Functionality")

@pytest.mark.parametrize(
    "data",
    [d for d in login_data if d["expected"] == "pass"]
)

def test_positive_login(driver, data):

    mobile_number = data["mobile"]

    allure.dynamic.title(
        f"Positive Login Test - {mobile_number}"
    )

    logger.info(
        "========== POSITIVE LOGIN TEST =========="
    )

    login = LoginPage(driver)

    # LOGIN FLOW
    login_flow(driver, mobile_number)

    logger.info(
        "Waiting For Manual OTP Entry"
    )

    print(
        f"\nPlease manually enter OTP for {mobile_number}"
    )

    time.sleep(20)

    login.click_verify_button()

    logger.info(
        "Clicked Verify Button"
    )

    capture_screenshot(
        driver,
        "positive_login_test"
    )

    assert "apollo" in driver.current_url.lower()

    logger.info(
        "Positive Login Test Passed"
    )


# =====================================================
# NEGATIVE LOGIN TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.order(3)

@allure.feature("Authentication")
@allure.story("Negative Login Functionality")

@pytest.mark.parametrize(
    "data",
    [d for d in login_data if d["expected"] == "fail"]
)

def test_negative_login(driver, data):

    mobile_number = data["mobile"]

    allure.dynamic.title(
        f"Negative Login Test - {mobile_number}"
    )

    logger.info(
        "========== NEGATIVE LOGIN TEST =========="
    )

    login = LoginPage(driver)

    # LOGIN FLOW
    login_flow(driver, mobile_number)

    capture_screenshot(
        driver,
        "negative_login_test"
    )

    error_message = login.get_invalid_login_error()

    assert "invalid" in error_message.lower()

    logger.info(
        "Negative Login Test Passed"
    )


# =====================================================
# POSITIVE SEARCH TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.order(4)

@allure.feature("Medicine Search")
@allure.story("Positive Medicine Search")

@pytest.mark.parametrize(
    "data",
    [
        d for d in medicine_search_data
        if d["expected"] == "success"
    ]
)

def test_positive_search_medicine(driver, data):

    medicine_name = data["search_text"]

    allure.dynamic.title(
        f"Positive Medicine Search - {medicine_name}"
    )

    logger.info(
        "========== POSITIVE SEARCH TEST =========="
    )

    search = SearchMedicinePage(driver)

    # CLOSE POPUP
    search.close_promotional_popup()

    logger.info(
        "Promotional Popup Closed"
    )

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )

    # SEARCH MEDICINE
    search.search_medicine(medicine_name)

    logger.info(
        f"Searched Medicine : {medicine_name}"
    )

    # VERIFY RESULT
    result = search.verify_search_results()

    capture_screenshot(
        driver,
        "positive_search_test"
    )

    assert result, \
        f"Search failed for {medicine_name}"

    logger.info(
        "Positive Search Test Passed"
    )


# =====================================================
# NEGATIVE SEARCH TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.order(5)

@allure.feature("Medicine Search")
@allure.story("Negative Medicine Search")

@pytest.mark.parametrize(
    "data",
    [
        d for d in medicine_search_data
        if d["expected"] == "failure"
    ]
)

def test_negative_search_medicine(driver, data):

    medicine_name = data["search_text"]

    allure.dynamic.title(
        f"Negative Medicine Search - {medicine_name}"
    )

    logger.info(
        "========== NEGATIVE SEARCH TEST =========="
    )

    search = SearchMedicinePage(driver)

    # CLOSE POPUP
    search.close_promotional_popup()

    logger.info(
        "Promotional Popup Closed"
    )

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )

    # SEARCH INVALID MEDICINE
    search.search_medicine(medicine_name)

    logger.info(
        f"Searched Invalid Medicine : {medicine_name}"
    )

    # VERIFY RESULT
    result = search.verify_search_results()

    capture_screenshot(
        driver,
        "negative_search_test"
    )

    assert not result, \
        f"Search unexpectedly succeeded for {medicine_name}"

    logger.info(
        "Negative Search Test Passed"
    )


# =====================================================
# POSITIVE ADD TO CART TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.order(6)

@allure.feature("Cart Functionality")
@allure.story("Add Product To Cart")

@pytest.mark.parametrize(
    "data",
    product_validation_data
)

def test_add_medicine_to_cart(driver, data):

    medicine_name = data["product_name"]

    allure.dynamic.title(
        f"Add Medicine To Cart - {medicine_name}"
    )

    logger.info(
        "========== ADD TO CART TEST =========="
    )

    search = SearchMedicinePage(driver)

    product = ProductPage(driver)

    cart = CartPage(driver)

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    # SEARCH PRODUCT
    search.search_medicine(medicine_name)

    logger.info(
        f"Searched Product : {medicine_name}"
    )

    # ADD PRODUCT
    product.add_first_product_to_cart()

    logger.info(
        "Product Added To Cart"
    )

    # OPEN CART
    cart.open_cart()

    logger.info(
        "Cart Opened Successfully"
    )

    # GET CART PRODUCT
    cart_product_name = cart.get_cart_product_name()

    logger.info(
        f"Product Found In Cart : {cart_product_name}"
    )

    normalized_expected = medicine_name.lower() \
        .replace(" ", "") \
        .replace("-", "")

    normalized_actual = cart_product_name.lower() \
        .replace(" ", "") \
        .replace("-", "")

    capture_screenshot(
        driver,
        "add_to_cart_test"
    )


    assert normalized_expected in normalized_actual, \
        f"Expected '{medicine_name}' but found '{cart_product_name}'"

    logger.info(
        "Add To Cart Test Passed"
    )

    # PROCEED PAYMENT
    cart.proceed_to_payment()

    logger.info(
        "Checkout Process Initiated Successfully"
    )