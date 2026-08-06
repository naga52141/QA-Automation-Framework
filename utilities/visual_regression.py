import io
import os
import time

import numpy as np
from PIL import Image, ImageChops

BASELINE_DIR = "baselines"
DIFF_DIR = "visual_diffs"


COMPARE_SIZE = (320, 180)


def wait_for_images_loaded(driver, selector=".inventory_item_img img", timeout=10):
    # Screenshots taken immediately after page load can race product
    # images that haven't finished loading yet (verified live: right
    # after login, all inventory images report naturalWidth 0), causing
    # flaky visual-regression diffs unrelated to any real change.
    script = (
        "return Array.from(document.querySelectorAll(arguments[0]))"
        ".every(img => img.complete && img.naturalWidth > 0);"
    )

    deadline = time.time() + timeout

    while time.time() < deadline:
        if driver.execute_script(script, selector):
            return
        time.sleep(0.2)


def wait_for_fonts_loaded(driver, timeout=10):
    # saucedemo loads custom webfonts (DM Mono, DM Sans) asynchronously --
    # verified live: document.fonts.status reads "loading" immediately
    # after page load. A screenshot taken before they finish shows
    # fallback-font text metrics, producing a small but real diff
    # (~5.4%, seen in CI) unrelated to any actual change. Resolves fast
    # in practice (~0.1s) but is a real race, not paranoia.
    deadline = time.time() + timeout

    while time.time() < deadline:
        if driver.execute_script("return document.fonts.status === 'loaded';"):
            return
        time.sleep(0.1)


def compare_screenshot(driver, name, threshold=0.05):

    os.makedirs(BASELINE_DIR, exist_ok=True)
    baseline_path = os.path.join(BASELINE_DIR, f"{name}.png")

    current_image = Image.open(
        io.BytesIO(driver.get_screenshot_as_png())
    ).convert("RGB")

    if not os.path.exists(baseline_path):
        current_image.save(baseline_path)
        return True, 0.0

    baseline_image = Image.open(baseline_path).convert("RGB")

    # Baselines must come from the same platform doing the comparing --
    # committed via CI's "commit auto-generated baselines" workflow step,
    # not captured locally. A macOS-captured baseline produced ~24-90%
    # false-positive diffs against Linux CI's font rendering even on an
    # unchanged page (verified). Downscaling before diffing still helps
    # absorb ordinary sub-pixel antialiasing jitter run-to-run, while
    # still catching real layout/content regressions (missing elements,
    # broken images, wrong colors, etc).
    baseline_small = baseline_image.resize(COMPARE_SIZE)
    current_small = current_image.resize(COMPARE_SIZE)

    diff = ImageChops.difference(baseline_small, current_small)
    diff_array = np.array(diff)
    changed_pixels = np.count_nonzero(diff_array.any(axis=-1))
    total_pixels = COMPARE_SIZE[0] * COMPARE_SIZE[1]
    diff_ratio = changed_pixels / total_pixels

    if diff_ratio > threshold:
        os.makedirs(DIFF_DIR, exist_ok=True)
        diff.resize(baseline_image.size).save(
            os.path.join(DIFF_DIR, f"{name}_diff.png")
        )
        current_image.save(os.path.join(DIFF_DIR, f"{name}_actual.png"))

    return diff_ratio <= threshold, diff_ratio
