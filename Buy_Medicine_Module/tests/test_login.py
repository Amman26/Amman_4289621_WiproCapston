import time
import pytest

from pages.login_page import LoginPage
from utils.csv_utils import read_csv_data

# Load data from the CSV file
test_data = read_csv_data("data/login_data.csv")

@pytest.mark.parametrize("data", test_data)
def test_login_page(driver, data):
    login = LoginPage(driver)

    # --- Close the popup before trying to interact with the page ---
    login.close_promotional_popup()

    # 1. Open the login side panel
    login.click_login_button()

    # 2. Enter the mobile number using the parameterized CSV data
    login.enter_mobile_number(data["mobile"])

    # 3. Click Continue to trigger the OTP text message
    login.click_continue_button()

    # 4. Pause execution so YOU can manually type the OTP on your screen
    print(f"\nScript paused: Please enter the OTP for {data['mobile']} manually in the browser...")
    time.sleep(20)

    # 5. Automatically click the Verify button once the sleep is over
    login.click_verify_button()

    print(f"\nLogin workflow completed for {data['mobile']}!")