from pages.product_detail_page import ProductDetailPage


def test_product_detail_shows_matching_name(inventory_page):

    names = inventory_page.get_product_names()
    inventory_page.open_product(index=0)

    detail_page = ProductDetailPage(inventory_page.driver)

    assert detail_page.get_product_name() == names[0]


def test_add_and_remove_from_detail_page(inventory_page):

    inventory_page.open_product(index=0)

    detail_page = ProductDetailPage(inventory_page.driver)
    detail_page.add_to_cart()

    assert inventory_page.is_displayed(inventory_page.CART_BADGE)

    detail_page.remove_from_cart()

    assert not inventory_page.is_displayed(inventory_page.CART_BADGE)


def test_back_button_returns_to_inventory(inventory_page):

    inventory_page.open_product(index=0)

    detail_page = ProductDetailPage(inventory_page.driver)
    detail_page.go_back()

    assert inventory_page.is_inventory_page_loaded()
