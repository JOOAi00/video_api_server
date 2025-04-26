from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World from FastAPI!"}

@app.get("/video_info")
def video_info(url: str):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url")
        }
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=400)
