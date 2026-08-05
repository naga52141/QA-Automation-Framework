from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductDetailPage(BasePage):

    PRODUCT_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESC = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    ADD_BUTTON = (By.ID, "add-to-cart")
    REMOVE_BUTTON = (By.ID, "remove")
    BACK_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_text(self.PRODUCT_PRICE)

    def add_to_cart(self):
        self.click(self.ADD_BUTTON)

    def remove_from_cart(self):
        self.click(self.REMOVE_BUTTON)

    def go_back(self):
        self.click(self.BACK_BUTTON)
