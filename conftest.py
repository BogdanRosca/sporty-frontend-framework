import yaml
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against"
    )

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    path = os.path.join("config", f"{env}.yaml")
    with open(path) as f:
        data = yaml.safe_load(f)
    return data

@pytest.fixture(scope="function")
def driver(config):
    """Setup and teardown for Selenium WebDriver"""
    chrome_options = Options()
    
    if config.get("mode") == "mobile":
        print("\n")
        print("Running tests with mobile configuration")
        print(f"Emulating {config.get('emulator_device')} device\n")
        mobile_emulation = {"deviceName": config.get("emulator_device")}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(config.get("timeout", 10))
    
    yield driver
    
    driver.quit()