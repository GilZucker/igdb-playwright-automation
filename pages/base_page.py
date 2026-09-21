from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self._page = page

    def _highlight(self, locator: str):

        element = self._page.locator(locator)
        element.evaluate(
            "el => el.style.border = '6px solid red'"
        )

    def fill_text(self, locator, text):
        self._highlight(locator)
        self._page.locator(locator).fill(text)


    def click(self, locator):
        self._highlight(locator)
        self._page.locator(locator).click()

    def select_option(self, locator, text):
        self._page.locator(locator).select_option(value=text)

    def get_text(self, locator):
        return self._page.locator(locator).inner_text().strip()

    def get_locator(self, selector: str):
        return self._page.locator(selector)

    def type_human(self, selector: str, text: str, delay: int = 100):

        locator = self.get_locator(selector)
        locator.click()
        locator.press_sequentially(text, delay=delay)

    def get_current_url(self) -> str:

        return self._page.url

    def remove_cookie_banner(self):
        """Removes the OneTrust consent banner if present in the DOM."""
        self._page.evaluate(
            "document.getElementById('onetrust-consent-sdk')?.remove();"
        )

    def press_key(self, locator_str: str, key: str):
        """Presses a specific keyboard key on the given locator."""
        self._page.locator(locator_str).press(key)

    def is_visible(self, selector: str) -> bool:
        """Verifies if an element is visible on the page."""
        return self._page.locator(selector).is_visible()


