def test_failing(config):
    assert True == False

def test_config(config):
    assert config["base_url"] == "https://m.twitch.tv/"

def test_open_page(driver, config):
    """Simple test to open the base URL and verify page loads"""
    driver.get(config["base_url"])
    
    assert driver.title != ""
    
    current_url = driver.current_url
    assert current_url == config["base_url"]