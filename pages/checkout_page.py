from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    SUMMARY_SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)

    def get_total_text(self):
        return self.get_text(self.SUMMARY_TOTAL_LABEL)

    def get_subtotal_amount(self):
        text = self.get_text(self.SUMMARY_SUBTOTAL_LABEL)
        return float(text.split("$")[1])

    def get_tax_amount(self):
        text = self.get_text(self.SUMMARY_TAX_LABEL)
        return float(text.split("$")[1])

    def get_total_amount(self):
        return float(self.get_total_text().split("$")[1])

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)

    def is_order_complete(self):
        return self.is_displayed(self.COMPLETE_HEADER)

    def get_complete_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def go_back_home(self):
        self.click(self.BACK_HOME_BUTTON)
