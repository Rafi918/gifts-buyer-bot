import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID", 0)
    CHECK_GIFT_INTERVAL = int(os.getenv("CHECK_GIFT_INTERVAL", 0))


config = Config()
