import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach


@pytest.fixture
def setup_browser():
    options = Options()

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": '128.0',
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor='https://user1:1234@selenoid.autotests.cloud/wd/hub',
        options=options
    )
    yield driver
    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)
    driver.quit()


@pytest.fixture
def create_test_file(setup_browser):
    file_path = os.path.join(os.path.dirname(__file__), "test_png.png")
    with open(file_path, "w") as file:
        file.write("test")
    yield file_path
    os.remove(file_path)
