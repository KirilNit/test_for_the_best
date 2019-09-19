from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from utils.logger import WebDrLogger
from selenium.webdriver.common.keys import Keys


class WebDriver(object):

    def __init__(self, browser="Chrome", browser_path='',
                 chrome_path='', driver=None):
        self.driver = driver if driver else webdriver.Chrome()
        self.logger = WebDrLogger(__name__)
        self.by = By
        self.timeout = 15
        super(WebDriver, self).__init__()

    def go_to_url(self, url):
        self.driver.get(url)

    def wait_for_web_element_to_be_located(self, element: str, timeout=False):
        wait = WebDriverWait(self.driver, timeout=timeout or self.timeout)
        self.logger.info(f"Waiting for WebElement with locator {element}")
        messageError = f"Element with locator {element} was not found after {timeout or self.timeout} seconds"
        web_element = wait.until(EC.presence_of_element_located((By.XPATH, element)), message=messageError)

        return web_element

    def wait_for_visibility_of_web_element(self, element: str, timeout=False):
        wait = WebDriverWait(self.driver, timeout=timeout or self.timeout)
        self.logger.info(f"Waiting for WebElement with locator {element}")
        messageError = f"Element with locator {element} was not visible after {timeout or self.timeout} seconds"
        web_element = wait.until(EC.visibility_of_element_located((By.XPATH, element)), message=messageError)
        return web_element

    def wait_for_web_element_to_be_clickable(self, element: str, timeout=False):
        wait = WebDriverWait(self.driver, timeout=timeout or self.timeout)
        self.logger.info(f"Waiting for WebElement with locator {element}")
        messageError = f"Element with locator {element} was not clickable after {timeout or self.timeout} seconds"
        self.wait_for_visibility_of_web_element(element)
        web_element = wait.until(EC.element_to_be_clickable((By.XPATH, element)), message=messageError)
        return web_element

    def wait_for_presence_of_element_located(self, element: str, timeout=False):
        wait = WebDriverWait(self.driver, timeout=timeout or self.timeout)
        self.logger.info(f"Waiting for WebElement with locator {element}")
        messageError = f"Element with locator {element} was not present after {timeout or self.timeout} seconds"
        self.wait_for_visibility_of_web_element(element)
        web_element = wait.until(EC.presence_of_element_located((By.XPATH, element)), message=messageError)
        return web_element

    def click_web_element(self, element: str, timeout=30):
        start_time = time.time()
        while time.time() < (start_time + timeout):
            element = self.wait_for_web_element_to_be_clickable(element)
            try:
                if element.is_displayed():
                    element.click()
                    break
            except Exception as e:
                self.logger.info(e)

    def set_web_element_text(self, element: str, text):
        try:
            web_element = self.driver.find_element_by_xpath(element)
            web_element.clear()
            web_element.send_keys(text)
        except (WebDriverException, StaleElementReferenceException) as ex:
            raise Exception("Fail in set_web_element_text with Exception - {}".format(ex))

    def get_web_element_text(self, path: str):
        text = self.driver.find_element_by_xpath(path).text
        return text

    def get_page_source(self):
        return self.driver.page_source

    def text_content(self, element):
        return self.driver.find_element_by_xpath(element).get_attribute('textContent')
