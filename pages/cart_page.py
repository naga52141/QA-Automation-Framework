from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def __init__(self, driver):
        super().__init__(driver)

    def get_cart_items_count(self):
        return len(self.driver.find_elements(*self.CART_ITEM))

    def get_cart_item_names(self):
        names = self.driver.find_elements(*self.ITEM_NAMES)
        return [name.text for name in names]

    def remove_item(self, product_id):
        self.click((By.ID, f"remove-{product_id}"))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
