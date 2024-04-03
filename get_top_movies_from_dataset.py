# dataset from: https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies
import pandas as pd

df = pd.read_csv('TMDB_movie_dataset_v11.csv')
df_sorted = df.sort_values(by='vote_count', ascending=False)
top_10000 = df_sorted.head(20000)
top_10000.to_csv('tmdb_top_20k_vote_count_240403.csv', index=False)