import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

scope = "user-top-read"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

#お気に入りのtracksを取得する
print(sp.current_user_saved_tracks(limit=1))
