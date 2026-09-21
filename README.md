# 🎭 IGDB End-to-End Playwright Automation Framework

* End-to-End automation framework for testing the IGDB (Internet Game Database) website. Built with Python, Playwright, and Pytest using the Page Object Model (POM) pattern.

---

## 🚀 Key Features & Highlights

* **Architecture:** Page Object Model with clean separation of locators, page actions, and test scenarios.
* **Locators & Waiting:** Built using Playwright standard selectors and CSS, relying on auto-waiting without artificial delays.
* **Reporting:** Pytest integration with Allure for execution steps and logs.
* **Test Types:** Functional UI flows, dynamic table filtering, search modal behaviors, and input/edge cases.

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.10+
* **Core Framework:** [Playwright for Python](https://playwright.dev/python/)
* **Test Runner:** [Pytest](https://docs.pytest.org/)
* **Reporting:** [Allure Pytest](https://docs.qameta.io/allure/)
* **Design Pattern:** Page Object Model (POM)

---

## 📁 Project Structure

```text
├── pages/                  # Page Object classes (Home, Top100, UpcomingReleases, etc.)
│   ├── base_page.py        # Base Page wrapping common Playwright actions
│   ├── igdb_home_page.py
│   ├── game_details_page.py
│   ├── search_results_page.py
│   ├── top_100_page.py
│   └── upcoming_releases_page.py

├── tests/                  # Test suites grouped by feature
│   ├── test_01_theme_toggle.py
│   ├── test_02_igdb_search.py
│   ├── test_03_search_and_navigate_to_game.py
│   ├── test_04_search_non_existent_game.py
│   ├── test_05_search_top_100.py
│   ├── test_06_filter_top_100.py
│   ├── test_07_filter_invalid_input.py
│   ├── test_08_top_100_companies.py
│   ├── test_09_random_game_navigation.py
│   ├── test_10_upcoming_releases.py
│   ├── test_11_browser_history_cache.py
│   ├── test_12_third_party_integration.py
│   └── test_upcoming_releases.py
├── requirements.txt        # Project dependencies
└── pytest.ini              # Pytest configuration & Allure settings

```

## 📋 Test Coverage & STD Summary
The automation suite is mapped directly to a Software Test Description (STD) coverage matrix:

| Suite / Feature | Test Description | Test Type | Target Element / Action |
| :--- | :--- | :--- | :--- |
| **Home / Search** | Validate real-time game search modal | Functional | `#search-input` / Modal Results |
| **Home / Security** | Verify system resilience & UI feedback on XSS injection | Negative / Edge | `<script>` Payload Input |
| **Top 100** | Filter top games by Platform & Year dynamically | Integration | Dynamic AJAX Table Rows |
| **Upcoming Releases** | Verify platform tab filtering and section headers | Functional | `ul.mar-md-bottom` / Covers |
| **API / Games** | Fetch game details by ID | API Functional | `GET /v4/games` | HTTP 200, JSON Schema validation |
| **API / Search** | Query endpoints with invalid parameters | API Negative | `POST /v4/search` | HTTP 400/422, Error payload structure |



## ⚙️ Setup & Installation

1. Clone the repository:

```bash
   git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   cd <YOUR-REPO-NAME>
```
2. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies and Playwright browsers:
```
pip install -r requirements.txt
playwright install
```

4. Run the test suite:
```
# Run all tests
pytest

# Run with Allure report generation
pytest --alluredir=allure-results
allure serve allure-results
```

