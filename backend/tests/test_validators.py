"""Unit tests for validator modules."""

import pytest
from app.validators.audio_validator import (
    validate_audio_file,
    check_file_format,
    verify_file_size,
    validate_path
)
from app.validators.format_validator import (
    is_valid_format,
    validate_sample_rate,
    validate_bitrate
)
from app.validators.parameter_validator import (
    validate_conversion_params,
    validate_mastering_params
)

class TestAudioValidator:
    def test_validate_path_valid(self, tmp_path):
        f = tmp_path / "exist.txt"
        f.touch()
        valid, err = validate_path(str(f))
        assert valid is True
        assert err is None

    def test_validate_path_invalid(self):
        valid, err = validate_path("non_existent_file.xyz")
        assert valid is False
        assert "does not exist" in err

    def test_check_file_format_valid(self):
        valid, err = check_file_format("song.mp3")
        assert valid is True
        
        valid, err = check_file_format("song.WAV")
        assert valid is True

    def test_check_file_format_invalid(self):
        valid, err = check_file_format("image.jpg")
        assert valid is False
        assert "Unsupported file format" in err

    def test_verify_file_size(self, tmp_path):
        f = tmp_path / "small.mp3"
        f.write_bytes(b"0" * 1024)  # 1KB
        
        valid, err = verify_file_size(f, max_size_mb=1)
        assert valid is True

class TestFormatValidator:
    def test_is_valid_format(self):
        assert is_valid_format("mp3") is True
        assert is_valid_format(".wav") is True
        assert is_valid_format("xyz") is False

    def test_validate_sample_rate(self):
        assert validate_sample_rate(44100)[0] is True
        assert validate_sample_rate(48000)[0] is True
        assert validate_sample_rate(12345)[0] is False

    def test_validate_bitrate(self):
        assert validate_bitrate("128k")[0] is True
        assert validate_bitrate("320k")[0] is True
        assert validate_bitrate("500k")[0] is False
        assert validate_bitrate("abc")[0] is False

class TestParameterValidator:
    def test_validate_conversion_params_valid(self):
        params = {"format": "mp3", "bitrate": "192k"}
        valid, err = validate_conversion_params(params)
        assert valid is True

    def test_validate_conversion_params_missing_format(self):
        params = {"bitrate": "192k"}
        valid, err = validate_conversion_params(params)
        assert valid is False
        assert "Missing required parameter" in err

    def test_validate_mastering_params_valid(self):
        params = {"preset": "music", "target_lufs": -14.0}
        valid, err = validate_conversion_params(params)
        # Note: This calls conversion params in original code? No, separate func.
        # Let's call the right one
        valid, err = validate_mastering_params(params)
        assert valid is True

    def test_validate_mastering_params_invalid_preset(self):
        params = {"preset": "invalid"}
        valid, err = validate_mastering_params(params)
        assert valid is False
        assert "Invalid preset" in err
