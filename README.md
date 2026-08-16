
<h1>
  <img src="public/icon.png" alt="App Icon" width="48" style="border-radius:8px; vertical-align:middle; margin-right:10px;" />
  Yu-Gi-Oh Codeforces Stats
</h1>
 


<p align="center">
  <img src="src/assets/readme/init.jpeg" alt="Init Image" width="90%" style="border-radius:8px; max-width: 480px" />
</p>
  Welcome to the documentation of Yu-Gi-Oh Codeforces Stats — a web application that converts your <a href="https://codeforces.com" target="_blank" rel="noopener noreferrer">Codeforces</a> username into a Yu-Gi-Oh card based on your problem-solving skills.

## Table of Contents

- [Frontend](#frontend)
- [Backend](#backend)

## Frontend

<p>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" style="margin-right:6px;" />
</p>

This section describes the frontend application that renders interactive Yu-Gi-Oh style cards, manages user interactions, and fetches data from the backend API.

### Cards
<p align="center">
  <img src="src/assets/readme/triade.png" alt="Triade cards" style="border-radius:8px; max-width:400px; width:90%; height:auto;" />
</p>

Codeforces users are modeled as Yu-Gi-Oh style cards based on their problem-solving skills and contest participation. The user statistics determine the card numeric stats, template color, and other visual elements.

The correspondences are:

- **Attack:** `max rating` — the highest rating the user has achieved on Codeforces.
- **Defense:** `problems solved` — total number of problems the user has solved.
- **Attribute:** `most-used programming language` — the language the user most commonly uses to solve problems.
- **Card template color:** `rank` — the user's current Codeforces rank (used to color the card template).
- **Card type:** `rank` — the user's current rank used to determine the card type.
- **Card level:** `max rank` — the user's maximum rank represented as a level (stars) on the card.

As a card's rank increases, additional animations and visual effects (for example: glow, animated borders, and particle accents) are applied to emphasize rarity and achievement.


### Badges

<div style="display:flex; flex-direction:row; justify-content:center; align-items:center; gap:12px; margin:12px 0;">
  <img src="src/assets/readme/badge1.png" alt="badge-1" style="width:72px; height:auto;" />
  <img src="src/assets/readme/badge2.png" alt="badge-2" style="width:72px; height:auto;" />
  <img src="src/assets/readme/badge3.png" alt="badge-3" style="width:72px; height:auto;" />
</div>

These badges are awarded to users for long tenure on the platform and are displayed in the bottom-right corner of the user's avatar on the card. Badges are obtained by web scraping each user's Codeforces profile — this process and the backend implementation details are explained in the [Backend](#backend) section.

## Backend

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" style="margin-right:6px;" />
</p>

- **Tech stack:** Python, FastAPI, `httpx` for HTTP requests, background tasks for cache updates.
- **What it does:** Collects user data from the Codeforces API and from individual profile scraping, persists and updates a local database/cache, and exposes endpoints used by the frontend. Key endpoints include:
  - `GET /user.info` — returns detailed user info
  - `GET /tops` — returns cached top-rated and top-contributor lists
  - `POST /update_tops_cache` and `POST /update_base_info` — trigger background updates
- **Cache/storage:** Cached files live under `backend/app/cache/` and the app initializes a local database on startup.


---

</div>
If you want, I can add run instructions, examples, or a short contributing section next.