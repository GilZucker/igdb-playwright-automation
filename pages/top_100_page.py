from pages.base_page import BasePage


class Top100Page(BasePage):
    """Page Object for the Top 100 Games Page."""
    # 1. Locators

    TOP_100_GAME_ROWS = "#games-top-list tr"
    TOP_100_GAME_TITLES = (
        "#games-top-list a[href*='/games/']:not(:has(img))"
    )

    PLATFORM_DROPDOWN_BUTTON = "//span[@class='select2-selection__rendered']"
    PLATFORM_SEARCH_INPUT = ".select2-search__field"
    PLATFORM_OPTION_LIST = ".select2-results__options .select2-results__option"

    FROM_YEAR_INPUT = "//input[@id='top_from_year']"
    TO_YEAR_INPUT = "//input[@id='top_to_year']"

    FIRST_GAME_TITLE_LINKS = "table tbody tr:first-child a[href*='/games/']"
    GAME_RATINGS = "#games-top-list small.text-muted:has-text('ratings')"
    SEARCHING_INDICATOR = ".select2-results__option:has-text('Searching')"
    COMPANIES_TAB = "//a[contains(text(),'Companies')]"
    FIRST_RESULT_ITEM = ".media-body .media-heading, .game-tile, .company-tile"

    def click_game_by_name(self, game_name: str):
        """Checks all the games in the list and click on the game with the desired name."""
        games = self._page.locator(self.TOP_100_GAME_ROWS)
        count = games.count()

        for i in range(count):

            title = games.nth(i).inner_text()

            if game_name in title:

                games.nth(i).click()
                break

    def get_games_count(self) -> int:
        return self._page.locator(self.TOP_100_GAME_ROWS).count()

    def get_game_title_by_index(self, index: int = 0) -> str:
        """Retrieves the game name by index from the list of titles."""
        return (
            self._page.locator(self.TOP_100_GAME_TITLES)
            .nth(index)
            .inner_text()
            .strip()
        )

    def select_platform(self, platform_name: str):
        self._page.locator(self.PLATFORM_DROPDOWN_BUTTON).click()
        self.fill_text(self.PLATFORM_SEARCH_INPUT, platform_name)

        option = self._page.locator(self.PLATFORM_OPTION_LIST).filter(has_text=platform_name).first
        option.click()
        self._page.wait_for_load_state("networkidle")

    def filter_by_year_range(self, from_year: str = None, to_year: str = None):
        if from_year:
            from_input = self._page.locator(self.FROM_YEAR_INPUT)
            from_input.click()
            from_input.fill(from_year)
            from_input.press("Enter")


        if to_year:
            to_input = self._page.locator(self.TO_YEAR_INPUT)
            to_input.click()
            to_input.fill(to_year)
            to_input.press("Enter")

        self._page.wait_for_load_state("networkidle")

    def get_first_game_details(self) -> dict:
        title_locator = self._page.locator(self.TOP_100_GAME_TITLES).first
        title = title_locator.inner_text().strip()

        ratings_locator = self._page.locator(self.GAME_RATINGS)


        if ratings_locator.count() > 0:
            rating = ratings_locator.first.inner_text().strip()
        else:
            rating = "N/A"

        return {"title": title, "rating": rating}

    def get_from_year_value(self) -> str:
        """Returns the current value that appears in the 'From Year' field."""
        return self._page.locator(self.FROM_YEAR_INPUT).input_value()

    def get_to_year_value(self) -> str:
        """Returns the current value that appears in the 'To Year' field."""
        return self._page.locator(self.TO_YEAR_INPUT).input_value()

    def fill_platform_raw(self, text: str):
        """Typing text in the platform field without clicking select, to test Searching..."""
        platform_input = self._page.locator(self.PLATFORM_SEARCH_INPUT)
        platform_input.click()
        platform_input.fill(text)

    def click_on_companies_btn(self):
        self.click(self.COMPANIES_TAB)

    def click_companies_tab(self, timeout_ms: int = 5000):
        """
        Clicks on the Companies segment.
        Accepts a custom timeout parameter to allow strict SLA testing.
        """

        self.get_locator(self.COMPANIES_TAB).click(timeout=timeout_ms)

    def is_companies_list_visible(self) -> bool:
        """Verifies that at least one item/company in the list is visible."""
        return self.is_visible(self.FIRST_RESULT_ITEM)

