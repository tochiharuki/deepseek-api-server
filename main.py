# main.py
import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    message: str
    mode: str = "chat"  # chat or quiz

@app.post("/ask")
def ask_deepseek(data: Prompt):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    url = "https://api.deepseek.com/v1/chat/completions"

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": data.message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()
    res_json = res.json()
    answer_text = res_json["choices"][0]["message"]["content"]

    # --- Quizモード ---
    if data.mode == "quiz":
        # DeepSeek が JSON を返してくる前提
        return json.loads(answer_text)

    # --- Chatモード ---
    return {"answer": answer_text}
