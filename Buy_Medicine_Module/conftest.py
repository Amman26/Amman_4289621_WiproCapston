import pytest

from utils.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()

    driver.get("https://www.apollo247.com/")

    yield driver

    driver.quit()