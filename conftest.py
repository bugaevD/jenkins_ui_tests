import os

import pytest
from dotenv import load_dotenv
from pygments.styles import default
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils import attach

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to use",
        choices=("chrome", "firefox", "edge")
    )
    parser.addoption(
        "--browser_version",
        default="128.0",
        help="Browser version to use",
        choices=("127.0", "128.0", "129.0b")
    )
    parser.addoption(
        "--headless",
        action="store",
        default=False,
        help="Run browser in headless mode",
        choices=("True", "False")
    )
    parser.addoption(
        "--window_size",
        default="1920x1080",
        help="Size of window to use",
        choices=("1920x1080", "2560x1440", "1280x720")
    )
    parser.addoption(
        "--base_url",
        default=os.getenv("BASE_URL"),
        help="website url"
    )


@pytest.fixture
def setup_browser(request):
    browser = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    headless = request.config.getoption("--headless")
    window_size = request.config.getoption("--window_size")

    selenoid_url = os.getenv("SELENOID_URL")
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    command_executor = f"https://{login}:{password}@{selenoid_url}"

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "safari":
        options = EdgeOptions()
    else:
        raise pytest.UsageError("Please choose chrome or firefox or edge")

    if headless:
        options.add_argument("--headless")

    options.add_argument(f"--window-size={window_size}")

    selenoid_capabilities = {
        "browserName": browser,
        "browserVersion": '128.0',
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=options
    )
    yield driver
    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)
    driver.quit()


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture
def create_test_file():
    file_path = os.path.join(os.path.dirname(__file__), "test_png.png")
    with open(file_path, "w") as file:
        file.write("test")
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)
