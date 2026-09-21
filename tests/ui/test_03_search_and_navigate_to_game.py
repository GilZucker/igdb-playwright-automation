import allure
import pytest



from pages.base_page import BasePage
from pages.igdb_home_page import IGDBHomePage
from pages.game_details_page import GameDetailsPage
from pages.search_results_page import SearchResultsPage


@pytest.mark.ui
@allure.title("UI Navigation - Search 'Cyberpunk 2077' and Navigate to Game Page")
def test_search_and_navigate_to_game_page(page):
    """
    1. Open IGDB Home Page and clear overlays
    2. Search for 'Cyberpunk 2077' in search modal
    3. Click the first search result
    4. Assert navigation to Game Details Page and verify URL + H1 Title
    """

    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)

    home_page.remove_cookie_banner()

    game_details_page = GameDetailsPage(page)

    search_query = "Cyberpunk 2077"


    home_page.open_search_modal()
    home_page.search_game_in_modal(search_query)
    home_page.get_first_result_text()

    home_page.select_first_search_result_and_navigate()
    current_url = game_details_page.get_current_url()
    page_title = game_details_page.get_game_title_text()


    assert (
        "cyberpunk-2077" in current_url.lower()
    ), f"Expected 'cyberpunk-2077' in URL, but got: '{current_url}'"

    assert (
        search_query.lower() in page_title.lower()
    ), f"Expected '{search_query}' in page title, but got: '{page_title}'"

@allure.feature("Search Functionality")
@allure.story("Keyboard Navigation")
def test_search_via_keyboard_enter(page):
    """
        Verifies that pressing 'Enter' after typing in the search modal
        successfully submits the search / navigates to the expected page.
        """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()

    with allure.step("1. Open home page and open search modal"):

        home_page.open_search_modal()
    with allure.step("2. Type game name and press Enter"):

        target_game = "red dead redemption 2"
        home_page.search_and_press_enter(target_game)

    with allure.step("3. Verify navigation to the target game page"):
        game_details_page = GameDetailsPage(page)
        actual_title = game_details_page.get_game_title_text()

        assert target_game.lower() in actual_title.lower(), (
            f"Expected '{target_game}' in title, but got '{actual_title}'"
        )

@allure.feature("Search Functionality")
@allure.story("Search Results Navigation")
def test_search_view_more_navigation(page):
    """Verifies that clicking 'View More ->' in the search modal, redirects the user to the full search results page"""

    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()

    with allure.step("1. Open search modal and type search query"):
        home_page.open_search_modal()
        target_game = "Grand Theft Auto: Vice City"
        home_page.search_game_in_modal(target_game)

    with allure.step("2. Click 'View More' in search modal"):
        search_results_page = SearchResultsPage(page)
        search_results_page.click_view_more_button()

    with allure.step("3. Verify redirection to search results page"):
        assert "/search" in page.url, f"Expected '/search' in URL, but got '{page.url}'"


@allure.feature("Search Functionality")
@allure.story("Sorting Bug Verification")
@pytest.mark.xfail(
    reason="Known Bug: Sorting search results by Title resets the query scope and returns unrelated games."
)
def test_search_sort_by_title_bug(page):
    """
    Bug Verification Test:
    Verifies that sorting search results by Title maintains the search query context.
    Expected to XFAIL due to a known search engine scope bug.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()

    with allure.step("1. Open search modal, search for game, and navigate to full results"):
        home_page.open_search_modal()

        target_game = "Grand Theft Auto: Vice City"
        home_page.search_game_in_modal(target_game)
        search_results_page = SearchResultsPage(page)
        search_results_page.click_view_more_button()
    with allure.step("2. Apply Sort by Title"):
        search_results_page.choose_sort_by_title()

    with allure.step("3. Verify first result title still contains the target query"):
        first_result_title = search_results_page.get_first_result_title()
        assert "Vice City" in first_result_title,(f"Expected 'Vice City' in title, but got '{first_result_title}'")



