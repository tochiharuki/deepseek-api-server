import os
import json
import re
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    message: str
    mode: str = "chat"


def extract_json(text: str):
    """
    DeepSeek が返したテキストから JSON 部分だけを抽出する
    """
    # ```json ... ``` を除去
    text = re.sub(r"```json|```", "", text).strip()

    # { から } までを抽出
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        return match.group(0)
    return text  # 最悪生テキスト


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

    if data.mode == "quiz":
        pure = extract_json(answer_text)  # ★ JSON 抽出
        return json.loads(pure)          # ★ ここで初めてパース

    return {"answer": answer_text}
