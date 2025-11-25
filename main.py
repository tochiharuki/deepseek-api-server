import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

    res = requests.post(url, json=payload, headers=headers, timeout=30)
    res.raise_for_status()

    res_json = res.json()
    answer_text = res_json["choices"][0]["message"]["content"]

    # Swift側のQuizResponse形式に整形
    try:
        import json
        quiz_json = json.loads(answer_text)  # DeepSeekがJSON文字列で返してくれることが前提
        return quiz_json
    except Exception:
        # 万が一JSONでなければデフォルトを返す
        return {
            "question": "取得できませんでした",
            "choices": ["", "", "", ""],
            "answerIndex": 0
        }
