from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Selenium natively handles downloading the exact right driver now!
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    return driver