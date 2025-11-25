import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS設定（Swiftアプリからのアクセス用）
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
    
    url = "https://api.deepseek.com/chat/completions"

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

    # DeepSeek の応答
    return res.json()
