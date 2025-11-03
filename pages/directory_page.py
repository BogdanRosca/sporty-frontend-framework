from selenium.webdriver.common.by import By
from utils.selenium import Selenium
import logging


logger = logging.getLogger(__name__)


class DirectoryPage(Selenium):

    CHANNELS_SECTION = (By.XPATH, "//*[@class='tw-title' and contains(text(), 'Channels')]")
    COOKIES_ACCEPT = (By.XPATH, "//*[@data-a-target='tw-core-button-label-text'][.//div[contains(text(), 'Accept')]]")
    COOKIES_BANNER = (By.CLASS_NAME, "consent-banner")
    COOKIES_REJECT = (By.XPATH, "//*[@data-a-target='tw-core-button-label-text'][.//div[contains(text(), 'Reject')]]")
    LIVE_STREAMS = (By.XPATH, "//button[contains(@class, 'tw-link') and .//div[contains(@class, 'tw-channel-status-text-indicator')]]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-a-target='tw-input']")

    def _cookies(self, accept: bool = True):
        """ Accepts or rejects cookies if the banner is visible """
        if self.is_visible(self.COOKIES_BANNER):
            if accept:
                self.click(self.COOKIES_ACCEPT)
                self.is_not_visible(self.COOKIES_BANNER)
            else:
                self.click(self.COOKIES_REJECT)
                self.is_not_visible(self.COOKIES_BANNER)
        else:
            pass

    def open(self, config):
        """ Opens /directory page """
        URL = f"{config['base_url']}/directory"
        self.driver.get(URL)
        self.is_visible(self.SEARCH_BUTTON)
        if self.driver.current_url != URL:
            raise RuntimeError(f"Not on {URL}")
        self._cookies(accept=True)

    def search(self, text: str):
        """  Types text in specified input element and press ENTER """
        self.type(self.SEARCH_BUTTON, text, clear_first=True)
        self.hit_enter(self.SEARCH_BUTTON)
        self.is_visible(self.CHANNELS_SECTION)

    def scroll_down(self, times: int):
        """ Performs scroll action in direction and for specified distance """
        for _ in range(times):
            self.scroll(direction='top', pixels=100, type='smooth')

    def start_streaming(self, index: int = 2):
        """ Click on a stream button by index """
        live_streams = self._find_all(self.LIVE_STREAMS)
        if live_streams:
            if index < len(live_streams):
                live_streams[index].click()
                logger.info(f"Clicked on stream at index {index} (total found: {len(live_streams)})")
            else:
                logger.error(f"Index {index} out of range. Only {len(live_streams)} streams found")
        else:
            logger.error("No live streams found")
