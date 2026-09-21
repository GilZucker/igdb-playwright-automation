import pytest
import allure
from pages.igdb_home_page import IGDBHomePage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

@pytest.mark.ui
@allure.title("UI Search Test - Verify search results in modal")
def test_search_game_in_igdb(page):
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    page.evaluate(
        "document.getElementById('onetrust-consent-sdk')?.remove();"
    )
    home_page = IGDBHomePage(page)
    home_page.open_search_modal()
    home_page.search_game_in_modal("Grand Theft Auto V")

    result_text = home_page.get_first_result_text()

    assert "Grand Theft Auto V" in result_text


@pytest.mark.ui
@allure.epic("UI Search")
@allure.feature("Security & Edge Cases")
@allure.title("UI Search - XSS Injection Must Provide User Feedback")
def test_search_xss_script_injection_handling(page):
    """1. Open Search Modal.

    2. Inject XSS <script> string.
    3. Expect either search results OR a clear 'No results' feedback message to the user.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()



    with allure.step("1. Open search modal and input XSS string"):
        home_page.open_search_modal()

        home_game_text = home_page.search_game_in_modal(
            "<script>alert('test')</script>"
        )

    with allure.step(
        "2. Verify user receives proper 'No results' feedback when no items match"
    ):
        results_count = home_page.get_search_results_count()
        has_no_results_msg = home_page.is_no_results_message_displayed()


        # If there are no results - there must be a feedback message, otherwise it's a UI/UX bug
        assert results_count == 0, (
            f"Security/UI Issue: XSS string yielded {results_count} search results "
            f"instead of 0!"
        )

        assert has_no_results_msg, (
            "UI Defect: Search yielded 0 results, but the modal failed to display "
            "a 'No results' feedback message to the user!"
        )