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

@app.post("/ask")
def ask_deepseek(data: Prompt) -> Any:
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

    # タイムアウト少し長めに
    res = requests.post(url, json=payload, headers=headers, timeout=30)
    res.raise_for_status()
    res_json = res.json()

    # DeepSeek の返答テキスト（ここは DeepSeek の仕様に合わせてください）
    answer_text = res_json["choices"][0]["message"]["content"]

    # ここで、DeepSeek が JSON を返したら quiz として扱い、
    # そうでなければテキスト回答として { "answer": text } を返す
    # main.py 修正版
    try:
        import json
        parsed = json.loads(answer_text)
        # title がある場合は Quiz とみなす
        if isinstance(parsed, dict) and "title" in parsed:
            return parsed
    except Exception:
        pass

    # テキスト回答として返す（キーは "answer"）
    return {"answer": answer_text}
