from datetime import timedelta
from app.models import User

from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx 

import asyncio
from contextlib import asynccontextmanager
import json

from app.services import get_top10_rated
from app.services import get_top10_contr
from app.services import get_badges
from app.services import process_null_rated

from app.utils import most_used_lang
from app.utils import unique_solved_problems
from app.utils import get_problems_tags
from app.utils import get_pos

from app.database import create_database
from app.database import get_user_info_db
from app.database import update_database 

from datetime import datetime, timezone

http_client : httpx.AsyncClient = httpx.AsyncClient()


@asynccontextmanager
async def lifespan(app : FastAPI):
    global http_client
    timeout = httpx.Timeout(30.0, connect = 10.0)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    create_database()
    http_client = httpx.AsyncClient(
        headers=headers, 
        follow_redirects=True,
        timeout=timeout,
        http2=False
        )

    yield
    await http_client.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5176",
        "http://localhost:5173",
        "https://yu-gi-oh-codeforces-stats.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)
    

async def update_tops_cache():
    rated : list[str] = await get_top10_rated()
    #update top 10 rated cache

    rated_path = 'app/cache/top10_rated_cache.json'
    rated_list : list[str] = []

    for user in rated:
        response = await user_info(user)
        rated_list.append(response)

    with open(rated_path, 'w') as file:
        json.dump(rated_list, file, indent=4)

    #update top 10 contributors
    contr = await get_top10_contr()

    contr_path = 'app/cache/top10_contributors_cache.json'
    contr_list = []

    for user in contr:
        response = await user_info(user)
        contr_list.append(response)

    with open(contr_path, 'w') as file:
        json.dump(contr_list, file, indent=4)

@app.post('/update_tops_cache')
async def trigger_cache_uptade(background_task : BackgroundTasks):
    background_task.add_task(update_tops_cache)
    return {'result': 'cache update started'}


@app.get('/tops')
async def get_tops():
    #return all top 10, contributors and rated
    
    top_rated = await get_top10_rated(True)
    top_contributors = await get_top10_contr(True)

    return {
        'top_rated' : top_rated,
        'top_contributors' : top_contributors
    }

async def get_individual_info(handle: str) -> User:
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
        user.rated_pos, user.contr_pos = await get_pos(user.handle)
    except AttributeError:
        user.handle = response.get('handle')
        user.contributions = response.get('contribution')
        user.avatar = response.get('titlePhoto')
        user.rated_pos, user.contr_pos = await get_pos(user.handle)

    await process_null_rated(user)


    await update_database([user])
    
    return user

async def codeforces_api_info():
    url_users_list =  'https://codeforces.com/api/user.ratedList?activeOnly=false&includeRetired=false'
    response = await http_client.get(url_users_list)
    response = response.json().get('result')
    
    #Add codeforces api info to a User instance
    users_list: list[User] = []
    for user_info in response:

        user: User = User()
        user.handle = user_info.get('handle')
        user.rating = user_info.get('rating')
        user.max_rating = user_info.get('maxRating')
        user.contributions = user_info.get('contribution')
        user.rank = user_info.get('rank').lower()
        user.max_rank = user_info.get('maxRank').lower()
        user.avatar = user_info.get('titlePhoto')
        user.rated_pos, user.contr_pos = await get_pos(user.handle)

        users_list.append(user)
    
    await update_database(users_list)

    return {'result': 'ok'}


@app.post('/update_base_info')
async def trigger_codeforces_api_info(background_task : BackgroundTasks):
    background_task.add_task(codeforces_api_info)
    
    return {"result": "base info is being updated"}


async def scrap_info(user: User):
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
    await update_database([user])
    
    return {'result': 'user have been updated succesfully'}


@app.get('/user.info')
async def user_info(handle : str = Query(...)) -> User:
    
    handle = handle.lower()
    user: User = await get_user_info_db(handle)
    if user is None:
        user: User = await get_individual_info(handle)

    await scrap_info(user)
    user: User = await get_user_info_db(user.handle)

    return user

@app.get('/health')
async def health():
    return {'status': 'ok'}


