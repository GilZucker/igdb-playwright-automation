import allure
import pytest

from pages import game_details_page
from pages.game_details_page import GameDetailsPage
from pages.igdb_home_page import IGDBHomePage

@pytest.mark.ui
@allure.feature("Game Details Navigation")
@allure.story("Random Game Flow")
class TestRandomGameNavigation:

    @allure.title("Verify navigation to a Random Game via Search Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_random_game_navigation(self, page):
        # 1. Open Search Modal and Click Random Game
        with allure.step("1. Open search modal and click 'Random Game'"):
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            page.goto("/")
            home_page = IGDBHomePage(page)

            home_page.remove_cookie_banner()
            home_page.open_search_modal()
            game_details_page = home_page.click_random_game()

        # 2. Verify URL Structure
        with allure.step("2. Verify URL redirected to a specific game page"):
            current_url = game_details_page.get_current_url()
            assert "/games/" in current_url, (
                f"Expected URL to contain '/games/', but got '{current_url}'"
            )

        # 3. Verify Game Title Visibility and Content
        with allure.step("3. Verify game title is rendered and non-empty"):
            assert game_details_page.is_game_title_visible(), (
                "Game title H1 is not visible on the details page"
            )
            title_text = game_details_page.get_game_title_text()
            assert len(title_text) > 0, "Game title text should not be empty"

        # 4. Verify Cover Image Display
        with allure.step("4. Verify game cover image is visible"):
            assert game_details_page.is_cover_image_visible(), (
                "Game cover image is not displayed on the details page"
            )

        # 5. Verify game details overview
        with allure.step("5. Verify game details components are visible and populated"):

            assert game_details_page.get_summary_text(), "Game summary is missing"
            assert game_details_page.get_storyline_text(), "Game storyline is missing"
            rating_text = game_details_page.get_rating_score_text()
            summary_text = game_details_page.get_summary_text()
            storyline_text = game_details_page.get_storyline_text()
            assert rating_text != "", "Expected rating score, but got empty text!"
            assert summary_text != "", "Expected summary text but got empty text!"
            assert storyline_text != "", "Expected storyline text but got empty text!"



    @allure.title("Verify Random Game button provides different games each time")
    @allure.severity(allure.severity_level.NORMAL)
    def test_random_game_uniqueness(self, page):

        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        page.goto("/")
        home_page = IGDBHomePage(page)
        home_page.remove_cookie_banner()
        with allure.step("1. Click Random Game for the first time"):
            home_page.open_search_modal()
            game_details_page = home_page.click_random_game()

            first_game_title = game_details_page.get_game_title_text()

        with allure.step("2. Navigate back home and click Random Game a second time"):
            page.goto("/")
            home_page.open_search_modal()
            game_details_page = home_page.click_random_game()
            second_game_title = game_details_page.get_game_title_text()
        with allure.step("3. Verify the two selected games are not identical"):
            assert first_game_title != second_game_title, f"Expected different games, but got '{first_game_title}' twice!"



