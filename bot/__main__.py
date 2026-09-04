import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
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
    "video/mpeg"
]

video_extensions = (
    ".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv",
    ".wmv", ".m4v", ".3gp", ".ts", ".mpg", ".mpeg"
)

if app:
    @app.on_message(filters.incoming & filters.command(['start', 'help']))
    def help_message(client, message: Message):
        user_mention = message.from_user.mention() if message.from_user else "User"
        message.reply_text(
            f"Hi {user_mention}\nIts bot to encode video to ffmpeg encode..\nJust send me video I will do the rest...\nThe bot is developed by @diablo_13N\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Clone this bot for free !", url="https://github.com/royal78/ffmpeg-cov")],
                [InlineKeyboardButton("My developer", url="t.me/diablo_13N")],
                [InlineKeyboardButton("Github page", url="https://github.com/royal78/ffmpeg-cov")],
                [InlineKeyboardButton("Join channel for updates", url="https://t.me/baka_no_onii")],
                [InlineKeyboardButton("Join group", url="https://t.me/anim_chatx")]
            ])
        )

    @app.on_message(filters.incoming & (filters.video | filters.document))
    def encode_video(client, message: Message):
        if message.document:
            mime = message.document.mime_type or ""
            file_name = (message.document.file_name or "").lower()
            is_video_mime = mime in video_mimetype or mime.startswith("video/")
            is_video_ext = file_name.endswith(video_extensions)

            if not (is_video_mime or is_video_ext):
                message.reply_text("```Invalid Video !\nMake sure its a valid video file.```", quote=True)
                return

        message.reply_text("```Added to queue !\n Wait for some time.```", quote=True)
        data.append(message)
        if len(data) == 1:
            add_task(message)

if __name__ == "__main__":
    if app:
        app.run()
    else:
        print("Bot client initialized without credentials. Set API_ID, API_HASH, and BOT_TOKEN environment variables to run.")
