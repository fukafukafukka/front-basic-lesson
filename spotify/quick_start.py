import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager= SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)

name = 'Monthly Mu & New Caledonia'
result = spotify.search(q='artist:' + name, type='artist')
print(result)

#print(spotify.current_user_playing_track())

#print(spotify.user("3132ozmy4z4qexsvr3sg5f34q6je"))

#iresults = spotify.current_user_saved_tracks()
#print(results)

#print(spotify.me())
#print(spotify.current_user())
#print(spotify.current_user_followed_artists(limit=20))

#playlists = spotify.user_playlists('3132ozmy4z4qexsvr3sg5f34q6je',limit=10, offset = 0)
#while playlists:
#    for i, playlist in enumerate(playlists['items']):
#        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#    if playlists['next']:
#        playlists = sp.next(playlists)
#    else:
#        playlists = None
