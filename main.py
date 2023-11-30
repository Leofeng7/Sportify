import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, abort, request

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials

def create_spotify_oauth(user_credentials):
    return SpotifyOAuth(client_id=user_credentials['SPOTIFY_CLIENT_ID'],
                        client_secret=user_credentials['SPOTIFY_CLIENT_SECRET'],
                        redirect_uri=user_credentials['REDIRECT_URI'],
                        scope="playlist-read-private")

def get_playlist_tracks(sp, username, playlist_id, limit=10):
    results = sp.user_playlist_tracks(username, playlist_id, limit=limit)
    tracks_with_images = []
    count = 0
    for item in results['items']:
        if count < limit:
            track = item['track']
            album_cover_url = track['album']['images'][0]['url']  
            tracks_with_images.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album_cover_url': album_cover_url
            })
            count += 1  
        else:
            break  
    while results['next'] and count < limit:
        results = sp.next(results)
        for item in results['items']:
            if count < limit:
                track = item['track']
                album_cover_url = track['album']['images'][0]['url']
                tracks_with_images.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album_cover_url': album_cover_url
                })
                count += 1
            else:
                break  

    return tracks_with_images
    
app = Flask(__name__)

@app.route("/<username>")
def index(username):
    credentials = load_credentials('credentials.json')
    user_credentials = credentials.get(username)
    
    if not user_credentials:
        abort(404)

    return render_template('index.html', tracks=None, username=username)

@app.route("/<username>/search")
def search(username):
    activity = request.args.get('activity', '')
    credentials = load_credentials('credentials.json')
    user_credentials = credentials.get(username)
    
    if not user_credentials:
        abort(404)

    return render_template('search.html', tracks=None, username=username, activity=activity)

@app.route("/<username>/playlist/daily-mix-1")
def daily_mix_1(username):
    credentials = load_credentials('credentials.json')
    user_credentials = credentials.get(username)
    
    if not user_credentials:
        abort(404)

    sp_oauth = create_spotify_oauth(user_credentials)
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    playlist_id = user_credentials['PLAYLIST_ID']
    tracks = get_playlist_tracks(sp, user_credentials['SPOTIFY_USERNAME'], playlist_id)
    return render_template('playlist.html', tracks=tracks, username=username)

if __name__ == "__main__":
    app.run(debug=False)
