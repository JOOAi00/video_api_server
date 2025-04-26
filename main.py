from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello, World from FastAPI!"})

@app.get("/download")
async def download_video(url: str):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {"title": info.get('title'), "url": url, "status": "Downloaded Successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
