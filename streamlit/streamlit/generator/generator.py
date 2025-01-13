"""
This file is managing about generator
"""

from openai import OpenAI, AzureOpenAI
from typing import List, Dict, Generator
from utils.models import APIConfig, ModelDetail


class BaseGenerator:
    """Base class for handling model generation."""

    def __init__(self, model_name: str, client):
        self.model_name = model_name
        self.client = client

    def gen(self, message_list: List[Dict[str, str]], **kwargs) -> Generator:
        """
        Generates streaming responses from the model.

        Args:
            message_list (List[Dict[str, str]]): List of messages.
            kwargs: Additional parameters for the API.

        Yields:
            Dict: Partial responses from the model.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=message_list,
                stream=True,
                **kwargs,
            )
            for response in completion:
                yield response
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}")


class OpenAIGenerator(BaseGenerator):
    def __init__(self, openai_config: APIConfig):
        super().__init__(openai_config.model_name, OpenAI(
            base_url=openai_config.base_url,
            api_key=openai_config.api_key.get_secret_value(),
        ))


class AzureGenerator(BaseGenerator):
    def __init__(self, azure_openai_config: APIConfig):
        super().__init__(azure_openai_config.model_name, AzureOpenAI(
            azure_endpoint=azure_openai_config.base_url,
            api_key=azure_openai_config.api_key.get_secret_value(),
            api_version=azure_openai_config.api_version,
        ))


def get_generator(model_config: ModelDetail) -> BaseGenerator:
    """Factory method for selecting a generator based on model configuration."""
    generators = {
        "azure": AzureGenerator,
        "openai": OpenAIGenerator,
    }
    if model_config.api_type not in generators:
        raise ValueError(f"Unsupported API type: {model_config.api_type}")
    return generators[model_config.api_type](model_config.api_config)
