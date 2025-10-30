from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pytest
import subprocess
import threading
import yaml


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against"
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


def pytest_configure(config):
    """Configure pytest with dynamic options based on environment config file"""
    
    env = config.getoption("--env", default="mobile")
    
    try:
        env_config = load_config(env)
        
        if env_config.get("reruns"):
            config.option.reruns = env_config.get("reruns")
            config.option.reruns_delay = env_config.get("reruns_delay", 1)
            print(f"Configured reruns: {env_config.get('reruns')} with delay: {env_config.get('reruns_delay', 1)}s")

        if env_config.get("run_in_parallel"):
            workers = env_config.get("run_in_parallel")
            config.option.numprocesses = workers
            print(f"Configured parallel execution: {workers} workers")

    except FileNotFoundError as e:
        print(f"Warning: {e}")


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


@pytest.fixture(scope="session", autouse=True)
def allure_report_generator(config):
    """
    Session-scoped fixture that generates and serves Allure report after all tests complete.
    This fixture runs automatically (autouse=True) and doesn't need to be explicitly called.
    """
    yield  # Allows tests to run first
    
    if config.get("generate_report"):
        
        def generate_and_serve_report():
            try:
                # Generate the report
                result = subprocess.run(["allure", "serve", "allure-result"])
                
                if result.returncode == 0:
                    print("✅ Allure report generated successfully!")
                    print("📊 Opening report in browser...")        
                else:
                    print("❌ Failed to generate Allure report:")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error generating Allure report: {e}")
        
        # Run in a separate thread to avoid blocking test execution
        report_thread = threading.Thread(target=generate_and_serve_report)
        report_thread.daemon = True
        report_thread.start()
