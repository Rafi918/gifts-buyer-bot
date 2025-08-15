# logger.py
import logging
import logging.handlers
import os
import sys

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

os.makedirs("logs", exist_ok=True)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
formatter = logging.Formatter(LOG_FORMAT)


console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[console], force=True)

bot_file = logging.handlers.RotatingFileHandler(
    "logs/bot.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
bot_file.setLevel(logging.INFO)
bot_file.setFormatter(formatter)

worker_file = logging.handlers.RotatingFileHandler(
    "logs/gift_worker.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
worker_file.setLevel(logging.INFO)
worker_file.setFormatter(formatter)


logger = logging.getLogger("gifts-buyer-bot")
logger.addHandler(bot_file)

worker_logger = logging.getLogger("gift_worker")
worker_logger.addHandler(worker_file)
