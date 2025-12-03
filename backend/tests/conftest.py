"""Pytest configuration and fixtures."""

import pytest
import os
import shutil
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def test_files_dir(tmp_path_factory):
    """Create a temporary directory for test files."""
    d = tmp_path_factory.mktemp("audio_files")
    return d

@pytest.fixture
def mock_mp3_file(test_files_dir):
    """Create a dummy MP3 file."""
    p = test_files_dir / "test.mp3"
    p.write_bytes(b"ID3" + b"\x00" * 100)  # Fake header
    return p

@pytest.fixture
def mock_wav_file(test_files_dir):
    """Create a dummy WAV file."""
    p = test_files_dir / "test.wav"
    p.write_bytes(b"RIFF" + b"\x00" * 36 + b"WAVEfmt ")
    return p

@pytest.fixture
def mock_text_file(test_files_dir):
    """Create a dummy text file (invalid audio)."""
    p = test_files_dir / "test.txt"
    p.write_text("This is not audio")
    return p
