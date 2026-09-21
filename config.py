import os

# Twitch & IGDB Credentials
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "yz7jpn01wjxegv7ht6o9e019ua3g6s")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET", "ihj5jpbmugpchljl9vmkp0ij507kqo")

# Endpoints
TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token"
IGDB_API_BASE_URL = "https://api.igdb.com/v4/"

UI_BASE_URL = "https://www.igdb.com"
DEFAULT_TIMEOUT = 10000
