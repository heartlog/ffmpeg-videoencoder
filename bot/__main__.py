from pyrogram import filters
from bot import app, data, sudo_users
from bot.helper.utils import add_task

video_mimetype = [
  "video/x-flv",
  "video/mp4",
  "application/x-mpegURL",
  "video/MP2T",
  "video/3gpp",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-ms-wmv",
  "video/x-matroska",
  "video/webm",
  "video/x-m4v",
  "video/quicktime",
  "video/mpeg"
  ]

@app.on_message(filters.incoming & filters.command(['start', 'help']))
def help_message(app, message):
    message.reply_text(f"Hi {message.from_user.mention()}\nIts bot to ensode video to ffmpeg encode..\nThe bot is developed by @diablo_13N\n"
