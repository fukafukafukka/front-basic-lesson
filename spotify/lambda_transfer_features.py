import os
import sys
from datetime import date
from io import StringIO
from boto3.session import Session
import pandas as pd
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

def get_track_features(track_ids):
    return list(filter(None, sp.audio_features(track_ids)))

def put_to_s3(access_key_id, secret_access_key, region_name, bucket_name, directory_name, file_name, encode, data):
    session = Session(
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name=region_name
                      )
    
    obj = session.resource('s3').Bucket(bucket_name).Object(directory_name + '/' +file_name)
    
    try:
        obj.put(
            Body=data.getvalue(),
            ContentEncoding=encode,
            ContentType='text/tsv'
        )
    except AttributeError as e:
        print(e)
        sys.exit()


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

    track_id_list = list(track_id_set)
    track_features=None
    start_point = 0
    end_point = 100
    while True:
        if len(track_id_list) - (start_point) >= 100:
            if track_features is None:
                track_features = get_track_features(track_id_list[start_point:end_point])
            else:
                track_features.extend(get_track_features(track_id_list[start_point:end_point]))
            start_point+=100
            end_point+=100
            continue
        else:
            if track_features is None:
                track_features = get_track_features(track_id_list[start_point:])
            else:
                track_features.extend(get_track_features(track_id_list[start_point:]))
            break

    tsv_buffer = StringIO()
    pd.DataFrame(track_features, columns=['id','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','type','duration_ms','time_signature','analysis_url','uri','track_href']).to_csv(tsv_buffer, sep='\t', index = False)

    put_to_s3(
            os.getenv('S3_ACCESS_KEY_ID'),
            os.getenv('S3_SECRET_ACCESS_KEY'),
            os.getenv('S3_REGION_NAME'),
            os.getenv('S3_BUCKET_NAME'),
            os.getenv('S3_DIRECTORY_PATH'),
            os.getenv('S3_FEATURES_FILE_PREFIX_NAME') + '_' + date.today().strftime('%Y%m%d') + '.tsv',
            os.getenv('S3_ENCODE'),
            tsv_buffer)

if __name__ == '__main__':
    lambda_handler(event=None, context=None)