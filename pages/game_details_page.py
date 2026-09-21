from pages.base_page import BasePage


class GameDetailsPage(BasePage):


    GAME_TITLE = "main h1"
    COVER_IMAGE = "main img[src*='t_cover']"
    RATING_SCORE = "main svg[data-icon='star'] + span"
    SUMMARY_TEXT = "main div[class*='MuiGrid2-grid-xs-9'] p"
    STORYLINE_TEXT = "h6 + p"
    YOUTUBE_LINKS = "a[href*='youtube.com']"
    MEDIA_SECTION = "a[href*='youtube'], div[class*='media'], div[class*='video'], .game-header-cover, img"

    def __init__(self, page):
        super().__init__(page)

    def get_game_title_text(self) -> str:
        return self.get_text(self.GAME_TITLE)

    def is_game_title_visible(self) -> bool:
        """Verifies if the game title is visible on the page."""
        return self._page.locator(self.GAME_TITLE).is_visible()

    def is_cover_image_visible(self) -> bool:
        return self._page.locator(self.COVER_IMAGE).first.is_visible()

    def get_rating_score_text(self) -> str:
        return self._page.locator(self.RATING_SCORE).nth(2).inner_text()



    def get_summary_text(self) -> str:
        """Returns the game summery text from the top gray segment."""
        locator = self._page.locator(self.SUMMARY_TEXT).nth(2)
        if locator.is_visible():
            return locator.inner_text().strip()
        return ""


    def get_storyline_text(self) -> str:
        """Returns the detailed game storyline text from bottom section."""
        locator = self._page.locator(self.STORYLINE_TEXT).first
        if locator.is_visible():
            return locator.inner_text().strip()
        return ""

    def is_youtube_link_present(self) -> bool:
        """
        Checks if at least one YouTube link/embed exists on the game page and is visible.
        """
        youtube_locator = self.get_locator(self.YOUTUBE_LINKS)

        return youtube_locator.count() > 0 and youtube_locator.first.is_visible()

    def is_media_section_visible(self) -> bool:
        """Fallback check: verifies if general media/video section is visible."""
        locator = self.get_locator(self.MEDIA_SECTION)
        return locator.count() > 0 and locator.first.is_visible()