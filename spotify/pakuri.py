import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from nested_lookup import nested_lookup

scope = "user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

def track_info(limit = 50):
    saved_tracks = sp.current_user_saved_tracks(limit=limit)

    track_id = lambda i: saved_tracks['items'][i]['track']['id']
    track_name = lambda i: sp.track(track_id(i))['name']

    info = [[track_id(i), track_name(i)] for i in range(limit)]
    return pd.DataFrame(info, columns = ['track_id','track_name'])

#1個目
# print(track_info())

#2個目
def track_features(track_ids, limit = 50):
    return pd.DataFrame(sp.audio_features(track_ids))
#2個目
# print(track_features(track_info()['track_id']).drop(['track_href', 'analysis_url', 'id', 'uri'], axis=1))

#3個目
def get_track_from_mode(mode = 1):
   info_with_features = pd.concat([track_info(), track_features(track_info()['track_id'])], axis = 1)
   return info_with_features[info_with_features['mode'] == mode]
#3個目
# print(get_track_from_mode()[['track_id', 'track_name', 'mode']])

#4個目
def make_playlist(playlist_name):
   user_id = sp.current_user()['id']

   if playlist_name not in nested_lookup('name', sp.current_user_playlists()):
       sp.user_playlist_create(user_id, playlist_name)
       print("get_track_from_mode()['track_id']")
       print(get_track_from_mode()['track_id'])
       sp.user_playlist_add_tracks(user = user_id, playlist_id = sp.current_user_playlists()['items'][0]['id'], tracks = get_track_from_mode()['track_id'])
#4個目
make_playlist('test')


