from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class ProductPage(BasePage):

    # First Add button from medicine grid
    FIRST_ADD_BUTTON = (
        By.XPATH,
        "(//button[contains(.,'Add')])[1]"
    )

    # Cart count after adding product
    CART_COUNT = (
        By.XPATH,
        "//span[contains(@class,'CartCount') or contains(@class,'cart-count')]"
    )

    # Cart icon
    CART_ICON = (
        By.XPATH,
        "//span[contains(@class,'Cart')] | //div[contains(@class,'cart')]"
    )

    # Product title from search/product grid
    PRODUCT_TITLE = (
        By.XPATH,
        "(//div[contains(@class,'ProductCardstyle__Name') or contains(@class,'ProductCard__Name')])[1]"
    )

    # Product name inside cart page
    CART_PRODUCT_NAME = (
        By.XPATH,
        "(//div[contains(@class,'ProductName') or contains(@class,'product-name')])[1]"
    )

    def add_first_product_to_cart(self):

        add_button = self.wait.until(
            EC.element_to_be_clickable(
                self.FIRST_ADD_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_button
        )

        try:
            self.wait.until(
                EC.presence_of_element_located(
                    self.CART_COUNT
                )
            )

        except TimeoutException:
            print("Cart count did not appear.")

    def open_cart(self):

        cart = self.wait.until(
            EC.element_to_be_clickable(
                self.CART_ICON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cart
        )

    def get_product_title(self):

        return self.get_text(
            self.PRODUCT_TITLE
        )

    def get_cart_product_name(self):

        return self.get_text(
            self.CART_PRODUCT_NAME
        )

    def verify_cart_updated(self):
        try:
            self.wait.until(
                EC.presence_of_element_located(self.CART_COUNT)
            )
            return True
        except TimeoutException:
            return False