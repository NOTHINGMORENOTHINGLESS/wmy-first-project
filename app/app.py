from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from app.analytics import evaluate_question, explain_with_model


def ensure_dataset_exists(path: str | os.PathLike[str]) -> Path:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Download it before launching the app.")
    return dataset_path


def load_dataframe(path: str | os.PathLike[str]) -> pd.DataFrame:
    dataset_path = ensure_dataset_exists(path)
    df = pd.read_csv(dataset_path)
    required_columns = {"date", "home_team", "away_team", "home_score", "away_score"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return df


def answer_question(question: str, df: pd.DataFrame):
    result = evaluate_question(df, question)
    explanation = explain_with_model(question, result.result, result.tool_name)
    return result, explanation
