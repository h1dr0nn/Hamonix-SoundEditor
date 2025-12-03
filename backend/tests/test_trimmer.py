"""Unit tests for the trimmer module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.handler.trimmer import (
    SilenceTrimmer,
    TrimRequest,
    TrimResult
)

class TestTrimmer:
    @pytest.fixture
    def mock_pydub(self):
        with patch("app.handler.trimmer.AudioSegment") as mock:
            yield mock

    @pytest.fixture
    def mock_silence(self):
        with patch("app.handler.trimmer.silence") as mock:
            yield mock

    def test_trim_request_outputs(self, tmp_path):
        input_file = tmp_path / "speech.wav"
        input_file.touch()
        output_dir = tmp_path / "trimmed"
        
        req = TrimRequest(
            input_paths=[input_file],
            output_directory=output_dir
        )
        
        outputs = list(req.outputs())
        assert len(outputs) == 1
        src, dst = outputs[0]
        assert dst.name == "speech.wav"

    def test_process_success(self, tmp_path, mock_pydub, mock_silence):
        input_file = tmp_path / "speech.wav"
        input_file.touch()
        output_dir = tmp_path / "trimmed"
        
        req = TrimRequest(
            input_paths=[input_file],
            output_directory=output_dir
        )
        
        # Mock audio and silence detection
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 10000
        mock_pydub.from_file.return_value = mock_audio
        
        # Mock detect_nonsilent returning start and end
        mock_silence.detect_nonsilent.return_value = [[1000, 9000]]
        
        # Mock slicing
        mock_audio.__getitem__.return_value = mock_audio
        
        with patch("app.handler.trimmer.validate_pydub_available"), \
             patch("app.handler.trimmer.resolve_environment"):
            
            result = SilenceTrimmer.process(req)
            
            assert result.success is True
            assert len(result.outputs) == 1
            mock_audio.export.assert_called_once()

    def test_no_silence_detected(self, tmp_path, mock_pydub, mock_silence):
        input_file = tmp_path / "speech.wav"
        input_file.touch()
        output_dir = tmp_path / "trimmed"
        
        req = TrimRequest(
            input_paths=[input_file],
            output_directory=output_dir
        )
        
        mock_audio = MagicMock()
        mock_pydub.from_file.return_value = mock_audio
        mock_silence.detect_nonsilent.return_value = []
        
        with patch("app.handler.trimmer.validate_pydub_available"), \
             patch("app.handler.trimmer.resolve_environment"):
            
            result = SilenceTrimmer.process(req)
            
            assert result.success is True
            # Should export original audio
            mock_audio.export.assert_called_once()
