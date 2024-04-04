import pandas as pd

df = pd.read_csv('tmdb_top_20k_vote_average_240403.csv')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
df_filtered = df[df['vote_count'] >= 200]
df.to_csv('filtered_dataset.csv', index=False)
