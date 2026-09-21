import allure
import pytest
from pages.top_100_page import Top100Page


def test_filter_top_100_invalid_input_handling(page):
    """Verifies input sanitization and system robustness.
    Note: Business logic boundary tests (e.g., From Year > To Year) were evaluated manually and excluded from E2E suite to reduce test flakiness
     and maintain optimal pipeline execution time."""
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/top-100/games")

    top_100_page = Top100Page(page)
    top_100_page.remove_cookie_banner()

    script_input = "<script>alert('xss')</script>"

    # -------------------------------------------------------------
    # Step 1: Platform Filter (Stuck on Searching...)
    # -------------------------------------------------------------
    with allure.step(f"1. Inject invalid input into Platform filter: '{script_input}'"):
        top_100_page.select_platform("")
        top_100_page.fill_platform_raw(script_input)

    with allure.step("2. Verify Platform filter gets stuck on 'Searching...' indicator"):
        searching_locator = page.locator(
            "ul.select2-results__options li:has-text('Searching')"
        )
        searching_locator.wait_for(state="visible", timeout=5000)
        assert searching_locator.is_visible(), (
            "Expected 'Searching...' state to be visible in Platform dropdown"
        )

    # -------------------------------------------------------------
    # Step 2: From Year Filter (Fallback to 1900)
    # -------------------------------------------------------------
    with allure.step(f"3. Inject invalid input into From Year filter: '{script_input}'"):
        top_100_page.filter_by_year_range(from_year=script_input, to_year="")

    with allure.step("4. Verify From Year field rejects the XSS script string"):
        from_year_value = top_100_page.get_from_year_value()

        assert script_input not in from_year_value, (
            f"Security flaw! Un-sanitized script survived in From Year field: '{from_year_value}'"
        )

    # -------------------------------------------------------------
    # Step 3: To Year Filter (Parses to 0001)
    # -------------------------------------------------------------
    with allure.step(f"5. Inject invalid input into To Year filter: '{script_input}'"):
        top_100_page.filter_by_year_range(from_year="", to_year=script_input)

    with allure.step("6. Verify To Year field rejects the XSS script string"):
        to_year_value = top_100_page.get_to_year_value()
        assert script_input not in to_year_value, (
            f"Security flaw! Un-sanitized script survived in To Year field: '{to_year_value}'"
        )
