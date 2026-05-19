import pytest

from utils.logger import setup_logger

logger = setup_logger()


@pytest.mark.order(1)
def test_website_launch(driver):

    logger.info("Starting Website Launch Test")

    assert "Apollo" in driver.title

    logger.info("Apollo 24/7 website launched successfully")