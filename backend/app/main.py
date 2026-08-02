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

1) Lista con todos los problemas, su dificultad y tags -> pending/ por ver
2) Maxrank y maxrating del usuraio
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

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    response = response.json().get('result', [])
    top = []
    for i in range(10):
        top.append(response[i].get('handle'))

    return top

async def get_top10_contr():

    url = 'https://codeforces.com'

    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    contributor_box = soup.select('div.top-contributed')[1]
    user_name = contributor_box.select('a.rated-user') 
    top = []

    for user in user_name:
        top.append(user.get('href')[9:])

    return top
    
async def get_badges(handle : str):

    url = f'https://codeforces.com/profile/{handle}'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.select('div.badge')
    badges = [i.img['src'] for i in soup]

    return badges
    

@app.get('/tops')
async def get_tops():
    #return all top 10, contributors and rated
    
    top_rated, top_contributors = await asyncio.gather(
        get_top10_rated(),
        get_top10_contr()
    )

    return {
        'top_rated' : top_rated,
        'top_contributors' : top_contributors
    }

@app.get('/user.info')
async def user_info(handle : str = Query(...)):
    
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

    lang, badges = await asyncio.gather(
        most_used_lang(problems),
        get_badges(handle)
    )
    

    ans : dict = {
        'handle' : handle,
        'rating' : response.get('rating'),
        'solved_problemes' : len(problems),
        'contributions' : response.get('contribution'),
        'rank' : response.get('rank'),
        'badges' : badges,
        'most_used_lang' : lang,
        'avatar' : response.get('titlePhoto') 
    }

    return ans


