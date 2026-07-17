"""
Phase 1: one API-level auth test, per the blueprint's chaining example
(Section 8.3): hit a login-type endpoint directly instead of driving the
browser, and check the response rather than a rendered page.

UPDATE (confirmed by an actual run, not a guess anymore): the endpoint
`/services/bank/login/{username}/{password}` is correct — it really does
return the customer record. It returns XML by default, not JSON, which is
why the first version of this test failed on `response.json()`. See
DEC-007 in docs/decision-log.md for the full story.
"""
import xml.etree.ElementTree as ET
import pytest


@pytest.mark.api
def test_valid_login_returns_customer_via_api(page):
    base = "https://parabank.parasoft.com/parabank"
    response = page.request.get(f"{base}/services/bank/login/john/demo")
    assert response.ok, (
        f"Expected a successful response, got {response.status}. "
        f"Body: {response.text()[:500]}"
    )

    # ParaBank's REST service returns XML here, confirmed against a real
    # response body: <customer><id>...</id><firstName>John</firstName>...
    root = ET.fromstring(response.text())
    first_name = root.find("firstName").text
    assert first_name == "John"
