from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

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
        """Attempts to close the Shadow DOM promotional popup if it exists."""
        try:
            self.driver.implicitly_wait(2)

            # Find the shadow host and pierce the shadow root
            shadow_host = self.driver.find_element(By.TAG_NAME, "ct-web-popup-imageonly")
            shadow_root = shadow_host.shadow_root

            # Find and click the close button inside
            close_button = shadow_root.find_element(By.ID, "close")
            close_button.click()

            print("Promotional popup detected and closed.")

        except NoSuchElementException:
            pass  # Ignore if popup isn't there
        finally:
            self.driver.implicitly_wait(0)