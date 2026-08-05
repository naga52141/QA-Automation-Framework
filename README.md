# QA Automation Framework

[![Tests](https://github.com/naga52141/QA-Automation-Framework/actions/workflows/tests.yml/badge.svg)](https://github.com/naga52141/QA-Automation-Framework/actions/workflows/tests.yml)

Selenium + pytest UI test automation framework for [saucedemo.com](https://www.saucedemo.com/), built with the Page Object Model.

**[Live Allure report →](https://naga52141.github.io/QA-Automation-Framework/)** — updated on every push to `main`, with trend history across runs.

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

Allure report (requires the [Allure commandline](https://allurereport.org/docs/install/) installed separately):

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

`allure serve` builds the report and opens it in your browser. Failed tests get the
screenshot attached inline, in addition to it being saved to `screenshots/`.

On failure, a screenshot is saved to `screenshots/`. Logs are written to `logs/automation.log`
(or `logs/automation-<worker>.log` per worker when running with `-n auto`).
