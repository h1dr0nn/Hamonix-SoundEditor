"""Unit tests for the modifier module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.handler.modifier import (
    ModificationRequest,
    process,
    build_filter_complex
)

class TestModifier:
    @pytest.fixture
    def mock_subprocess(self):
        with patch("app.handler.modifier.subprocess") as mock:
            yield mock

    def test_modification_request_outputs(self, tmp_path):
        input_file = tmp_path / "music.mp3"
        input_file.touch()
        output_dir = tmp_path / "modified"
        
        req = ModificationRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            speed=1.5,
            pitch=2,
            cut_start=0,
            cut_end=100
        )
        
        outputs = list(req.outputs())
        assert len(outputs) == 1
        src, dst = outputs[0]
        assert dst.name == "music_modified.wav"

    def test_build_filter_complex(self):
        # Test speed only
        f1 = build_filter_complex(speed=1.5, pitch=0, sample_rate=44100)
        assert "atempo=1.5" in f1
        
        # Test pitch only
        f2 = build_filter_complex(speed=1.0, pitch=12, sample_rate=44100)
        assert "asetrate=88200" in f2
        assert "atempo=0.5" in f2
        
        # Test both
        f3 = build_filter_complex(speed=2.0, pitch=12, sample_rate=44100)
        assert "asetrate=88200" in f3
        # Pitch +12 -> ratio 2.0 -> tempo correction 0.5
        # Speed 2.0 -> tempo 2.0
        # Combined might vary in implementation order, but should contain both logic
        assert "atempo" in f3

    def test_process_success(self, tmp_path, mock_subprocess):
        input_file = tmp_path / "music.mp3"
        input_file.touch()
        output_dir = tmp_path / "modified"
        
        req = ModificationRequest(
            input_paths=[input_file],
            output_directory=output_dir,
            speed=1.0,
            pitch=0,
            cut_start=10,
            cut_end=90
        )
        
        # Mock ffprobe output
        mock_subprocess.check_output.return_value = b'{"streams": [{"duration": "100.0", "sample_rate": "44100"}]}'
        
        with patch("app.handler.modifier.resolve_environment"), \
             patch("app.handler.modifier.validate_input_paths"):
            
            outputs = process(req)
            
            assert len(outputs) == 1
            assert mock_subprocess.run.call_count == 1
            
            # Verify cut args
            args = mock_subprocess.run.call_args[0][0]
            assert "-ss" in args
            assert "10.0" in args # 10% of 100s
            assert "-to" in args
            assert "90.0" in args # 90% of 100s
