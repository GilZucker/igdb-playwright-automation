import allure
from faker import Faker

import config
import pytest

# ==========================================
# 1. UI & Browser Setup (Playwright)
# ==========================================


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,
        "args": [
            "--start-maximized",  # Opens window as full screen
            "--disable-search-engine-choice-screen",  # Filter Chrome popups the interrupts the automation
            "--disable-features=FindInPage",  # Blocks the Find tool that appear on the screen
        ],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,  # Support for full screen view on ultrawide screen
    }


# ==========================================
# 2. API Setup & Authentication (IGDB)
# ==========================================


@pytest.fixture(scope="session")
def igdb_auth_context(playwright):
    """Creates a session-scoped APIRequestContext with OAuth Access Token for IGDB API."""


    # 1. Create a RequestContext for a temporary token from Twitch
    temp_context = playwright.request.new_context()

    auth_response = temp_context.post(
        config.TWITCH_AUTH_URL,
        params={
            "client_id": config.TWITCH_CLIENT_ID,
            "client_secret": config.TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )

    assert (
        auth_response.ok
    ), f"Failed to authenticate with Twitch: {auth_response.status_text}"
    token_data = auth_response.json()
    access_token = token_data["access_token"]
    temp_context.dispose()

    # 2. Creation of the constant RequestContext with headers for IGDB
    api_context = playwright.request.new_context(
        base_url=config.IGDB_API_BASE_URL,
        extra_http_headers={
            "Client-ID": config.TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "text/plain",
        },
    )

    # Context ready for the tests
    yield api_context

    # Closing the context post session
    api_context.dispose()

def faker_gen():  # Using faker_gen for auto generate saved keywords
    return Faker()

# ==========================================
# 3. Reporting Hooks (Allure Screenshot on Failure)
# ==========================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto screenshot for Allure in case of test failure."""
    outcome = yield
    report = outcome.get_result()


    # Checking if the current state of the tests fail
    if report.when == "call" and report.failed:

        # Checking if Fixture 'page' was used during the test (UI test and not API)
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )