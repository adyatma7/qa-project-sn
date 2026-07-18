BASE_URL = "https://parabank.parasoft.com/parabank/"
# Trailing slash kept intentionally — same lesson as DEC-008 in the
# Playwright suite, applied here from the start instead of re-discovering
# it the hard way a second time.


def url_for(path: str) -> str:
    # Selenium has no baseURL config the way pytest-playwright does; this
    # is the manual equivalent.
    return BASE_URL + path
