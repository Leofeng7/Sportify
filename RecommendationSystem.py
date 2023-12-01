class Recommender():
    def __init__(self, user_songs, activity_feature, sp):
        self.user_songs = user_songs
        self.activity_feature = activity_feature
        self.sp = sp
    
    def get_recommendation_pool(self):

        target_features = {'target_danceability': self.activity_feature[1], 
                           'target_energy' : self.activity_feature[2], 'target_loudness' : self.activity_feature[3], 
                           'target_mode' : int(self.activity_feature[4]), 'target_valence' : self.activity_feature[5], 'target_tempo' : self.activity_feature[6]} 

        print(target_features)
        recommendations = self.sp.recommendations(seed_genres=['pop'],limit=10, target=target_features)
        return recommendations
            

