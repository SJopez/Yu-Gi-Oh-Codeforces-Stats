from curl_cffi import AsyncSession
from bs4 import BeautifulSoup

import json

async def get_top10_rated(cached : bool = False):
    if cached:
        with open('app/cache/top10_rated_cache.json', 'r') as file:
            data = json.load(file)
            
        return data

    url = 'https://codeforces.com'

    async with AsyncSession(impersonate='firefox') as s:
        response = await s.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    contributor_box = soup.select('div.top-contributed')[0]
    user_name = contributor_box.select('a.rated-user') 
    top = []

    for user in user_name:
        top.append(user.get('href')[9:])

    return top

async def get_top10_contr(cached : bool = False):
    if cached:
        with open('app/cache/top10_contributors_cache.json', 'r') as file:
            data = json.load(file)

        return data

    url = 'https://codeforces.com'

    async with AsyncSession(impersonate='firefox') as s:
        response = await s.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    contributor_box = soup.select('div.top-contributed')[1]
    user_name = contributor_box.select('a.rated-user') 
    top = []

    for user in user_name:
        top.append(user.get('href')[9:])

    return top
    
async def get_badges(handle : str):

    url = f'https://codeforces.com/profile/{handle}'

    async with AsyncSession(impersonate='firefox') as s:
        response = await s.get(url)
    
    if response.status_code != 200:
        return [response.status_code]

    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.select('div.badge')
    badges = [i.img['src'] for i in soup]

    return badges

async def process_null_rated(user_info : dict = None):
    handle = user_info.get('handle')
    url = f'https://codeforces.com/profile/{handle}'
    
    #rank, maxrank, rating, maxrating

    async with AsyncSession(impersonate='firefox') as s:
        response = await s.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.select_one('div.userbox div.info')

    li = soup.select_one('ul li')
    span = li.select('span')

    rank = soup.select_one('div.user-rank span').text[:-1]
    max_rank : str = li.select_one('span.smaller').select('span')[0].text
    max_rank = max_rank.capitalize()[:-2]

    rating = span[0].text
    max_rating = li.select_one('span.smaller').select('span')[1].text

    user_info.update({
        'rank' : rank,
        'max_rank' : max_rank,
        'rating' : rating,
        'max_rating' : max_rating
    })





    