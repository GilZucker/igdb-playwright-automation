import allure
import pytest
from pages.igdb_home_page import IGDBHomePage
from pages.top_100_page import Top100Page


@pytest.mark.ui
@allure.epic("UI Search")
@allure.feature("Top 100 games")
@allure.title("UI Search - Verifying Top 100 games page")
def test_search_top_100_page(page):
    """1. Open IGDB Home Page.

    2. Open the Search Modal.
    3. Validate navigation to the Top 100 games page.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    home_page = IGDBHomePage(page)

    home_page.remove_cookie_banner()

    with allure.step("1. Open search modal"):
        home_page.open_search_modal()

    with allure.step("2. Click the Top 100 games"):
        home_page.click_to_100_games_button()

    with allure.step("3. Validate navigation to Top 100 page"):
        page.wait_for_url("**/top-100/games**")

    assert "/top-100/games" in page.url, (
        f"Expected '/top-100/games' in URL, but got: {page.url}"
    )

    top_100_page = Top100Page(page)
    top_100_page.remove_cookie_banner()


    with allure.step("4. Assert total games count is exactly 100"):
        games_count = top_100_page.get_games_count()
        assert (
                games_count == 100
        ), f"Expected 100 games on Top 100 page, but got: {games_count}"

    with allure.step("5. Assert top #1 game title is valid"):
        first_game_title = top_100_page.get_game_title_by_index(0)
        assert (
                len(first_game_title) > 0
        ), "Expected top game title to not be empty"
        allure.attach(
            first_game_title,
            name="Top #1 Game Title",
            attachment_type=allure.attachment_type.TEXT,
        )