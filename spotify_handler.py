import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE, DOWNLOADED_SONGS_FILE

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
))

def get_user_playlists():
    """ Fetches all Spotify playlists of the user. """
    return {playlist["name"]: playlist["id"] for playlist in sp.current_user_playlists(limit=50)["items"]}

def get_playlist_tracks(playlist_id):
    """ Fetches all tracks from the given playlist. """
    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results["items"]:
            track = item["track"]

            if track is None:  #  Handle missing track data
                continue

            track_info = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "spotify_url": track["external_urls"].get("spotify", "N/A")  #  Use .get() to avoid KeyError
            }
            
            tracks.append(track_info)

        results = sp.next(results) if results["next"] else None

    return tracks

def load_downloaded_songs():
    """ Loads previously downloaded songs from JSON file. """
    if os.path.exists(DOWNLOADED_SONGS_FILE):
        with open(DOWNLOADED_SONGS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_downloaded_songs(downloaded_songs):
    """ Saves downloaded songs to a JSON file. """
    with open(DOWNLOADED_SONGS_FILE, "w") as file:
        json.dump(downloaded_songs, file, indent=4)
