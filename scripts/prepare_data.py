from __future__ import annotations

import os

import streamlit as st

from app.ai_layer import answer_question, load_dataframe


st.set_page_config(page_title="AI Football Insights", page_icon="⚽", layout="wide")
st.title("AI Football Insights")
st.caption("Deterministic analytics for the seven inspiration questions.")

with st.sidebar:
    st.header("Dataset")
    default_path = os.getenv("DATASET_PATH", "data/international_results.csv")
    dataset_path = st.text_input("CSV path", value=default_path)
    st.caption("Keep the raw Kaggle dataset outside the repository.")

    st.markdown("### Example questions")
    for question in [
        "What was the first ever international football match?",
        "Which national team has won the most matches?",
        "Which teams have met the most times?",
        "Which city has hosted the most matches?",
        "Which teams have the best or worst home advantage?",
        "What percentage of matches have ended in a draw?",
        "How does match frequency vary over history, by country, or by tournament?",
    ]:
        st.write(f"- {question}")

if not dataset_path:
    st.warning("Enter a valid dataset path.")
    st.stop()

try:
    df = load_dataframe(dataset_path)
except FileNotFoundError:
    st.warning("Dataset not found. Download the Kaggle CSV to the local file path and try again.")
    st.stop()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

question = st.text_input("Ask a question", value="Which national team has won the most matches?")

if st.button("Run analysis"):
    with st.spinner("Computing the analytics and explanation..."):
        result, explanation = answer_question(question, df)
    st.subheader("Result")
    st.write(result.summary)
    st.json(result.result)
    st.subheader("Explanation")
    st.write(explanation)
