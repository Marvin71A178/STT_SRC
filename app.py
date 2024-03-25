import os , sys
sys.path.append('\\Marvin\\env\\src\\STT_SRC\\Music\\api\\audiocraft')

from fastapi.responses import FileResponse
import  Mood.predict as mood_pd
import  Music.api.demos.predict as music_pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from starlette.concurrency import run_in_threadpool
import uvicorn

class process_Mood_pd(BaseModel):
    TestData: str

class process_Music_pd(BaseModel):
    texts: str
    duration: float
    

app = FastAPI()

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
            music_pd._do_predictions ,
            request.texts,
            request.duration,
        )
        return FileResponse(result , filename="generated_sound.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app , host = '0.0.0.0' , port = 8050)