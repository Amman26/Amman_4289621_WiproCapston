import time
import pytest

from pages.login_page import LoginPage
from utils.csv_utils import read_csv_data


# Load CSV test data
test_data = read_csv_data("data/login_data.csv")


@pytest.mark.parametrize("data", test_data)
def test_login_page(driver, data):

    login = LoginPage(driver)

    # Open login panel
    login.click_login_button()

    # Enter mobile number
    login.enter_mobile_number(data["mobile"])

    # Click continue
    login.click_continue_button()

    # Manual OTP handling
    print(
        f"\nPlease manually enter OTP for "
        f"{data['mobile']}..."
    )

    time.sleep(20)

    # Click verify after OTP entry
    login.click_verify_button()

    print(
        f"\nLogin completed for "
        f"{data['mobile']}"
    )