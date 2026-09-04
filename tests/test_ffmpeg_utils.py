import os
import shutil
import tempfile
import subprocess
import pytest
from bot.helper.ffmpeg_utils import (
    get_codec,
    encode,
    get_thumbnail,
    get_duration,
    get_width_height,
)

@pytest.fixture
def temp_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)

@pytest.fixture
def sample_h264_video(temp_dir):
    video_path = os.path.join(temp_dir, "sample_h264.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=2:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=2",
        "-c:v", "libx264", "-c:a", "aac",
        video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return video_path

@pytest.fixture
def sample_hevc_video(temp_dir):
    video_path = os.path.join(temp_dir, "sample_hevc.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=2:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=2",
        "-c:v", "libx265", "-tag:v", "hvc1", "-c:a", "aac",
        video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return video_path

def test_get_codec(sample_h264_video):
    v_codec = get_codec(sample_h264_video, channel="v:0")
    assert len(v_codec) >= 1
    assert "h264" in v_codec[0].lower()

    a_codec = get_codec(sample_h264_video, channel="a:0")
    assert len(a_codec) >= 1
    assert "aac" in a_codec[0].lower()

def test_get_duration_and_resolution(sample_h264_video):
    duration = get_duration(sample_h264_video)
    assert duration in (1, 2)

    width, height = get_width_height(sample_h264_video)
    assert width == 320
    assert height == 240

def test_get_thumbnail(sample_h264_video, temp_dir):
    thumb = get_thumbnail(sample_h264_video, temp_dir, ttl=1.0)
    assert thumb is not None
    assert os.path.isfile(thumb)
    assert os.path.getsize(thumb) > 0

def test_encode_h264_to_hevc(sample_h264_video):
    original_path = sample_h264_video
    encoded_file = encode(original_path)
    assert encoded_file is not None
    assert os.path.isfile(encoded_file)
    assert not os.path.exists(original_path)

    v_codec = get_codec(encoded_file, channel="v:0")
    assert "hevc" in v_codec[0].lower()

def test_encode_already_hevc(sample_hevc_video):
    encoded_file = encode(sample_hevc_video)
    assert encoded_file is None
    assert os.path.isfile(sample_hevc_video)

def test_encode_non_existent():
    result = encode("non_existent_file.mp4")
    assert result is None
