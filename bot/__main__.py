from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ForceReply, \
    InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from bot import app, data
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
    message.reply_text(f"Hi {message.from_user.mention()}\nIts bot to encode video to ffmpeg encode..\nJust send me video I will do the rest...\nThe bot is developed by @diablo_13N\n",
                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Clone this bot for free !",
                                                                                  url="https://github.com/royal78/ffmpeg-cov")],
                                                          [InlineKeyboardButton("My developer",
                                                                                url="t.me/diablo_13N")],
                                                          [InlineKeyboardButton("Github page",
                                                                                url="https://github.com/royal78/ffmpeg-cov")],
                                                          [InlineKeyboardButton("Join channel for updates",
                                                                                url="https://t.me/baka_no_onii")],
                                                          [InlineKeyboardButton("Join group",
                                                                                url="https://t.me/anim_chatx")]]))

@app.on_message(filters.incoming & (filters.video | filters.document))
def encode_video(app, message):
    if message.document:
      if not message.document.mime_type in video_mimetype:
        message.reply_text("```Invalid Video !\nMake sure its a valid video file.```", quote=True)
        return
    message.reply_text("```Added to queue !\n Wait for some time.```", quote=True)
    data.append(message)
    if len(data) == 1:
      add_task(message)

app.run()
