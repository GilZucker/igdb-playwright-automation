import allure
import pytest
from pages.igdb_home_page import IGDBHomePage


@pytest.mark.ui
@allure.title("UI Search - Negative Test: Search for Non-Existent Game")
def test_search_non_existent_game(page):
    """1. Open IGDB Home Page & clear overlays

    2. Search for non-existent query '!@#$%^&*' in modal
    3. Verify 'No results for...' message is displayed
    """
    # Bypass web bots
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)

    home_page.remove_cookie_banner()


    invalid_search_query = "!@#$%^&*"

    # Searching
    home_page.open_search_modal()
    home_page.search_game_in_modal(invalid_search_query)

    # Fetching the text
    no_results_text = home_page.get_no_results_text()

    # Assertions
    assert "no results for" in no_results_text.lower(), (
        f"Expected 'No results for' in message, but got: '{no_results_text}'"
    )
    assert invalid_search_query in no_results_text, (
        f"Expected search query '{invalid_search_query}' inside message, but got: '{no_results_text}'"
    )