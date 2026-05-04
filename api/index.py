from fastapi import FastAPI, BackgroundTasks, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os
import uuid
import re
import urllib.parse
import glob
import shutil

app = FastAPI(title="YouTube Downloader API (Vercel Ready)")

# Path file cookies di dalam folder api
COOKIE_PATH_SRC = os.path.join(os.path.dirname(__file__), "cookies.txt")

# Fungsi copy cookie ke /tmp/ agar bisa dibaca Vercel
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
    <!DOCTYPE html>
    <html lang="id">
    <head><title>Pro YT Downloader</title></head>
    <body style="font-family:sans-serif; text-align:center; padding:50px;">
        <h2>🔗 Auto YT Downloader</h2>
        <form id="p-form">
            <input type="url" id="url" style="padding:10px; width:80%;" placeholder="Link YouTube..." required><br><br>
            <input type="radio" name="fmt" value="mp3" checked> MP3 &nbsp;
            <input type="radio" name="fmt" value="mp4"> MP4 <br><br>
            <button type="submit" id="btn">Proses</button>
        </form>
        <div id="res" style="display:none; margin-top:20px;">
            <b id="title"></b><br><br>
            <a id="dl-btn" style="background:green; color:white; padding:10px; text-decoration:none;">📥 Download Sekarang</a>
        </div>
        <script>
            document.getElementById('p-form').onsubmit = async (e) => {
                e.preventDefault();
                const url = document.getElementById('url').value;
                const fmt = document.querySelector('input[name="fmt"]:checked').value;
                const btn = document.getElementById('btn');
                btn.disabled = true; btn.innerText = "Memproses...";
                const res = await fetch('/api/process/'+fmt, {method:'POST', body:new URLSearchParams({url})});
                const data = await res.json();
                if(data.success){
                    document.getElementById('title').innerText = data.title;
                    document.getElementById('dl-btn').href = data.full_download_url;
                    document.getElementById('res').style.display = 'block';
                } else { alert("Error: "+data.error); }
                btn.disabled = false; btn.innerText = "Proses";
            };
        </script>
    </body>
    </html>
    """)

@app.post("/api/process/mp3")
async def process_mp3(request: Request, url: str = Form(...)):
    cookie_path = get_tmp_cookie_path()
    opts = {'quiet': True, 'cookiefile': cookie_path}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Audio')
        url_enc = urllib.parse.quote(url)
        full = f"{str(request.base_url).rstrip('/')}/api/download/mp3?url={url_enc}"
        return {"success": True, "title": title, "full_download_url": full}
    except Exception as e: return {"success": False, "error": str(e)}

@app.post("/api/process/mp4")
async def process_mp4(request: Request, url: str = Form(...)):
    cookie_path = get_tmp_cookie_path()
    opts = {'quiet': True, 'cookiefile': cookie_path}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
        url_enc = urllib.parse.quote(url)
        full = f"{str(request.base_url).rstrip('/')}/api/download/mp4?url={url_enc}"
        return {"success": True, "title": title, "full_download_url": full}
    except Exception as e: return {"success": False, "error": str(e)}

@app.get("/api/download/mp3")
async def execute_mp3(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    base = f"/tmp/temp_{file_id}"
    cookie_path = get_tmp_cookie_path()
    opts_info = {'quiet': True, 'cookiefile': cookie_path}
    try:
        with yt_dlp.YoutubeDL(opts_info) as ydl:
            title = ydl.extract_info(url, download=False).get('title', 'Audio')
        opts_dl = {'outtmpl': f"{base}.%(ext)s", 'format': 'bestaudio/best', 'quiet': True, 'cookiefile': cookie_path}
        with yt_dlp.YoutubeDL(opts_dl) as ydl: ydl.download([url])
        files = glob.glob(f"{base}.*")
        f = files[0]
        background_tasks.add_task(delete_file, f)
        return FileResponse(path=f, media_type="audio/mpeg", filename=f"{sanitize_filename(title)}.{f.split('.')[-1]}")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/mp4")
async def execute_mp4(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    base = f"/tmp/temp_{file_id}"
    cookie_path = get_tmp_cookie_path()
    opts_info = {'quiet': True, 'cookiefile': cookie_path}
    try:
        with yt_dlp.YoutubeDL(opts_info) as ydl:
            title = ydl.extract_info(url, download=False).get('title', 'Video')
        opts_dl = {'outtmpl': f"{base}.%(ext)s", 'format': 'best[ext=mp4]/best', 'quiet': True, 'cookiefile': cookie_path}
        with yt_dlp.YoutubeDL(opts_dl) as ydl: ydl.download([url])
        files = glob.glob(f"{base}.*")
        f = files[0]
        background_tasks.add_task(delete_file, f)
        return FileResponse(path=f, media_type="video/mp4", filename=f"{sanitize_filename(title)}.mp4")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
