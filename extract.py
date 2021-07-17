import requests
# import sqlalchemy
import pandas as pd
# from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
import datetime as dt
import sqlite3

DB_LOCATION = "sqlite:///my_tracks.sqlite"
USER_ID = "thisisishara"
TOKEN = "BQBL-yeMBTwnOFd0Y_E2CWoyD8PBv-InImdsX5_FqHBjm4kKZdz-1mQInjqJrWyLxw21G1fePbyYkghRBYpKXeR19BSEV4TYyeOvIKWvQymEoQmpfR0DjlAUBgbSUezSyIDOvmdxEzroGZvMBDdX2-oFa_qqSTKHK8-7"

if __name__ == '__main__':

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.now()
    ydy = today - dt.timedelta(days=1)
    ydy_unix_timestamp = int(ydy.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
        time=ydy_unix_timestamp), headers=headers)

    data = r.json()

    # print(data)

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

    print(songs_dataframe)
