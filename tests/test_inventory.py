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


def test_sort_name_z_to_a(inventory_page):

    inventory_page.sort_by("za")

    names = inventory_page.get_product_names()

    assert names == sorted(names, reverse=True)


def test_sort_price_low_to_high(inventory_page):

    inventory_page.sort_by("lohi")

    prices = inventory_page.get_product_prices()

    assert prices == sorted(prices)


def test_sort_price_high_to_low(inventory_page):

    inventory_page.sort_by("hilo")

    prices = inventory_page.get_product_prices()

    assert prices == sorted(prices, reverse=True)


def test_add_and_remove_every_product(inventory_page):

    for product_id in inventory_page.PRODUCT_IDS:
        inventory_page.add_product_to_cart(product_id)

    assert inventory_page.get_cart_count() == str(
        len(inventory_page.PRODUCT_IDS)
    )

    for product_id in inventory_page.PRODUCT_IDS:
        inventory_page.remove_product_from_cart(product_id)

    assert not inventory_page.is_displayed(
        inventory_page.CART_BADGE
    )