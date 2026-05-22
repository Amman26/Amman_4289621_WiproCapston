from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

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

        self.click_element(
            self.BUY_MEDICINES_LINK
        )

    def search_medicine(self, medicine_name):

        # CLICK INITIAL SEARCH BAR
        self.click_element(
            self.INITIAL_SEARCH_BAR
        )

        # WAIT FOR SEARCH BOX
        search_box = self.wait.until(
            EC.visibility_of_element_located(
                self.SEARCH_BOX
            )
        )

        # CLEAR EXISTING TEXT
        search_box.clear()

        # ENTER MEDICINE NAME
        search_box.send_keys(
            medicine_name
        )

        # PRESS ENTER
        search_box.send_keys(
            Keys.RETURN
        )

    def verify_search_results(self):

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    self.SEARCH_RESULTS
                )
            )

            elements = self.driver.find_elements(
                *self.SEARCH_RESULTS
            )

            return len(elements) > 0

        except TimeoutException:

            return False