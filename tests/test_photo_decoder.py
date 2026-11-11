import base64
import os
import tempfile
from pathlib import Path

import pytest

from multicook_agent.photo_decoder import SelectionMode, image_to_data_url


class TestSelectionMode:
    def test_single_value(self):
        assert SelectionMode.SINGLE.value == "single"

    def test_multi_value(self):
        assert SelectionMode.MULTI.value == "multi"


class TestImageToDataUrl:
    def test_valid_image_returns_data_url(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="))
            tmp_path = f.name
        try:
            result = image_to_data_url(Path(tmp_path))
            assert result.startswith("data:image/png;base64,")
            decoded = base64.b64decode(result.split(",")[1])
            assert decoded == base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
        finally:
            os.unlink(tmp_path)

    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            image_to_data_url(Path("/nonexistent/path/to/image.png"))

    def test_non_image_file_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"not an image")
            tmp_path = f.name
        try:
            with pytest.raises(ValueError):
                image_to_data_url(Path(tmp_path))
        finally:
            os.unlink(tmp_path)
