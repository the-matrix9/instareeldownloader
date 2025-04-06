from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Instagram Reel Downloader is running!"}

@app.get("/download")
def download(url: str = Query(...)):
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'outtmpl': filename,
        'format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return FileResponse(filename, media_type="video/mp4", filename="reel.mp4")
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(filename):
            os.remove(filename)
