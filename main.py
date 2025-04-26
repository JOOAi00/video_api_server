from fastapi import FastAPI, HTTPException
from pytube import YouTube

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World from FastAPI!"}

@app.get("/fetch_video_info/")
def fetch_video_info(url: str):
    try:
        yt = YouTube(url)
        video_info = {
            "title": yt.title,
            "thumbnail_url": yt.thumbnail_url,
            "length_seconds": yt.length,
            "views": yt.views,
            "author": yt.author,
        }
        return video_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
