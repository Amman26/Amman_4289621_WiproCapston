from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    # Keeps only the locator for the 'Add' button on the grid
    FIRST_ADD_BUTTON = (
        By.XPATH,
        "(//button[@aria-label='Add'])[1]"
    )

    # Keeps the locator to verify the cart icon updated
    CART_COUNT = (
        By.XPATH,
        "//span[contains(@class,'CartCount')]"
    )

    def add_first_product_to_cart(self):
        """Clicks the 'Add' button directly from the search grid."""
        self.click_element(self.FIRST_ADD_BUTTON)

    def verify_cart_updated(self):
        """Checks if the cart count element is visible after adding."""
        return self.is_element_visible(self.CART_COUNT)