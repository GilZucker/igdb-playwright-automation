import allure
import pytest
from pages.igdb_home_page import IGDBHomePage
from pages.top_100_page import Top100Page


@pytest.mark.ui
@allure.epic("UI Filtering")
@allure.feature("Top 100 Filters")
@allure.title("Filter Top 100 Games by Platform and Year Range")
def test_filter_top_100_by_platform_and_year(page):
    """1. Open IGDB Home Page.
    2. Click the search modal
    3. Navigate to Top 100 Games page.

    4. Apply Platform filter (e.g., 'PC (Microsoft Windows)').
    5. Apply Year range filter (e.g., 2020 - 2026).
    6. Verify results update correctly.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()


    home_page.open_search_modal()
    home_page.click_to_100_games_button()

    top_100_page = Top100Page(page)

    top_100_page.remove_cookie_banner()

    with allure.step("1. Select Platform filter"):
        top_100_page.select_platform("PC")

    with allure.step("2. Select Year range filter"):
        top_100_page.filter_by_year_range(from_year="2020", to_year="2026")

    games_count = top_100_page.get_games_count()

    with allure.step(f"3. Verify filtered results are displayed correctly (found {games_count} games in list)"):
        assert(top_100_page.get_games_count() > 0), "Expected to find games after applying filters"


@pytest.mark.ui
@allure.epic("UI Filtering")
@allure.feature("Top 100 Filters")
@allure.title("Filter Top 100 Games with Narrow Range (Specific Platform/Years)")
def test_filter_top_100_narrow_results(page):
    """Verifies that applying a narrow filter returns a specific reduced number
    of games."""
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/top-100/games")

    top_100_page = Top100Page(page)
    top_100_page.remove_cookie_banner()

    with allure.step("1. Select a different Platform filter (DOS)"):
        top_100_page.select_platform("DOS")

    with allure.step("2. Apply narrow filter (From Year 1990 till 1991)"):
        top_100_page.filter_by_year_range(from_year="1990", to_year="1991")
        games_count = top_100_page.get_games_count()

    with allure.step(
            f"3. Assert reduced games list count (Found {games_count} games)"
    ):
            assert (0 < games_count < 100
        ), f"Expected less than 100 games for narrow filter, but got {games_count}"

    game_data = top_100_page.get_first_game_details()
    with allure.step(f"4. Verify top game data: (Found '{game_data['title']}' with {game_data['rating']})"):

        assert game_data['title'] != "", "Game title should not be empty"
        assert game_data['rating'] != "", "Game rating should not be empty"