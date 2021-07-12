import sqlalchemy
import pandas as pd

from sqlalchemy.orm import sessionmaker

import requests

import json

import datetime

import sqlite3

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded")
        return False

    if not pd.Series(df['played_at_list']).is_unique:
        raise Exception("PK Check is violated")

    if df.isnull().values.any():
        raise Exception("null valued found")

    return True

DATABASE_LOCATION = "sqlite:///db.sqlite"
USER_ID = "<id_spotify>"
TOKEN = "<token_from_spotifyAPI>"

if __name__ == "__main__":

    ### EXTRACT
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN) 
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=60)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    # print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"]) 
        played_at_list.append(song["played_at"]) 
        timestamps.append(song["played_at"][0:10])

    to_df = {
        "song" : song_names,
        "artist" : artist_names,
        "played_at_list" : played_at_list,
        "timestamp" : timestamps
    }

    df = pd.DataFrame(to_df)
    # print(df)


    ### TRANSFORM
    if check_if_valid_data(df):
        print("OK")

    ### LOAD
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS tracks (
        song VARCHAR(200),
        artist VARCHAR(200),
        played_at_list VARCHAR(200),
        timestamp VARCHAR(200),

        CONSTRAINT primary_key_constraint PRIMARY KEY(played_at_list)
    );
    """

    cursor.execute(sql_query)

    try:
        df.to_sql("tracks", engine, index=False, if_exists="append")
    except:
        print("ga boleh")

    q = """
    select * from tracks;
    """
    cursor.execute(q)
    a = cursor.fetchall()

    s = pd.DataFrame(a)

    print(s)

    

