import os
import sys
from io import StringIO
from boto3.session import Session
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


scope = "user-library-read playlist-read-private"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=False))

def get_track_and_artist_info(saved_tracks):
    track_id = lambda i: saved_tracks['items'][i]['track']['id']
    track_name = lambda i: saved_tracks['items'][i]['track']['name']
    artist_id = lambda i: saved_tracks['items'][i]['track']['artists'][0]['id']
    artist_name = lambda i: saved_tracks['items'][i]['track']['artists'][0]['name']
    return [[track_id(i), track_name(i), artist_id(i), artist_name(i)] for i in range(len(saved_tracks['items']))]

def get_my_library_list():
    my_library_list=None
    MAX_LIMIT=50
    offset=0
    while True:
        saved_tracks = sp.current_user_saved_tracks(limit=MAX_LIMIT, offset=offset)

        if not saved_tracks['items']:
            print("saved_tracks is empty")
            break
        
        if my_library_list is None:
            my_library_list = get_track_and_artist_info(saved_tracks)
        else:
            my_library_list.extend(get_track_and_artist_info(saved_tracks))
        
        offset+=50
    return my_library_list

def put_to_s3(data):
    session = Session(
                    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('S3_REGION_NAME')
                      )
    
    obj = session.resource('s3').Bucket(os.getenv('S3_BUCKET_NAME')).Object(os.getenv('S3_FILE_NAME'))
    
    try:
        obj.put(
            Body=data.getvalue(),
            ContentEncoding=os.getenv('S3_ENCODE'),
            ContentType='text/tsv'
        )
    except AttributeError as e:
        print(e)
        sys.exit()


def lambda_handler(event, context):
    my_library_list = get_my_library_list()

    tsv_buffer = StringIO()
    pd.DataFrame(my_library_list, columns=['track_id','track_name','artist_id','artist_name']).to_csv(tsv_buffer, sep='\t', index = False)

    put_to_s3(tsv_buffer)

    return {
        'status_code': 200
    }

if __name__ == '__main__':
    lambda_handler(event=None, context=None)