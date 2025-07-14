import asyncio
import base64
from datetime import datetime, timedelta
import os
import random
import re
import shutil
import tempfile
import imgbbpy
import requests
from bs4 import BeautifulSoup
from moviepy.video.io.VideoFileClip import VideoFileClip
from decouple import config
import subprocess
from pathlib import Path


class Utils:

    @staticmethod
    def sleep(ms):
        asyncio.sleep(ms / 1000.0)

    @staticmethod
    def fetch(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def fetch_buffer(url):
        response = requests.get(url, stream=True)
        return response.content

    @staticmethod
    def is_truthy(value):
        return value is not None and value is not False

    @staticmethod
    def readdir_recursive(directory):
        results = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                results.append(os.path.join(root, file))

        return results

    @staticmethod
    def buffer_to_base64(buffer):
        return base64.b64encode(buffer).decode("utf-8")

    @staticmethod
    def webp_to_mp4(webp):
        def request(form, file=None):
            url = (
                f"https://ezgif.com/webp-to-mp4/{file}"
                if file
                else "https://ezgif.com/webp-to-mp4"
            )
            response = requests.post(url, files=form)
            return BeautifulSoup(response.text, "html.parser")

        files = {"new-image": ("bold.webp", webp, "image/webp")}
        soup1 = request(files)
        file = soup1.find("input", {"name": "file"})["value"]
        files = {"file": (file, "image/webp"), "convert": "Convert WebP to MP4!"}
        soup2 = request(files, file)
        video_url = (
            "https:"
            + soup2.find("div", {"id": "output"}).find("video").find("source")["src"]
        )
        return requests.get(video_url).content

    @staticmethod
    def extract_numbers(content):
        try:
            number_pattern = re.compile(r"\b\d+\b")
            numbers = number_pattern.findall(content)
            return numbers
        except:
            pass

    @staticmethod
    def get_random_int(min, max):
        return random.randint(min, max)

    @staticmethod
    def get_random_float(min, max):
        return random.uniform(min, max)

    @staticmethod
    def get_random_item(array):
        return random.choice(array)

    @staticmethod
    def get_random_items(array, count):
        return [Utils.get_random_item(array) for _ in range(count)]

    @staticmethod
    def extract_links(text):
        url_pattern = r"https?://[^\s]+"
        return re.findall(url_pattern, text)
    
    @staticmethod
    def convert_to_webp(input_path, width=512, fps=15, loop=True, compress=6):
        input_path = Path(input_path)
        output_path = input_path.with_suffix(".webp")
    
        if not input_path.exists():
            print("❌ File not found.")
            return
    
        file_ext = input_path.suffix.lower()
        type_ = "image" if file_ext in [".jpg", ".jpeg", ".png"] else "video"
    
        # Get file size for quality logic
        buffer_size = input_path.stat().st_size
        if buffer_size < 300_000:
            quality = "30"
        elif buffer_size < 400_000:
            quality = "20"
        else:
            quality = "15"
        
        if type_ == "image":
            quality = "75"
    
        vf_filter = (
            f"scale='min({width},iw)':min'({width},ih)':force_original_aspect_ratio=decrease,"
            f"fps={fps},"
            f"pad={width}:{width}:-1:-1:color=white@0.0,"
            "split[a][b];"
            "[a]palettegen=reserve_transparent=on:transparency_color=ffffff[p];"
            "[b][p]paletteuse"
        )
    
        command = [
            "ffmpeg",
            "-y",  # overwrite
            "-i", str(input_path),
            "-vf", vf_filter,
            "-loop", "0" if loop else "1",
            "-lossless", "1" if type_ == "image" else "0",
            "-compression_level", str(compress),
            "-quality", quality,
            "-preset", "picture",
            "-an",
            "-vsync", "0",
            "-f", "webp",
            str(output_path)
        ]
    
        try:
            subprocess.run(command, check=True)
            print(f"✅ Converted: {output_path}")
        except subprocess.CalledProcessError:
            print("❌ ffmpeg failed to convert the file.")


    @staticmethod
    def gif_to_mp4(gif):
        temp_dir = tempfile.mkdtemp()
        gif_path = os.path.join(temp_dir, "temp.gif")
        mp4_path = os.path.join(temp_dir, "temp.mp4")

        with open(gif_path, "wb") as f:
            f.write(gif)

        clip = VideoFileClip(gif_path)
        clip.write_videofile(mp4_path, codec="libx264")

        with open(mp4_path, "rb") as f:
            buffer = f.read()

        shutil.rmtree(temp_dir)
        return buffer

    @staticmethod
    def capitalize(s):
        return s[0].upper() + s[1:]

    @staticmethod
    def humanbytes(size):
        """Input size in bytes,
        outputs in a human readable format"""
        # https://stackoverflow.com/a/49361727/4723940
        if not size:
            return ""
        # 2 ** 10 = 1024
        power = 2**10
        raised_to_pow = 0
        dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
        while size > power:
            size /= power
            raised_to_pow += 1
        return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

    @staticmethod
    def uptime():
        try:
            with open("/proc/uptime") as f:
                total_seconds = float(f.read().split()[0])
        except IOError:
            return "Cannot open uptime file: /proc/uptime"

        MINUTE, HOUR, DAY = 60, 3600, 86400
        days, remainder = divmod(total_seconds, DAY)
        hours, remainder = divmod(remainder, HOUR)
        minutes, seconds = divmod(remainder, MINUTE)

        parts = [
            f"{int(days)} day{'s' if days != 1 else ''}",
            f"{int(hours)} hour{'s' if hours != 1 else ''}",
            f"{int(minutes)} minute{'s' if minutes != 1 else ''}",
            f"{int(seconds)} second{'s' if seconds != 1 else ''}",
        ]
        return ", ".join(part for part in parts if not part.startswith("0"))


    @staticmethod
    def img_to_url(img_path):
        client = imgbbpy.SyncClient(config("IMGBB_KEY", default=None))
        if client:
            image = client.upload(file=img_path)
            return image.url
     
    
    @staticmethod
    def get_tenor_gif_urls(search_query: str, limit: int = 30) -> list:
        api_key = "LIVDSRZULELA"
        url = f"https://g.tenor.com/v1/search?q={search_query}&key={api_key}&limit={limit}"

        response = requests.get(url)

        if response.status_code != 200:
            return(f"Failed to fetch from Tenor: {response.status_code}")

        data = response.json()
        gif_urls = []
   
        for result in data.get("results", []):
           gif_data = result.get("media", [])[0].get("gif", {})
           gif_url = gif_data.get("url")
           if gif_url:
               gif_urls.append(gif_url)
   
        return gif_urls

