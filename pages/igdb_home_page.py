from pages.base_page import BasePage


class IGDBHomePage(BasePage):

    # 1. Locators
    SEARCH_TRIGGER = "[data-testid='SearchIcon']"
    SEARCH_FIELD = "[placeholder='What are you looking for?']"

    COOKIE_ACCEPT_BTN = "#onetrust-accept-btn-handler"
    NO_RESULTS_MESSAGE = "//*[contains(text(), 'No results for')]"
    SEARCH_RESULT_GAME_ITEMS = ".MuiModal-root a:has(img)"

    THEME_TOGGLE_BTN = "(//button[contains(@class, 'MuiIconButton-root MuiIconButton-sizeMedium')])[2]"
    SEARCH_MODAL_TOP_100_BTN = ".MuiModal-root a[href*='/top-100/games']"
    SEARCH_MODAL_RANDOM_GAME = ".MuiModal-root a[href*='random']"
    SEARCH_MODAL_COMING_SOON = ".MuiModal-root a[href*='coming']"
    HAMBURGER_MENU_BTN = "//button[@id='menu-header-icon']"
    HAMBURGER_COMING_SOON_LINK = "a[href*='/games/coming_soon']"



    def __init__(self, page):
        super().__init__(page)

    def open_search_modal(self):

        self.click(self.SEARCH_TRIGGER)

    def search_game_in_modal(self, game_name: str):
        self.type_human(self.SEARCH_FIELD, game_name, delay=100)

    def click_to_100_games_button(self):
        self.click(self.SEARCH_MODAL_TOP_100_BTN)

    def get_first_result_text(self) -> str:
        return self._page.locator(self.SEARCH_RESULT_GAME_ITEMS).first.inner_text()

    def select_first_search_result_and_navigate(self):
        first_result_selector = f"{self.SEARCH_RESULT_GAME_ITEMS} >> nth=0"
        self.click(first_result_selector)

    def get_no_results_text(self) -> str:
        return self.get_text(self.NO_RESULTS_MESSAGE)


    def handle_cookies(self):
        try:

            self.get_locator(self.COOKIE_ACCEPT_BTN).click(timeout=3000)
        except Exception:
            pass

    def get_search_results_count(self) -> int:

        return self._page.locator(self.SEARCH_RESULT_GAME_ITEMS).first.count()


    def is_no_results_message_displayed(self) -> bool:

        return self._page.locator(self.NO_RESULTS_MESSAGE).is_visible()

    def toggle_theme(self):
       self.click(self.THEME_TOGGLE_BTN)

    def get_theme_style(self) -> str:
        html_style = self._page.locator("html").get_attribute("style") or ""
        body_style = self._page.locator("body").get_attribute("style") or ""
        return html_style + body_style

    def click_random_game(self) -> GameDetailsPage:
        """Clicks on the Random Game link from the search modal and navigates to GameDetailsPage."""
        self.click(self.SEARCH_MODAL_RANDOM_GAME)

        self._page.wait_for_load_state("networkidle")

        from pages.game_details_page import GameDetailsPage
        return GameDetailsPage(self._page)

    def search_and_press_enter(self, game_name: str):
       """Types a game name into the search input and presses enter."""
       self.fill_text(self.SEARCH_FIELD, game_name)
       self.press_key(self.SEARCH_FIELD, "Enter")

    def navigate_to_coming_soon_via_modal(self):
        """Entry Point 1: Navigates via Search Modal."""
        self.open_search_modal()
        self.click(self.SEARCH_MODAL_COMING_SOON)

    def navigate_to_coming_soon_via_hamburger(self):
        """Entry Point 2: Navigates via Main Hamburger Navigation Menu."""
        self.click(self.HAMBURGER_MENU_BTN)
        self._page.locator(self.HAMBURGER_COMING_SOON_LINK).nth(1).click()
