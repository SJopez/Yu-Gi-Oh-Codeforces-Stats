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


@app.get('/user.info')
async def user_info(handles : list[str] = Query(...)):
    handles_str = ';'.join(handles)

    user_url = 'https://codeforces.com/api/user.info'
    params = {'handles' : handles_str}
    

    async with httpx.AsyncClient() as client:
        response = await client.get(user_url, params=params)
    
    return response.json()
