<div align="center">
  
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Television.png" alt="TV" width="100" />

  # 🚀 Auto YT Downloader (Pro API)
  
  [![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&pause=1000&color=007BFF&center=true&vCenter=true&width=500&lines=Fast+%26+Lightweight+API;Bypass+YouTube+HTTP+429;Auto-Fetch+Video+Titles;100%25+Free+and+Open+Source)](https://git.io/typing-svg)

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp">
    <img src="https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg">
  </p>
  
  **Aplikasi Web & API modern untuk mengunduh video dan audio YouTube dengan nama file asli secara otomatis.**
  
  ---
</div>

## ✨ Fitur Unggulan

- 🛡️ **Anti-Blokir (Bypass HTTP 429):** Menggunakan teknik *Android Client Spoofing* untuk menembus proteksi terbaru YouTube.
- 🤖 **Developer Ready:** Dilengkapi 4 endpoint API super bersih yang siap dihubungkan ke Bot WhatsApp / Telegram Anda.
- 🎵 **Konversi Otomatis:** Otomatis mengubah media menjadi `MP3` murni (via FFmpeg) atau `MP4` kualitas tinggi.
- 🏷️ **Smart Naming:** URL API sangat pendek. Server akan mencari judul video secara otomatis di latar belakang dan menamai file unduhan sesuai aslinya.
- 🧹 **Zero Junk Files:** Sistem *Background Tasks* otomatis menghapus file sementara di server segera setelah file selesai dikirim ke pengguna.
- 📱 **Clean Web UI:** Antarmuka responsif dan modern untuk penggunaan manual.

## 🛠️ Tech Stack

<div align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,ubuntu,vercel,bash" />
  </a>
</div>

## 🚀 Cara Instalasi (VPS / Server Lokal)

Server dengan sistem operasi Ubuntu / Debian sangat direkomendasikan untuk mendapatkan kualitas video maksimal menggunakan `ffmpeg`.

### 1. Persiapan Sistem
```bash
sudo apt update
sudo apt install python3-pip python3-venv ffmpeg tmux -y
