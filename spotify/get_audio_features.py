import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from datetime import date

scope = "user-top-read"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

#オーディオ機能を取得
#print(sp.audio_features(["6Sa5NyKHX0gikNuG4t3CZr", "6VrWy16VpW7rz1XYe3uTRV"]))

features_list=[]
date_dict = {"year_month_date":date.today().strftime('%Y-%m-%d')}

# 以下完成系
for feature_dict in list(filter(None, sp.audio_features(["6Sa5NyKHX0gikNuG4t3CZr", "6VrWy16VpW7rz1XYe3uTRV"]))):
  feature_dict.update(date_dict)
  features_list.append(feature_dict)
print(features_list)

