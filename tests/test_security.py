import pytest
import requests

# Passive checks only. saucedemo.com is a third-party site we don't own or
# have authorization to penetration-test -- no exploit/injection attempts
# here, just read-only inspection of what the site already exposes.

BASE_URL = "https://www.saucedemo.com/"


def test_http_redirects_to_https():

    response = requests.get(BASE_URL.replace("https://", "http://"), timeout=10)

    assert response.url.startswith("https://")


def test_password_field_is_masked(login_page):

    field_type = login_page.get_attribute(login_page.PASSWORD, "type")

    assert field_type == "password"


@pytest.mark.xfail(
    reason="saucedemo.com (static GitHub Pages hosting) sends none of the "
    "standard security response headers -- verified live via curl -I, not "
    "something fixable from this framework",
    strict=True,
)
def test_security_headers_present():

    response = requests.get(BASE_URL, timeout=10)

    expected_headers = {
        "content-security-policy",
        "x-frame-options",
        "strict-transport-security",
        "x-content-type-options",
    }

    present_headers = {h.lower() for h in response.headers}

    assert expected_headers & present_headers, (
        "None of the expected security headers are present: "
        f"{sorted(expected_headers)}"
    )
