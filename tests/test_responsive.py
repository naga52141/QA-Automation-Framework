def test_login_works_on_mobile_viewport(mobile_login_page):

    mobile_login_page.login("standard_user", "secret_sauce")

    assert mobile_login_page.is_login_successful()


def test_add_to_cart_works_on_mobile_viewport(mobile_inventory_page):
    # Native click() has been observed to hang intermittently under
    # headless + mobile emulation on more than just the hamburger menu
    # (verified live: this exact button hung on one run) -- click_via_js
    # sidesteps it, same as the menu interaction below.

    assert mobile_inventory_page.is_inventory_page_loaded()

    mobile_inventory_page.click_via_js(mobile_inventory_page.BACKPACK_ADD_BUTTON)

    assert mobile_inventory_page.get_cart_count() == "1"


def test_hamburger_menu_usable_on_mobile_viewport(mobile_inventory_page):

    mobile_inventory_page.click_via_js(mobile_inventory_page.MENU_BUTTON)
    mobile_inventory_page.click_via_js(mobile_inventory_page.LOGOUT_LINK)

    assert (
        mobile_inventory_page.driver.current_url.rstrip("/")
        == "https://www.saucedemo.com"
    )
