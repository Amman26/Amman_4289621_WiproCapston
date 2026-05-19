import pytest

from pages.search_medicine_page import SearchMedicinePage
from pages.product_page import ProductPage
from utils.csv_utils import read_csv_data


test_data = read_csv_data(
    "data/product_validation_data.csv"
)

@pytest.mark.order(5)
@pytest.mark.parametrize("data", test_data)
def test_product_validation(driver, data):
    search = SearchMedicinePage(driver)
    product = ProductPage(driver)
    medicine_name = data["product_name"]

    # ADD THIS STEP: Navigate to the Buy Medicines section first
    search.click_buy_medicines()

    search.search_medicine(medicine_name)
    product.add_first_product_to_cart()

    actual_title = product.get_product_title()
    assert medicine_name.lower() in actual_title.lower()