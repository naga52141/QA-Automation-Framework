from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_continue_shopping_returns_to_inventory(cart_page):

    cart_page.continue_shopping()

    inventory_page = InventoryPage(cart_page.driver)

    assert inventory_page.is_inventory_page_loaded()


def test_remove_item_from_cart_page(cart_page):

    assert cart_page.get_cart_items_count() == 1

    cart_page.remove_item("sauce-labs-backpack")

    assert cart_page.get_cart_items_count() == 0


def test_multiple_items_in_cart(inventory_page):

    inventory_page.add_backpack_to_cart()
    inventory_page.add_product_to_cart("sauce-labs-bike-light")
    inventory_page.open_cart()

    cart_page = CartPage(inventory_page.driver)

    names = cart_page.get_cart_item_names()

    assert cart_page.get_cart_items_count() == 2
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names
