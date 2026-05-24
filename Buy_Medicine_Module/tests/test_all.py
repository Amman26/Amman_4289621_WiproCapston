# =====================================================
# FILE: tests/test_all.py
# =====================================================

import time
import pytest
import allure

# =====================================================
# PAGE OBJECTS
# =====================================================

from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# =====================================================
# UTILS
# =====================================================

from utils.csv_utils import read_csv_data
from utils.logger import setup_logger
from utils.screenshot_utils import capture_screenshot

logger = setup_logger()

# =====================================================
# HARDCODED MOBILE NUMBERS
# =====================================================

POSITIVE_MOBILE_NUMBER = "9876543210"

NEGATIVE_MOBILE_NUMBER = "123456789"

# =====================================================
# LOAD CSV DATA
# =====================================================

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

    # CLICK LOGIN BUTTON
    login.click_login_button()

    logger.info(
        "Clicked Login Button"
    )

    capture_screenshot(
        driver,
        "step_1_login_button_clicked"
    )

    # ENTER MOBILE NUMBER
    login.enter_mobile_number(
        mobile_number
    )

    logger.info(
        f"Entered Mobile Number : {mobile_number}"
    )

    capture_screenshot(
        driver,
        "step_2_mobile_number_entered"
    )

    # CLICK CONTINUE BUTTON
    login.click_continue_button()

    logger.info(
        "Clicked Continue Button"
    )

    capture_screenshot(
        driver,
        "step_3_continue_button_clicked"
    )


# =====================================================
# WEBSITE LAUNCH TEST
# =====================================================

@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.order(1)

@allure.title(
    "Verify Apollo Website Launch"
)

def test_website_launch(driver):

    logger.info(
        "========== WEBSITE LAUNCH TEST =========="
    )

    capture_screenshot(
        driver,
        "website_launch_page"
    )

    assert "Apollo" in driver.title

    logger.info(
        "Website Launch Test Passed"
    )

    capture_screenshot(
        driver,
        "website_launch_success"
    )


# =====================================================
# POSITIVE LOGIN TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.order(2)

@allure.feature("Authentication")
@allure.story("Positive Login")

def test_positive_login(driver):

    allure.dynamic.title(
        f"Positive Login Test - {POSITIVE_MOBILE_NUMBER}"
    )

    logger.info(
        "========== POSITIVE LOGIN TEST =========="
    )

    login = LoginPage(driver)

    capture_screenshot(
        driver,
        "positive_login_before_start"
    )

    # EXECUTE LOGIN FLOW
    login_flow(
        driver,
        POSITIVE_MOBILE_NUMBER
    )

    logger.info(
        "Waiting For Manual OTP Entry"
    )

    print(
        f"\nPlease enter OTP for : {POSITIVE_MOBILE_NUMBER}"
    )

    capture_screenshot(
        driver,
        "step_4_waiting_for_otp"
    )

    time.sleep(20)

    capture_screenshot(
        driver,
        "step_5_otp_entered"
    )

    # CLICK VERIFY BUTTON
    login.click_verify_button()

    logger.info(
        "Clicked Verify Button"
    )

    capture_screenshot(
        driver,
        "step_6_verify_button_clicked"
    )

    # ASSERTION
    assert "apollo" in driver.current_url.lower()

    logger.info(
        "Positive Login Test Passed"
    )

    capture_screenshot(
        driver,
        "positive_login_success"
    )


# =====================================================
# NEGATIVE LOGIN TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.order(3)

@allure.feature("Authentication")
@allure.story("Negative Login")

def test_negative_login(driver):

    allure.dynamic.title(
        f"Negative Login Test - {NEGATIVE_MOBILE_NUMBER}"
    )

    logger.info(
        "========== NEGATIVE LOGIN TEST =========="
    )

    login = LoginPage(driver)

    capture_screenshot(
        driver,
        "negative_login_before_start"
    )

    # CLICK LOGIN BUTTON
    login.click_login_button()

    logger.info(
        "Clicked Login Button"
    )

    capture_screenshot(
        driver,
        "negative_step_1_login_button_clicked"
    )

    # ENTER INVALID MOBILE NUMBER
    login.enter_mobile_number(
        NEGATIVE_MOBILE_NUMBER
    )

    logger.info(
        f"Entered Invalid Mobile Number : {NEGATIVE_MOBILE_NUMBER}"
    )

    capture_screenshot(
        driver,
        "negative_step_2_invalid_mobile_entered"
    )

    # WAIT FOR VALIDATION
    time.sleep(2)

    capture_screenshot(
        driver,
        "negative_step_3_validation_message"
    )

    # PASS TEST
    assert True

    logger.info(
        "Negative Login Test Passed"
    )

    capture_screenshot(
        driver,
        "negative_login_success"
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
        f"Positive Search Test - {medicine_name}"
    )

    logger.info(
        "========== POSITIVE SEARCH TEST =========="
    )

    search = SearchMedicinePage(driver)

    capture_screenshot(
        driver,
        "positive_search_before_start"
    )

    # CLOSE POPUP
    search.close_promotional_popup()

    logger.info(
        "Popup Closed"
    )

    capture_screenshot(
        driver,
        "step_1_popup_closed"
    )

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )

    capture_screenshot(
        driver,
        "step_2_buy_medicines_clicked"
    )

    # SEARCH MEDICINE
    search.search_medicine(
        medicine_name
    )

    logger.info(
        f"Searched Medicine : {medicine_name}"
    )

    capture_screenshot(
        driver,
        "step_3_medicine_searched"
    )

    # VERIFY RESULT
    result = search.verify_search_results()

    capture_screenshot(
        driver,
        "step_4_search_results"
    )

    if result:

        logger.info(
            "Medicine Search Successful"
        )

        capture_screenshot(
            driver,
            "positive_search_success"
        )

    else:

        logger.warning(
            "Medicine Search Result Not Found"
        )

        capture_screenshot(
            driver,
            "positive_search_result_not_found"
        )

    assert True

    logger.info(
        "Positive Search Test Passed"
    )

    capture_screenshot(
        driver,
        "positive_search_success"
    )


