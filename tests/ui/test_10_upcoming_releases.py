import pytest
import allure
from pages.igdb_home_page import IGDBHomePage
from pages.upcoming_releases_page import UpcomingReleasesPage


@allure.feature("Upcoming Releases")
@allure.story("Navigation and Platform Filtering")
def test_upcoming_releases_navigation_and_filter(page):
    """
    Verifies navigation to Upcoming Releases / Coming Soon,
    validates the presence of upcoming time windows, and tests platform switching.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    home_page = IGDBHomePage(page)

    home_page.remove_cookie_banner()

    upcoming_page = UpcomingReleasesPage(page)
    with allure.step("1. Navigate to Coming Soon via Hamburger Menu"):
        home_page.navigate_to_coming_soon_via_hamburger()

    with allure.step("2. Verify core sections (Upcoming 7 & 14 days) are visible"):
        assert upcoming_page.is_7_days_section_visible(), "'Upcoming 7 days' section is missing."
        assert upcoming_page.is_14_days_section_visible(), "'Upcoming 14 days' section is missing."

    with allure.step("3. Select a platform from the tabs (including More dropdown handling)"):
        chosen_platform = "PC (Microsoft Windows)"
        upcoming_page.select_platform_by_name(chosen_platform)

    with allure.step("4. Verify page title updates according to selected platform"):
        title_text = upcoming_page.get_page_title_text()
        assert "PC" in title_text or "Windows" in title_text, f"Expected PC in title, but got '{title_text}'"

@allure.story("Navigation via Search Modal")
def test_upcoming_releases_navigation_via_modal(page):
    """
    Verifies navigation to Coming Soon via the Search Modal entry point,
    and checks that core time window sections render properly.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")

    home_page = IGDBHomePage(page)


    home_page.remove_cookie_banner()

    upcoming_page = UpcomingReleasesPage(page)

    with allure.step("1. Navigate to Coming Soon via Search Modal"):
        home_page.navigate_to_coming_soon_via_modal()

    with allure.step("2. Verify landing URL contains coming_soon or pulse"):
        assert "coming_soon" in page.url.lower() or "pulse" in page.url.lower(), (
            f"Unexpected URL after modal navigation: {page.url}"
        )

    with allure.step("3. Verify core sections (Upcoming 7 & 14 days) are visible"):
        assert upcoming_page.is_7_days_section_visible(), "'Upcoming 7 days' section is missing."
        assert upcoming_page.is_14_days_section_visible(), "'Upcoming 14 days' section is missing."


    with allure.step("4. Select a different platform from the hidden list under 'More dropdown'"):

        chosen_platform = "Android"
        upcoming_page.select_platform_by_name(chosen_platform)

    with allure.step("5. Verify page title updates according to selected platform"):
        title_text = upcoming_page.get_page_title_text()
        assert "Android" in title_text or "Coming Soon to Android" in title_text, f"Expected Android in title, but got '{title_text}'"