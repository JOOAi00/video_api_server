from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# السماح لكل الناس تستخدم الـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoInfo(BaseModel):
    title: str
    thumbnail: str
    duration: str
    webpage_url: str

def format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours} ساعة و {minutes} دقيقة و {sec} ثانية"
    elif minutes > 0:
        return f"{minutes} دقيقة و {sec} ثانية"
    else:
        return f"{sec} ثانية"

@app.get("/", response_model=VideoInfo)
async def get_video_info(url: str = Query(..., description="رابط الفيديو")):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return VideoInfo(
            title=info.get("title", "لا يوجد عنوان"),
            thumbnail=info.get("thumbnail", ""),
            duration=format_duration(info.get("duration", 0)),
            webpage_url=info.get("webpage_url", url)
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"خطأ: {str(e)}")
