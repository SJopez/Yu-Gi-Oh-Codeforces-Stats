from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx 
from collections import defaultdict
from bs4 import BeautifulSoup 
import asyncio


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0'
    ),
    'Accept-Language': 'en-US,en;q=0.5',
}

'''
Needed info 

##4) Lista con todos los problemas, su dificultad y tags -> pending/ por ver
6) Premios -> pending

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

async def get_is_top10_rated(handle :str):
    url = 'https://codeforces.com/api/user.ratedList?activeOnly=true'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    response = response.json().get('result', [])
    for i in range(10):
        if handle == response[i].get('handle'):
            return True
    return False
    
async def get_is_top10_contr(handle : str):

    url = 'https://codeforces.com'

    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    contributor_box = soup.select('div.top-contributed')[1]
    user_name = contributor_box.select('a.rated-user')
    

    return True if (handle in user_name) else False
    
async def get_badges(handle : str):

    url = f'https://codeforces.com/profile/{handle}'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.select('div.badge')
    badges = [i.img['src'] for i in soup]

    return badges
    

@app.get('/user.info')
async def user_info_main(handle : str = Query(...)):
    
    #main info in user.info api request from codeforces

    url_info = 'https://codeforces.com/api/user.info'
    url_stat = 'https://codeforces.com/api/user.status'

    async with httpx.AsyncClient() as client:
        response, response_2 = await asyncio.gather(
            client.get(url_info,params={'handles':handle}),
            client.get(url_stat,params={'handle':handle})
        )

    response = response.json().get('result')[0]
    response_2 = response_2.json().get('result', [])
    
    problems = await unique_solved_problems(response_2)

    lang, is_top10_rated, is_top10_contr, badges = await asyncio.gather(
        most_used_lang(problems),
        get_is_top10_rated(handle),
        get_is_top10_contr(handle),
        get_badges(handle)
    )
    

    ans : dict = {
        'handle' : handle,
        'rating' : response.get('rating'),
        'solved_problemes' : len(problems),
        'contributions' : response.get('contribution'),
        'rank' : response.get('rank'),
        'is_top10_rated' : is_top10_rated,
        'is_top10_contr' : is_top10_contr,
        'badges' : badges,
        'most_used_lang' : lang,
        'avatar' : response.get('titlePhoto') 
    }

    return ans


