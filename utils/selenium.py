from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Literal
import logging
import time


logger = logging.getLogger(__name__)


class Selenium:
    """ Wrapper class over Selenium commands """
    def __init__(self, driver: webdriver, timeout: int = 10) -> None:
        self.driver = driver
        self.timeout = timeout

    def _find(self, locator: str) -> WebElement:
        """ Waits untill an element is found or timeouts """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def _find_all(self, locator: str) -> list[WebElement]:
        """ Waits untill a list of elements are found or timeouts """
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    def click(self, locator: str) -> None:
        """ Finds element by locator, waits till clickable and performs action or timeouts """
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        logger.info(f"Clicked {locator}")

    def type(self, locator: str , text: str, clear_first: bool = True) -> None:
        """ Finds input field by locator and sends keys """
        element = self._find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Typed '{text}' into {locator}")
    
    def hit_enter(self, locator: str) -> None:
        """ Finds input field by locator and press ENTER """
        element = self._find(locator)
        element.send_keys(Keys.RETURN)
        logger.info(f"Hit ENTER")

    def scroll(self, direction: Literal['top', 'left', 'right', 'bottom'], pixels: int, type: Literal['smooth', 'auto'] = 'smooth') -> None:
        """ Scrolls by specified pixels in the specified direction """
        self.driver.execute_script(f"""
            window.scrollBy({{
                {direction}: {pixels},
                behavior: '{type}'
            }});
        """)
        logger.info(f"Scrolled {type} {pixels} pixels in direction: {direction}")
        time.sleep(2)

    def is_visible(self, locator: str) -> bool:
        """ Checks if an element is visible """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
        
    def is_not_visible(self, locator: str) -> bool:
        """ Checks if an element is not visible or not present """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
