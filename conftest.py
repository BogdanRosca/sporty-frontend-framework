from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure
import logging
import os
import pytest
import subprocess
import threading
import time
import yaml


logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="mobile",
        help="Environment to run tests against"
    )


def load_config(env):
    """Helper function to load configuration from YAML file"""

    config_path = os.path.join("config", f"{env}.yaml")

    if os.path.exists(config_path):
        with open(config_path) as f:
            return yaml.safe_load(f)
    else:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")


@pytest.fixture(scope="session")
def config(request):
    """Read content of config file passed through --env flag"""

    env = request.config.getoption("--env")
    return load_config(env)


@pytest.fixture(scope="function")
def driver(config):
    """Setup and teardown for Selenium WebDriver"""
    chrome_options = Options()

    if config.get("mode") == "mobile":
        print("\n")
        print("Running tests with mobile configuration")
        print(f"Emulating {config.get('emulator_device')} device\n")
        mobile_emulation = {"deviceName": config.get("emulator_device")}
        chrome_options.add_experimental_option(
            "mobileEmulation",
            mobile_emulation
        )
        chrome_options.add_argument('--window-size=390,844')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(config.get("timeout", 10))

    yield driver

    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def allure_report_generator(config):
    """
    Generates and serves Allure report after all tests complete
    """
    yield  # Allows tests to run first

    if config.get("generate_report"):

        def generate_and_serve_report():
            try:
                result = subprocess.run(
                    ["allure", "serve", "allure_results"],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print("✅ Allure report generated successfully!")
                else:
                    print("❌ Failed to generate Allure report:")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error generating Allure report: {e}")

        # Run in a separate thread to avoid blocking test execution
        report_thread = threading.Thread(target=generate_and_serve_report)
        report_thread.daemon = True
        report_thread.start()


@pytest.fixture
def screenshot_on_teardown(config, driver):
    """Take screenshot of viewport at the end of the test"""
    yield  # Allows tests to run first

    time.sleep(60)
    logger.info("Wait 60 seconds")
    screenshot_path = os.path.join(
        config.get('screenshot_folder'),
        'screenshot.png'
    )
    driver.save_screenshot(screenshot_path)
    logger.info(f"Snapshot saved at: {screenshot_path}")

    with open(screenshot_path, "rb") as image_file:
        allure.attach(
            image_file.read(),
            name="Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
