from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException





class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type(self, locator, text):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def get_value(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).get_attribute("value")

    def is_displayed(self, locator):
        try:
            element = self.wait.until(
            EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
            return False