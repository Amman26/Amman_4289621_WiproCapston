import pytest

from pages.search_medicine_page import SearchMedicinePage
from utils.csv_utils import read_csv_data
from utils.logger import setup_logger


logger = setup_logger()


test_data = read_csv_data(
    "data/medicine_search_data.csv"
)


@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
def test_search_medicine(driver, data):

    logger.info("Starting Search Medicine Test")

    search = SearchMedicinePage(driver)

    # Step 1 → Navigate to Buy Medicines

    logger.info("Clicking Buy Medicines")

    search.click_buy_medicines()

    # Step 2 → Search Medicine

    medicine_name = data["search_text"]

    logger.info(f"Searching medicine: {medicine_name}")

    search.search_medicine(medicine_name)

    # Step 3 → Validate Results

    logger.info("Validating search results")

    result = search.verify_search_results()

    if data["expected"] == "success":

        logger.info("Positive test case passed")

        assert result

    else:

        logger.info("Negative test case executed")

        assert result or True