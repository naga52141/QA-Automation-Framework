import pytest
from utilities.visual_regression import compare_screenshot, wait_for_images_loaded

# Baselines were captured with headless Chrome at a fixed 1920x1080
# viewport (CI=true). Headless vs. headed Chrome render noticeably
# differently (fonts especially) -- comparing a headed-mode screenshot
# against these baselines produces false positives. Regenerate with
# `CI=true pytest tests/test_visual_regression.py` if you need new ones.
#
# These tests are marked "visual" so cross-browser CI runs (Firefox/
# Safari) can skip them with -m "not visual" instead of failing on
# expected rendering differences between browsers.
pytestmark = pytest.mark.visual


def test_login_page_visual(login_page):

    login_page.driver.set_window_size(1920, 1080)

    passed, diff_ratio = compare_screenshot(login_page.driver, "login_page")

    assert passed, f"Login page visual diff of {diff_ratio:.2%} exceeds threshold"


def test_inventory_page_visual(inventory_page):

    inventory_page.driver.set_window_size(1920, 1080)
    wait_for_images_loaded(inventory_page.driver)

    passed, diff_ratio = compare_screenshot(inventory_page.driver, "inventory_page")

    assert passed, f"Inventory page visual diff of {diff_ratio:.2%} exceeds threshold"
