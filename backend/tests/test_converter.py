"""Unit tests for the converter module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.handler.converter import (
    SoundConverter,
    ConversionRequest,
    ConversionResult,
    ConversionProgress
)

class TestConverter:
    @pytest.fixture
    def mock_ffmpeg(self):
        with patch("app.handler.converter._run_ffmpeg_conversion") as mock:
            yield mock

    @pytest.fixture
    def mock_resolve(self):
        with patch("app.handler.converter._resolve_converter_path") as mock:
            mock.return_value = Path("/usr/bin/ffmpeg")
            yield mock

    def test_conversion_request_outputs(self, tmp_path):
        input_file = tmp_path / "test.wav"
        input_file.touch()
        output_dir = tmp_path / "out"
        
        req = ConversionRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            output_format="mp3"
        )
        
        outputs = list(req.outputs())
        assert len(outputs) == 1
        src, dst = outputs[0]
        assert src == input_file
        assert dst == output_dir / "test.mp3"

    def test_conversion_request_no_overwrite(self, tmp_path):
        input_file = tmp_path / "test.wav"
        input_file.touch()
        output_dir = tmp_path / "out"
        output_dir.mkdir()
        
        # Create existing file
        (output_dir / "test.mp3").touch()
        
        req = ConversionRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            output_format="mp3",
            overwrite_existing=False
        )
        
        outputs = list(req.outputs())
        src, dst = outputs[0]
        assert dst.name == "test (1).mp3"

    def test_convert_success(self, tmp_path, mock_ffmpeg, mock_resolve):
        input_file = tmp_path / "test.wav"
        input_file.touch()
        output_dir = tmp_path / "out"
        
        req = ConversionRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            output_format="mp3"
        )
        
        # Mock validation to avoid pydub check
        with patch("app.handler.converter.validate_pydub_available"), \
             patch("app.handler.converter.resolve_environment"):
            
            result = SoundConverter.convert(req)
            
            assert result.success is True
            assert len(result.outputs) == 1
            assert mock_ffmpeg.call_count == 1

    def test_convert_failure(self, tmp_path, mock_ffmpeg, mock_resolve):
        input_file = tmp_path / "test.wav"
        input_file.touch()
        output_dir = tmp_path / "out"
        
        req = ConversionRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            output_format="mp3"
        )
        
        mock_ffmpeg.side_effect = RuntimeError("FFmpeg failed")
        
        with patch("app.handler.converter.validate_pydub_available"), \
             patch("app.handler.converter.resolve_environment"):
            
            result = SoundConverter.convert(req)
            
            assert result.success is False
            assert "FFmpeg failed" in result.message
