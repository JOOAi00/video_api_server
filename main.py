from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import yt_dlp
import urllib.parse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🔥 API شغالة وجاهزة 🔥"}

@app.get("/info")
async def get_video_info(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": f"{info.get('duration') // 60} دقيقة و {info.get('duration') % 60} ثانية",
                "webpage_url": info.get("webpage_url"),
                "uploader": info.get("uploader"),
                "available_formats": [f"{f.get('format_id')} - {f.get('format_note') or ''} - {f.get('ext')}" for f in info.get("formats", []) if f.get("vcodec") != "none"]
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_video")
async def download_video(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [f for f in info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') != 'none']

            if not formats:
                raise HTTPException(status_code=404, detail="No suitable video format found")

            best_format = formats[-1]  # ناخد اعلى جوده متاحه
            download_url = best_format['url']

            return RedirectResponse(url=download_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_audio")
async def download_audio(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [f for f in info['formats'] if f.get('vcodec') == 'none']

            if not formats:
                raise HTTPException(status_code=404, detail="No suitable audio format found")

            best_audio = formats[-1]
            download_url = best_audio['url']

            return RedirectResponse(url=download_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
