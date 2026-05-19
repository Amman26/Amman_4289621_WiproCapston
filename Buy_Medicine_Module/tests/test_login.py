import time
import pytest

from pages.login_page import LoginPage
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger


# Initialize logger
logger = setup_logger()

# Load CSV test data
test_data = read_csv_data("data/login_data.csv")


@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
def test_login_page(driver, data):

    logger.info("Starting Login Test")

    login = LoginPage(driver)

    # Open login panel
    login.click_login_button()

    logger.info("Clicked Login Button")

    # Enter mobile number
    login.enter_mobile_number(data["mobile"])

    logger.info(
        f"Entered Mobile Number: {data['mobile']}"
    )

    # Click continue
    login.click_continue_button()

    logger.info("Clicked Continue Button")

    # Manual OTP handling
    print(
        f"\nPlease manually enter OTP for "
        f"{data['mobile']}..."
    )

    logger.info(
        f"Waiting for manual OTP entry "
        f"for {data['mobile']}"
    )

    time.sleep(20)

    # Click verify after OTP entry
    login.click_verify_button()

    logger.info("Clicked Verify Button")

    print(
        f"\nLogin completed for "
        f"{data['mobile']}"
    )

    logger.info(
        f"Login completed successfully "
        f"for {data['mobile']}"
    )