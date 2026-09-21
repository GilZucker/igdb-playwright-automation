import pytest
import allure
from pages.igdb_home_page import IGDBHomePage
from pages.upcoming_releases_page import UpcomingReleasesPage


@allure.feature("Browser Navigation & State")
@allure.story("History Back and Forward Cache Validation")
def test_browser_history_navigation_cache(page):
    """
    Verifies that browser back and forward navigation preserves page state
    and URLs correctly without cache corruption or broken UI.
    """

    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )


    page.goto("/")
    home_page = IGDBHomePage(page)
    upcoming_page = UpcomingReleasesPage(page)
    home_page.remove_cookie_banner()

    with allure.step("1. Navigate to Coming Soon via Hamburger Menu"):
        home_page.navigate_to_coming_soon_via_hamburger()
        base_coming_soon_url = upcoming_page.get_current_url()
        assert "coming_soon" in base_coming_soon_url.lower() or "release_dates" in base_coming_soon_url.lower(), (
            f"Expected URL to contain 'coming_soon', but got '{base_coming_soon_url}'"
        )



    with allure.step("2. Select 'PC (Microsoft Windows)' platform filter"):
        chosen_platform = "PC (Microsoft Windows)"
        upcoming_page.select_platform_by_name(chosen_platform)
        pc_filtered_url = upcoming_page.get_current_url()
        assert "pfilter=" in pc_filtered_url, f"Expected 'pfilter=' parameter in URL, but got '{pc_filtered_url}'"
        assert pc_filtered_url != base_coming_soon_url, "URL did not change after selecting a platform filter."

    with allure.step("3. Navigate BACK in browser history and verify state"):
        page.go_back()
        page.wait_for_load_state("domcontentloaded")
        current_url = upcoming_page.get_current_url()
        assert base_coming_soon_url == current_url, (
            f"Expected '{base_coming_soon_url}', but got '{current_url}'"
        )



    with allure.step("4. Navigate FORWARD in browser history and verify state restoration"):
        page.go_forward()
        page.wait_for_load_state("domcontentloaded")
        restored_url = upcoming_page.get_current_url()
        assert restored_url == pc_filtered_url, f"Expected '{pc_filtered_url}', but got '{restored_url}'"
        assert "pfilter=" in restored_url, f"Expected restored URL to retain 'pfilter=', but got '{restored_url}'"