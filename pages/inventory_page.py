from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):

    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    BACKPACK_ADD_BUTTON = (
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    )

    BACKPACK_REMOVE_BUTTON = (
        By.ID,
        "remove-sauce-labs-backpack"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def is_inventory_page_loaded(self):
        return self.is_displayed(self.PRODUCTS_TITLE)

    def add_backpack_to_cart(self):
        self.click(self.BACKPACK_ADD_BUTTON)

    def remove_backpack(self):
        self.click(self.BACKPACK_REMOVE_BUTTON)

    def open_cart(self):
        self.click(self.CART_ICON)

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)