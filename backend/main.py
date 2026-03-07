from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import uuid

app = FastAPI()

@app.get("/download")
def download(url: str):

    file = str(uuid.uuid4()) + ".mp4"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': file,
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return FileResponse(file, media_type='video/mp4', filename="tiktok.mp4")
