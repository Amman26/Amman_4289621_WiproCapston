import os
import allure

from datetime import datetime


def capture_screenshot(driver, test_name):

    # SCREENSHOT FOLDER
    folder_path = "reports/screenshots"

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    # TIMESTAMP
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # FILE NAME
    file_name = f"{test_name}_{timestamp}.png"

    # FULL PATH
    file_path = os.path.join(
        folder_path,
        file_name
    )

    # SAVE SCREENSHOT
    driver.save_screenshot(
        file_path
    )

    # ATTACH TO ALLURE REPORT
    allure.attach.file(
        file_path,
        name=test_name,
        attachment_type=allure.attachment_type.PNG
    )

    return file_path