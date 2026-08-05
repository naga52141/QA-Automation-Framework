import pytest
from axe_selenium_python import Axe
from selenium.webdriver.common.keys import Keys


def _run_axe_and_log(page):

    axe = Axe(page.driver)
    axe.inject()
    results = axe.run()

    for violation in results["violations"]:
        page.logger.info(
            f"a11y [{violation['impact']}] {violation['id']}: {violation['help']}"
        )

    return [
        v for v in results["violations"] if v["impact"] in ("critical", "serious")
    ]


def test_login_page_accessibility(login_page):

    critical_or_serious = _run_axe_and_log(login_page)

    assert not critical_or_serious, (
        "Critical/serious accessibility violations: "
        + ", ".join(v["id"] for v in critical_or_serious)
    )


@pytest.mark.xfail(
    reason="saucedemo's sort <select> has no accessible name (axe rule "
    "'select-name', critical impact) -- verified live, not fixed upstream",
    strict=True,
)
def test_inventory_page_accessibility(inventory_page):

    critical_or_serious = _run_axe_and_log(inventory_page)

    assert not critical_or_serious, (
        "Critical/serious accessibility violations: "
        + ", ".join(v["id"] for v in critical_or_serious)
    )


def test_login_keyboard_only_navigation(login_page):

    username_field = login_page.driver.find_element(*login_page.USERNAME)
    username_field.send_keys("standard_user")
    username_field.send_keys(Keys.TAB)

    password_field = login_page.driver.switch_to.active_element
    password_field.send_keys("secret_sauce")
    password_field.send_keys(Keys.ENTER)

    assert login_page.is_login_successful()
