from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config_reader import read_config


def get_driver():

    # READ CONFIG
    config = read_config()

    browser = config.get(
        "DEFAULT",
        "browser"
    )

    implicit_wait = config.get(
        "DEFAULT",
        "implicit_wait"
    )

    if browser.lower() == "chrome":

        chrome_options = Options()

        chrome_options.add_argument(
            "--start-maximized"
        )

        chrome_options.add_argument(
            "--disable-notifications"
        )

        chrome_options.add_argument(
            "--disable-popup-blocking"
        )

        driver = webdriver.Chrome(
            options=chrome_options
        )

        driver.implicitly_wait(
            int(implicit_wait)
        )

        return driver

    else:

        raise Exception(
            f"Browser '{browser}' is not supported."
        )