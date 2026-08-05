import logging
import os
from datetime import datetime

import allure
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
    config.addinivalue_line(
        "markers", "visual: marks visual-regression tests (Chrome-baseline only)"
    )


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests in: chrome, firefox, edge, or safari",
    )


@pytest.fixture
def driver(request):

    browser = request.config.getoption("--browser")
    headless = bool(os.getenv("CI"))

    if browser == "firefox":
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        driver = webdriver.Firefox(options=options)

        if not headless:
            driver.maximize_window()

    elif browser == "edge":
        options = webdriver.EdgeOptions()

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        driver = webdriver.Edge(options=options)

    elif browser == "safari":
        driver = webdriver.Safari()
        driver.maximize_window()

    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)
    yield driver

    driver.quit()

@pytest.fixture
def mobile_driver():

    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 2.0},
        "userAgent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
            "Mobile/15E148 Safari/604.1"
        ),
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    if os.getenv("CI"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)
    yield driver

    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def mobile_login_page(mobile_driver):
    return LoginPage(mobile_driver)

@pytest.fixture
def mobile_inventory_page(mobile_driver):

    login = LoginPage(mobile_driver)

    login.login(
        "standard_user",
        "secret_sauce"
    )

    return InventoryPage(mobile_driver)

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

        driver = item.funcargs.get("driver") or item.funcargs.get("mobile_driver")

        if driver:
            # A test failure can leave the browser/session in a bad state,
            # and screenshot capture over the WebDriver wire can then hang
            # for the full 120s command timeout. Uncaught, that exception
            # crashes the whole xdist session (seen locally and in CI on a
            # completely fresh runner -- not a one-off fluke). Never let
            # failure-reporting itself take down the test run.
            try:
                os.makedirs("screenshots", exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshots/{item.name}_{timestamp}.png"

                screenshot_png = driver.get_screenshot_as_png()

                with open(filename, "wb") as screenshot_file:
                    screenshot_file.write(screenshot_png)

                allure.attach(
                    screenshot_png,
                    name="failure screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as screenshot_error:
                logging.getLogger().warning(
                    f"Could not capture failure screenshot for "
                    f"{item.nodeid}: {screenshot_error}"
                )