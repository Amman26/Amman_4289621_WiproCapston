from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # <-- Added Keys import
from pages.base_page import BasePage


class SearchMedicinePage(BasePage):
    BUY_MEDICINES_LINK = (
        By.LINK_TEXT,
        "Buy Medicines"
    )

    INITIAL_SEARCH_BAR = (
        By.XPATH,
        "//div[@data-placeholder='Search Medicines']"
    )

    SEARCH_BOX = (
        By.ID,
        "searchProduct"
    )

    SEARCH_RESULTS = (
        By.XPATH,
        "//div[contains(@class,'ProductCardstyle__ProductCardWrapper')] | //a[contains(@href,'/otc/')]"
    )

    def click_buy_medicines(self):
        self.click_element(self.BUY_MEDICINES_LINK)

    def search_medicine(self, medicine_name):
        # 1. Click the dummy search bar to open the real one
        self.click_element(self.INITIAL_SEARCH_BAR)

        # 2. Type the medicine name
        self.enter_text(
            self.SEARCH_BOX,
            medicine_name
        )

        # 3. Hit ENTER to submit the search
        search_box = self.wait.until(
            EC.visibility_of_element_located(
                self.SEARCH_BOX
            )
        )
        search_box.send_keys(Keys.RETURN)

        # 4. Wait for the results to load
        self.wait.until(
            EC.presence_of_element_located(
                self.SEARCH_RESULTS
            )
        )

    def verify_search_results(self):
        elements = self.driver.find_elements(
            *self.SEARCH_RESULTS
        )
        return len(elements) > 0