from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Reel Downloader API running 🎬"}

@app.get("/download")
def download_reel(url: str = Query(...)):
    file_id = str(uuid.uuid4())
    output_filename = f"{file_id}.mp4"

    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return FileResponse(output_filename, media_type='video/mp4', filename='reel.mp4')
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)
