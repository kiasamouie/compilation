import json
import yt_dlp
import os
from moviepy.editor import *
import shutil as sh
import subprocess
import random
from datetime import datetime
import pyperclip
from youtube_uploader import YouTubeUploader

def Get_Info(url):
    return yt_dlp.YoutubeDL({}).extract_info(url=url, download=False, process=False)

def Create_Dir(url):
    if not os.path.isdir(url):
        os.mkdir(url)

def Clean_Dir(url):
    sh.rmtree(url)
    os.mkdir(url)

compilation_directory = "comps"
videos_directory = "videos"
save_directory = os.path.join(compilation_directory, datetime.now().strftime('%Y.%m.%d.%H.%M.%S'))

Clean_Dir(videos_directory)
Create_Dir(compilation_directory)

if not os.path.isdir(videos_directory):
    os.mkdir(f"{videos_directory}")

if not os.path.isdir(save_directory):
    os.mkdir(f"{save_directory}")

with open("AlreadyUsed.json", "r") as file:
    used = json.loads(file.read())

with open("@DailyDoseOfInternet.json", "r") as file:
    videos = list(filter(lambda x: x not in used, json.loads(file.read())))
    random.shuffle(videos)
    videos = videos[:30]

merged_videos = []
with open(os.path.join(save_directory,"info.txt"), "w", encoding="utf8") as file:
    for id in videos:
        if merged_videos and sum([video.duration for video in merged_videos]) >= 3600:
            break
        url = f"https://www.youtube.com/watch?v={id}"
        info = Get_Info(url)
        command = [
            'yt-dlp',
            '--format', 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080][ext=mp4]',
            '--output', os.path.join(videos_directory, "%(id)s.%(ext)s"),
            # '--postprocessor-args', f"-ss 3.1 -t {info['duration'] - 10} -c:v libx264 -c:a aac",
            '--postprocessor-args', f"-ss 3.1 -c:v libx264 -c:a aac",
            url
        ]
        subprocess.run(command,shell=True)
        merged_videos.append(VideoFileClip(os.path.join(videos_directory,f"{id}.mp4")))
        used.append(id)
        backslash = "\n" if id != videos[-1] else ""
        file.write(f"{info['title']}: {url}{backslash}")

concatenate_videoclips(merged_videos,method="compose").write_videofile(
    os.path.join(save_directory,"video.mp4"),
    codec="libx264",
    audio_codec="aac",
    threads=32
)

with open("AlreadyUsed.json", "w") as file:
    json.dump(used,file,indent=4)

Clean_Dir(videos_directory)

YouTubeUploader().upload_video(
    video_file=os.path.join(save_directory,"video.mp4"),
    title='1 Hour of Daily Dose of Internet (NO INTROS)',
    description='',
    category_id='22',
    tags=['dailydose', 'viral', 'interweb', '1hour']
)