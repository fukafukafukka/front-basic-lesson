import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import time

scope = "user-library-read playlist-read-private"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=False))

MAX_LIMIT=50
offset=0

# seed_artists=os.environ['seed_artists']
# seed_genres=os.environ['seed_genres']
# seed_tracks=os.environ['seed_tracks']
seed_artists=["5iZweZ1uY4DshuBUYN6Fn4"]
seed_genres=["Alternative R&B"]
seed_tracks=["7s8phfghmLs4la0gdZhGKg"]

recommendations=sp.recommendations(seed_artists, seed_genres, seed_tracks, limit=3, country=None)

artist_id_name_list=[]
for recommendation in recommendations["tracks"]:
    for artist in recommendation["album"]["artists"]:
        artist_id_name_list.append([artist["id"], artist["name"]])
        time.sleep(2)

print(pd.DataFrame(artist_id_name_list, columns=['artists_id','artists_name']))
    # time.sleep(30)
