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
    res.raise_for_status()  # 失敗時は例外を出す

    res_json = res.json()
    # OpenAI 互換の JSON から必要な部分だけ抽出
    answer_text = res_json["choices"][0]["message"]["content"]

    return {"question": data.message, "answer": answer_text}
