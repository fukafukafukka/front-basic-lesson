import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

scope = "user-top-read"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

#playlist内のトラックを取得する
print(sp.playlist_items(playlist_id="37i9dQZF1DX9ATVoGjsqqY", limit=1))
