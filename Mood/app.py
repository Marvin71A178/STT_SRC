
from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import predict
import uvicorn
import argparse
import psutil
from dotenv import load_dotenv
import os

# 加载環境變量
load_dotenv()

# 從環境變量中獲取端口號，如果不存在則默認使用8000
port = int(os.getenv("PORT", 8050))

# API Model
class MoodAnaLyzeModel(BaseModel):
  text: str  

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test API
@app.get('/')
def root() -> object:
  return {"hello": "world!"}

@app.get("/resources")
def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }

async def process_emotion_ana(text):
  return predict.mood_ana_api(text)

# For Analyzing Emotion
@app.post('/emotion_analysis', response_model=int)
async def mood_analyze_api(moodAnaLyzeModel: MoodAnaLyzeModel, request: Request) -> int: 
  if request.headers.get('Content-Type') != 'application/json':
    return HTTPException(status_code=422, detail="Invalid Content-Type")
  
  if moodAnaLyzeModel.text is None or moodAnaLyzeModel.text == '':
    return HTTPException(status_code=400, detail="text is Null!")
  
  return await process_emotion_ana(moodAnaLyzeModel.text)
