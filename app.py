import streamlit as st
import json
import sys
import os

sys.path.append(os.path.dirname(__file__))

from sentiment import analyze_sentiment

st.title("📊 Financial Sentiment Analysis App")
st.write("Enter any financial text below and analyze with OpenAI NLP")

text = st.text_area("Enter financial news / tweet / message")

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Please enter text.")
    else:
        try:
            result = analyze_sentiment(text)

            st.subheader("🔍 Sentiment Result")
            st.json(result)

            st.metric("Sentiment", result["sentiment"])
            st.metric("Market View", result["market_view"])
            st.metric("Score", result["sentiment_score"])
            st.subheader("📘 Summary")
            st.write(result["summary"])

        except Exception as e:
            st.error("❌ Failed to parse response.")
            st.write(str(e))
