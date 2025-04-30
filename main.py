from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
import yt_dlp
from config_data import app_config

# مفتاح الحماية
API_KEY = "YoussefJoxs07571980@@##"

app = FastAPI()

def verify_key(request: Request):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="مفتاح API غلط أو ناقص ❌")

@app.get("/")
def read_root():
    return {"message": "🔥 API شغالة وجاهزة 🔥"}

@app.get("/info")
async def get_video_info(request: Request, url: str = Query(..., description="Video URL")):
    verify_key(request)
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": f"{info.get('duration') // 60} دقيقة و {info.get('duration') % 60} ثانية",
                "webpage_url": info.get("webpage_url"),
                "uploader": info.get("uploader"),
                "available_formats": [
                    {
                        "format_id": f.get("format_id"),
                        "format_note": f.get("format_note") or "",
                        "ext": f.get("ext"),
                        "resolution": f.get("resolution") or "",
                        "filesize": f.get("filesize") or ""
                    }
                    for f in info.get("formats", []) if f.get("url")
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_video")
async def download_video(request: Request, url: str = Query(..., description="Video URL"), format_id: str = Query(None, description="Format ID to download")):
    verify_key(request)
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # لو فيه format_id
            if format_id:
                selected_format = next((f for f in info['formats'] if f['format_id'] == format_id), None)
                if not selected_format:
                    raise HTTPException(status_code=404, detail="الصيغة المطلوبة مش موجودة ❌")
            else:
                # لو مفيش، نختار أعلى جودة افتراضيًا
                selected_format = next((f for f in reversed(info['formats']) if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

            if not selected_format:
                raise HTTPException(status_code=404, detail="مفيش فيديو مناسب للتحمل ❌")

            download_url = selected_format['url']
            return RedirectResponse(url=download_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_audio")
async def download_audio(request: Request, url: str = Query(..., description="Video URL"), format_id: str = Query(None, description="Format ID to download")):
    verify_key(request)
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if format_id:
                selected_format = next((f for f in info['formats'] if f['format_id'] == format_id), None)
                if not selected_format:
                    raise HTTPException(status_code=404, detail="الصيغة الصوتية المطلوبة مش موجودة ❌")
            else:
                selected_format = next((f for f in reversed(info['formats']) if f.get('vcodec') == 'none'), None)

            if not selected_format:
                raise HTTPException(status_code=404, detail="مفيش صوت مناسب للتحمل ❌")

            download_url = selected_format['url']
            return RedirectResponse(url=download_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/app_config")
async def get_app_config(request: Request):
    verify_key(request)
    return JSONResponse(content=app_config)

