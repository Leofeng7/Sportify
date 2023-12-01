import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class Recommender():
    def __init__(self, user_songs, activity_feature, genres, sp):
        self.activity_feature = activity_feature
        self.sp = sp
        self.genres = genres
        self.recommendation_pool = self.get_recommendation_pool()
        #self.user_songs = self.build_user_songs_dataframe(user_songs)
        self.relevant_features = ['popularity',
                                'danceability',
                                'energy',
                                'loudness',
                                'mode',
                                'valence',
                                'tempo']
        self.scaler = StandardScaler()
        self.scaler.fit(self.recommendation_pool[self.relevant_features])
        self.recommendation_pool = self.transform_features(self.recommendation_pool)
        
    def transform_features(self, songscopy):
        songscopy[self.relevant_features] = self.scaler.transform(songscopy[self.relevant_features])
        return songscopy 

    # Gets recommendations from spotify based on various genres and music features correlated with an activity. These feature vectors are generated
    # in main using the GptAPI class. 
    def get_recommendation_pool(self):
        spotify_data = pd.read_csv('spotify_data.csv')

        spotify_data = spotify_data[spotify_data['genre'].isin(self.genres)]
        return spotify_data

        #all_recommendations = []
        #for genre in self.genres:
            #recommendations = self.sp.recommendations(seed_genres=[genre],limit=2, target=target_features)
            #all_recommendations.append(recommendations['tracks'])

        #return self.build_recommendation_dataframe(all_recommendations)
    
    # Builds a DataFrame representing the features of the songs the user has saved (to learn about their preferences)
    def build_user_songs_dataframe(self, user_songs):
        songs_data = []
        for item in user_songs:
            track = item['track']
            audio_features = self.sp.audio_features(track['id'])[0]
            track_data = {
                'track_id': track['id'],
                'popularity': track['popularity'],
                'year': int(track['album']['release_date'].split('-')[0]),
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'loudness': audio_features['loudness'],
                'valence': audio_features['valence'],
                'tempo': audio_features['tempo'],
                'added_at': int(item['added_at'].split('-')[0])
            }
            songs_data.append(track_data)
            saved_songs = pd.DataFrame(songs_data)
            return saved_songs
        
    # Builds a dataframe of the recommendations received from the spotipy API, with specific features aligned with the feature vector
    # Generated from the ChatGPT API
    def build_recommendation_dataframe(self, tracks_list):
        songs_dataframe = pd.DataFrame([])
        for tracks in tracks_list:
            songs_data = []
            for track in tracks:
                audio_features = self.sp.audio_features(track['id'])[0]
                track_data = {
                    'artist_name': track['artists'][0]['name'],
                    'album_cover_url': track['album']['images'][0]['url'],
                    'track_name': track['name'],
                    'track_id': track['id'],
                    'popularity': track['popularity'],
                    'year': int(track['album']['release_date'].split('-')[0]),
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'loudness': audio_features['loudness'],
                    'valence': audio_features['valence'],
                    'tempo': audio_features['tempo'],
                }
                songs_data.append(track_data)
            songs_data = pd.DataFrame(songs_data)
            songs_dataframe = pd.concat([songs_dataframe, songs_data], ignore_index=True)

        songs_dataframe = songs_dataframe.drop_duplicates(subset='track_id')
        return songs_dataframe       
    
    def get_recommendations(self):
        activity_vector = np.array(self.activity_feature).reshape(1, -1)

        similarity = cosine_similarity(self.recommendation_pool[self.relevant_features], self.scaler.transform(activity_vector))
        self.recommendation_pool['cosine_similarity'] = similarity
        best_recommendations = self.recommendation_pool.sort_values(by='cosine_similarity', ascending=False).head(10)
        
        best_track_dictionary = []

        for index, row in best_recommendations.iterrows():
            best_track_dictionary.append({
                'name': row['track_name'],
                'artist': row['artist_name'],
                'album_cover_url': self.sp.track(row['track_id'])['album']['images'][0]['url']
            })

        return best_track_dictionary




