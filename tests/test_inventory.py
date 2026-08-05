def test_inventory_page_loaded(inventory_page):

    assert inventory_page.is_inventory_page_loaded()


def test_add_backpack(inventory_page):

    inventory_page.add_backpack_to_cart()

    assert inventory_page.get_cart_count() == "1"


def test_remove_backpack(inventory_page):

    inventory_page.add_backpack_to_cart()

    inventory_page.remove_backpack()

    assert not inventory_page.is_displayed(
        inventory_page.CART_BADGE
    )