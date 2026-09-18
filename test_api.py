import os
import requests
from dotenv import load_dotenv
from main import get_best_odds

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
params = {
    "apiKey": API_KEY,
    "regions": "uk",
    "markets": "h2h",
    "oddsFormat": "decimal",
}

response = requests.get(url, params=params)
matches = response.json()

first_match = matches[0]
result = get_best_odds(first_match)

print(result)