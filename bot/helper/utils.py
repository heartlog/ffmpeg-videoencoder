import os
import logging
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    if data:
        del data[0]
    if data:
        add_task(data[0])

def add_task(message: Message):
    msg = None
    filepath = None
    new_file = None
    thumb = None
    try:
        msg = message.reply_text("`Downloading video Baka wait for some time !!...`", quote=True)
        filepath = message.download(file_name=download_dir)
        if not filepath or not os.path.exists(filepath):
            if msg:
                msg.edit("`Failed to download video!`")
            return

        if msg:
            msg.edit("`Started encoding video...`")

        new_file = encode(filepath)
        if new_file and os.path.exists(new_file):
            if msg:
                msg.edit("`Video Encoded, getting metadata...`")
            duration = get_duration(new_file)
            thumb = get_thumbnail(new_file, download_dir, duration / 4 if duration else 0)
            width, height = get_width_height(new_file)
            if msg:
                msg.edit("`Started to process and upload...`")

            message.reply_video(
                video=new_file,
                quote=True,
                supports_streaming=True,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height
            )
            if msg:
                msg.edit("`Video Encoded to x265`")
        else:
            if msg:
                msg.edit("`Something went wrong while encoding your file. Make sure it is not already in HEVC format.`")
    except Exception as e:
        logging.error(f"Error processing task: {e}")
        if msg:
            try:
                msg.edit(f"`Error: {e}`")
            except Exception:
                pass
        else:
            try:
                message.reply_text(f"`Error: {e}`", quote=True)
            except Exception:
                pass
    finally:
        for file_path in (filepath, new_file, thumb):
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logging.warning(f"Could not remove temporary file {file_path}: {e}")
        on_task_complete()
