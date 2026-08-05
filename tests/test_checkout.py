def test_checkout_requires_first_name(checkout_page):

    checkout_page.fill_checkout_info("", "Doe", "12345")

    assert "First Name is required" in checkout_page.get_error_message()


def test_checkout_requires_postal_code(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "")

    assert "Postal Code is required" in checkout_page.get_error_message()


def test_checkout_shows_total(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "12345")

    assert "Total" in checkout_page.get_total_text()


def test_checkout_complete_flow(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "12345")
    checkout_page.finish_checkout()

    assert checkout_page.is_order_complete()
    assert "Thank you for your order" in checkout_page.get_complete_message()


def test_checkout_requires_last_name(checkout_page):

    checkout_page.fill_checkout_info("John", "", "12345")

    assert "Last Name is required" in checkout_page.get_error_message()


def test_checkout_step_one_cancel_returns_to_cart(checkout_page):

    checkout_page.cancel()

    assert "cart.html" in checkout_page.driver.current_url


def test_checkout_step_two_cancel_returns_to_inventory(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "12345")
    checkout_page.cancel()

    assert "inventory.html" in checkout_page.driver.current_url


def test_checkout_total_equals_subtotal_plus_tax(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "12345")

    subtotal = checkout_page.get_subtotal_amount()
    tax = checkout_page.get_tax_amount()
    total = checkout_page.get_total_amount()

    assert round(subtotal + tax, 2) == round(total, 2)


def test_back_home_button_returns_to_inventory(checkout_page):

    checkout_page.fill_checkout_info("John", "Doe", "12345")
    checkout_page.finish_checkout()
    checkout_page.go_back_home()

    assert "inventory.html" in checkout_page.driver.current_url
