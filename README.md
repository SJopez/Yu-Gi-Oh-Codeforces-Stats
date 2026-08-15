
<h1>
  <img src="public/icon.png" alt="App Icon" width="48" style="border-radius:8px; vertical-align:middle; margin-right:10px;" />
  Yu-Gi-Oh Codeforces Stats
</h1>
 
<p align="center">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" style="margin-right:6px;" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</p>

<p align="center">
  <img src="src/assets/readme/init.jpeg" alt="Init Image" width="480" style="border-radius:8px;" />
</p>
Welcome to the documentation for Yu-Gi-Oh Codeforces Stats — a web application that converts your [Codeforces](https://codeforces.com) usern into a Yu-Gi-Oh card based on your problem-solving statistics.

## Table of Contents

- [Frontend](#frontend)
- [Backend](#backend)

## Frontend

- **Tech stack:** React, TypeScript, Vite, `html2canvas`, `react-hot-toast`.
- **What it does:** Provides the user interface and visualizations. The React app (in `src/`) renders card components, fetches data from the backend API (e.g. `/user.info`, `/tops`), and allows users to view/download styled representations of Codeforces profiles.

## Backend

- **Tech stack:** Python, FastAPI, `httpx` for HTTP requests, background tasks for cache updates.
- **What it does:** Collects user data from the Codeforces API and from individual profile scraping, persists and updates a local database/cache, and exposes endpoints used by the frontend. Key endpoints include:
  - `GET /user.info` — returns detailed user info
  - `GET /tops` — returns cached top-rated and top-contributor lists
  - `POST /update_tops_cache` and `POST /update_base_info` — trigger background updates
- **Cache/storage:** Cached files live under `backend/app/cache/` and the app initializes a local database on startup.

---

If you want, I can add run instructions, examples, or a short contributing section next.