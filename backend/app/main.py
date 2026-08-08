from fastapi import FastAPI, Query
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

http_client : httpx.AsyncClient = None


@asynccontextmanager
async def lifespan(app : FastAPI):
    global http_client
    timeout = httpx.Timeout(30.0, connect = 10.0)
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

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
        "https://yu-gi-oh-codeforces-stats.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
    

@app.post('/update_tops_cache')
async def update_tops_cache():
    rated = await get_top10_rated()
    #update top 10 rated cache

    rated_path = 'app/cache/top10_rated_cache.json'
    rated_list = []

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

    return {'result' : 'update'}


@app.get('/tops')
async def get_tops():
    #return all top 10, contributors and rated
    
    top_rated = await get_top10_rated(True)
    top_contributors = await get_top10_contr(True)

    return {
        'top_rated' : top_rated,
        'top_contributors' : top_contributors
    }

@app.get('/user.info')
async def user_info(handle : str = Query(...)):
    
    #main info in user.info api request from codeforces

    url_info = 'https://codeforces.com/api/user.info'
    url_stat = 'https://codeforces.com/api/user.status'

    response, response_2 = await asyncio.gather(
        http_client.get(url_info,params={'handles':handle}),
        http_client.get(url_stat,params={'handle':handle})
    )

    response = response.json().get('result')[0]
    response_2 = response_2.json().get('result', [])
    
    problems = await unique_solved_problems(response_2)
    
    problems_tags = await get_problems_tags(problems)
    
    lang, badges = await asyncio.gather(
        most_used_lang(problems),
        get_badges(handle)
    )

    ans : dict = {
        'handle' : handle,
        'rating' : response.get('rating'),
        'max_rating' : response.get('maxRating'),
        'solved_problemes' : len(problems),
        'tags': problems_tags,
        'contributions' : response.get('contribution'),
        'rank' : response.get('rank'),
        'max_rank' : response.get('maxRank'),
        'badges' : badges,
        'most_used_lang' : lang,
        'avatar' : response.get('titlePhoto') 
    }

    if response.get('rank') is None or response.get('maxRank') is None:
        await process_null_rated(ans)

    return ans


@app.get('/health')
async def health():
    return {'status': 'ok'}

