import time
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

CLIENT_ID = "INSERT-CLIENT-ID"
CLIENT_SECRET = "INSERT-CLIENT-SECRET"
REDIRECT_URI = "http://localhost:8080/callback"


SCOPE = "user-read-private user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

currentSong = ""
def get_current_user():
    user = sp.current_user()
    print(f"Begin session\nLog-in as: {user['display_name']}")

# Get the currently playing song
def get_current_song():
    currently_playing = sp.currently_playing()
    if currently_playing and currently_playing.get('is_playing'):
        song_name = currently_playing['item']['name']
        artist_name = ", ".join(artist['name'] for artist in currently_playing['item']['artists'])
        return [song_name, artist_name]
    else:
        return []

def listening():
    while True:
        try:
            update_song()
        except KeyboardInterrupt:
            print('Ending session')
            break
        except ReadTimeout:
            time.sleep(20)

def update_song():
    global currentSong
    data = []
    song = get_current_song()
    if song:
        name = song[0]
        if name != currentSong:
            current_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S%p").split(" ")
            date = current_time[0]
            time_of_date = current_time[1]
            artist = song[1]
            data.append([date, name, artist, time_of_date])
            with open('SongHistory.csv', 'a', newline='') as csvfile:
                dw = csv.writer(csvfile)
                dw.writerows(data)
            currentSong = name
            time.sleep(10)

def main():
    get_current_user()
    listening()

if __name__ == "__main__":
    main()
