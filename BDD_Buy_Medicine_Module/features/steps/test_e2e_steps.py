import time
import allure

from behave import given, when, then
from allure_commons.types import AttachmentType

from pages.login_page import LoginPage
from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

from utils.csv_utils import read_csv_data
from utils.logger import setup_logger


logger = setup_logger()

# LOAD TEST DATA
login_data = read_csv_data(
    "data/login_data.csv"
)

medicine_data = read_csv_data(
    "data/medicine_search_data.csv"
)

E2E_MOBILE = login_data[0]["mobile"]


@given("User launches Apollo 24/7 website")
def launch_website(context):

    driver = context.driver

    assert "Apollo" in driver.title

    logger.info(
        "Apollo 24/7 website launched successfully"
    )

    allure.attach(
        driver.get_screenshot_as_png(),
        name="Launch_Website",
        attachment_type=AttachmentType.PNG
    )


@when("User logs in with valid mobile number")
def login_user(context):

    driver = context.driver

    login = LoginPage(driver)

    logger.info(
        "Starting Login Process"
    )

    login.click_login_button()

    login.enter_mobile_number(
        E2E_MOBILE
    )

    login.click_continue_button()

    print(
        f"\nPlease manually enter OTP for {E2E_MOBILE}..."
    )

    time.sleep(20)

    login.click_verify_button()

    logger.info(
        "Login Successful"
    )

    allure.attach(
        driver.get_screenshot_as_png(),
        name="Login_Success",
        attachment_type=AttachmentType.PNG
    )


@when("User searches and adds multiple medicines to cart")
def add_multiple_items(context):

    driver = context.driver

    search = SearchMedicinePage(driver)

    product = ProductPage(driver)

    for index, row in enumerate(
        medicine_data[:3],
        start=1
    ):

        medicine_name = row["search_text"]

        logger.info(
            f"Adding Medicine: {medicine_name}"
        )

        if index == 1:
            search.close_promotional_popup()

        search.click_buy_medicines()

        search.search_medicine(
            medicine_name
        )

        assert search.verify_search_results(), \
            f"Search failed for {medicine_name}"

        product.add_first_product_to_cart()

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Added_{medicine_name}",
            attachment_type=AttachmentType.PNG
        )


@then("User proceeds to checkout successfully")
def checkout(context):

    driver = context.driver

    cart = CartPage(driver)

    logger.info(
        "Opening Cart"
    )

    cart.open_cart()

    cart.proceed_to_payment()

    logger.info(
        "Checkout Initiated Successfully"
    )

    allure.attach(
        driver.get_screenshot_as_png(),
        name="Checkout",
        attachment_type=AttachmentType.PNG
    )