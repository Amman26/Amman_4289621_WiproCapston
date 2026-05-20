from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ICON = (
        By.XPATH,
        "//a[@aria-label='Cart Icon']"
    )

    CART_PRODUCT_NAME = (
        By.XPATH,
        "//h2[contains(@class, 'MedicineProductCard_title')]"
    )

    # UPDATED LOCATOR: Using the specific class from your screenshot or a broader text match
    PROCEED_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'primaryPharmaBtn') or contains(., 'Proceed')]"
    )

    def open_cart(self):
        self.click_element(self.CART_ICON)

    def get_cart_product_name(self):
        return self.get_text(self.CART_PRODUCT_NAME)

    def proceed_to_payment(self):
        # UPDATED WAIT: Just wait for it to exist, then force click it with JS
        proceed_btn = self.wait.until(
            EC.presence_of_element_located(self.PROCEED_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_btn)
        self.driver.execute_script("arguments[0].click();", proceed_btn)