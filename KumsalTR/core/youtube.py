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
            if os.path.exists(self.cookie_dir):
                for file in os.listdir(self.cookie_dir):
                    if file.endswith(".txt"):
                        self.cookies.append(f"{self.cookie_dir}/{file}")
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies are missing; YouTube might block the bot.")
            return None
        return random.choice(self.cookies)

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

    def get_cookies(self):
        if not self.checked:
            self.cookies = []
            if not os.path.exists("KumsalTR/cookies"):
                os.makedirs("KumsalTR/cookies")
            
            for file in os.listdir("KumsalTR/cookies"):
                if file.endswith(".txt"):
                    path = os.path.join("KumsalTR/cookies", file)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read(512)
                            if "# Netscape" in content or "youtube.com" in content:
                                self.cookies.append(path)
                    except: pass
            self.checked = True
        return self.cookies

    async def download(self, video_id: str, video: bool = False) -> str | None:
        url = self.base + video_id
        ext = "mp4" if video else "webm"
        filename = f"downloads/{video_id}.{ext}"

        if Path(filename).exists():
            return filename

        if not self.cookies:
            self.get_cookies()
            
        # KRİTİK ÖNLEM: Eğer çerez kalmadıysa ve URL varsa otomatik yenile
        if not self.cookies and config.COOKIES_URL:
            logger.info("Çerez havuzu boşaldı, buluttan yenileniyor...")
            try:
                await self.save_cookies(config.COOKIES_URL)
                self.checked = False
                self.get_cookies()
            except: pass

        format_attempts = [
            "bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?720]+bestaudio/best[height<=?720]/best" if video else "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
            "bestaudio/best", "best",
        ]

        # Daha geniş User-Agent Rotasyonu
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]

        attempts = [None] + list(self.cookies)
        random.shuffle(attempts)

        for cookie in attempts:
            agent = random.choice(user_agents)
            for fmt in format_attempts:
                ydl_opts = {
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "quiet": True,
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "cookiefile": cookie,
                    "extractor_args": {
                        "youtube": {
                            "player_client": ["android", "ios"],
                            "player_skip": ["webpage", "configs"],
                            "skip": ["dash", "hls"],
                        }
                    },
                    "http_headers": {
                        "User-Agent": agent,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                    },
                    "format": fmt,
                }
                
                try:
                    def _dl(_opts=ydl_opts, _url=url):
                        with yt_dlp.YoutubeDL(_opts) as ydl:
                            ydl.download([_url])

                    await asyncio.wait_for(asyncio.to_thread(_dl), timeout=70)
                    if os.path.exists(filename):
                        return filename
                except Exception as e:
                    err = str(e).lower()
                    if "403" in err:
                        logger.warning("403 hatası, bu yöntem atlanıyor...")
                        break 
                    if "sign in to confirm" in err:
                        if cookie and cookie in self.cookies:
                            logger.error(f"Geçersiz çerez: {os.path.basename(cookie)}")
                            try:
                                self.cookies.remove(cookie)
                                os.remove(cookie)
                            except: pass
                        break
                    continue
        return None



