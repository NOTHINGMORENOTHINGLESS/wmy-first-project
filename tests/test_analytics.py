from __future__ import annotations

import pandas as pd

from app.analytics import (
    city_with_most_matches,
    draw_percentage,
    first_ever_match,
    home_advantage,
    match_frequency,
    most_opponents,
    most_wins,
    route_question,
)


def test_route_question_works():
    assert route_question("Which team has won the most matches?") == "most_wins"
    assert route_question("What was the first ever international match?") == "first_ever_match"
    assert route_question("Which city has hosted the most matches?") == "city_with_most_matches"
    assert route_question("How has match frequency changed over time?") == "match_frequency"
    assert route_question("What percentage of matches ended in a draw?") == "draw_percentage"


def test_first_ever_match_result():
    df = pd.DataFrame(
        [
            {"date": "1872-11-30", "home_team": "Scotland", "away_team": "England", "home_score": 0, "away_score": 0, "city": "Glasgow", "tournament": "Friendly"},
            {"date": "1873-03-08", "home_team": "England", "away_team": "Scotland", "home_score": 4, "away_score": 2, "city": "London", "tournament": "Friendly"},
        ]
    )
    result = first_ever_match(df)
    assert result.result["home_team"] == "Scotland"
    assert result.result["away_team"] == "England"


def test_most_wins_and_draw_percentage():
    df = pd.DataFrame(
        [
            {"date": "2020-01-01", "home_team": "Brazil", "away_team": "Argentina", "home_score": 2, "away_score": 1},
            {"date": "2020-01-02", "home_team": "Brazil", "away_team": "Germany", "home_score": 1, "away_score": 1},
            {"date": "2020-01-03", "home_team": "Argentina", "away_team": "Germany", "home_score": 3, "away_score": 0},
            {"date": "2020-01-04", "home_team": "Brazil", "away_team": "France", "home_score": 2, "away_score": 0},
        ]
    )
    wins = most_wins(df)
    draws = draw_percentage(df)
    assert wins.result["team"] == "Brazil"
    assert wins.result["wins"] == 2
    assert draws.result["draw_percentage"] == 25.0


def test_city_and_home_advantage():
    df = pd.DataFrame(
        [
            {"date": "2021-01-01", "home_team": "France", "away_team": "Belgium", "home_score": 2, "away_score": 1, "city": "Paris"},
            {"date": "2021-01-02", "home_team": "France", "away_team": "Italy", "home_score": 3, "away_score": 3, "city": "Paris"},
            {"date": "2021-01-03", "home_team": "Spain", "away_team": "Portugal", "home_score": 1, "away_score": 2, "city": "Madrid"},
            {"date": "2021-01-04", "home_team": "England", "away_team": "Germany", "home_score": 2, "away_score": 0, "city": "London"},
        ]
    )
    city = city_with_most_matches(df)
    home = home_advantage(df)
    assert city.result["city"] == "Paris"
    assert home.result["team"] in {"France", "Spain", "England"}


def test_match_frequency_and_opponents():
    df = pd.DataFrame(
        [
            {"date": "2019-01-01", "home_team": "France", "away_team": "Brazil", "home_score": 1, "away_score": 0, "city": "Paris"},
            {"date": "2019-01-02", "home_team": "France", "away_team": "Brazil", "home_score": 2, "away_score": 2, "city": "Paris"},
            {"date": "2020-01-01", "home_team": "France", "away_team": "Brazil", "home_score": 2, "away_score": 1, "city": "Paris"},
            {"date": "2020-01-02", "home_team": "France", "away_team": "Croatia", "home_score": 3, "away_score": 0, "city": "Paris"},
        ]
    )
    frequency = match_frequency(df)
    matchup = most_opponents(df)
    assert frequency.result["top_year"] in {2019, 2020}
    assert matchup.result["matches"] >= 2
