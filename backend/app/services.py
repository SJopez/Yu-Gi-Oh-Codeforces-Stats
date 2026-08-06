from curl_cffi import AsyncSession
from bs4 import BeautifulSoup

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