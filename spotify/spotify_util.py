import spotipy
import spotipy.util as util

scope='user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
username='3132ozmy4z4qexsvr3sg5f34q6je'
token = util.prompt_for_user_token(scope, username)
sp = spotipy.Spotify(auth = token)
