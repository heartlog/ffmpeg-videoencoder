import os
import shutil
import tempfile
import subprocess
from unittest.mock import MagicMock
import pytest

from bot import data
from bot.helper.utils import add_task, on_task_complete

@pytest.fixture
def temp_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)

@pytest.fixture
def sample_video(temp_dir):
    video_path = os.path.join(temp_dir, "test.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=1",
        "-c:v", "libx264", "-c:a", "aac",
        video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return video_path

def test_add_task_success(sample_video, temp_dir, monkeypatch):
    data.clear()
    monkeypatch.setattr("bot.helper.utils.download_dir", temp_dir)

    mock_msg = MagicMock()
    status_msg = MagicMock()
    mock_msg.reply_text.return_value = status_msg
    mock_msg.download.return_value = sample_video

    data.append(mock_msg)
    add_task(mock_msg)

    assert mock_msg.download.called
    assert mock_msg.reply_video.called
    assert len(data) == 0

def test_add_task_download_failed(temp_dir, monkeypatch):
    data.clear()
    monkeypatch.setattr("bot.helper.utils.download_dir", temp_dir)

    mock_msg = MagicMock()
    status_msg = MagicMock()
    mock_msg.reply_text.return_value = status_msg
    mock_msg.download.return_value = None

    data.append(mock_msg)
    add_task(mock_msg)

    status_msg.edit.assert_called_with("`Failed to download video!`")
    assert len(data) == 0
