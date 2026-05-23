import time
import allure

from behave import given, when, then

from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage

from utils.logger import setup_logger
from utils.screenshot_utils import capture_screenshot
from utils.csv_utils import read_csv_data


logger = setup_logger()


# =====================================================
# WEBSITE LAUNCH
# =====================================================

@given("User launches Apollo website")
def launch_website(context):

    logger.info(
        "Launching Apollo Website"
    )


@then("Website should launch successfully")
def verify_website(context):

    capture_screenshot(
        context.driver,
        "website_launch"
    )

    assert "Apollo" in context.driver.title


# =====================================================
# POSITIVE LOGIN
# =====================================================

@when("User performs positive login")
def perform_positive_login(context):

    login_data = read_csv_data(
        "data/login_data.csv"
    )

    valid_users = [
        data for data in login_data
        if data["expected"] == "pass"
    ]

    for user in valid_users:

        mobile = user["mobile"]

        login = LoginPage(
            context.driver
        )

        login.click_login_button()

        logger.info(
            "Clicked Login Button"
        )

        login.enter_mobile_number(
            mobile
        )

        logger.info(
            f"Entered Mobile Number : {mobile}"
        )

        login.click_continue_button()

        logger.info(
            "Clicked Continue Button"
        )

        print(
            f"\nPlease manually enter OTP for {mobile}"
        )

        time.sleep(20)

        login.click_verify_button()

        logger.info(
            "Clicked Verify Button"
        )


@then("User should login successfully")
def verify_login(context):

    capture_screenshot(
        context.driver,
        "positive_login"
    )

    assert "apollo" in context.driver.current_url.lower()

    logger.info(
        "Positive Login Successful"
    )


# =====================================================
# NEGATIVE LOGIN
# =====================================================

@when("User performs negative login")
def perform_negative_login(context):

    login_data = read_csv_data(
        "data/login_data.csv"
    )

    invalid_users = [
        data for data in login_data
        if data["expected"] == "fail"
    ]

    for user in invalid_users:

        mobile = user["mobile"]

        login = LoginPage(
            context.driver
        )

        login.click_login_button()

        login.enter_mobile_number(
            mobile
        )

        login.click_continue_button()

        logger.info(
            f"Invalid Mobile Entered : {mobile}"
        )


@then("Invalid login error should display")
def verify_invalid_login(context):

    login = LoginPage(
        context.driver
    )

    error_message = login.get_invalid_login_error()

    capture_screenshot(
        context.driver,
        "negative_login"
    )

    assert "invalid" in error_message.lower()

    logger.info(
        "Negative Login Validation Passed"
    )


# =====================================================
# SEARCH MEDICINE
# =====================================================

@given("User opens Buy Medicines page")
def open_buy_medicines(context):

    search = SearchMedicinePage(
        context.driver
    )

    search.close_promotional_popup()

    logger.info(
        "Popup Closed"
    )

    search.click_buy_medicines()

    logger.info(
        "Clicked Buy Medicines"
    )


# =====================================================
# POSITIVE SEARCH
# =====================================================

@when("User performs positive medicine search")
def perform_positive_search(context):

    medicine_data = read_csv_data(
        "data/medicine_search_data.csv"
    )

    valid_medicines = [
        data for data in medicine_data
        if data["expected"] == "success"
    ]

    search = SearchMedicinePage(
        context.driver
    )

    for medicine in valid_medicines:

        medicine_name = medicine["search_text"]

        search.search_medicine(
            medicine_name
        )

        logger.info(
            f"Searched Medicine : {medicine_name}"
        )


@then("Search results should display")
def verify_search(context):

    search = SearchMedicinePage(
        context.driver
    )

    result = search.verify_search_results()

    capture_screenshot(
        context.driver,
        "positive_search"
    )

    assert result

    logger.info(
        "Positive Search Passed"
    )


# =====================================================
# NEGATIVE SEARCH
# =====================================================

@when("User performs negative medicine search")
def perform_negative_search(context):

    medicine_data = read_csv_data(
        "data/medicine_search_data.csv"
    )

    invalid_medicines = [
        data for data in medicine_data
        if data["expected"] == "fail"
    ]

    search = SearchMedicinePage(
        context.driver
    )

    for medicine in invalid_medicines:

        medicine_name = medicine["search_text"]

        search.search_medicine(
            medicine_name
        )

        logger.info(
            f"Searched Invalid Medicine : {medicine_name}"
        )


@then("No valid results should display")
def verify_invalid_search(context):

    search = SearchMedicinePage(
        context.driver
    )

    result = search.verify_search_results()

    capture_screenshot(
        context.driver,
        "negative_search"
    )

    assert not result

    logger.info(
        "Negative Search Passed"
    )