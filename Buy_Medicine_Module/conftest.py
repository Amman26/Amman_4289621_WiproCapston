import pytest

from utils.driver_factory import get_driver
from utils.config_reader import read_config
from pages.base_page import BasePage


config = read_config()

base_url = config.get("DEFAULT", "base_url")


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()

    driver.get(base_url)

    # Close promotional popup if present
    base_page = BasePage(driver)

    base_page.close_promotional_popup()

    yield driver

    driver.quit()