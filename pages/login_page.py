from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger


class LoginPage(BasePage):

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "h3[data-test='error']"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    def login(self, username, password):

        self.logger.info(
            "Entering Username"
        )

        self.type(
            self.USERNAME,
            username
        )

        self.logger.info(
            "Entering Password"
        )

        self.type(
            self.PASSWORD,
            password
        )

        self.logger.info(
            "Clicking Login Button"
        )

        self.click(
            self.LOGIN_BUTTON
        )

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_successful(self):
        return "inventory" in self.driver.current_url