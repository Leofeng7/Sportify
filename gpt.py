from openai import OpenAI
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class GptAPI:
    def load_activity_feature_vectors(self):
        activities = ["traveling", "writing", "drawing", "cleaning", "meditating" ,"gardening","shopping"
        ,"socializing","streaming" ,"daydreaming","coding"
        ,"working","studying","cooking","relaxing","commuting"
        ,"exercising","gaming"
        ,"partying","sleeping"]
        feature_vectors = {}

        for activity in activities:
            prompt = f"Generate a comma-separated float feature vector for the activity '{activity}' based on the spotify API for the features in songs: popularity, danceability, energy, loudness, mode, valence, and tempo. Please provide the values in the specified order and format only. Popularity should be between 0 and 100. Danceability and energy should be between 0 and 1, and loudness should be in decibels. Mode should be 0 or 1, and valence should be between 0 and 1. Tempo should be in beats per minute. Do not specify units such as 'dB' after the values."
            response = self.client.completions.create(model="text-davinci-003", prompt=prompt, max_tokens=100)

            try:
                feature_vector = [float(x.strip().replace('−', '-')) for x in response.choices[0].text.split(',')]
                feature_vectors[activity] = feature_vector
            #error handling
            except ValueError as e:
                print(f"Error parsing response for activity '{activity}': {e}")
                print("Response received:", response.choices[0].text)

        self.feature_vectors = feature_vectors

    def get_activity_feature_vectors(self):
        return self.feature_vectors

    def __init__(self):
        self.client = OpenAI(api_key="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")
        self.load_activity_feature_vectors()

#selected_features = ['popularity', 'danceability', 'energy', 'loudness', 'mode', 'valence', 'tempo']

#songs_scaled = scaler.fit_transform(songs[selected_features])
#songs_scaled_df = pd.DataFrame(songs_scaled, columns=selected_features)

#K = 5
#nearest_songs = {}

#for activity, vector in feature_vectors.items():
    #activity_vector = np.array(vector).reshape(1, -1)

    #similarities = cosine_similarity(activity_vector, songs_scaled_df.values)
    #k_indices = np.argsort(similarities[0])[-K:]
    #nearest_songs[activity] = songs.iloc[k_indices][['track_name', 'artists', 'album_name']]

# Display the recommendations for each activity
#for activity, recommendations in nearest_songs.items():
    #print(f"\nTop {K} song recommendations for {activity}:")
    #for i, song in recommendations.iterrows():
        #print(f"{i+1}. '{song['track_name']}' by {song['artists']} (Album: {song['album_name']})")

