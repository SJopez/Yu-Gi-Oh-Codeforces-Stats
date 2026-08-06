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
        "https://yu-gi-oh-codeforces-stats.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


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

def normalize_lang(lang: str) -> str:
    if not lang:
        return "Otros"
    
    lang_lower = lang.lower()
    
    if "c++" in lang_lower or "g++" in lang_lower:
        return "C++"
    if "c#" in lang_lower or "mono c#" in lang_lower:
        return "C#"
    if "c11" in lang_lower or "gnu c" in lang_lower or lang_lower == "c":
        return "C"
    if "python" in lang_lower or "pypy" in lang_lower:
        return "Python"
    if "java" in lang_lower:
        return "Java"
    if "kotlin" in lang_lower:
        return "Kotlin"
    if "rust" in lang_lower:
        return "Rust"
    if "pascal" in lang_lower or "fpc" in lang_lower:
        return "Pascal"
    if "f#" in lang_lower:
        return "F#"
    
    mapping = {
        "go": "Go",
        "haskell": "Haskell",
        "javascript": "JavaScript",
        "node.js": "JavaScript",
        "scala": "Scala",
        "ruby": "Ruby",
        "php": "PHP",
        "perl": "Perl",
        "ocaml": "OCaml",
        "delphi": "Delphi",
        "d": "D",
        "tcl": "Tcl",
        "io": "Io",
        "pike": "Pike",
        "befunge": "Befunge",
        "cobol": "Cobol",
        "factor": "Factor",
        "roco": "Roco",
        "ada": "Ada",
        "false": "FALSE",
        "picat": "Picat",
        "j": "J"
    }
    
    return mapping.get(lang_lower, lang.split()[0] if lang else "Otros")

async def most_used_lang(problems):
    langs = defaultdict(int)

    for problem in problems.values():
        raw_lang = problem.get('prog_lang')
        if raw_lang:
            norm_lang = normalize_lang(raw_lang)
            langs[norm_lang] += 1
    
    if not langs:
        return None

    best_lang = max(langs.items(), key=lambda x: x[1])
    return best_lang[0]

async def get_top10_rated():
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

async def get_problems_tags(problems : dict):
    tag = defaultdict(int)

    for problem in problems.values():
        for tag_ in problem.get('tags'):
            tag[tag_] += 1

    tag = sorted(tag, key=lambda x: tag.get(x), reverse=True)
    return tag
    

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

    return ans


@app.get('/health')
async def health():
    return {'status': 'ok'}