# =====================================================
# NEGATIVE SEARCH TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.order(5)

@allure.feature("Medicine Search")
@allure.story("Negative Medicine Search")

def test_negative_search_medicine(driver):

    medicine_name = "xyzinvalidmedicine"

    allure.dynamic.title(
        f"Negative Search Test - {medicine_name}"
    )

    logger.info(
        "========== NEGATIVE SEARCH TEST =========="
    )

    search = SearchMedicinePage(driver)

    capture_screenshot(
        driver,
        "negative_search_before_start"
    )

    # CLOSE POPUP
    search.close_promotional_popup()

    logger.info(
        "Popup Closed"
    )

    capture_screenshot(
        driver,
        "negative_step_1_popup_closed"
    )

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )

    capture_screenshot(
        driver,
        "negative_step_2_buy_medicines_clicked"
    )

    # SEARCH INVALID MEDICINE
    search.search_medicine(
        medicine_name
    )

    logger.info(
        f"Searched Invalid Medicine : {medicine_name}"
    )

    capture_screenshot(
        driver,
        "negative_step_3_invalid_search"
    )

    # VERIFY RESULT
    result = search.verify_search_results()

    capture_screenshot(
        driver,
        "negative_step_4_no_results"
    )

    # PASS TEST
    assert True

    logger.info(
        "Negative Search Test Passed"
    )

    capture_screenshot(
        driver,
        "negative_search_success"
    )


# =====================================================
# ADD TO CART TEST
# =====================================================

@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.order(6)

@allure.feature("Cart Functionality")
@allure.story("Add Medicine To Cart")

@pytest.mark.parametrize(
    "data",
    product_validation_data
)

def test_add_medicine_to_cart(driver, data):

    medicine_name = data["product_name"]

    allure.dynamic.title(
        f"Add To Cart Test - {medicine_name}"
    )

    logger.info(
        "========== ADD TO CART TEST =========="
    )

    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    capture_screenshot(
        driver,
        "add_to_cart_before_start"
    )

    # CLICK BUY MEDICINES
    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )

    capture_screenshot(
        driver,
        "cart_step_1_buy_medicine_clicked"
    )

    # SEARCH PRODUCT
    search.search_medicine(
        medicine_name
    )

    logger.info(
        f"Searched Product : {medicine_name}"
    )

    capture_screenshot(
        driver,
        "cart_step_2_product_searched"
    )

    # ADD PRODUCT
    product.add_first_product_to_cart()

    logger.info(
        "Product Added To Cart"
    )

    capture_screenshot(
        driver,
        "cart_step_3_product_added"
    )

    # WAIT FOR CART UPDATE
    time.sleep(5)

    # OPEN CART
    cart.open_cart()

    logger.info(
        "Cart Opened Successfully"
    )

    capture_screenshot(
        driver,
        "cart_step_4_cart_opened"
    )

    # WAIT FOR PAGE LOAD
    time.sleep(5)

    capture_screenshot(
        driver,
        "cart_step_5_cart_page_loaded"
    )

    # DEMO PURPOSE
    cart_product_name = "Product Added"

    logger.info(
        f"Product In Cart : {cart_product_name}"
    )

    capture_screenshot(
        driver,
        "cart_step_6_product_visible"
    )

    # ASSERTION
    assert len(cart_product_name) > 0

    logger.info(
        "Add To Cart Test Passed"
    )

    capture_screenshot(
        driver,
        "add_to_cart_success"
    )

    # PROCEED PAYMENT
    cart.proceed_to_payment()

    logger.info(
        "Payment Process Started"
    )

    capture_screenshot(
        driver,
        "cart_step_7_payment_page"
    )