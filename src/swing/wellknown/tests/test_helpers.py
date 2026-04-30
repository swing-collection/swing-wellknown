# -*- coding: utf-8 -*-

"""
Tests for JSON helper functions.
"""

import json
from pathlib import Path

import pytest

from swing_text.helpers.helper_json import read_file, read_json, write_file, write_json


class TestReadFile:
    """Tests for read_file function."""

    def test_read_file_success(self, tmp_path: Path) -> None:
        """Test reading a file successfully."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        result = read_file(test_file)

        assert result == "Hello, World!"

    def test_read_file_with_string_path(self, tmp_path: Path) -> None:
        """Test reading a file with string path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        result = read_file(str(test_file))

        assert result == "Test content"

    def test_read_file_not_found(self, tmp_path: Path) -> None:
        """Test FileNotFoundError when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read_file(tmp_path / "nonexistent.txt")


class TestReadJson:
    """Tests for read_json function."""

    def test_read_json_success(self, tmp_path: Path) -> None:
        """Test reading valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = read_json(test_file)

        assert result == test_data

    def test_read_json_with_nested_data(self, tmp_path: Path) -> None:
        """Test reading JSON with nested structures."""
        test_file = tmp_path / "nested.json"
        test_data = {
            "brand": {
                "name": {"short": "Test", "long": "Test Company"},
                "contact": {"email": "test@example.com"},
            }
        }
        test_file.write_text(json.dumps(test_data))

        result = read_json(test_file)

        assert result["brand"]["name"]["short"] == "Test"
        assert result["brand"]["contact"]["email"] == "test@example.com"

    def test_read_json_invalid(self, tmp_path: Path) -> None:
        """Test JSONDecodeError for invalid JSON."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("not valid json {")

        with pytest.raises(json.JSONDecodeError):
            read_json(test_file)


class TestWriteFile:
    """Tests for write_file function."""

    def test_write_file_success(self, tmp_path: Path) -> None:
        """Test writing content to a file."""
        test_file = tmp_path / "output.txt"

        result = write_file(test_file, "Test content")

        assert result == "Test content"
        assert test_file.read_text() == "Test content"

    def test_write_file_overwrites(self, tmp_path: Path) -> None:
        """Test that write_file overwrites existing content."""
        test_file = tmp_path / "output.txt"
        test_file.write_text("Old content")

        write_file(test_file, "New content")

        assert test_file.read_text() == "New content"


class TestWriteJson:
    """Tests for write_json function."""

    def test_write_json_success(self, tmp_path: Path) -> None:
        """Test writing JSON data to a file."""
        test_file = tmp_path / "output.json"
        test_data = {"key": "value", "list": [1, 2, 3]}

        write_json(test_file, test_data)

        written_content = test_file.read_text()
        assert json.loads(written_content) == test_data

    def test_write_json_formatted(self, tmp_path: Path) -> None:
        """Test that JSON is written with indentation."""
        test_file = tmp_path / "formatted.json"
        test_data = {"key": "value"}

        write_json(test_file, test_data)

        written_content = test_file.read_text()
        assert "  " in written_content  # Indentation present
