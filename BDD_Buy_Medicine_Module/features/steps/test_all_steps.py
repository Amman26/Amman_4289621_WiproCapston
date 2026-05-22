import time
import allure

from behave import given, when, then

from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

from utils.logger import setup_logger
from utils.screenshot_utils import capture_screenshot


logger = setup_logger()


# =====================================================
# WEBSITE LAUNCH
# =====================================================

@given("User launches Apollo website")
def launch_website(context):

    logger.info("Launching Apollo Website")


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

@when('User enters mobile number "{mobile}"')
def enter_mobile(context, mobile):

    login = LoginPage(context.driver)

    login.click_login_button()

    login.enter_mobile_number(mobile)

    login.click_continue_button()

    logger.info(f"Entered Mobile : {mobile}")


@when("User completes OTP verification")
def complete_otp(context):

    print("\nPlease Enter OTP Manually")

    time.sleep(20)

    login = LoginPage(context.driver)

    login.click_verify_button()


@then("User should login successfully")
def verify_login(context):

    capture_screenshot(
        context.driver,
        "positive_login"
    )

    assert "apollo" in context.driver.current_url.lower()


# =====================================================
# NEGATIVE LOGIN
# =====================================================

@when('User enters invalid mobile number "{mobile}"')
def enter_invalid_mobile(context, mobile):

    login = LoginPage(context.driver)

    login.click_login_button()

    login.enter_mobile_number(mobile)

    login.click_continue_button()


@then("Invalid login error should display")
def verify_invalid_login(context):

    login = LoginPage(context.driver)

    error_message = login.get_invalid_login_error()

    capture_screenshot(
        context.driver,
        "negative_login"
    )

    assert "invalid" in error_message.lower()


# =====================================================
# SEARCH MEDICINE
# =====================================================

@given("User opens Buy Medicines page")
def open_buy_medicines(context):

    search = SearchMedicinePage(context.driver)

    search.close_promotional_popup()

    search.click_buy_medicines()


@when('User searches medicine "{medicine}"')
def search_medicine(context, medicine):

    search = SearchMedicinePage(context.driver)

    search.search_medicine(medicine)

    logger.info(f"Searched : {medicine}")


@then("Search results should display")
def verify_search(context):

    search = SearchMedicinePage(context.driver)

    result = search.verify_search_results()

    capture_screenshot(
        context.driver,
        "positive_search"
    )

    assert result


# =====================================================
# NEGATIVE SEARCH
# =====================================================

@when('User searches invalid medicine "{medicine}"')
def search_invalid_medicine(context, medicine):

    search = SearchMedicinePage(context.driver)

    search.search_medicine(medicine)


@then("No valid results should display")
def verify_invalid_search(context):

    search = SearchMedicinePage(context.driver)

    result = search.verify_search_results()

    capture_screenshot(
        context.driver,
        "negative_search"
    )

    assert not result