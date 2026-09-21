from pages.base_page import BasePage

class UpcomingReleasesPage(BasePage):
    # Locators
    PAGE_TITLE = "h1.media-heading, h1"
    SECTION_7_DAYS = "h4:has-text('Upcoming 7 days')"
    SECTION_14_DAYS = "h4:has-text('Upcoming 14 days')"
    PLATFORM_TAB_BY_NAME = "ul.mar-md-bottom a:text-is('{platform}'), ul.mar-md-bottom li:text-is('{platform}')"
    GAME_COVERS = ".game-cover, .img-responsive"
    MORE_BUTTON = "//*[contains(@class, 'dropdown-toggle')]"

    def click_the_more_button(self):
        return self.click(self.MORE_BUTTON)

    def get_page_title_text(self) -> str:
        """Returns the main page title text."""
        return self.get_text(self.PAGE_TITLE)

    def is_7_days_section_visible(self) -> bool:
        """Verifies if 'Upcoming 7 days' section is visible."""
        return self.is_visible(self.SECTION_7_DAYS)

    def is_14_days_section_visible(self) -> bool:
        """Verifies if 'Upcoming 14 days' section is visible."""
        return self.is_visible(self.SECTION_14_DAYS)


    def select_platform_by_name(self, platform_name: str):
        """
        Filters the platform tabs list by exact/partial text match and clicks the chosen platform.
        Example: platform_name = "PC (Microsoft Windows)"
        """

        selector = self.PLATFORM_TAB_BY_NAME.format(platform=platform_name)

        if not self.is_visible(selector):
            self.click(self.MORE_BUTTON)

        self.click(selector)