import os
import time
import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import logging


def get_codec(filepath, channel="v:0"):
    try:
        output = check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                channel,
                "-show_entries",
                "stream=codec_name,codec_tag_string",
                "-of",
                "default=nokey=1:noprint_wrappers=1",
                filepath,
            ]
        )
        return output.decode("utf-8").split()
    except Exception as e:
        logging.error(f"Error getting codec for {filepath} ({channel}): {e}")
        return []


def encode(filepath):
    if not filepath or not os.path.isfile(filepath):
        logging.error(f"Input file does not exist: {filepath}")
        return None

    basefilepath = os.path.splitext(filepath)[0]
    output_filepath = basefilepath + ".HEVC" + ".mp4"
    if output_filepath == filepath:
        output_filepath = basefilepath + "_encoded.HEVC.mp4"

    if os.path.isfile(output_filepath):
        logging.info(f'Skipping "{output_filepath}": file already exists')
        return None

    logging.info(f"Encoding file: {filepath}")
    video_codec = get_codec(filepath, channel="v:0")
    if not video_codec:
        logging.info("Skipping: no video codec reported")
        return None

    codec_name = video_codec[0].lower() if len(video_codec) > 0 else ""
    codec_tag = video_codec[1].lower() if len(video_codec) > 1 else ""

    if codec_name == "hevc":
        if codec_tag == "hvc1":
            logging.info("Skipping: already h265 / hvc1")
            return None
        else:
            video_opts = "-c:v copy -tag:v hvc1"
    else:
        video_opts = "-c:v libx265 -crf 28 -tag:v hvc1 -preset fast -threads 8"

    audio_codec = get_codec(filepath, channel="a:0")
    if not audio_codec:
        audio_opts = ""
    elif audio_codec[0].lower() == "aac":
        audio_opts = "-c:a copy"
    else:
        audio_opts = "-c:a aac -b:a 128k"

    cmd = ["ffmpeg", "-y", "-i", filepath]
    if video_opts:
        cmd.extend(video_opts.split())
    if audio_opts:
        cmd.extend(audio_opts.split())
    cmd.append(output_filepath)

    res = call(cmd)
    if res == 0 and os.path.isfile(output_filepath) and os.path.getsize(output_filepath) > 0:
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logging.warning(f"Could not remove original file {filepath}: {e}")
        return output_filepath
    else:
        logging.error(f"FFmpeg encoding failed with return code {res}")
        if os.path.isfile(output_filepath):
            try:
                os.remove(output_filepath)
            except Exception as e:
                logging.warning(f"Could not remove failed output file {output_filepath}: {e}")
        return None


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, f"thumb_{time.time()}.jpg")
    try:
        ss_val = max(0.0, float(ttl)) if ttl is not None else 0.0
        (
            ffmpeg.input(in_filename, ss=ss_val)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        if os.path.isfile(out_filename) and os.path.getsize(out_filename) > 0:
            return out_filename
        if os.path.isfile(out_filename):
            os.remove(out_filename)
        return None
    except Exception as e:
        logging.error(f"Error extracting thumbnail: {e}")
        if os.path.isfile(out_filename):
            try:
                os.remove(out_filename)
            except Exception:
                pass
        return None


def get_duration(filepath):
    try:
        parser = createParser(filepath)
        if parser:
            with parser:
                metadata = extractMetadata(parser)
                if metadata and metadata.has("duration"):
                    return int(metadata.get("duration").seconds)
    except Exception as e:
        logging.warning(f"hachoir failed to get duration: {e}")

    try:
        output = check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nokey=1:noprint_wrappers=1", filepath
        ])
        return int(float(output.decode("utf-8").strip()))
    except Exception as e:
        logging.error(f"ffprobe failed to get duration for {filepath}: {e}")
        return 0


def get_width_height(filepath):
    try:
        parser = createParser(filepath)
        if parser:
            with parser:
                metadata = extractMetadata(parser)
                if metadata and metadata.has("width") and metadata.has("height"):
                    return int(metadata.get("width")), int(metadata.get("height"))
    except Exception as e:
        logging.warning(f"hachoir failed to get resolution: {e}")

    try:
        output = check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0", filepath
        ])
        res = output.decode("utf-8").strip().split("x")
        if len(res) == 2:
            return int(res[0]), int(res[1])
    except Exception as e:
        logging.error(f"ffprobe failed to get resolution for {filepath}: {e}")

    return 1280, 720
