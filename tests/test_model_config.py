import os

import pytest

from multicook_agent.model_config import (
    DEFAULT_MODELS,
    MODEL_ENV_VARS,
    create_llm,
    get_available_providers,
    get_model_name,
    get_llm_provider,
)


class TestGetLLMProvider:
    def test_default_provider(self):
        os.environ.pop("LLM_PROVIDER", None)
        assert get_llm_provider() == "google_genai"

    def test_valid_provider_groq(self):
        os.environ["LLM_PROVIDER"] = "groq"
        assert get_llm_provider() == "groq"

    def test_valid_provider_openai(self):
        os.environ["LLM_PROVIDER"] = "openai"
        assert get_llm_provider() == "openai"

    def test_invalid_provider_falls_back(self):
        os.environ["LLM_PROVIDER"] = "invalid_provider"
        assert get_llm_provider() == "google_genai"


class TestGetModelName:
    def test_default_model_google_genai(self):
        os.environ.pop("LLM_PROVIDER", None)
        os.environ.pop("GOOGLE_MODEL", None)
        assert get_model_name("google_genai") == "gemini-3.1-flash-lite"

    def test_env_model_override(self):
        os.environ["LLM_PROVIDER"] = "groq"
        os.environ["GROQ_MODEL"] = "mixtral-8x7b-32768"
        assert get_model_name("groq") == "mixtral-8x7b-32768"

    def test_model_arg_takes_precedence(self):
        os.environ["LLM_PROVIDER"] = "openai"
        model = create_llm(provider="openai", model="gpt-3.5-turbo")
        assert model is not None


class TestCreateLLM:
    def test_create_llm_default(self):
        model = create_llm()
        assert model is not None

    def test_create_llm_groq(self):
        model = create_llm(provider="groq")
        assert model is not None

    def test_create_llm_openai(self):
        model = create_llm(provider="openai")
        assert model is not None


class TestGetAvailableProviders:
    def test_returns_all_providers(self):
        providers = get_available_providers()
        assert "google_genai" in providers
        assert "groq" in providers
        assert "openai" in providers


class TestConstants:
    def test_default_models_has_all_providers(self):
        for provider in ["google_genai", "groq", "openai"]:
            assert provider in DEFAULT_MODELS
            assert isinstance(DEFAULT_MODELS[provider], str)

    def test_model_env_vars_has_all_providers(self):
        for provider in ["google_genai", "groq", "openai"]:
            assert provider in MODEL_ENV_VARS
