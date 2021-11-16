import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

scope = "user-top-read"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

#オーディオ機能を取得
print(sp.audio_analysis("6Sa5NyKHX0gikNuG4t3CZr"))
