# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "31939892"))
        self.API_HASH = getenv("API_HASH", "a7f3a115764c8c6eebba8b3cfdccc022")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8441056561:AAFhSeSQ49OoXZiuipYD-J94xjgjISd4KS0")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://mongoguess:guessmongo@cluster0.zcwklzz.mongodb.net/?retryWrites=true&w=majority")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003639948579"))
        self.OWNER_ID = int(getenv("OWNER_ID", "8237345360"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "AQHnXTQAhgWqZPOW_ETenb8krJLsH5blQI0iWxMP1oHEyssbF2Qpr36XCjR69hj07OZWLnhr0bn-XEdZj2qBtDlCVR2MqXdLSCXj0kVae5cwc0mXXKp844J4OZWMIIcTL5pn46799RoSq4fg6miR8AojrOY6K3rVQnKA9i_FTq8KFe7Um8BFazoSJvoaYQ2B4kjWW_EUugIQ5MvGtiHO_DE3_60uiXuyA9q2FkCbVUlxOJb0T3rM2EZXJtaJkrPyd2es9qpOx8bM9quHVY1-xwvWws2TCYbJO7VzBHHSbuC2vM0Rg_5jNS3o24Ikc7kD1pawplOUStuKCYxTGq_2Bm8xB3N91QAAAAH00xWPAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/grupgirdap")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/grupgirdap")

        def parse_bool(key: str, default: bool) -> bool:
            val = getenv(key)
            if val is None:
                return default
            return str(val).lower() in ["true", "1", "yes"]

        self.AUTO_END: bool = parse_bool("AUTO_END", False)
        self.AUTO_LEAVE: bool = parse_bool("AUTO_LEAVE", False)
        self.VIDEO_PLAY: bool = parse_bool("VIDEO_PLAY", True)
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "https://batbin.me/sandbank").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB
        self.START_IMG = getenv("START_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
