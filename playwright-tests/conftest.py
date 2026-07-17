# Intentionally empty for now. Its presence tells pytest this directory is
# the project root, which is what makes `from pages.login_page import LoginPage`
# resolve correctly from inside tests/. Shared fixtures (e.g. a pre-logged-in
# page) will land here starting Phase 1 — not needed yet for one test.
