import os
from pyrogram import Client


api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")
download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")
app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

data = []

if not download_dir.endswith("/"):
  download_dir = str(download_dir) + "/"
if not os.path.isdir(download_dir):
  os.makedirs(download_dir)
