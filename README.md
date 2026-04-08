# RetoGen

Electronics review platform — expert reviews, community ratings, and price tracking.

## Stack

- **Frontend** — Nuxt 4, Vue 3, Pinia
- **Backend** — FastAPI, MongoDB

## Setup

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
# create .env with: NUXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

Requires Python 3.10+, Node 18+, and MongoDB running on `localhost:27017`.
