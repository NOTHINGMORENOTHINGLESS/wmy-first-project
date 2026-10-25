from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/international_results.csv"))
MODEL_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-6-astra")
MODEL_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
