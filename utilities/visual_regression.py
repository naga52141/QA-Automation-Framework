import io
import os

import numpy as np
from PIL import Image, ImageChops

BASELINE_DIR = "baselines"
DIFF_DIR = "visual_diffs"


def compare_screenshot(driver, name, threshold=0.02):

    os.makedirs(BASELINE_DIR, exist_ok=True)
    baseline_path = os.path.join(BASELINE_DIR, f"{name}.png")

    current_image = Image.open(
        io.BytesIO(driver.get_screenshot_as_png())
    ).convert("RGB")

    if not os.path.exists(baseline_path):
        current_image.save(baseline_path)
        return True, 0.0

    baseline_image = Image.open(baseline_path).convert("RGB")

    if baseline_image.size != current_image.size:
        current_image = current_image.resize(baseline_image.size)

    diff = ImageChops.difference(baseline_image, current_image)
    diff_array = np.array(diff)
    changed_pixels = np.count_nonzero(diff_array.any(axis=-1))
    total_pixels = baseline_image.size[0] * baseline_image.size[1]
    diff_ratio = changed_pixels / total_pixels

    if diff_ratio > threshold:
        os.makedirs(DIFF_DIR, exist_ok=True)
        diff.save(os.path.join(DIFF_DIR, f"{name}_diff.png"))
        current_image.save(os.path.join(DIFF_DIR, f"{name}_actual.png"))

    return diff_ratio <= threshold, diff_ratio
