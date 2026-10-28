# AI Football Insights Demo

This project is intentionally separate from any existing football-results dashboard repository. It focuses only on the seven inspiration questions below and keeps the data and generated artifacts out of the public repo.

## The Seven Inspiration Questions

1. What was the first ever international football match?
2. Which national team has won the most matches?
3. Which teams have met the most times?
4. Which city has hosted the most matches?
5. Which teams have the best or worst home advantage?
6. What percentage of matches have ended in a draw?
7. How does match frequency vary over history, by country, or by tournament?

## Scope guardrails

- Premier League-inspired scenarios are out of scope.
- The app covers the men's international match results dataset only.
- The model layer explains the result after deterministic analytics computes the answer.
- The repository contains no raw dataset, no notebook snapshots, and no generated artifacts.

## Q&A answer for out-of-scope questions

If a viewer asks about team play styles, counterattacks, or player performance patterns, use this answer:

> Those scenarios are out of scope for this dataset. The dataset contains international match results, scores, cities, venues, and related historical records, but it does not include club-level event data, tracking data, or player-level performance data. Those questions require a different dataset and are not covered in this demo.

## Project goals

- Build a public-facing football insights web app.
- Keep the analytics deterministic and explainable.
- Show a model-backed explanation layer grounded in computed results.
- Run locally with Docker Compose and support AKS/ACA deployment patterns.
- Keep the repository public and shareable while storing local data in a non-committed location.

## Local setup

1. Create a virtual environment.
2. Install dependencies.
3. Download the official international football results CSV locally.
4. Run the app.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
python scripts/prepare_data.py
streamlit run app/app.py
```

## Docker Compose

```bash
docker compose up --build
```

## Repository layout

- `app/analytics.py` – deterministic analytics for the seven questions.
- `app/ai_layer.py` – model-backed explanation layer.
- `app/app.py` – Streamlit web UI.
- `app/config.py` – environment configuration.
- `scripts/prepare_data.py` – local data guidance script.
- `docs/aks-vs-aca.md` – AKS vs ACA decision guide.
- `docs/hackathon-guide.md` – attendee guide.
- `deploy/aks/deployment.yaml` – AKS template.
- `deploy/aca/deployment.yaml` – ACA template.
- `tests/test_analytics.py` – automated validation for analytics routing and common outcomes.

## Data handling

The official dataset is not committed to this repository. Keep it in a local folder such as `data/international_results.csv` or in private Azure storage during the proof-of-concept.

## Notes

This repo intentionally stays focused on the seven inspiration questions and does not attempt to build team style, counterattack, or player performance analytics.

See OVERLAY_CONTRACT.md for the broadcast overlay data contract.
