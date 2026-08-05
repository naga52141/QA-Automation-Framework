import pytest
from utilities.csv_reader import read_login_data

login_data = read_login_data("testdata/login.csv")


@pytest.mark.parametrize(
    "data",
    login_data
)
def test_login_from_csv(login_page, data):

    login_page.login(
        data["Username"],
        data["Password"]
    )

    if data["Expected"] == "Pass":
        assert login_page.is_login_successful()

    else:
        assert "Epic sadface" in login_page.get_error_message()