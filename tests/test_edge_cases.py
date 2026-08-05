import time

import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_problem_user_images_are_broken(login_page):

    login_page.login("problem_user", "secret_sauce")

    inventory_page = InventoryPage(login_page.driver)
    image_sources = inventory_page.get_product_image_sources()

    assert len(set(image_sources)) == 1


def test_problem_user_checkout_fields_are_broken(login_page):

    login_page.login("problem_user", "secret_sauce")

    inventory_page = InventoryPage(login_page.driver)
    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    cart_page = CartPage(login_page.driver)
    cart_page.checkout()

    checkout_page = CheckoutPage(login_page.driver)
    checkout_page.type(checkout_page.FIRST_NAME, "John")
    checkout_page.type(checkout_page.LAST_NAME, "Doe")

    first_name_value = checkout_page.get_value(checkout_page.FIRST_NAME)
    last_name_value = checkout_page.get_value(checkout_page.LAST_NAME)

    assert first_name_value != "John" or last_name_value != "Doe"


@pytest.mark.slow
def test_performance_glitch_user_login_is_slow(login_page):

    start = time.time()

    login_page.login("performance_glitch_user", "secret_sauce")

    assert login_page.is_login_successful()
    assert time.time() - start > 2


def test_error_user_remove_from_cart_is_broken(login_page):

    login_page.login("error_user", "secret_sauce")

    inventory_page = InventoryPage(login_page.driver)
    inventory_page.add_backpack_to_cart()
    inventory_page.remove_backpack()

    assert inventory_page.is_displayed(inventory_page.CART_BADGE)


def test_visual_user_first_product_image_is_broken(login_page):

    login_page.login("visual_user", "secret_sauce")

    inventory_page = InventoryPage(login_page.driver)
    image_sources = inventory_page.get_product_image_sources()

    assert "sl-404" in image_sources[0]
