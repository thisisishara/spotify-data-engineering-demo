import requests
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
import datetime as dt
import sqlite3

def validate_songs_data(df: pd.DataFrame):
    # Empty Dataset check
    if df.empty:
        print("The recently played song list is empty. Exiting execution.")
        return False

    # Business Key violation check
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary Key constraint violated.")

    # Null check
    if df.isnull().values.any():
        raise Exception("Null values are present in the dataset. Exiting execution.")

    # Timestamp check
    ydy_t = datetime.now() - dt.timedelta(days=1)
    ydy_t = ydy_t.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps_l = df["timestamp"].tolist()
    for t_stamp in timestamps_l:
        if datetime.strptime(t_stamp, "%Y-%m-%d") < ydy_t:
            raise Exception(f"{datetime.strptime(t_stamp, '%Y-%m-%d')}\nIncompatible Timestamp found. Exiting execution.")

    return True


def run_spotify_etl():

    db_loc = "sqlite:///my_tracks.sqlite"
    user_id = "thisisishara"
    token = "BQDeDjuOJTzxcGsZgadXFtMOWh1qO1gynyZkjUdTiJJmo0vLEOd2gXwH4c-AtAY3CGCA1c-YiMs04UbOunhkuBvi5bm5Z0d-Ql1jjzmAT0VLv2oEVeSMdMVtRElqGDNLljHlZ10ACwHJijoHLYTH7MCNNJxaZASolHEO"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=token)
    }

    today = datetime.now()
    ydy = today - dt.timedelta(days=1)
    ydy_unix_timestamp = int(ydy.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
        time=ydy_unix_timestamp), headers=headers)

    data = r.json()

    # print(data)

    if "error" in data:
        print("Couldn't acquire recently played song data.\n{status}: {msg}.".format(status=data["error"]["status"],
                                                                                     msg=data["error"]["message"]))
        quit()

    song_names = []
    artist_names = []
    played_times = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_times.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_times,
        "timestamp": timestamps
    }

    songs_dataframe = pd.DataFrame(song_dict, columns=song_dict.keys())
    # print(songs_dataframe)

    # Data validation
    if not validate_songs_data(songs_dataframe):
        print("Data validation failed.")
        quit()

    print("valid data")

    # Load Data
    engine = sqlalchemy.create_engine(db_loc)
    conn = sqlite3.connect('my_tracks.sqlite')
    cursor = conn.cursor()

    sql_q = """
            CREATE TABLE IF NOT EXISTS my_recent_tracks(
                song_name VARCHAR(200),
                artist_name VARCHAR(200),
                played_at VARCHAR(200),
                timestamp VARCHAR(200),
                CONSTRAINT my_recent_tracks_pk PRIMARY KEY (played_at)
            );           
            """
    cursor.execute(sql_q)

    try:
        songs_dataframe.to_sql("my_recent_tracks", engine, index=False, if_exists="append")
    except:
        print("Possible duplication. Data insertion aborted.")

    conn.close()
    print("Connection closed.\nData insertion succeeded.")
