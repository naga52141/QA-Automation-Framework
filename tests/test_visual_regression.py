import pytest
from utilities.visual_regression import compare_screenshot, wait_for_images_loaded

# Baselines live in baselines/ and are auto-generated + committed by the
# main "Tests" GitHub Actions workflow the first time it runs without
# them (see the "Commit auto-generated visual-regression baselines" step)
# -- they're Linux-CI-native, at a fixed 1920x1080 headless viewport.
# Don't regenerate them locally on macOS: a locally-captured baseline
# produced large false-positive diffs against Linux's font rendering,
# verified live. If you need to force new ones, delete baselines/*.png
# and push to main; CI will recreate and commit them on that run.
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
