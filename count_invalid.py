import pandas as pd

occurrences = {}

for i in range(32, 401):
    file_name = f'ratings/ratings_{i}_of_400.csv'
    try:
        df = pd.read_csv(file_name)
        count = (df['google_rating'] == -1).sum()
        occurrences[file_name] = count
    except FileNotFoundError:
        continue

for file_name, count in occurrences.items():
    if count > 0:
        print(f"{file_name}: {count} occurrences of -1 in 'google_rating' column")