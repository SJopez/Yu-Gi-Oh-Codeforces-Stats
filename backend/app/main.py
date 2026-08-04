from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx 
from bs4 import BeautifulSoup 
from curl_cffi import AsyncSession

from collections import defaultdict
import asyncio
from contextlib import asynccontextmanager


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
        "http://localhost:5173",
        "https://yu-gi-oh-codeforces-stats.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
Needed info 

1) Lista con todos los problemas, su dificultad y tags -> pending/ por ver
3) Nombre de los badges

'''


async def unique_solved_problems(response_2):
    problems = dict()
    for sub in response_2:
        if sub.get('verdict') == 'OK':
            contesId = sub.get('contestId')
            problem_index = sub.get('problem').get('index')
            
            prog_lang = sub.get('programmingLanguage')
            tags = sub.get('problem').get('tags')
            rating = sub.get('problem').get('rating')

            #null rating == unrated contest

            problems.update({
                f'{contesId}_{problem_index}' : {
                    'prog_lang' : prog_lang,
                    'tags' : tags,
                    'rating' : rating
                } 
            })

    return problems

async def most_used_lang(problems):
    langs = defaultdict(int)

    for problem in problems.values():
        lang = problem.get('prog_lang')
        
        langs[lang] += 1
    
    ans = ['C++', 0]
    for lang in langs.items():
        if lang[1] >= ans[1]:
            ans = lang
            

    return ans[0]

async def get_top10_rated():
    url = 'https://codeforces.com/api/user.ratedList?activeOnly=true'

    response = await http_client.get(url)
    
    response = response.json().get('result', [])
    top = []
    for i in range(10):
        top.append(response[i].get('handle'))

    return top

async def get_top10_contr():

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
    

@app.get('/tops')
async def get_tops():
    #return all top 10, contributors and rated
    
    top_rated = await get_top10_rated()
    top_contributors = await get_top10_contr()

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

    lang, badges = await asyncio.gather(
        most_used_lang(problems),
        get_badges(handle)
    )
    

    ans : dict = {
        'handle' : handle,
        'rating' : response.get('rating'),
        'max_rating' : response.get('maxRating'),
        'solved_problemes' : len(problems),
        'contributions' : response.get('contribution'),
        'rank' : response.get('rank'),
        'max_rank' : response.get('maxRank'),
        'badges' : badges,
        'most_used_lang' : lang,
        'avatar' : response.get('titlePhoto') 
    }

    return ans


