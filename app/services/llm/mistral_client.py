import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL_NAME = "mistral-small"  # or mistral-medium / mistral-large (if available)

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}


def ask_mistral(context: str, question: str) -> str:
    """
    Send a prompt to Mistral API and return the model's response.
    """
    prompt = f"""Use the following context to answer the question:

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"[ERROR] Mistral API failed: {e}"
