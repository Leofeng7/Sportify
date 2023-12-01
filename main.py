import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, abort, request
import gpt
import RecommendationSystem

class Sportify:
    def __init__(self, name, gptAPI):
        self.app = Flask(name)
        self.setup_routes()
        self.gptAPI = gptAPI
        self.credentials = self.load_credentials('credentials.json')
    
    def setup_routes(self):
        @self.app.route("/<username>")
        def index(username):
            user_credentials = self.credentials.get(username)
            if not user_credentials:
                abort(404)
            return render_template('index.html', tracks=None, username=username)

        @self.app.route("/<username>/search")
        def search(username):
            activity = request.args.get('activity', '')
            user_credentials = self.credentials.get(username)
            if not user_credentials:
                abort(404)
            
            sp_oauth = self.create_spotify_oauth(user_credentials)
            sp = spotipy.Spotify(auth_manager=sp_oauth)
            feature_vector = self.gptAPI.get_activity_feature_vectors()[activity]

            recommender = RecommendationSystem.Recommender(sp.current_user_saved_tracks(), feature_vector, self.gptAPI.get_activity_genres(activity), sp)
            recommendations = recommender.get_recommendations()
            return render_template('search.html', tracks=recommendations, username=username, activity=activity)

        @self.app.route("/<username>/playlist/daily-mix-1")
        def daily_mix_1(username):
            credentials = self.load_credentials('credentials.json')
            user_credentials = credentials.get(username)
            if not user_credentials:
                abort(404)
            sp_oauth = self.create_spotify_oauth(user_credentials)
            sp = spotipy.Spotify(auth_manager=sp_oauth)
            playlist_id = user_credentials['PLAYLIST_ID']
            tracks = self.get_playlist_tracks(sp, user_credentials['SPOTIFY_USERNAME'], playlist_id)

            return render_template('playlist.html', tracks=tracks, username=username)

    def load_credentials(self, file_path):
        with open(file_path, 'r') as file:
            credentials = json.load(file)
        return credentials

    def create_spotify_oauth(self, user_credentials):
        return SpotifyOAuth(client_id=user_credentials['SPOTIFY_CLIENT_ID'],
                            client_secret=user_credentials['SPOTIFY_CLIENT_SECRET'],
                            redirect_uri=user_credentials['REDIRECT_URI'],
                            scope="playlist-read-private")
    
    def build_tracks_with_images2(self, results):
        tracks_with_images = []
        for track in results['tracks']:
            album_cover_url = track['album']['images'][0]['url']  
            tracks_with_images.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album_cover_url': album_cover_url
            })
        return tracks_with_images

    def build_tracks_with_images(self, results, limit=10):
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
            results = self.sp.next(results)
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


    def get_playlist_tracks(self, sp, username, playlist_id, limit=10):
        results = sp.user_playlist_tracks(username, playlist_id, limit=limit) 
        return self.build_tracks_with_images(results)

if __name__ == "__main__":
    gptAPI = gpt.GptAPI()
    sportify_app = Sportify(__name__, gptAPI)
    sportify_app.app.run(port=5020)