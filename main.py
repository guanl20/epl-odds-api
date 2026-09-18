import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from database import SessionLocal, Match, OddsSnapshot

load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.cache = None 
def get_best_odds(match: dict) -> dict:
    best_odds = {}

    for bookmaker in match["bookmakers"]:
        bookmaker_name = bookmaker["title"]

        for market in bookmaker["markets"]:
            if market["key"] != "h2h":
                continue

            for outcome in market["outcomes"]:
                outcome_name = outcome["name"]
                price = outcome["price"]

                if outcome_name not in best_odds or price > best_odds[outcome_name]["price"]:
                    best_odds[outcome_name] = {
                        "price": price,
                        "bookmaker": bookmaker_name
                    }

    return {
        "match": f"{match['home_team']} vs {match['away_team']}",
        "commence_time": match["commence_time"],
        "best_odds": best_odds
    }

@app.get("/")
def read_root():
    key_status = "loaded" if ODDS_API_KEY else "MISSING"
    return {"message": "EPL Odds API is running", "api_key_status": key_status}

@app.get("/odds/epl")
def get_epl_odds():
    url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "uk",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to reach The Odds API", "type": type(e).__name__}

    matches = response.json()
    return [get_best_odds(match) for match in matches]

@app.post("/odds/epl/snapshot")
def save_snapshot():
    url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "uk",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to reach The Odds API", "type": type(e).__name__}

    matches = response.json()
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    for match in matches:
        db_match = db.query(Match).filter_by(api_match_id=match["id"]).first()
        if not db_match:
            db_match = Match(
                api_match_id=match["id"],
                home_team=match["home_team"],
                away_team=match["away_team"],
                commence_time=match["commence_time"],
            )
            db.add(db_match)
            db.flush()

        for bookmaker in match["bookmakers"]:
            for market in bookmaker["markets"]:
                if market["key"] != "h2h":
                    continue
                for outcome in market["outcomes"]:
                    db.add(OddsSnapshot(
                        match_id=db_match.id,
                        bookmaker=bookmaker["title"],
                        outcome=outcome["name"],
                        price=outcome["price"],
                        recorded_at=now,
                    ))

    db.commit()
    db.close()
    return {"status": "saved", "matches_processed": len(matches)}

@app.get("/odds/epl/history/{match_id}")
def get_history(match_id: int):
    db = SessionLocal()
    rows = db.query(OddsSnapshot).filter_by(match_id=match_id).order_by(OddsSnapshot.recorded_at).all()
    db.close()
    return [
        {"bookmaker": r.bookmaker, "outcome": r.outcome, "price": r.price, "recorded_at": r.recorded_at}
        for r in rows
    ]

@app.get("/gui/matches")
def gui_matches(request: Request):
    url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "uk",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException:
   
        return templates.TemplateResponse(request, "matches.html", {"matches": []})

    matches = response.json()
    aggregated = [get_best_odds(m) for m in matches]
       return templates.TemplateResponse(request, "matches.html", {"matches": aggregated})

@app.get("/gui/history/{match_id}")
def gui_history(request: Request, match_id: int):
    db = SessionLocal()
    rows = db.query(OddsSnapshot).filter_by(match_id=match_id).order_by(OddsSnapshot.recorded_at).all()
    db.close()
    return templates.TemplateResponse(request, "history.html", {"match_id": match_id, "rows": rows})