from openai import OpenAI
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class GptAPI:
    def load_activity_feature_vectors(self, activity):
        feature_vector = []
        prompt = f"Generate a comma-separated float feature vector for the activity '{activity}' based on the spotify API for the features in songs: popularity, danceability, energy, loudness, mode, valence, and tempo. Please provide the values in the specified order and format only. Popularity should be between 0 and 100. Danceability and energy should be between 0 and 1, and loudness should be in decibels. Mode should be 0 or 1, and valence should be between 0 and 1. Tempo should be in beats per minute. Do not specify units such as 'dB' after the values."
        response = self.client.completions.create(model="text-davinci-003", prompt=prompt, max_tokens=100)

        try:
            feature_vector = [float(x.strip().replace('−', '-')) for x in response.choices[0].text.split(',')]
        #error handling
        except ValueError as e:
            print(f"Error parsing response for activity '{activity}': {e}")
            print("Response received:", response.choices[0].text)

        return feature_vector

    def __init__(self):
        self.client = OpenAI(api_key="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")
        self.activity_genre_map = {
            "traveling": ["alternative", "indie", "pop"],
            "writing": ["ambient", "chill", "classical"],
            "drawing": ["indie", "chill", "ambient"],
            "cleaning": ["pop", "dance", "edm"],
            "meditating": ["ambient", "chill", "classical"],
            "gardening": ["country", "chill", "classical"],
            "shopping": ["pop", "dance", "edm"],
            "socializing": ["pop", "r-n-b", "hip-hop"],
            "streaming": ["pop", "edm", "hip-hop"],
            "daydreaming": ["ambient", "indie", "chill"],
            "coding": ["study", "chill", "ambient"],
            "working": ["study", "work-out", "classical"],
            "studying": ["study", "classical", "ambient"],
            "cooking": ["pop", "country", "dance"],
            "relaxing": ["chill", "ambient", "classical"],
            "commuting": ["pop", "indie", "hip-hop"],
            "exercising": ["work-out", "edm", "hip-hop"],
            "gaming": ["edm", "rock", "hip-hop"],
            "partying": ["club", "dance", "hip-hop"],
            "sleeping": ["sleep", "ambient", "chill"]
        }

    def get_activity_genres(self, activity):
        return self.activity_genre_map[activity]

