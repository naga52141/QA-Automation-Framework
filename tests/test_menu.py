def test_logout_returns_to_login_page(inventory_page):

    inventory_page.open_menu()
    inventory_page.logout()

    assert inventory_page.driver.current_url.rstrip("/") == "https://www.saucedemo.com"


def test_all_items_link_returns_to_inventory(inventory_page):

    inventory_page.open_product(index=0)

    inventory_page.open_menu()
    inventory_page.click_all_items()

    assert inventory_page.is_inventory_page_loaded()


def test_about_link_points_to_sauce_labs(inventory_page):

    inventory_page.open_menu()

    assert "saucelabs.com" in inventory_page.get_about_link_href()


def test_reset_app_state_clears_cart(inventory_page):

    inventory_page.add_backpack_to_cart()

    inventory_page.open_menu()
    inventory_page.reset_app_state()

    assert not inventory_page.is_displayed(inventory_page.CART_BADGE)
