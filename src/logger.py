import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("gifts-buyer-bot")
bot_file_handler = logging.FileHandler("logs/bot.log")
bot_file_handler.setLevel(logging.INFO)
bot_file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
logger.addHandler(bot_file_handler)


worker_logger = logging.getLogger("gift_worker")
worker_logger.setLevel(logging.INFO)

worker_file_handler = logging.FileHandler("logs/gift_worker.log")
worker_file_handler.setLevel(logging.INFO)
worker_file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
worker_logger.addHandler(worker_file_handler)
