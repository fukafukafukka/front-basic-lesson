import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

scope = "user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private"
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

def grep_features(track_features):
    track_target_features=track_features.loc[:,['danceability','energy','tempo']]
    return track_target_features.query('tempo >= 100 & danceability >= 0.600 & energy >= 0.600')
    
def set_playlist_id_list_and_playlist_name_list():
    global playlist_id_list
    global playlist_name_list

    current_user_playlist=sp.current_user_playlists()

    playlist_ids=lambda i: current_user_playlist['items'][i]['id']
    playlist_names=lambda i: current_user_playlist['items'][i]['name']

    playlist_id_list=[playlist_ids(i) for i in range(len(current_user_playlist['items']))]
    playlist_name_list=[playlist_names(i) for i in range(len(current_user_playlist['items']))]

def get_playlist_id(playlist_name: str):
    global playlist_id_list
    global playlist_name_list
    return playlist_id_list[playlist_name_list.index(playlist_name)]


user_id = sp.current_user()['id']
playlist_id_list = None
playlist_name_list = None
playlist_id = None
MAX_LIMIT=50
offset=0
first_roop_flag=1
PLAYLIST_NAME="running_playlist"
while True:
    saved_tracks = sp.current_user_saved_tracks(limit=MAX_LIMIT, offset=offset)

    if not saved_tracks['items']:
        print("saved_tracks is empty")
        break
    
    track_id_and_track_name = get_track_id_and_track_name(saved_tracks)

    track_features = get_track_features(track_id_and_track_name['track_id'])

    grepd_track_features = grep_features(track_features)

    if first_roop_flag == 1:
        set_playlist_id_list_and_playlist_name_list()
        if PLAYLIST_NAME in playlist_name_list:
            playlist_id = get_playlist_id(PLAYLIST_NAME)
            # 同じ曲が1つのプレイリストに入るのは避けたいため、breakさせている。
            break
            # 取得できる曲数が50件までの縛りの中で、差分だけ抽出して既存プレイリストに追加するのは難しい。
            # かつ
            # プレイリストの中身全消し&洗い替えの実装ができればLambdaだけで良いが、プレイリスト全消しのためにトラック全て取得するのは実装が難しいためDBで全曲を保持させて、それを運用する方が良いと考える。
        else:
            result = sp.user_playlist_create(user_id, PLAYLIST_NAME)
            playlist_id = result["id"]

        first_roop_flag = 0
    
    target_track_ids=pd.concat([track_id_and_track_name, grepd_track_features], axis=1).dropna(how='any')['track_id']

    sp.user_playlist_add_tracks(user = user_id, playlist_id = playlist_id, tracks = target_track_ids)

    offset+=MAX_LIMIT