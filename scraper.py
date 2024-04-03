import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_user_rating_percent(title, year):
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

df = pd.read_csv('tmdb_top_20k_vote_count_240403.csv')
sorted = df.nlargest(20000, 'vote_count')

for batch in range(0, 200):
    start_index = batch * 100
    end_index = start_index + 100
    top_batch = sorted.iloc[start_index:end_index]

    user_ratings = []
    for index, row in top_batch.iterrows():
        title = row['title']
        year = row['release_date'][:4]
        user_rating_percent = get_user_rating_percent(title, year)
        print(f'{index + start_index} {title} {user_rating_percent}')
        user_ratings.append({'id': row['id'], 'title': title,'year': year, 'google_rating': user_rating_percent,
                             'vote_average': row['vote_average'], 'vote_count': row['vote_count'], 'revenue': row['revenue'],
                             'runtime': row['runtime']})

    user_ratings_df = pd.DataFrame(user_ratings)
    user_ratings_df.to_csv(f'ratings_{batch + 1}.csv', index=False)

# user_ratings = []
# for index, row in top_10[:10].iterrows():
#     title = row['title']
#     year = row['release_date'][:4]
#     user_rating_percent = get_user_rating_percent(title, year)
#     user_ratings.append({'id': row['id'], 'title': title,'year': year, 'google_rating': user_rating_percent,
#                          'vote_average': row['vote_average'], 'vote_count': row['vote_count'], 'revenue': row['revenue'],
#                          'runtime': row['runtime']})
#
# user_ratings_df = pd.DataFrame(user_ratings)
# user_ratings_df.to_csv('top_10_with_google_rating.csv', index=False)