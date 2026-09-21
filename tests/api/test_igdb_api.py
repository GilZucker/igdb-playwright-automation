import allure
import pytest
import requests
from faker import Faker

@allure.epic("IGDB API")
@pytest.mark.api
@allure.feature("Games Search & Retrieval")
class TestIGDBApi:
    #faker = Faker()

    @allure.title("Fetch top rated and most popular games from IGDB")
    def test_get_popular_games(self, igdb_auth_context):
        """API Search - Top popular games from IGDB"""

        # Apicalypse query: Sort by total rating count to get major, mainstream titles
        query = "fields name, rating, total_rating_count; where total_rating_count > 1000; sort total_rating_count desc; limit 5;"

        response = igdb_auth_context.post("games", data=query)

        # Validate HTTP 200 OK status code
        assert response.status == 200, f"Expected status 200, but got {response.status}"

        games = response.json()
        assert len(games) > 0, "Games list returned empty"

        print("\n=== Top All-Time Popular Games Fetched from IGDB ===")
        for game in games:
            rating = round(game.get('rating', 0), 1)
            count = game.get('total_rating_count', 0)
            print(f"- {game.get('name')} | Rating: {rating} | Total Reviews: {count}")

    @allure.title("Fetch a specific game from IGDB with exact name match")
    def test_search_game_by_name(self, igdb_auth_context):
        """API Search - Specific game from IGDB"""
        # Search using total_rating_count sort to get the mainstream original title
        query = (
            'fields name, rating, first_release_date; '
            'where name = "Half-Life 2" & first_release_date >= 1073001600 & first_release_date <= 1104537599; '
            'limit 1;'
        )
        response = igdb_auth_context.post("games", data=query)

        assert response.status == 200, f"Expected status 200, but got {response.status}"

        games = response.json()
        assert len(games) > 0, "No games returned for the given search query"

        first_game = games[0]
        game_title = first_game.get("name")
        game_rating = round(first_game.get("rating", 0), 1)

        assert game_title == "Half-Life 2", f"Expected 'Half-Life 2', but got '{game_title}'"

        print(f"\n=== Successfully fetched original 2004 game: '{game_title}' | Rating: {game_rating}/100 ===")

    @allure.title("Search for a non-existent game")
    def test_search_non_existent_game(self, igdb_auth_context):
        """API Search - For non-existing games from IGDB"""
        query = ('search "non_existent_game_xyz_99999"; fields name;')

        response = igdb_auth_context.post("games", data=query)

        assert response.status == 200
        games = response.json()


        assert len(games) == 0

        print("\n=== Verified: Non-existent game returned empty list ===")

    @allure.title("Filter games by specific Genre (Shooter) and Platform (PC)")
    def test_filter_games_by_genre_and_platform(self, igdb_auth_context):
        """API Search - Filtered search based on genre and platform"""
        from datetime import datetime, timezone

        query = (
            "fields name, genres, platforms, rating, first_release_date; "
            "where genres = (5) & platforms = (6) & rating != null; "
            "sort rating desc; "
            "limit 5;"
        )

        response = igdb_auth_context.post("games", data=query)

        assert response.status == 200, f"Expected status 200, but got {response.status}"

        games = response.json()
        assert len(games) > 0, "No Shooter games found for PC platform"

        print("\n=== Top Rated Shooter Games for PC ===")


        for game in games:
            game_name = game.get("name")
            rating = round(game.get("rating", 0), 1)
            genres = game.get("genres", [])
            platforms = game.get("platforms", [])

            # Extract release year if available (converting Unix timestamp)
            release_timestamp = game.get("first_release_date")
            release_year = "N/A"
            if release_timestamp:
                release_year = datetime.fromtimestamp(release_timestamp, tz=timezone.utc).year

            # Validate that Genre (5) and Platform (6) are present
            assert 5 in genres, f"Game '{game_name}' does not contain Shooter genre (5)"
            assert 6 in platforms, f"Game '{game_name}' does not contain PC platform (6)"

            print(f"- {game_name} ({release_year}) | Rating: {rating}/100")

    @allure.title("Filter games by theme (Sci-Fi)")

    def test_filter_games_by_theme(self, igdb_auth_context):
        """API Search - Filtered search based on theme"""
        from datetime import datetime, timezone

        # Clean query string matching our working Postman request
        query = "fields name, themes, rating, first_release_date; where themes = (18) & rating != null; sort rating desc; limit 5;"

        response = igdb_auth_context.post("games", data=query)

        assert response.status == 200, f"Expected status 200, but got {response.status}"

        games = response.json()
        assert len(games) == 5, f"Expected exactly 5 games, but got {len(games)}"

        print("\n=== Sci-Fi Games Found ===")

        for game in games:
            game_name = game.get("name")
            rating = round(game.get("rating", 0), 1) if game.get("rating") else "N/A"
            themes = game.get("themes", [])

            release_timestamp = game.get("first_release_date")
            release_year = "N/A"
            if release_timestamp:
                release_year = datetime.fromtimestamp(release_timestamp, tz=timezone.utc).year

            # Validate that Sci-Fi theme (18) is present in the returned array
            assert 18 in themes, f"Game '{game_name}' does not contain Sci-Fi theme (18)"

            print(f"- {game_name} ({release_year}) | Rating: {rating}")

    @allure.title("Unauthorized access test using invalid token header")
    def test_unauthorized_access(self, igdb_auth_context):
        """Unauthorized access using invalid token header"""
        query = (
            "fields name, genres, platforms, rating, first_release_date; "
            "sort rating desc; "
            "limit 5;"
        )


        custom_headers = {"Authorization": "Bearer invalid_token_xyz"}

        response = igdb_auth_context.post(
            "games", data=query, headers=custom_headers
        )

        assert response.status == 401, (
            f"Expected status 401, but got {response.status} ({response.status_text})"
        )

    @allure.title("Unauthorized access test using wrong client_id")
    def test_unauthorized_invalid_client_id(self, igdb_auth_context):
        """Unauthorized access using wrong client_ID"""
        query = (
            "fields name, genres, platforms, rating, first_release_date; "
            "sort rating desc; "
            "limit 5;"
        )

        custom_headers = {"Client-ID": "Unauthorized Client ID"}
        response = igdb_auth_context.post(
            "games", data=query, headers=custom_headers
        )

        assert response.status == 401, (
            f"Expected status 401, but got {response.status} ({response.status_text})"
        )

    @allure.title("Unauthorized access test using missing client_id")
    def test_unauthorized_missing_client_id(self, igdb_auth_context):
        """Unauthorized access using missing client_ID"""
        query = (
            "fields name, genres, platforms, rating, first_release_date; "
            "sort rating desc; "
            "limit 5;"
        )

        custom_headers = {"Client-ID": ""}
        response = igdb_auth_context.post(
            "games", data=query, headers=custom_headers
        )

        assert response.status == 401, (
            f"Expected status 401, but got {response.status} ({response.status_text})"
        )
    @allure.title("Pagination Test - Verify unique items per page")
    def test_pagination_offset(self, igdb_auth_context):
        """API pagination test - Checking for unique items"""
        query_page_1 = (
            "fields name; "
            "sort id asc; "
            "limit 5; "
            "offset 0;"  # First 5 games
        )
        response_1 = igdb_auth_context.post(
            "games", data=query_page_1, headers={"Content-Type": "text/plain"}
        )
        games_page_1 = response_1.json()

        query_page_2 = (
            "fields name; "
            "sort id asc; "
            "limit 5; "
            "offset 5;" # 5 games from the 5th index (skip the first 5)
        )
        response_2 = igdb_auth_context.post(
            "games", data=query_page_2, headers={"Content-Type": "text/plain"}
        )
        games_page_2 = response_2.json()

        ids_page_1 = [game["id"] for game in games_page_1]
        ids_page_2 = [game["id"] for game in games_page_2]

        overlap = set(ids_page_1).intersection(set(ids_page_2))
        assert len(overlap) == 0, (
            f"Found duplicate game IDs between pages: {overlap}"
        )

    @allure.title("Nested Fields Test - Fetch and verify nested cover details")
    def test_fetch_nested_cover_fields(self, igdb_auth_context):
        # Filtering only games with covers to receive a nested structure
        query = (
            "fields name, cover.url, cover.image_id; "
            "where cover != null; "
            "limit 3;"
        )

        response = igdb_auth_context.post(
            "games", data=query, headers={"Content-Type": "text/plain"}
        )
        assert response.status == 200, f"Expected 200, got {response.status}"

        games = response.json()
        assert len(games) > 0, "Expected to receive at least one game"

        # For loop on the games to verify each game has a cover
        for game in games:
            assert "cover" in game, f"Game {game.get('name')} missing 'cover' field"

            cover = game["cover"]
            assert "url" in cover, f"Cover for {game['name']} missing 'url'"
            assert "image_id" in cover, f"Cover for {game['name']} missing 'image_id'"

            # Checking that the URL starts with // and is not empty
            assert cover["url"].startswith("//") or cover["url"].startswith("http"), (
                f"Invalid image URL format: {cover['url']}"
            )

    @pytest.mark.api
    @allure.title("Random game name search test")
    def test_search_game_with_random_faker_string(self, igdb_auth_context):
        """API Search - Negative Testing with Faker Generated Queries"""
        fake_generator = Faker()
        random_game_name = fake_generator.sentence(nb_words=3)

        body = f'search "{random_game_name}"; fields name, rating;'


        response = igdb_auth_context.post("games", data=body)

        assert response.ok, f"Expected 200 OK, got {response.status}"
        assert isinstance(
            response.json(), list
        ), "Response payload should be a list"