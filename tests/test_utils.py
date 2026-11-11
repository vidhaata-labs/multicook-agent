import pytest

from multicook_agent.utils import extract_text_content


class TestExtractTextContent:
    def test_string_input(self):
        assert extract_text_content("hello world") == "hello world"

    def test_empty_string(self):
        assert extract_text_content("") == ""

    def test_list_of_dict_blocks(self):
        content = [
            {"type": "text", "text": "Hello "},
            {"type": "text", "text": "world"},
        ]
        assert extract_text_content(content) == "Hello world"

    def test_list_of_dict_blocks_with_content_key(self):
        content = [
            {"type": "text", "content": "foo"},
            {"type": "image_url", "image_url": {"url": "data:..."}},
        ]
        assert extract_text_content(content) == "foo"

    def test_list_of_string_blocks(self):
        content = ["Hello ", "world"]
        assert extract_text_content(content) == "Hello world"

    def test_mixed_blocks(self):
        content = ["Hello ", {"type": "text", "text": "world"}, "!"]
        assert extract_text_content(content) == "Hello world!"

    def test_empty_list(self):
        assert extract_text_content([]) == ""

    def test_dict_without_text(self):
        content = [{"type": "image_url", "image_url": {"url": "data:..."}}]
        assert extract_text_content(content) == ""
