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
