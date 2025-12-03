"""Unit tests for utility functions."""

import pytest
from app.utils.audio_utils import db_to_float, float_to_db, ms_to_samples
from app.utils.string_utils import slugify, format_duration

class TestAudioUtils:
    def test_db_to_float(self):
        assert db_to_float(0) == 1.0
        assert db_to_float(-6) == pytest.approx(0.5, rel=0.01)
        
    def test_float_to_db(self):
        assert float_to_db(1.0) == 0.0
        assert float_to_db(0.5) == pytest.approx(-6.02, rel=0.01)
        
    def test_ms_to_samples(self):
        assert ms_to_samples(1000, 44100) == 44100
        assert ms_to_samples(500, 48000) == 24000

class TestStringUtils:
    def test_slugify(self):
        assert slugify("Hello World") == "hello-world"
        assert slugify("Test_File.mp3") == "test-filemp3"
        assert slugify("Café") == "cafe"
        
    def test_format_duration(self):
        assert format_duration(65) == "01:05"
        assert format_duration(3665) == "01:01:05"
