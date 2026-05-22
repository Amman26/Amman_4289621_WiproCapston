from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    LOGIN_BUTTON = (By.ID, "loginPopup")
    MOBILE_INPUT = (By.NAME, "mobileNumber")
    CONTINUE_BUTTON = (By.XPATH, "//button[text()='Continue']")
    VERIFY_BUTTON = (By.XPATH, "//button[text()='Verify']")

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def enter_mobile_number(self, mobile):
        self.enter_text(self.MOBILE_INPUT, mobile)

    def click_continue_button(self):
        self.click_element(self.CONTINUE_BUTTON)

    def click_verify_button(self):
        self.click_element(self.VERIFY_BUTTON)