import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template

def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('/'):
                continue
            key, value = line.strip().split('=', 1)
            credentials[key] = value
    return credentials

credentials = load_credentials('credentials.txt')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials['SPOTIFY_CLIENT_ID'],
                                               client_secret=credentials['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=credentials['REDIRECT_URI'],
                                               scope="playlist-read-private"))
def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

app = Flask(__name__)

@app.route("/")
def index():
    username = '1295463866'
    playlist_id = '2b8pyKWkXM7PvPtXZ6aNLH'
    tracks = get_playlist_tracks(username, playlist_id)
    return render_template('index.html', tracks=tracks)

@app.route("/playlist/daily-mix-1")
def daily_mix_1():
    username = '1295463866'
    playlist_id = '2b8pyKWkXM7PvPtXZ6aNLH'
    tracks = get_playlist_tracks(username, playlist_id)
    return render_template('playlist.html', tracks=tracks)

if __name__ == "__main__":
    app.run(debug=False)