import os , sys
sys.path.append('\\Marvin\\env\\src\\STT_SRC\\Music\\api\\audiocraft')
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import  Mood.predict as mood_pd
from Music.api.demos.predict import _do_predictions , load_model
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from starlette.concurrency import run_in_threadpool
import uvicorn
from spider.spider import Novel , Novel_content 


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
class process_Mood_pd(BaseModel):
    TestData: str

class process_Music_pd(BaseModel):
    texts: str
    duration: float
class process_Novel_class(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Welcome to the AudioCraft API. Use /mood_analyze/ to perform mood analysis and /music_generate/ to generate music based on mood."}

@app.post("/Novel_catalog/")
async def cat_Novel_catalog(request: process_Novel_class):
    try:
        novel = Novel(request.url)  # 初始化 Novel 對象
        result = await run_in_threadpool(novel.check_website)  # 異步執行網站檢查
        return novel.dic  # 返回字典結果
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/Novel_page_content/")
async def cat_Novel_page_content(request: process_Novel_class):
    try:
        novel_content = Novel_content(request.url)  # 初始化 Novel_content 對象
        content = await run_in_threadpool(novel_content.check_website)  # 異步執行網站檢查
        return novel_content.content  # 返回頁面內容
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/mood_analyze/")
async def perform_mood_pd(request: process_Mood_pd):
    try:
        result = await run_in_threadpool(mood_pd.prediction, request.TestData)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/music_generate/")
async def perform_music_pd(request: process_Music_pd):
    try:
        result = await run_in_threadpool(
            _do_predictions ,
            texts = [request.texts],
            duration = request.duration,
        )
        return FileResponse(result[0] , filename="generated_sound.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    load_model()
    uvicorn.run(app , host = '0.0.0.0' , port = 8050)
    