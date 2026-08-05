from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):

    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    FOOTER_SOCIAL_LINKS = (By.CSS_SELECTOR, ".social a")

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")

    PRODUCT_IDS = [
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
        "sauce-labs-fleece-jacket",
        "sauce-labs-onesie",
        "test.allthethings()-t-shirt-(red)",
    ]

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

    def add_product_to_cart(self, product_id):
        self.click((By.ID, f"add-to-cart-{product_id}"))

    def remove_product_from_cart(self, product_id):
        self.click((By.ID, f"remove-{product_id}"))

    def open_cart(self):
        self.click(self.CART_ICON)

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)

    def get_product_image_sources(self):
        images = self.driver.find_elements(*self.PRODUCT_IMAGES)
        return [image.get_attribute("src") for image in images]

    def get_product_names(self):
        names = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [name.text for name in names]

    def get_product_prices(self):
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(price.text.replace("$", "")) for price in prices]

    def sort_by(self, value):
        select = Select(
            self.wait.until(
                lambda driver: driver.find_element(*self.SORT_DROPDOWN)
            )
        )
        select.select_by_value(value)
        self.logger.info(f"Sorted products by: {value}")

    def open_product(self, index=0):
        products = self.driver.find_elements(*self.PRODUCT_NAMES)
        products[index].click()
        self.logger.info(f"Opened product detail at index: {index}")

    def open_menu(self):
        self.click(self.MENU_BUTTON)

    def click_all_items(self):
        self.click(self.ALL_ITEMS_LINK)

    def click_about(self):
        self.click(self.ABOUT_LINK)

    def get_about_link_href(self):
        return self.get_attribute(self.ABOUT_LINK, "href")

    def logout(self):
        self.click(self.LOGOUT_LINK)

    def reset_app_state(self):
        self.click(self.RESET_APP_STATE_LINK)

    def get_footer_social_links(self):
        links = self.driver.find_elements(*self.FOOTER_SOCIAL_LINKS)
        return [link.get_attribute("href") for link in links]
