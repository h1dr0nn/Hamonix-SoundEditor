"""Unit tests for the mastering module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.handler.mastering import (
    MasteringEngine,
    MasteringRequest,
    MasteringParameters,
    MasteringResult
)

class TestMastering:
    @pytest.fixture
    def mock_pydub(self):
        with patch("app.handler.mastering.AudioSegment") as mock:
            yield mock

    @pytest.fixture
    def mock_effects(self):
        with patch("app.handler.mastering.effects") as mock:
            yield mock

    def test_mastering_request_outputs(self, tmp_path):
        input_file = tmp_path / "song.wav"
        input_file.touch()
        output_dir = tmp_path / "mastered"
        
        req = MasteringRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            preset="Music",
            parameters=MasteringParameters()
        )
        
        outputs = list(req.outputs())
        assert len(outputs) == 1
        src, dst = outputs[0]
        assert dst.name == "song_mastered.wav"

    def test_process_success(self, tmp_path, mock_pydub, mock_effects):
        input_file = tmp_path / "song.wav"
        input_file.touch()
        output_dir = tmp_path / "mastered"
        
        req = MasteringRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            preset="Music",
            parameters=MasteringParameters()
        )
        
        # Mock audio segment
        mock_audio = MagicMock()
        mock_audio.dBFS = -20.0
        mock_audio.max_dBFS = -6.0
        mock_pydub.from_file.return_value = mock_audio
        mock_effects.compress_dynamic_range.return_value = mock_audio
        mock_audio.apply_gain.return_value = mock_audio
        
        with patch("app.handler.mastering.validate_pydub_available"), \
             patch("app.handler.mastering.resolve_environment"):
            
            result = MasteringEngine.process(req)
            
            assert result.success is True
            assert len(result.outputs) == 1
            mock_audio.export.assert_called_once()

    def test_process_failure(self, tmp_path, mock_pydub):
        input_file = tmp_path / "song.wav"
        input_file.touch()
        output_dir = tmp_path / "mastered"
        
        req = MasteringRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            preset="Music",
            parameters=MasteringParameters()
        )
        
        mock_pydub.from_file.side_effect = Exception("Corrupt file")
        
        with patch("app.handler.mastering.validate_pydub_available"), \
             patch("app.handler.mastering.resolve_environment"):
            
            result = MasteringEngine.process(req)
            
            assert result.success is False
            assert "Corrupt file" in result.message
