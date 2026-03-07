from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Frontend’den gelen talepler için CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
def download(url: str):
    # Geçici dosya oluştur
    file = str(uuid.uuid4()) + ".mp4"

    # yt-dlp seçenekleri
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': file,
        'merge_output_format': 'mp4',  # Zorla MP4
    }

    # Video indir
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Dosyayı kullanıcıya gönder
    response = FileResponse(file, media_type='video/mp4', filename="tiktok-video.mp4")

    # Arka planda silme
    @response.call_on_close
    def cleanup():
        if os.path.exists(file):
            os.remove(file)

    return response
