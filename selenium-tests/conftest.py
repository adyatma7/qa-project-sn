"""
WebDriver setup/teardown, plus manual screenshot-on-failure — both are
automatic in the Playwright suite, explicit here on purpose. Full list of
what's different and why: selenium-tests/README.md.
"""
import os
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    # No explicit Service/driver download step — Selenium 4.6+ bundles
    # "Selenium Manager," which detects the installed Chrome version and
    # resolves a matching driver automatically. Originally used the
    # third-party webdriver-manager package for this; switched after it
    # failed with a corrupted-download error (see DEC-016) — this removes
    # an entire dependency instead of just working around the failure.
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # explicit waits only, see README
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Manual screenshot-on-failure. The Playwright suite does this with
    # one config line (`screenshot: 'only-on-failure'`); Selenium has no
    # built-in equivalent, hence this hook.
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("reports/screenshots", exist_ok=True)
            drv.save_screenshot(f"reports/screenshots/{item.name}.png")
