def test_failing(config):
    """Failing test to validate rerun"""
    assert False


def test_config(config):
    """Check loading of configuration through conftest fixture"""
    assert config["base_url"] == "https://m.twitch.tv"


def test_open_page(driver, config):
    """Simple test to open the base URL and verify page loads"""
    driver.get(config["base_url"])

    assert driver.title != ""

    current_url = driver.current_url
    assert current_url == config["base_url"] + "/"


def test_youtube(driver):
    driver.get('https://www.youtube.com/')
    driver.get('https://www.youtube.com/watch?v=jyFXlF9olfI')
