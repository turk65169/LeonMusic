import os
import re
import yt_dlp
import random
import asyncio
import aiohttp
from typing import Optional
from pathlib import Path

from py_yt import Playlist, VideosSearch

from KumsalTR import logger
from KumsalTR.helpers import Track, utils


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "KumsalTR/cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )

    def get_cookies(self):
        if not self.checked:
            self.cookies = []
            if not os.path.exists(self.cookie_dir):
                os.makedirs(self.cookie_dir)
            
            for file in os.listdir(self.cookie_dir):
                if file.endswith(".txt"):
                    path = os.path.join(self.cookie_dir, file)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read(512)
                            if "# Netscape" in content or "youtube.com" in content:
                                self.cookies.append(path)
                    except: pass
            self.checked = True
        return self.cookies

    async def save_cookies(self, urls: list[str]) -> None:
        logger.info("Saving cookies from urls...")
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(urls):
                path = f"{self.cookie_dir}/cookie_{i}.txt"
                link = "https://batbin.me/api/v2/paste/" + url.split("/")[-1]
                async with session.get(link) as resp:
                    resp.raise_for_status()
                    with open(path, "wb") as fw:
                        fw.write(await resp.read())
        logger.info(f"Cookies saved in {self.cookie_dir}.")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    async def search(self, query: str, m_id: int, user: Optional[str] = None, user_id: int = 0, video: bool = False) -> Track | None:
        _search = VideosSearch(query, limit=1, with_live=False)
        results = await _search.next()
        if results and results["result"]:
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:25],
                thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                user=user,
                user_id=user_id,
                video=video,
            )
        return None

    async def playlist(self, limit: int, user: str, user_id: int, url: str, video: bool) -> list[Track | None]:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    title=data.get("title")[:25],
                    thumbnail=data.get("thumbnails")[-1].get("url").split("?")[0],
                    url=data.get("link").split("&list=")[0],
                    user=user,
                    user_id=user_id,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except:
            pass
        return tracks


    async def download(self, video_id: str, video: bool = False) -> str | None:
        url = self.base + video_id
        # Define base path without extension to check for existing files
        base_path = f"downloads/{video_id}"
        
        # Check if already exists in any common format
        for ext in ["mp4", "mkv", "webm", "m4a", "mp3"]:
            if os.path.exists(f"{base_path}.{ext}"):
                return f"{base_path}.{ext}"

        if not self.cookies:
            self.get_cookies()
            
        if not self.cookies and config.COOKIES_URL:
            logger.info("Cookie pool empty, refreshing from cloud...")
            try:
                await self.save_cookies(config.COOKIES_URL)
                self.checked = False
                self.get_cookies()
            except: pass

        # Robust format selection in a single string to avoid redundant extraction attempts
        if video:
            fmt = "bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?720]+bestaudio/best[height<=?720]/best"
        else:
            fmt = "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best"

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]

        attempts = [None] + list(self.cookies)
        random.shuffle(attempts)

        # Optimization: Limit cookie attempts to avoid long delays
        for cookie in attempts[:5]:
            opts = {
                "outtmpl": f"{base_path}.%(ext)s",
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "cookiefile": cookie,
                "format": fmt,
                "socket_timeout": 10,
                "concurrent_fragment_downloads": 10,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "web"],
                        "skip": ["web_safari", "ios"]
                    }
                },
                "http_headers": {
                    "User-Agent": random.choice(user_agents),
                    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Connection": "keep-alive",
                },
            }
            
            try:
                def _dl():
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        return ydl.prepare_filename(info)

                # Return the actual filename returned by yt-dlp
                res_path = await asyncio.wait_for(asyncio.to_thread(_dl), timeout=90)
                if res_path and os.path.exists(res_path):
                    return res_path
            except Exception as e:
                err = str(e).lower()
                if "403" in err or "429" in err:
                    continue
                if "sign in to confirm" in err:
                    if cookie and cookie in self.cookies:
                        logger.error(f"Invalid cookie removed: {os.path.basename(cookie)}")
                        try:
                            self.cookies.remove(cookie)
                            os.remove(cookie)
                        except: pass
                    continue
        return None









