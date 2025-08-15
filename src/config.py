import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID", 0)
    CHECK_GIFT_INTERVAL = int(os.getenv("CHECK_GIFT_INTERVAL", 30))
    API_URL = os.getenv("API_URL", "https://gifts.vikiapi.xyz/")
    API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", 3))
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", 5))



config = Config()
