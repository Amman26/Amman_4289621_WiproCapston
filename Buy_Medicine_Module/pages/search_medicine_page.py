from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchMedicinePage(BasePage):
    # ================= Locators =================

    BUY_MEDICINES_LINK = (
        By.LINK_TEXT,
        "Buy Medicines"
    )

    # 1. The dummy search bar on the home page
    INITIAL_SEARCH_BAR = (
        By.XPATH,
        "//div[@data-placeholder='Search Medicines']"
    )

    # 2. The REAL input field where you type (from your latest screenshot!)
    SEARCH_BOX = (
        By.ID,
        "searchProduct"
    )

    SEARCH_RESULTS = (
        By.XPATH,
        "//div[contains(@class,'ProductCardstyle__ProductCardWrapper')]"
    )

    # ================= Actions =================

    def click_buy_medicines(self):
        self.click_element(self.BUY_MEDICINES_LINK)

    def search_medicine(self, medicine_name):
        # Click the dummy bar to open the search screen
        self.click_element(self.INITIAL_SEARCH_BAR)

        # Type into the real input field using its ID
        self.enter_text(self.SEARCH_BOX, medicine_name)

    def verify_search_results(self):
        return self.is_element_visible(self.SEARCH_RESULTS)