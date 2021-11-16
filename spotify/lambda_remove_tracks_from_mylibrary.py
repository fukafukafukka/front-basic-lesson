import os
import sys
from datetime import date
from io import StringIO
from boto3.session import Session
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-modify"
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

def remove_tracks_from_myLibrary(track_id_list):
    # 50個ずつしか追加できないので、以下の実装となっている。
    start_point = 0
    end_point = 50
    while True:
        if len(track_id_list) - (start_point) >= 50:
            sp.current_user_saved_tracks_delete(track_id_list[start_point:end_point])
            start_point+=50
            end_point+=50
            continue
        else:
            #sp.current_user_saved_tracks_delete(track_id_list[start_point:])
            sp.current_user_saved_tracks_delete(['5ZHZZ3pLEJWVYpKikkZfG9', '0GI4cqCrJber7aM1MgFXng', '13M8jXMGKe2lziMAzCI8Eo', '3zUPDIYRJdsUADk014nT0U', '1qTtUGIadTvH8Dmkq5mPfX', '4ZUQi2DvFFwNqkhsxNnQIA', '6dRd5ySNNQpPMVR9Uz2qWs', '1ym4KwgWGyOeqROuoSGUZ5', '7l5bzhIGZD6KCrTm6uhH93', '1Eanz2WgGT0LU4k7xcwrjC', '0U06wd20yXK4TMPUwDOmme'])
            break

def lambda_handler(event, context):
    track_id_list = []
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
        track_id_list = df["track_id"].tolist()

    if len(track_id_list) > 0:
        remove_tracks_from_myLibrary(track_id_list)

if __name__ == '__main__':
    lambda_handler(event=None, context=None)
