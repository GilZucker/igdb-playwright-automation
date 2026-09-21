import allure
import pytest
from pages.igdb_home_page import IGDBHomePage

@pytest.mark.ui
@allure.epic("UI Theme")
@allure.feature("Theme Toggle")
@allure.title("UI Theme - Switch between Light and Dark mode")
def test_toggle_dark_light_theme(page):
    """1. Fetch initial body style attribute.

    2. Click theme toggle button.
    3. Verify that body style updated to reflect
    theme change.
    """
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page.goto("/")
    home_page = IGDBHomePage(page)
    home_page.remove_cookie_banner()




    with allure.step("1. Get initial body style"):
        initial_style = home_page.get_theme_style()

    with allure.step("2. Click theme toggle button"):
        home_page.toggle_theme()
        page.wait_for_timeout(500)

    with allure.step("3. Verify body style changed after toggle"):
        updated_style = home_page.get_theme_style()


        assert initial_style != updated_style, (
            f"Theme did not change! Initial: '{initial_style}', Updated: '{updated_style}'"
        )