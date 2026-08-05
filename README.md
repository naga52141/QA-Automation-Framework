# QA Automation Framework

Selenium + pytest UI test automation framework for [saucedemo.com](https://www.saucedemo.com/), built with the Page Object Model.

## Structure

- `pages/` — page objects (login, inventory, cart, checkout)
- `tests/` — test suites
- `utilities/` — config, CSV data reader, logger
- `testdata/` — CSV-driven test data (e.g. login credentials)
- `conftest.py` — pytest fixtures (driver, page objects) and the failure-screenshot hook

## Setup

```bash
pip install -r requirements.txt
```

Requires Chrome and a matching chromedriver (managed automatically by Selenium Manager).

## Running tests

```bash
pytest -v
```

In parallel (via `pytest-xdist`):

```bash
pytest -n auto -v
```

HTML report:

```bash
pytest --html=reports/report.html
```

On failure, a screenshot is saved to `screenshots/`. Logs are written to `logs/automation.log`
(or `logs/automation-<worker>.log` per worker when running with `-n auto`).
