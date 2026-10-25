from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class QuestionResult:
    question: str
    tool_name: str
    summary: str
    result: Any


def normalize_team(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def first_ever_match(df: pd.DataFrame) -> QuestionResult:
    ordered = df.sort_values("date").reset_index(drop=True)
    first_match = ordered.iloc[0]
    return QuestionResult(
        question="What was the first ever international football match?",
        tool_name="first_ever_match",
        summary="The earliest match in the dataset.",
        result={
            "date": str(first_match["date"]),
            "home_team": normalize_team(first_match.get("home_team")),
            "away_team": normalize_team(first_match.get("away_team")),
            "home_score": int(first_match.get("home_score", 0) or 0),
            "away_score": int(first_match.get("away_score", 0) or 0),
            "city": normalize_team(first_match.get("city")),
            "tournament": normalize_team(first_match.get("tournament")),
        },
    )


def team_win_counts(df: pd.DataFrame) -> pd.Series:
    home_wins = df.groupby("home_team", dropna=False).apply(lambda g: int((g["home_score"] > g["away_score"]).sum()))
    away_wins = df.groupby("away_team", dropna=False).apply(lambda g: int((g["away_score"] > g["home_score"]).sum()))
    total = home_wins.add(away_wins, fill_value=0)
    return total.sort_values(ascending=False)


def most_wins(df: pd.DataFrame) -> QuestionResult:
    totals = team_win_counts(df)
    team = totals.idxmax()
    wins = int(totals.max())
    return QuestionResult(
        question="Which national team has won the most matches?",
        tool_name="most_wins",
        summary="The team with the highest win total across the dataset.",
        result={"team": team, "wins": wins},
    )


def most_opponents(df: pd.DataFrame) -> QuestionResult:
    pair_counts: dict[tuple[str, str], int] = {}
    for _, row in df.iterrows():
        team_a = normalize_team(row.get("home_team"))
        team_b = normalize_team(row.get("away_team"))
        if not team_a or not team_b:
            continue
        key = tuple(sorted((team_a, team_b)))
        pair_counts[key] = pair_counts.get(key, 0) + 1

    if not pair_counts:
        raise ValueError("No valid team pair data found in the dataset.")

    (team_a, team_b), matches = max(pair_counts.items(), key=lambda item: (item[1], item[0]))
    return QuestionResult(
        question="Which teams have met the most times?",
        tool_name="most_opponents",
        summary="The most common team matchup in the dataset.",
        result={"team_a": team_a, "team_b": team_b, "matches": matches},
    )


def city_with_most_matches(df: pd.DataFrame) -> QuestionResult:
    city_counts = df["city"].fillna("Unknown").astype(str).str.strip().value_counts()
    city = city_counts.idxmax()
    matches = int(city_counts.max())
    return QuestionResult(
        question="Which city has hosted the most matches?",
        tool_name="city_with_most_matches",
        summary="The city with the highest number of hosted matches.",
        result={"city": city, "matches": matches},
    )


def home_advantage(df: pd.DataFrame) -> QuestionResult:
    team_records: dict[str, dict[str, int]] = {}

    for _, row in df.iterrows():
        home_team = normalize_team(row.get("home_team"))
        away_team = normalize_team(row.get("away_team"))
        home_goals = int(row.get("home_score", 0) or 0)
        away_goals = int(row.get("away_score", 0) or 0)

        for team, team_goals, opp_goals in [
            (home_team, home_goals, away_goals),
            (away_team, away_goals, home_goals),
        ]:
            if not team:
                continue
            stats = team_records.setdefault(team, {"wins": 0, "draws": 0, "losses": 0, "points": 0})
            if team_goals > opp_goals:
                stats["wins"] += 1
                stats["points"] += 3
            elif team_goals == opp_goals:
                stats["draws"] += 1
                stats["points"] += 1
            else:
                stats["losses"] += 1

    if not team_records:
        raise ValueError("No team records were found in the dataset.")

    team, stats = max(team_records.items(), key=lambda item: (item[1]["points"], item[1]["wins"], item[0]))
    return QuestionResult(
        question="Which teams have the best or worst home advantage?",
        tool_name="home_advantage",
        summary="Team with the strongest historical home-result performance in the dataset.",
        result={
            "team": team,
            "points": stats["points"],
            "wins": stats["wins"],
            "draws": stats["draws"],
            "losses": stats["losses"],
        },
    )


def draw_percentage(df: pd.DataFrame) -> QuestionResult:
    total_matches = len(df)
    draws = int((df["home_score"].astype(float) == df["away_score"].astype(float)).sum())
    pct = (draws / total_matches * 100) if total_matches else 0.0
    return QuestionResult(
        question="What percentage of matches have ended in a draw?",
        tool_name="draw_percentage",
        summary="Percentage of matches ending in a draw.",
        result={
            "draws": draws,
            "total_matches": total_matches,
            "draw_percentage": round(pct, 2),
        },
    )


def match_frequency(df: pd.DataFrame) -> QuestionResult:
    working = df.copy()
    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working = working.dropna(subset=["date"]).copy()
    working["year"] = working["date"].dt.year
    yearly_counts = working.groupby("year").size().sort_index()
    top_year = int(yearly_counts.idxmax())
    top_count = int(yearly_counts.max())
    return QuestionResult(
        question="How does match frequency vary over history, by country, or by tournament?",
        tool_name="match_frequency",
        summary="Yearly match volume in the dataset.",
        result={"top_year": top_year, "top_year_matches": top_count, "yearly_counts": yearly_counts.to_dict()},
    )


def route_question(question: str) -> str:
    lowered = question.lower()

    if "first" in lowered and "match" in lowered:
        return "first_ever_match"
    if "win" in lowered and "most" in lowered:
        return "most_wins"
    if "met" in lowered or "matchup" in lowered or "opponent" in lowered:
        return "most_opponents"
    if "city" in lowered or "host" in lowered:
        return "city_with_most_matches"
    if "home" in lowered and ("advantage" in lowered or "best" in lowered or "worst" in lowered):
        return "home_advantage"
    if "draw" in lowered or "level" in lowered:
        return "draw_percentage"
    if "frequency" in lowered or "year" in lowered or "history" in lowered or "tournament" in lowered or "country" in lowered:
        return "match_frequency"

    return "most_wins"


def evaluate_question(df: pd.DataFrame, question: str) -> QuestionResult:
    tool_name = route_question(question)
    if tool_name == "first_ever_match":
        return first_ever_match(df)
    if tool_name == "most_wins":
        return most_wins(df)
    if tool_name == "most_opponents":
        return most_opponents(df)
    if tool_name == "city_with_most_matches":
        return city_with_most_matches(df)
    if tool_name == "home_advantage":
        return home_advantage(df)
    if tool_name == "draw_percentage":
        return draw_percentage(df)
    if tool_name == "match_frequency":
        return match_frequency(df)
    raise ValueError(f"Unsupported route: {tool_name}")
