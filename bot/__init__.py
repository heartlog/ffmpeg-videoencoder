import os
import logging
from dotenv import load_dotenv
from pyrogram import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

load_dotenv()

raw_api_id = os.environ.get("API_ID") or os.environ.get("api_id")
api_id = int(raw_api_id) if raw_api_id and raw_api_id.isdigit() else None
api_hash = os.environ.get("API_HASH") or os.environ.get("api_hash")
bot_token = os.environ.get("BOT_TOKEN") or os.environ.get("bot_token")
download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")

data = []

if not download_dir.endswith("/"):
    download_dir = str(download_dir) + "/"
if not os.path.isdir(download_dir):
    os.makedirs(download_dir)

if api_id and api_hash and bot_token:
    app = Client("ffmpeg_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
else:
    app = None
