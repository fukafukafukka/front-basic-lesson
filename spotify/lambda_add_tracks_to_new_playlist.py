import os
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
from io import StringIO
from boto3.session import Session
import pandas as pd
from nested_lookup import nested_lookup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read playlist-read-private"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path="./cache")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True))

def check_s3_object(access_key_id, secret_access_key, region_name, bucket_name, directory_name, file_name):
    session = Session(
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name=region_name
                      )
    
    bucket = session.resource('s3').Bucket(bucket_name)
    objs = bucket.meta.client.list_objects_v2(Bucket=bucket.name, Prefix=directory_name, MaxKeys=100)

    key = lambda i: objs["Contents"][i]["Key"]
    key_list = [key(i) for i in range(len(objs["Contents"]))]

    if directory_name + '/' + file_name in key_list:
        return True
    else:
        return False
    
def get_s3_object(access_key_id, secret_access_key, region_name, bucket_name, directory_name, file_name):
    session = Session(
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name=region_name
                      )
    
    obj = session.resource('s3').Bucket(bucket_name).Object(directory_name + '/' +file_name)

    body=None
    try:
        body = obj.get()['Body'].read().decode('utf-8')
    except AttributeError as e:
        print(e)
        sys.exit()
    return body

def make_playlist(user_id, playlist_name):
    if playlist_name not in nested_lookup('name', sp.current_user_playlists()):
        return sp.user_playlist_create(user_id, playlist_name)

    # playlistが既に存在する場合は、playlist_nameでもってid検索して返すようにしたい。
    return None

def add_tracks_to_playlist(user_id, playlist_id, track_id_list):
    # 100個ずつしか追加できないので、以下の実装となっている。
    start_point = 0
    end_point = 100
    while True:
        if len(track_id_list) - (start_point) >= 100:
            sp.user_playlist_add_tracks(user_id, playlist_id, track_id_list[start_point:end_point])
            start_point+=100
            end_point+=100
            continue
        else:
            sp.user_playlist_add_tracks(user_id, playlist_id, track_id_list[start_point:])
            break

def lambda_handler(event, context):
    track_id_set = set()
    if (check_s3_object(
            os.getenv('S3_ACCESS_KEY_ID'),
            os.getenv('S3_SECRET_ACCESS_KEY'),
            os.getenv('S3_REGION_NAME'),
            os.getenv('S3_BUCKET_NAME'),
            os.getenv('S3_DIRECTORY_PATH'),
            os.getenv('S3_FILE_PREFIX_NAME') + '_' + date.today().strftime('%Y%m%d') + '.tsv'
            )
        ):
        buffer_in = StringIO(
            get_s3_object(
                os.getenv('S3_ACCESS_KEY_ID'),
                os.getenv('S3_SECRET_ACCESS_KEY'),
                os.getenv('S3_REGION_NAME'),
                os.getenv('S3_BUCKET_NAME'), 
                os.getenv('S3_DIRECTORY_PATH'),
                os.getenv('S3_FILE_PREFIX_NAME') + '_' + date.today().strftime('%Y%m%d') + '.tsv'
                )
            )
        df = pd.read_csv(buffer_in, sep="\t", lineterminator='\n')
        track_id_set = set(df["track_id"].tolist())

    user_id = sp.current_user()['id']

    response = make_playlist(user_id, "myLibrary"+"_"+(date.today() - relativedelta(months=1)).strftime('%Y%m'))
    if response is None:
        return {
            'status_code': 200
        }
    
    add_tracks_to_playlist(user_id, response["id"], list(track_id_set))

if __name__ == '__main__':
    lambda_handler(event=None, context=None)