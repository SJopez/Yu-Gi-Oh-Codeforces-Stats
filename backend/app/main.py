from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx 

app = FastAPI()


#get main user info provided by codeforces api /user.info

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176"],
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
Needed info 

#1) Username -> provided by user_info()
#2) Rating -> provided by user_info()
##3) Cantiad de problemas resueltos -> pending
##4) Lista con todos los problemas, su dificultad y tags -> pending
#5) Contribution -> provided by user_info()
6) Premios -> pending
7) Si es top mundial o no -> pending
8) Si es top contribution o no -> pending
##9) Lenguage mas usado -> pending
#10) Rank -> provided by user_info()
#11) Avatar -> provided by user_info()

'''

def unique_solved_problems(response_2):
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




@app.get('/user.info')
async def user_info_main(handle : str = Query(...)):
    
    #main info in user.info api request from codeforces

    url = 'https://codeforces.com/api/user.info'
    params = {'handles' : handle}
    

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response = response.json().get('result')[0]

    #extra info unavailable from user.info api request 


    url = 'https://codeforces.com/api/user.status'
    params = {'handle' : handle}

    async with httpx.AsyncClient() as client:
        response_2 = await client.get(url, params=params)

    response_2 = response_2.json().get('result', [])
    problems = unique_solved_problems(response_2)

    ans : dict = {
        'handle' : handle,
        'rating' : response.get('rating'),
        'solved_problemes' : len(problems),
        'contributions' : response.get('contribution'),
        'rank' : response.get('rank'),
        'avatar' : response.get('titlePhoto') 

    }

    return ans



