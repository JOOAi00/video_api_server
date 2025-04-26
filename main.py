from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "Server is running perfectly!"}

@app.post("/fetch-info")
def fetch_video_info(request: VideoRequest):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "download_url": info.get("url")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
