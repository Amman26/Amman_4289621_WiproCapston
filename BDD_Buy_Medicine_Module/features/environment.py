import time
import allure

from utils.driver_factory import get_driver
from utils.config_reader import read_config
from utils.screenshot_utils import capture_screenshot
from pages.base_page import BasePage


config = read_config()

base_url = config.get("DEFAULT", "base_url")


# =====================================================
# BEFORE SCENARIO
# =====================================================

def before_scenario(context, scenario):

    # START DRIVER
    context.driver = get_driver()

    # OPEN APPLICATION
    context.driver.get(base_url)

    # WAIT FOR REACT APP TO LOAD (IMPORTANT)
    time.sleep(2)

    # CLOSE POPUP IF PRESENT
    try:
        base_page = BasePage(context.driver)
        base_page.close_promotional_popup()
    except Exception:
        pass


# =====================================================
# AFTER SCENARIO
# =====================================================

def after_scenario(context, scenario):

    if hasattr(context, "driver") and context.driver:

        try:
            screenshot_path = capture_screenshot(
                context.driver,
                scenario.name.replace(" ", "_")
            )

            with open(screenshot_path, "rb") as file:
                allure.attach(
                    file.read(),
                    name=scenario.name,
                    attachment_type=allure.attachment_type.PNG
                )

        except Exception as e:
            print(f"Screenshot Capture Failed : {e}")

        finally:
            try:
                context.driver.quit()
            except Exception:
                pass