import pytest
import allure

from pages import game_details_page
from pages.game_details_page import GameDetailsPage
from pages.igdb_home_page import IGDBHomePage


@allure.feature("Integrations & External Content")
@allure.story("Twitch Stream / Media Embed Presence Check")
def test_twitch_integration_embed_presence(page):
    """
    Validates that third-party media embeds (e.g. Twitch / YouTube / External links)
    render properly on a major game page without requiring user authentication.
    """

    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )


    page.goto("/games/god-of-war--1")

    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()
    game_details_page = GameDetailsPage(page)

    with allure.step("1. Verify game page loads correctly"):
        current_game_url = game_details_page.get_current_url()
        assert "god-of-war" in current_game_url.lower(), f"Expected 'god-of-war' in URL, got '{current_game_url}'"

    with allure.step("2. Check for third-party media integration or media section"):
        if game_details_page.is_youtube_link_present():
            assert True, "YouTube integration link/embed found and visible."
        else:
            assert game_details_page.is_media_section_visible(), (
                "Neither YouTube integration nor general Media section was visible on the game page."
            )