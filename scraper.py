import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_user_rating_percent(title, year):
    title = title.replace('&', 'and')
    query = f"{title} {year} movie"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    rating_element = soup.find("div", class_="a19vA")
    if rating_element:
        return int(''.join(c for c in rating_element.text if c.isdigit()))
    else:
        return -1


# configure------
entries_per_batch = 50
start = 24  # 1 indexed
do_splits = 300
# -----------------

pd.set_option('display.max_columns', None)
df = pd.read_csv('tmdb_top_20k_vote_count_240403.csv')
total_size = 20000
sorted = df.nlargest(total_size, 'vote_count')
total_splits = total_size // entries_per_batch

for batch in range(start - 1, start - 1 + do_splits):
    start_index = batch * entries_per_batch
    end_index = start_index + entries_per_batch
    top_batch = sorted.iloc[start_index:end_index]

    user_ratings = []
    for index, row in top_batch.iterrows():
        title = row['title']
        year = row['release_date'][:4]
        user_rating_percent = get_user_rating_percent(title, year)
        print(f'{index} {title} {user_rating_percent}')
        user_ratings.append({'id': row['id'], 'title': title, 'year': year, 'google_rating': user_rating_percent,
                             'vote_average': row['vote_average'], 'vote_count': row['vote_count'],
                             'revenue': row['revenue'],
                             'runtime': row['runtime']})

    user_ratings_df = pd.DataFrame(user_ratings)
    user_ratings_df.to_csv(f'ratings/ratings_{batch + 1}_of_{total_splits}.csv', index=False)
    time.sleep(240)
