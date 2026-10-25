from __future__ import annotations

import json
from typing import Any

import requests

from app.config import MODEL_API_VERSION, MODEL_DEPLOYMENT, MODEL_ENDPOINT, MODEL_KEY


def build_model_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if MODEL_KEY:
        headers["api-key"] = MODEL_KEY
    return headers


def fallback_explanation(question: str, result: dict[str, Any], tool_name: str) -> str:
    if tool_name == "first_ever_match":
        return (
            f"The earliest match in the dataset was {result['home_team']} versus {result['away_team']} on {result['date']} "
            f"in {result['city']} with a score of {result['home_score']} to {result['away_score']}."
        )
    if tool_name == "most_wins":
        return f"{result['team']} has the highest win total in the dataset with {result['wins']} wins."
    if tool_name == "most_opponents":
        return f"The most frequent matchup is {result['team_a']} versus {result['team_b']} with {result['matches']} matches."
    if tool_name == "city_with_most_matches":
        return f"{result['city']} hosted the most matches in the dataset, with {result['matches']} matches."
    if tool_name == "home_advantage":
        return f"The strongest home-record result in the dataset belongs to {result['team']} with {result['points']} points."
    if tool_name == "draw_percentage":
        return f"{result['draw_percentage']}% of matches ended in a draw, based on {result['draws']} draws out of {result['total_matches']} matches."
    if tool_name == "match_frequency":
        return f"The busiest year in the dataset was {result['top_year']} with {result['top_year_matches']} matches."
    return f"The result for your question is: {result}"


def explain_with_model(question: str, result: dict[str, Any], tool_name: str) -> str:
    if not MODEL_ENDPOINT or not MODEL_KEY or not MODEL_DEPLOYMENT:
        return fallback_explanation(question, result, tool_name)

    endpoint = f"{MODEL_ENDPOINT.rstrip('/')}/openai/deployments/{MODEL_DEPLOYMENT}/chat/completions?api-version={MODEL_API_VERSION}"
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a football analytics assistant. Interpret the supplied statistics only. "
                    "Never invent a value or claim data not present in the result."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n"
                    f"Tool: {tool_name}\n"
                    f"Result JSON: {json.dumps(result, ensure_ascii=False)}\n"
                    "Write a concise, grounded explanation for a public livestream audience."
                ),
            },
        ],
        "temperature": 0.1,
        "max_tokens": 300,
    }

    try:
        response = requests.post(endpoint, headers=build_model_headers(), json=payload, timeout=30)
        response.raise_for_status()
        body = response.json()
        return body["choices"][0]["message"]["content"].strip()
    except Exception:
        return fallback_explanation(question, result, tool_name)
