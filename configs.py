import os

class Config(object):
        api_id = int(os.environ.get("API_ID", "2176353"))
        api_hash = os.environ.get("API_HASH")
        bot_token = os.environ.get("BOT_TOKEN")
        download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")
        
