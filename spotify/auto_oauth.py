import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

#現在のユーザーのトップトラックを取得する
while True:
  print(sp.current_user_top_artists(limit=1))
  time.sleep(600)
