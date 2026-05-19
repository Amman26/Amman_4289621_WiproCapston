from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    # Updated to use the aria-label attribute for better stability
    CART_ICON = (
        By.XPATH,
        "//a[@aria-label='Cart Icon']"
    )

    CART_PRODUCT_NAME = (
        By.XPATH,
        "//h2[contains(@class, 'MedicineProductCard_title')]"
    )

    def open_cart(self):
        self.click_element(self.CART_ICON)

    def get_cart_product_name(self):
        return self.get_text(self.CART_PRODUCT_NAME)