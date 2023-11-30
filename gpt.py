from openai import OpenAI
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

client = OpenAI(api_key="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")

activities = ['studying', 'gym', 'sleep', 'work', 'relaxing']
feature_vectors = {}

for activity in activities:
    prompt = f"Generate a comma-separated feature vector for the activity '{activity}' with numerical scores out of 1 for the features: popularity, danceability, energy, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms. Please provide the values in the specified order and format only."
    response = client.completions.create(model="text-davinci-003", prompt=prompt, max_tokens=100)

    try:
        feature_vector = [float(x.strip()) for x in response.choices[0].text.split(',')]
        feature_vectors[activity] = feature_vector
    #error handling
    except ValueError as e:
        print(f"Error parsing response for activity '{activity}': {e}")
        print("Response received:", response.choices[0].text)

print(feature_vectors)

selected_features = ['popularity', 'danceability', 'energy', 'loudness', 'mode',
                     'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo', 'duration_ms']

songs_scaled = scaler.fit_transform(songs[selected_features])
songs_scaled_df = pd.DataFrame(songs_scaled, columns=selected_features)


K = 5
nearest_songs = {}

for activity, vector in feature_vectors.items():
    activity_vector = np.array(vector).reshape(1, -1)

    similarities = cosine_similarity(activity_vector, songs_scaled_df.values)
    k_indices = np.argsort(similarities[0])[-K:]
    nearest_songs[activity] = songs.iloc[k_indices][['track_name', 'artists', 'album_name']]

# Display the recommendations for each activity
for activity, recommendations in nearest_songs.items():
    print(f"\nTop {K} song recommendations for {activity}:")
    for i, song in recommendations.iterrows():
        print(f"{i+1}. '{song['track_name']}' by {song['artists']} (Album: {song['album_name']})")

