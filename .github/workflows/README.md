# EPL Odds Analytics API

A FastAPI backend that fetches live English Premier League betting odds, aggregates the best available price per outcome across UK bookmakers, and persists historical snapshots to track how odds move over time.

## Problem it solves
Betting odds vary across bookmakers and shift constantly. This API centralizes live odds, surfaces the best price per match outcome, and builds a historical record for line-movement analysis — data that's otherwise only visible one bookmaker/moment at a time.

## Tech stack
- **Python 3.14 + FastAPI** — web framework and API layer
- **PostgreSQL (hosted on Neon)** — persistent storage
- **SQLAlchemy** — ORM for database models and queries
- **The Odds API** — live odds data source
- **GitHub Actions** — scheduled automation (odds snapshots every 6 hours)
- **Render** — cloud deployment

## Endpoints
- `GET /` — health check, confirms API key loaded
- `GET /odds/epl` — live, aggregated best odds per match (not persisted)
- `POST /odds/epl/snapshot` — fetches current odds and saves every bookmaker price to the database
- `GET /odds/epl/history/{match_id}` — full historical price record for one match, chronological

## Local setup
1. Clone the repo, create a virtual environment, activate it
2. `pip install -r requirements.txt`
3. Create a `.env` file with:
4. `python database.py` (creates tables)
5. `uvicorn main:app --reload`

## Live deployment
Deployed on Render: [your URL here]

## Known limitations
- Free-tier hosting means cold starts after inactivity
- Free-tier odds API caps usage at 500 requests/month
- `match_id` foreign key is not yet a formally enforced database constraint
- No automated tests yet
- Single sport/league (EPL) and single region (UK bookmakers) by design, to stay within free quota

## Future improvements
- Automated tests (pytest)
- Enforce foreign key constraint between snapshots and matches
- Support multiple leagues/regions
- Simple frontend for browsing odds and line-movement charts