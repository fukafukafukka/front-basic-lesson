import os
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
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
        print("exit")
        return True
    else:
        print("not exit")
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

def get_related_artist_id_list(artist_ids):
    artist_id = lambda i: artist_ids[i]
    api = lambda i: sp.artist_related_artists(artist_id(i))
    related_infos = [api(i)["artists"] for i in range(len(artist_ids))]

    related_artist_id_set = set()
    for one_artist_related_infos in related_infos:
        for one_artist_related_info in one_artist_related_infos:
            related_artist_id_set.add(one_artist_related_info["id"])
    return list(related_artist_id_set)

def get_artist_top_tracks(artist_ids):
    artist_id = lambda i: artist_ids[i]
    api = lambda i: sp.artist_top_tracks(artist_id(i))
    top_tracks = [api(i)["tracks"] for i in range(len(artist_ids))]

    artist_track_list = []
    for one_artist_top_tracks in top_tracks:
        for one_artist_top_track in one_artist_top_tracks:
            for i in range(len(one_artist_top_track["artists"])):
                artist_track_list.append([one_artist_top_track["id"], one_artist_top_track["name"], one_artist_top_track["artists"][i]["id"], one_artist_top_track["artists"][i]["name"]])
    return pd.DataFrame(artist_track_list, columns=['track_id','track_name','artists_id','artists_name'])

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
    print('今月のartist_id')
    artist_id_set = set()
    if (check_s3_object(
            os.getenv('S3_ACCESS_KEY_ID'),
            os.getenv('S3_SECRET_ACCESS_KEY'),
            os.getenv('S3_REGION_NAME'),
            os.getenv('S3_BUCKET_NAME'),
            os.getenv('S3_DIRECTORY_PATH'),
            os.getenv('S3_FILE_PREFIX_NAME') + '_' + date.today().strftime('%Y%m%d') + '.tsv')):
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
        artist_id_set = set(df["artist_id"].tolist())

    print('先月のartist_id')
    artist_id_set_at_last_month = set()
    if (check_s3_object(
            os.getenv('S3_ACCESS_KEY_ID'),
            os.getenv('S3_SECRET_ACCESS_KEY'),
            os.getenv('S3_REGION_NAME'),
            os.getenv('S3_BUCKET_NAME'),
            os.getenv('S3_DIRECTORY_PATH'),
            os.getenv('S3_FILE_PREFIX_NAME') + '_' + (date.today() - relativedelta(months=1)).strftime('%Y%m%d') + '.tsv')):
        buffer_in = StringIO(
            get_s3_object(
                os.getenv('S3_ACCESS_KEY_ID'),
                os.getenv('S3_SECRET_ACCESS_KEY'),
                os.getenv('S3_REGION_NAME'),
                os.getenv('S3_BUCKET_NAME'),
                os.getenv('S3_DIRECTORY_PATH'),
                os.getenv('S3_FILE_PREFIX_NAME') + '_' + (date.today() - relativedelta(months=1)).strftime('%Y%m%d') + '.tsv'
                )
            )
        df = pd.read_csv(buffer_in, sep="\t", lineterminator='\n')
        artist_id_set_at_last_month = set(df["artist_id"].tolist())

    print('差分を抽出する。')
    artist_id_list = list(artist_id_set - artist_id_set_at_last_month)
    if (len(artist_id_list) == 0):
        return {
            'status_code': 200
        }

    print('get_related_artist_id_list')
    related_artist_id_list = get_related_artist_id_list(artist_id_list)

    print('get_artist_top_tracks')
    artist_track_list = get_artist_top_tracks(related_artist_id_list)


    print('tsv_buffer = StringIO()')
    tsv_buffer = StringIO()
    pd.DataFrame(artist_track_list, columns=['track_id','track_name','artists_id','artists_name']).to_csv(tsv_buffer, sep='\t', index = False)

    print('put_to_s3')
    put_to_s3(
            os.getenv('S3_ACCESS_KEY_ID'),
            os.getenv('S3_SECRET_ACCESS_KEY'),
            os.getenv('S3_REGION_NAME'),
            os.getenv('S3_BUCKET_NAME'),
            os.getenv('S3_DIRECTORY_PATH'),
            os.getenv('S3_RELATED_FILE_PREFIX_NAME') + '_' + date.today().strftime('%Y%m%d') + '.tsv',
            os.getenv('S3_ENCODE'),
            tsv_buffer)

    return {
        'status_code': 200
    }

if __name__ == '__main__':
    lambda_handler(event=None, context=None)