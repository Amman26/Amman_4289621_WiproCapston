from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from utils.config_reader import read_config


config = read_config()

timeout = int(config.get("DEFAULT", "timeout"))


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, timeout)

    def click_element(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def enter_text(self, locator, text):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.clear()
        element.send_keys(text)

    def get_text(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def is_element_visible(self, locator):

        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()

        except TimeoutException:
            return False

    def close_promotional_popup(self):

        """Close promotional popup if present"""

        try:

            self.driver.implicitly_wait(2)

            shadow_host = self.driver.find_element(
                By.TAG_NAME,
                "ct-web-popup-imageonly"
            )

            shadow_root = shadow_host.shadow_root

            close_button = shadow_root.find_element(
                By.ID,
                "close"
            )

            close_button.click()

            print("Popup closed successfully")

        except NoSuchElementException:

            print("Popup not present")

        finally:

            self.driver.implicitly_wait(0)