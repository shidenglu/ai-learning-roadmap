import os
import yt_dlp

url = "https://www.bilibili.com/video/BV1npun6nEFx/"

output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

ydl_opts = {
    "format": "bv*+ba/b",
    "merge_output_format": "mp4",
    "outtmpl": os.path.join(
        output_dir,
        "%(title)s.%(ext)s"
    ),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("下载完成")
print("保存位置：", os.path.abspath(output_dir))