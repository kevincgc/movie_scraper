import pandas as pd

dfs = []
last_valid = 0
for i in range(1, 401):
    file_name = f'ratings/ratings_{i}_of_400.csv'
    try:
        df = pd.read_csv(file_name)
        df['index'] = range(50 * (i-1), df.shape[0] + 50 * (i-1))
        dfs.append(df)
        last_valid = i
    except FileNotFoundError:
        continue

combined_df = pd.concat(dfs, ignore_index=True)
sorted_df = combined_df.sort_values(by='google_rating', ascending=False)
sorted_df.to_csv(f'combined/ratings_combined_1_to_{last_valid}.csv', index=False)
