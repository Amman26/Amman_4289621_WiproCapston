import pytest

from utils.driver_factory import get_driver
from utils.config_reader import read_config
from utils.screenshot_utils import capture_screenshot

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


# Screenshot capture on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            try:
                capture_screenshot(driver, item.name)

            except Exception as e:
                print(f"Screenshot capture failed: {e}")