from openai import OpenAI
import json
import re

client = OpenAI(api_key = 'Enter your api key')

def clean_model_output(output):
    """
    Removes Markdown code blocks like ```json ... ```
    and cleans common JSON formatting errors.
    """

    # Remove Markdown block ```
    output = re.sub(r"```json|```", "", output).strip()

    # Remove trailing commas
    output = re.sub(r",\s*}", "}", output)
    output = re.sub(r",\s*]", "]", output)

    # Replace single quotes with double quotes
    output = output.replace("'", '"')

    # Convert numeric strings to numbers
    output = re.sub(r'":\s*"([0-9.]+)"', r'": \1', output)

    return output


def analyze_sentiment(text):
    prompt = f"""
You are a financial sentiment analysis model.
Return ONLY valid JSON. No markdown, no code blocks, no ```json.

Statement:
{text}

JSON format:
{{
    "sentiment": "Positive or Negative or Neutral",
    "sentiment_score": 0.0,
    "summary": "short explanation",
    "market_view": "Bullish or Bearish or Neutral"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # Clean markdown + fix JSON issues
    cleaned = clean_model_output(raw)

    # Parse with json
    return json.loads(cleaned)
