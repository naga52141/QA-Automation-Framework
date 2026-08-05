from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.logger import get_logger




class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = get_logger()

    def click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()
        self.logger.info(f"Clicked element: {locator}")

    def type(self, locator, text):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Typed into element: {locator}")

    def get_text(self, locator):
        text = self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text
        self.logger.info(f"Read text '{text}' from element: {locator}")
        return text

    def get_value(self, locator):
        value = self.wait.until(
            EC.visibility_of_element_located(locator)
        ).get_attribute("value")
        self.logger.info(f"Read value '{value}' from element: {locator}")
        return value

    def get_attribute(self, locator, name):
        value = self.wait.until(
            EC.visibility_of_element_located(locator)
        ).get_attribute(name)
        self.logger.info(f"Read attribute '{name}'='{value}' from element: {locator}")
        return value

    def is_displayed(self, locator):
        try:
            element = self.wait.until(
            EC.visibility_of_element_located(locator)
            )
            displayed = element.is_displayed()
            self.logger.info(f"Element displayed ({displayed}): {locator}")
            return displayed
        except TimeoutException:
            self.logger.info(f"Element not displayed (timeout): {locator}")
            return False
