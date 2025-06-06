from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 允许跨域请求（如果前端在本地或不同端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求体结构
class Query(BaseModel):
    question: str

# 调用 DeepSeek 的 API 接口
@app.post("/ai-search")
def ai_search(query: Query):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"error": "API 密钥未设置"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek-chat",  # 确保你使用的是正确模型名
        "messages": [
            {"role": "system", "content": "你是一个帮助用户搜索九尾狐相关文化知识的智能助理。"},
            {"role": "user", "content": query.question}
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        return {"answer": answer}
    else:
        return {"error": response.text}
