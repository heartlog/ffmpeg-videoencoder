import os
from pyrogram import Client
from dotenv import load_dotenv
from configs import Config


api_id = Config.api_id
api_hash = Config.api_hash
bot_token = Config.bot_token
download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")
sudo_users = "1771615392"
app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

data = []

if not download_dir.endswith("/"):
  download_dir = str(download_dir) + "/"
if not os.path.isdir(download_dir):
  os.makedirs(download_dir)
