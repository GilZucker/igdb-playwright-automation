from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    VIEW_MORE_BTN = "(//a[contains(text(),'View more →')])[1]"
    SORT_TITLE_BTN = "//a[contains(text(),'Title')]"
    FIRST_RESULT_TITLE = "(//a[contains(@class, 'link-dark h4')])[1]"


    def click_view_more_button(self):
        self.click(self.VIEW_MORE_BTN)

    def choose_sort_by_title(self):
        self.click(self.SORT_TITLE_BTN)

    def get_first_result_title(self):
        return self.get_text(self.FIRST_RESULT_TITLE)


