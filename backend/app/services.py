from datetime import datetime, timezone, timedelta

from curl_cffi import AsyncSession
from bs4 import BeautifulSoup
from app.models import User

import json

from app.database import update_database

from app.utils import unique_solved_problems
from app.utils import get_problems_tags
from app.utils import most_used_lang

from app.card_matcher import most_close_card

async def update_cache_if_in_top(users: list[User], update_type: str = 'rate'):
    if update_type == 'rate':
        rated_data = await get_top10_rated(True)
    else:
        contr_data = await get_top10_contr(True)

    rated_updated = False
    contr_updated = False
    
    for user in users:
        if update_type == 'rate':
            for i, cached_user in enumerate(rated_data):
                if cached_user.get('handle') == user.handle:
                    rated_data[i] = user.model_dump(mode='json')
                    rated_updated = True
                    break
        
        if update_type == 'contr':
            for i, cached_user in enumerate(contr_data):
                if cached_user.get('handle') == user.handle:
                    contr_data[i] = user.model_dump(mode='json')
                    contr_updated = True
                    break

    if rated_updated and update_type == 'rate':
        with open('app/cache/top10_rated_cache.json', 'w') as file:
            json.dump(rated_data, file, indent=4)

    if contr_updated and update_type == 'contr':
        with open('app/cache/top10_contributors_cache.json', 'w') as file:
            json.dump(contr_data, file, indent=4)

async def get_individual_info(handle: str, http_client: AsyncSession = None) -> User:
    url = 'https://codeforces.com/api/user.info'
    params = {'handles': handle}

    response = await http_client.get(url,params=params)
    response = response.json().get('result')[0]

    user: User = User()

    try:
        user.handle = response.get('handle')
        user.rating = response.get('rating')
        user.max_rating = response.get('maxRating')
        user.contributions = response.get('contribution')
        user.rank = response.get('rank').lower()
        user.max_rank = response.get('maxRank').lower()
        user.avatar = response.get('titlePhoto')
    except AttributeError:
        user.handle = response.get('handle')
        user.contributions = response.get('contribution')
        user.avatar = response.get('titlePhoto')

    user.match_card = await most_close_card(user)

    await process_null_rated(user)

    return user

async def scrap_info(user: User, http_client: AsyncSession = None, update_type: str = 'rate'):
    now_time = datetime.now(timezone.utc).replace(tzinfo=None)
    if user.timestamp is not None:
        if (now_time - user.timestamp) < timedelta(hours=24):
            return {'result': 'user is already update'}

    extra = user.rating and user.max_rating
    extra = extra and user.rank and user.max_rank
    
    if not extra:
        await process_null_rated(user)
    
    url_stats = 'https://codeforces.com/api/user.status'
    response_2 = await http_client.get(url_stats,params={'handle': user.handle})
    response_2 = response_2.json().get('result')
    problems = await unique_solved_problems(response_2)

    user.solved_problems = len(problems)
    user.tags = await get_problems_tags(problems)
    user.most_used_lang = await most_used_lang(problems)
    user.badges = await get_badges(user.handle)
    user.timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    user.match_card = await most_close_card(user)

    await update_database([user])
    await update_cache_if_in_top([user],update_type)
    
    return {'result': 'user have been updated succesfully'}

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

async def process_null_rated(user: User):
    handle = user.handle
    url = f'https://codeforces.com/profile/{handle}'
    
    #rank, maxrank, rating, maxrating

    async with AsyncSession(impersonate='firefox') as s:
        response = await s.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.select_one('div.userbox div.info')
    
    li = soup.select_one('ul li')
    span = li.select('span')

    try :
        rank = soup.select_one('div.user-rank span').text[:-1]
        max_rank : str = li.select_one('span.smaller').select('span')[0].text
        max_rank = max_rank[:-2]

        rating = span[0].text
        max_rating = li.select_one('span.smaller').select('span')[1].text
    except AttributeError:
        rank = soup.select_one('div.user-rank span').text[:-1]
        max_rank = rank
        rating = 0
        max_rating = 0

    user.rank = rank.lower()
    user.max_rank = max_rank.lower()
    user.rating = int(rating)
    user.max_rating = int(max_rating)

    await update_database([user])

