from pages.directory_page import DirectoryPage


def test_start_streaming(driver, config, screenshot_on_teardown):
    """Validate streaming of a StarCraft II game"""
    page = DirectoryPage(driver)

    page.open(config)
    page.search(text="StarCraft II")
    page.scroll_down(times=2)
    page.start_streaming()
