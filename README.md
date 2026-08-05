# QA Automation Framework

[![Tests](https://github.com/naga52141/QA-Automation-Framework/actions/workflows/tests.yml/badge.svg)](https://github.com/naga52141/QA-Automation-Framework/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Selenium](https://img.shields.io/badge/selenium-4.44-43B02A)
![pytest](https://img.shields.io/badge/pytest-8.3-0A9EDC)

A Selenium + pytest UI test automation framework built around the **Page Object Model**, testing the full user journey on [saucedemo.com](https://www.saucedemo.com/) — from login through checkout, including the site's deliberately broken test accounts, edge cases, and site-wide navigation.

**[Live Allure report →](https://naga52141.github.io/QA-Automation-Framework/)** — regenerated on every push to `main`, with pass-rate and duration trends across runs.

---

## Overview

- **39 automated tests** covering login, inventory, product detail, cart, checkout, the hamburger menu, and the footer
- **Data-driven login testing** via CSV, exercising all 6 of saucedemo's seeded accounts
- **Documented, live-verified bugs** on saucedemo's intentionally broken test accounts (`problem_user`, `error_user`, `visual_user`, `performance_glitch_user`) — each assertion was checked against the real site before being written, not assumed from documentation
- **Parallel execution** via `pytest-xdist`, cutting a ~90s serial run to ~40s
- **CI/CD** on GitHub Actions: headless Chrome, parallel test execution, dual reporting, and screenshot capture on failure
- **Dual reporting**: `pytest-html` for a quick local summary, and Allure for step-by-step detail with screenshots attached inline and cross-run trend graphs
- **Centralized logging**: every click, type, and read across every page object is logged automatically, not just the login flow

## Tech Stack

| Layer | Tool |
|---|---|
| Browser automation | Selenium 4 |
| Test runner | pytest |
| Parallelization | pytest-xdist |
| Reporting | pytest-html, Allure |
| CI/CD | GitHub Actions |
| Test data | CSV |

## Project Structure

```
QA-Automation-Framework/
├── .github/workflows/tests.yml   CI pipeline
├── conftest.py                   Fixtures, failure-screenshot hook, Allure attachment
├── pages/                        Page Object Model
│   ├── base_page.py              Shared click/type/read primitives + logging
│   ├── login_page.py
│   ├── inventory_page.py         Sort, add/remove, hamburger menu, footer
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py             CSV-driven, all 6 accounts
│   ├── test_inventory.py         Sort orders, add/remove all products
│   ├── test_product_detail.py
│   ├── test_cart.py
│   ├── test_checkout.py          Validation, cancel flows, exact total math
│   ├── test_menu.py              Logout, reset app state, about, all items
│   ├── test_footer.py
│   └── test_edge_cases.py        Verified bugs on the broken test accounts
├── utilities/
│   ├── config.py
│   ├── csv_reader.py
│   └── logger.py                 xdist-safe, per-worker log files
├── testdata/login.csv
└── requirements.txt
```

## Getting Started

```bash
pip install -r requirements.txt
```

Requires Chrome; chromedriver is managed automatically by Selenium Manager.

## Running Tests

```bash
pytest -v
```

In parallel:

```bash
pytest -n auto -v
```

Excluding the slow test (`performance_glitch_user`'s login):

```bash
pytest -m "not slow" -v
```

## Test Reports

**HTML report:**

```bash
pytest --html=reports/report.html
```

**Allure report** (requires the [Allure commandline](https://allurereport.org/docs/install/)):

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

`allure serve` builds the report and opens it in your browser. Failed tests get their
screenshot attached inline, in addition to it being saved to `screenshots/`.

On failure, a screenshot is also saved to `screenshots/`. Logs are written to
`logs/automation.log` (or `logs/automation-<worker>.log` per worker under `-n auto`).

## CI/CD

Every push and pull request to `main` triggers a GitHub Actions workflow that:

1. Runs the full suite headlessly, in parallel, against Chrome
2. Generates both an HTML and an Allure report
3. On pushes to `main`, publishes the Allure report to GitHub Pages, carrying forward
   history from the previous run so trend graphs build up over time
4. Uploads the HTML report, Allure report, and any failure screenshots as workflow
   artifacts

## Test Coverage

| Area | What's covered |
|---|---|
| Login | All 6 seeded accounts, invalid password, locked-out user |
| Inventory | Page load, add/remove for all 6 products, all 4 sort orders |
| Product detail | Navigation, name match, add/remove, back button |
| Cart | Multi-item cart, remove from cart page, continue shopping |
| Checkout | Field validation (first/last name, postal code), both cancel buttons, exact subtotal + tax = total, back-home button |
| Menu | Logout, reset app state, all items, about link |
| Footer | Social link targets |
| Edge cases | `problem_user` (broken images, mangled checkout fields), `error_user` (broken remove-from-cart), `visual_user` (broken product image), `performance_glitch_user` (slow login) |

The edge-case tests target saucedemo's intentionally broken demo accounts, seeded by the
site itself for exactly this kind of testing — not bugs in this framework.
