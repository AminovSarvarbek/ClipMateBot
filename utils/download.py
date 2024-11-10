import re
import requests
import yt_dlp
import instaloader
import subprocess
import os

# Instagram yuklash funksiyasi
async def download_youtube(url: str):
    try:
        video_path = "youtube_video.mp4"
        ydl_opts = {
            'format': 'best',
            'outtmpl': video_path,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return video_path
    except Exception as e:
        print(f"Xatolik yuz berdi (YouTube): {e}")
        return "error"

# Instagram yuklash funksiyasi
async def download_instagram(url: str):
    try:
        video_path = "instagram_video.mp4"
        loader = instaloader.Instaloader()
        post_shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)

        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url, stream=True)
            with open(video_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return video_path
        else:
            print("Bu post video emas.")
            return "error"
    except Exception as e:
        print(f"Xatolik yuz berdi (Instagram): {e}")
        return "error"

# URL turini aniqlash funksiyasi
async def identify_and_download(url: str):
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/')
    instagram_pattern = re.compile(r'(https?://)?(www\.)?(instagram)\.com/')

    if youtube_pattern.search(url):
        print("Aniqlandi: YouTube video")
        return await download_youtube(url)
    elif instagram_pattern.search(url):
        print("Aniqlandi: Instagram video")
        return await download_instagram(url)
    else:
        print("Xato: URL manzili noto'g'ri yoki qo'llab-quvvatlanmaydi.")
        return "error"