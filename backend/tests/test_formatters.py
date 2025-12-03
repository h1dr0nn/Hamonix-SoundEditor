"""Unit tests for the formatters module."""

import pytest
from pathlib import Path
from app.formatters.output_formatter import (
    format_success,
    format_error,
    format_progress,
    format_analysis_result
)
from app.formatters.path_formatter import (
    sanitize_filename,
    ensure_unique_path
)

class TestOutputFormatter:
    def test_format_success(self):
        data = {"file": "test.mp3"}
        result = format_success("convert", data, "Done")
        assert result["status"] == "success"
        assert result["operation"] == "convert"
        assert result["data"] == data
        assert result["message"] == "Done"

    def test_format_error(self):
        result = format_error("convert", "Something went wrong", error_code="500")
        assert result["status"] == "error"
        assert result["operation"] == "convert"
        assert result["error"]["message"] == "Something went wrong"
        assert result["error"]["code"] == "500"

    def test_format_progress(self):
        result = format_progress("convert", percent=50.0, current_file="test.mp3")
        assert result["status"] == "progress"
        assert result["operation"] == "convert"
        assert result["progress"]["percent"] == 50.0
        assert result["progress"]["file"] == "test.mp3"

class TestPathFormatter:
    def test_sanitize_filename(self):
        assert sanitize_filename("test/file.mp3") == "test_file.mp3" # sanitize replaces / with _
        assert sanitize_filename("Invalid:Name?.wav") == "Invalid_Name_.wav"
        
    def test_ensure_unique_path(self, tmp_path):
        # Create a file
        p1 = tmp_path / "test.txt"
        p1.touch()
        
        # Request same path
        p2 = ensure_unique_path(tmp_path / "test.txt")
        assert p2.name == "test_1.txt"
        
        # Create that one too
        p2.touch()
        p3 = ensure_unique_path(tmp_path / "test.txt")
        assert p3.name == "test_2.txt"
