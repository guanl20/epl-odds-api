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
