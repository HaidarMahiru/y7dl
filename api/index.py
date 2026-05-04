from fastapi import FastAPI, BackgroundTasks, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os
import uuid
import re
import urllib.parse

app = FastAPI(title="YouTube Downloader API (Vercel Edition)")

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)

def sanitize_filename(name: str):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Auto YT Downloader (Vercel)</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f4f9; }
            .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            input[type="url"] { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #ccc; box-sizing: border-box; }
            .radio-group { display: flex; gap: 10px; margin: 15px 0; }
            .radio-group label { flex: 1; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; }
            .radio-group input[type="radio"] { display: none; }
            .radio-group input[type="radio"]:checked + span { color: #007bff; font-weight: bold; }
            .radio-group label:has(input[type="radio"]:checked) { border-color: #007bff; background: #e9f5ff; }
            button { width: 100%; padding: 14px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
            #result-box { margin-top: 25px; display: none; padding: 15px; border: 1px solid #ddd; border-radius: 10px; background: #fafafa; }
            .btn-download-final { display: block; background: #28a745; color: white; text-align: center; text-decoration: none; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 15px; }
            .api-box { margin-top: 20px; padding-top: 15px; border-top: 1px dashed #ccc; }
            .url-display { background: #eee; padding: 10px; border-radius: 6px; border: 1px solid #ccc; word-break: break-all; font-family: monospace; font-size: 12px; color: #555; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🔗 Auto YT Downloader</h2>
            <form id="process-form">
                <input type="url" name="url" id="url-input" placeholder="Tempel Link YouTube di sini..." required>
                <div class="radio-group">
                    <label><input type="radio" name="format_type" value="mp3" checked><span>🎵 MP3</span></label>
                    <label><input type="radio" name="format_type" value="mp4"><span>🎬 MP4</span></label>
                </div>
                <button type="submit" id="submit-btn">Proses Video</button>
            </form>
            <div id="status" style="text-align:center; margin-top:15px; color:#007bff; font-weight:bold;"></div>
            <div id="result-box">
                <div style="text-align:center;"><b id="res-title"></b></div>
                <a id="res-link-btn" href="#" class="btn-download-final" target="_blank">📥 Download Sekarang</a>
                <div class="api-box">
                    <div style="font-size: 12px; color: #666; margin-bottom: 5px;"><b>URL Eksekusi (API):</b></div>
                    <div id="res-url" class="url-display"></div>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('process-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const btn = document.getElementById('submit-btn');
                const status = document.getElementById('status');
                const resultBox = document.getElementById('result-box');
                const urlValue = document.getElementById('url-input').value;
                const formatType = document.querySelector('input[name="format_type"]:checked').value;
                btn.disabled = true;
                status.innerText = "Mengambil data...";
                resultBox.style.display = 'none';
                
                const formData = new FormData();
                formData.append("url", urlValue);
                const endpoint = formatType === 'mp3' ? '/api/process/mp3' : '/api/process/mp4';
                try {
                    const response = await fetch(endpoint, { method: 'POST', body: formData });
                    const data = await response.json();
                    if(data.success) {
                        status.innerText = "";
                        document.getElementById('res-title').innerText = data.title;
                        document.getElementById('res-link-btn').href = data.full_download_url;
                        document.getElementById('res-url').innerText = data.full_download_url;
                        resultBox.style.display = 'block';
                    } else { status.innerText = "Error: " + data.error; }
                } catch (err) { status.innerText = "Koneksi gagal."; }
                btn.disabled = false;
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/process/mp3")
async def process_mp3(request: Request, url: str = Form(...)):
    ydl_opts = {'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android']}}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Media')
        base_url = str(request.base_url).rstrip('/')
        encoded_url = urllib.parse.quote(url)
        full_url = f"{base_url}/api/download/mp3?url={encoded_url}"
        return {"success": True, "title": title, "full_download_url": full_url}
    except Exception as e: return {"success": False, "error": str(e)}

@app.post("/api/process/mp4")
async def process_mp4(request: Request, url: str = Form(...)):
    ydl_opts = {'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android']}}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Media')
        base_url = str(request.base_url).rstrip('/')
        encoded_url = urllib.parse.quote(url)
        full_url = f"{base_url}/api/download/mp4?url={encoded_url}"
        return {"success": True, "title": title, "full_download_url": full_url}
    except Exception as e: return {"success": False, "error": str(e)}

@app.get("/api/download/mp3")
async def execute_download_mp3(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    # PERUBAHAN PENTING UNTUK VERCEL: Gunakan /tmp/
    final_file = f"/tmp/temp_{file_id}.mp3" 
    
    ydl_opts_info = {'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android']}}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Audio')
        safe_title = sanitize_filename(title)
        
        ydl_opts_dl = {
            'outtmpl': f"/tmp/temp_{file_id}.%(ext)s", # Harus di /tmp/
            'format': 'bestaudio/best',
            # Postprocessor dicopot/diubah karena Vercel biasanya tidak punya ffmpeg bawaan
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url])
            
        # Jika file ternyata ekstensi m4a/webm dari youtube, kita biarkan saja karena tidak ada ffmpeg
        downloaded_file = final_file if os.path.exists(final_file) else final_file.replace('.mp3', '.m4a')
        if not os.path.exists(downloaded_file):
            downloaded_file = final_file.replace('.mp3', '.webm')
            
        background_tasks.add_task(delete_file, downloaded_file)
        return FileResponse(path=downloaded_file, media_type="audio/mpeg", filename=f"{safe_title}.mp3")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/mp4")
async def execute_download_mp4(background_tasks: BackgroundTasks, url: str):
    file_id = str(uuid.uuid4())[:8]
    # PERUBAHAN PENTING UNTUK VERCEL: Gunakan /tmp/
    final_file = f"/tmp/temp_{file_id}.mp4"
    
    ydl_opts_info = {'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android']}}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
        safe_title = sanitize_filename(title)
        
        ydl_opts_dl = {
            'outtmpl': f"/tmp/temp_{file_id}.%(ext)s", # Harus di /tmp/
            # Format diubah karena merge butuh ffmpeg. Kita ambil mp4 yang sudah jadi satu (kualitas mungkin turun ke 720p)
            'format': 'best[ext=mp4]/best', 
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url])
            
        background_tasks.add_task(delete_file, final_file)
        return FileResponse(path=final_file, media_type="video/mp4", filename=f"{safe_title}.mp4")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
