from fastapi import FastAPI, BackgroundTasks, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os
import uuid
import re
import urllib.parse
import glob
import shutil

app = FastAPI(title="YouTube Downloader API (Final Fix)")

COOKIE_PATH_SRC = os.path.join(os.path.dirname(__file__), "cookies.txt")
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

def get_tmp_cookie_path():
    dst = "/tmp/cookies.txt"
    if os.path.exists(COOKIE_PATH_SRC):
        shutil.copy(COOKIE_PATH_SRC, dst)
        return dst
    return None

def delete_file(path):
    if path and os.path.exists(path):
        os.remove(path)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""
    <html><body>
    <h2>Auto YT Downloader is Running</h2>
    <p>API is ready for integration.</p>
    </body></html>
    """)

# --- PROCESS MP3 ---
@app.post("/api/process/mp3")
async def process_mp3(request: Request, url: str = Form(...)):
    opts = {'quiet': True, 'cookiefile': get_tmp_cookie_path(), 'user_agent': USER_AGENT}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Audio')
        full = f"{str(request.base_url).rstrip('/')}/api/download/mp3?url={urllib.parse.quote(url)}"
        return {"success": True, "title": title, "full_download_url": full}
    except Exception as e: return {"success": False, "error": str(e)}

# --- PROCESS MP4 ---
@app.post("/api/process/mp4")
async def process_mp4(request: Request, url: str = Form(...)):
    opts = {'quiet': True, 'cookiefile': get_tmp_cookie_path(), 'user_agent': USER_AGENT}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
        full = f"{str(request.base_url).rstrip('/')}/api/download/mp4?url={urllib.parse.quote(url)}"
        return {"success": True, "title": title, "full_download_url": full}
    except Exception as e: return {"success": False, "error": str(e)}

# --- DOWNLOAD MP3 ---
@app.get("/api/download/mp3")
async def execute_mp3(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    base = f"/tmp/temp_{file_id}"
    cookie_path = get_tmp_cookie_path()
    
    opts_dl = {
        'outtmpl': f"{base}.%(ext)s", 
        'format': 'bestaudio/best', 
        'quiet': True, 
        'cookiefile': cookie_path,
        'user_agent': USER_AGENT
    }
    
    try:
        with yt_dlp.YoutubeDL(opts_dl) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Audio')
        
        files = glob.glob(f"{base}.*")
        f = files[0]
        background_tasks.add_task(delete_file, f)
        return FileResponse(path=f, media_type="audio/mpeg", filename=f"{sanitize_filename(title)}.{f.split('.')[-1]}")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# --- DOWNLOAD MP4 ---
@app.get("/api/download/mp4")
async def execute_mp4(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    base = f"/tmp/temp_{file_id}"
    cookie_path = get_tmp_cookie_path()
    
    opts_dl = {
        'outtmpl': f"{base}.%(ext)s", 
        'format': 'best[ext=mp4]/best', 
        'quiet': True, 
        'cookiefile': cookie_path,
        'user_agent': USER_AGENT
    }
    
    try:
        with yt_dlp.YoutubeDL(opts_dl) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Video')
        
        files = glob.glob(f"{base}.*")
        f = files[0]
        background_tasks.add_task(delete_file, f)
        return FileResponse(path=f, media_type="video/mp4", filename=f"{sanitize_filename(title)}.mp4")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
