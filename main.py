from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from yt_dlp import YoutubeDL
from urllib.parse import unquote

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🎬 Video Info API is running!"}

@app.get("/fetch_video_info/")
async def fetch_video_info(request: Request):
    try:
        url = request.query_params.get("url")
        
        if not url:
            return JSONResponse(status_code=400, content={"error": "Missing 'url' parameter."})
        
        # فك تشفير الرابط لو متشفر بالغلط
        url = unquote(url)

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'best',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        result = {
            "title": info.get('title'),
            "duration": info.get('duration'),
            "thumbnail": info.get('thumbnail'),
            "webpage_url": info.get('webpage_url'),
        }

        return result

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
