import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
SPOTIFY_SCOPE = "playlist-read-private user-library-read"

# Paths & File Names
DOWNLOADS_FOLDER = "Downloads"
DOWNLOADED_SONGS_FILE = "downloaded_songs.json"

# Ensure the Downloads folder exists
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
