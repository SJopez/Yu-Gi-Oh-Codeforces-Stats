from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx 

from contextlib import asynccontextmanager
import json

from app.services import get_top10_rated
from app.services import get_top10_contr
from app.services import get_individual_info
from app.services import scrap_info

from app.database import create_database
from app.database import get_user_info_db
from app.database import update_database 

from app.models import User

from app.card_matcher import most_close_card

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
    contr: list[str] = await get_top10_contr()
    #update top 10 rated cache

    rated_path = 'app/cache/top10_rated_cache.json'
    rated_list : list[str] = []

    for user_handle in rated:
        response: User = await user_info(user_handle, 'rate')
        rated_list.append(response.model_dump(mode='json'))

    with open(rated_path, 'w') as file:
        json.dump(rated_list, file, indent=4)

    #update top 10 contributors

    contr_path = 'app/cache/top10_contributors_cache.json'
    contr_list = []

    for user_handle in contr:
        response: User = await user_info(user_handle, 'contr')
        contr_list.append(response.model_dump(mode='json'))

    with open(contr_path, 'w') as file:
        json.dump(contr_list, file, indent=4)


@app.post('/update_tops_cache')
async def trigger_cache_uptade(background_task : BackgroundTasks):
    background_task.add_task(update_tops_cache)
    return {'result': 'cache update started'}


@app.get('/tops')
async def get_tops():
    #return all top 10, contributors and rated
    
    top_rated: list[User] = await get_top10_rated(True)
    top_contributors: list[User] = await get_top10_contr(True)

    return {
        'top_rated' : top_rated,
        'top_contributors' : top_contributors
    }

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
        user.match_card = await most_close_card(user)

        users_list.append(user)
    
    await update_database(users_list)


@app.post('/update_base_info')
async def trigger_codeforces_api_info(background_task : BackgroundTasks):
    background_task.add_task(codeforces_api_info)
    
    return {"result": "base info is being updated"}


@app.get('/user.info')
async def user_info(handle : str = Query(...), update_type: str = 'rate'):
    
    handle = handle.lower()
    user: User = await get_user_info_db(handle)
    if user is None:
        user: User = await get_individual_info(handle, http_client)

    await scrap_info(user, http_client, update_type)
    if user.match_card is None:
        user.match_card = await most_close_card(user)
    
    user: User = await get_user_info_db(user.handle)

    return user

@app.get('/health')
async def health():
    return {'status': 'ok'}



