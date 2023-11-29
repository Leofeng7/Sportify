import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, abort

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials

def create_spotify_oauth(user_credentials):
    return SpotifyOAuth(client_id=user_credentials['SPOTIFY_CLIENT_ID'],
                        client_secret=user_credentials['SPOTIFY_CLIENT_SECRET'],
                        redirect_uri=user_credentials['REDIRECT_URI'],
                        scope="playlist-read-private")

def get_playlist_tracks(sp, username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

app = Flask(__name__)

@app.route("/<username>")
def index(username):
    credentials = load_credentials('credentials.json')
    user_credentials = credentials.get(username)
    
    if not user_credentials:
        abort(404)

    sp_oauth = create_spotify_oauth(user_credentials)
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    playlist_id = '2b8pyKWkXM7PvPtXZ6aNLH'  
    tracks = get_playlist_tracks(sp, user_credentials['SPOTIFY_USERNAME'], playlist_id)
    return render_template('index.html', tracks=tracks, username=username)

@app.route("/<username>/playlist/daily-mix-1")
def daily_mix_1(username):
    credentials = load_credentials('credentials.json')
    user_credentials = credentials.get(username)
    
    if not user_credentials:
        abort(404)

    sp_oauth = create_spotify_oauth(user_credentials)
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    playlist_id = '2b8pyKWkXM7PvPtXZ6aNLH'  
    tracks = get_playlist_tracks(sp, user_credentials['SPOTIFY_USERNAME'], playlist_id)
    return render_template('playlist.html', tracks=tracks, username=username)

if __name__ == "__main__":
    app.run(debug=False)
