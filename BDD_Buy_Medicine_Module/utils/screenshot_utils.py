import os
from datetime import datetime


def capture_screenshot(driver, test_name):

    folder_path = os.path.join(
        "reports",
        "screenshots"
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_name = f"{test_name}_{timestamp}.png"

    file_path = os.path.join(
        folder_path,
        file_name
    )

    driver.save_screenshot(
        file_path
    )

    return file_path