import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

scope = "user-library-read playlist-read-private"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

def get_track_id_and_track_name(tracks):
    track_id = lambda i: saved_tracks['items'][i]['track']['id']
    track_name = lambda i: sp.track(track_id(i))['name']

    id_and_name_records = [[track_id(i), track_name(i)] for i in range(len(saved_tracks['items']))]
    return pd.DataFrame(id_and_name_records, columns=['track_id','track_name'])

def get_track_features(track_ids):
    audio_features_filterd_list = list(filter(None, sp.audio_features(track_ids)))
    return pd.DataFrame(audio_features_filterd_list).drop(['id','uri','track_href','analysis_url'], axis=1)

MAX_LIMIT=50
offset=0
track_id_name_features=None
while True:
    saved_tracks = sp.current_user_saved_tracks(limit=MAX_LIMIT, offset=offset)
    if not saved_tracks['items']:
        print("saved_tracks is empty")
        break
    
    track_id_and_track_name = get_track_id_and_track_name(saved_tracks)

    track_features = get_track_features(track_id_and_track_name['track_id'])

    if track_id_name_features is None:
        track_id_name_features = pd.concat([track_id_and_track_name, track_features], axis=1).dropna(how='any')
    else:
        new=pd.concat([track_id_and_track_name, track_features], axis=1).dropna(how='any')
        track_id_name_features=track_id_name_features.append(new, ignore_index=True, verify_integrity=True)

    offset+=MAX_LIMIT

track_id_name_features.to_csv("spotify-my-music.tsv", sep='\t', index = False)