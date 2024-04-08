import numpy as np
import pandas as pd
import ast
df_ava = pd.read_csv("Spotify Account Data/sortedAva.csv")
df_will = pd.read_csv("Spotify Account Data/sortedWill.csv")
def convert_genre_list(genre_string):
    try:
        return ast.literal_eval(genre_string)
    except (ValueError, SyntaxError):
        return []
    

df_will.rename(columns={'artistName': 'Artist'}, inplace=True)
df_will['artist_genres'] = df_will['artist_genres'].apply(convert_genre_list)
df_ava['artist_genres'] = df_ava['artist_genres'].apply(convert_genre_list)

combined_genres = pd.Series(df_will['artist_genres'].sum() + df_ava['artist_genres'].sum())
top_genres = combined_genres.value_counts().head(10).index.tolist()

def filter_songs(df_listened, df_not_listened, top_genres):
    recommended_songs = []
    for genre in top_genres:
        # Find songs in the listened dataframe that match the genre and are not in the not listened dataframe
        filtered_songs = df_listened[
            df_listened['artist_genres'].apply(lambda genres: genre in genres) &
            ~df_listened['trackName'].isin(df_not_listened['trackName'])
        ]
        recommended_songs.extend(filtered_songs[['Artist', 'trackName']].drop_duplicates().to_dict('records'))
    
    return recommended_songs[:20]

# Get recommendations for Ava based on Will's listening and vice versa
recommendations_for_ava = filter_songs(df_will, df_ava, top_genres)
recommendations_for_will = filter_songs(df_ava, df_will, top_genres)

print("Recommendations for Ava:", recommendations_for_ava[:10])  # Show the first five recommendations
print("Recommendations for Will:", recommendations_for_will[:10])  # Show the first five recommendations