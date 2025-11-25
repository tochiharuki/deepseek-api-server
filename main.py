import os
import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 設定
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
        "messages": [{"role": "user", "content": data.message}],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # DeepSeek API 呼び出し
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        res_json = res.json()
        answer_text = res_json["choices"][0]["message"]["content"]
    except Exception as e:
        return {
            "type": "answer",
            "answer": f"APIエラー: {str(e)}"
        }

    # ● Quiz形式 JSON として返ってきたか？
    try:
        parsed = json.loads(answer_text)

        # quiz 形式の妥当性チェック
        if (
            "question" in parsed and
            "choices" in parsed and
            "answerIndex" in parsed
        ):
            return {
                "type": "quiz",
                "question": parsed["question"],
                "choices": parsed["choices"],
                "answerIndex": parsed["answerIndex"],
                "explanation": parsed.get("explanation", "")
            }

    except Exception:
        pass

    # ● 通常メッセージ → Answer モードとして返す
    return {
        "type": "answer",
        "answer": answer_text
    }
