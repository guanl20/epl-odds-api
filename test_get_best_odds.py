from main import get_best_odds

def test_get_best_odds_picks_highest_price():
    fake_match = {
        "home_team": "Team A",
        "away_team": "Team B",
        "commence_time": "2026-01-01T00:00:00Z",
        "bookmakers": [
            {
                "title": "BookmakerX",
                "markets": [
                    {"key": "h2h", "outcomes": [
                        {"name": "Team A", "price": 2.0},
                        {"name": "Team B", "price": 3.0},
                        {"name": "Draw", "price": 3.5},
                    ]}
                ]
            },
            {
                "title": "BookmakerY",
                "markets": [
                    {"key": "h2h", "outcomes": [
                        {"name": "Team A", "price": 2.5},
                        {"name": "Team B", "price": 2.8},
                        {"name": "Draw", "price": 3.6},
                    ]}
                ]
            },
        ]
    }

    result = get_best_odds(fake_match)

    assert result["best_odds"]["Team A"]["price"] == 2.5
    assert result["best_odds"]["Team A"]["bookmaker"] == "BookmakerY"
    assert result["best_odds"]["Team B"]["price"] == 3.0
    assert result["best_odds"]["Team B"]["bookmaker"] == "BookmakerX"
    assert result["best_odds"]["Draw"]["price"] == 3.6


# --- NEW: added below ---
def test_get_best_odds_handles_no_bookmakers():
    fake_match = {
        "home_team": "Team A",
        "away_team": "Team B",
        "commence_time": "2026-01-01T00:00:00Z",
        "bookmakers": []
    }

    result = get_best_odds(fake_match)

    assert result["best_odds"] == {}
    assert result["match"] == "Team A vs Team B"