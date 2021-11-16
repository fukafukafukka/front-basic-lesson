import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing playlist-modify-public user-library-read user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

current_playing = sp.current_user_playing_track()
track_name = current_playing['item']['name']
track_id = current_playing["item"]["id"]
artist_name = current_playing['item']['artists'][0]['name']
print(track_name + "/" + artist_name)

#Spotifyの注目のプレイリストのリストを取得する
#print(sp.featured_playlists())

#現在のユーザーのトップトラックを取得する
print(sp.current_user_top_artists(limit=10))
