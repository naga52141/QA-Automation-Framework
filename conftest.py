import os
from datetime import datetime

import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from utilities.config import BASE_URL
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage



def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (e.g. performance_glitch_user)"
    )


@pytest.fixture
def driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--incognito")

    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)
    yield driver

    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def inventory_page(driver):

    login = LoginPage(driver)

    login.login(
        "standard_user",
        "secret_sauce"
    )

    return InventoryPage(driver)

@pytest.fixture
def cart_page(inventory_page):

    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    return CartPage(inventory_page.driver)

@pytest.fixture
def checkout_page(cart_page):

    cart_page.checkout()

    return CheckoutPage(cart_page.driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:
            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{item.name}_{timestamp}.png"

            driver.save_screenshot(filename)