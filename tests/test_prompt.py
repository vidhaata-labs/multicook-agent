import pytest

from multicook_agent.prompt import SYSTEM_CHEF_PROMPT, USER_CHEF_PROMPT


class TestPrompt:
    def test_system_chef_prompt_is_non_empty(self):
        assert isinstance(SYSTEM_CHEF_PROMPT, str)
        assert len(SYSTEM_CHEF_PROMPT) > 0

    def test_user_chef_prompt_is_non_empty(self):
        assert isinstance(USER_CHEF_PROMPT, str)
        assert len(USER_CHEF_PROMPT) > 0

    def test_system_mentions_chef(self):
        assert "chef" in SYSTEM_CHEF_PROMPT.lower()

    def test_user_mentions_recipe(self):
        assert "recipe" in USER_CHEF_PROMPT.lower()
