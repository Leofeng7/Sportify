# Sportify

## Description

A spotify-like music recommender system that suggests songs based on the user's current activity and the features of their saved songs.

## How it Works

When a user asks for recommendations for a certain activity, the app queries ChatGPT for a feature vector containing features of songs that fit the chosen activity. The key features we query for are danceability, energy, loudness, mode, valence, and tempo. After receiving this feature vector, we retrieve recommendation candidates for our user. We scale the features so that they are all on the same magnitude, and compute cosine similarity between the feature vector and a DataFrame containing feature vectors of over a million songs. This DataFrame contains data from a Kaggle dataset where the dataset creator queried the Spotify API, retrieving song features for a plethora of songs in every genre. After the 200 most similar songs to our activity feature vector, we compute a mean feature vector for our user as well. This is done by querying the Spotify API for songs from the user's Spotify library and computing a weighted scaled mean (weighted by date saved: recently saved songs have more weight). We then compute cosine similarity between this user feature vector and the feature vector of the 200 recommendation candidates to finalize the ten recommendations provided to the user. 

## Instructions

Make sure you have the dependencies installed. You do so by running `pip install -r requirements.txt`

Run the Flask web app using `python3 main.py` and that should start up the web server. Click [127.0.0.1:](http://127.0.0.1:5000) to access it.

## Demo

https://github.com/Leofeng7/Sportify/assets/108312435/56090f0a-95f5-4bf8-852d-169f71d18f11





