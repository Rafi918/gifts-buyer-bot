from pyrogram import Client
from config import config

user_bot = Client("user_bot", api_id=config.API_ID,
                  api_hash=config.API_HASH, workdir="sessions/user")
