import os
import json
from typing import Dict, Optional, Literal
from pydantic import BaseModel, SecretStr
from utils.models.health_checker import ModelHealthChecker


class APIConfig(BaseModel):
    """API Parameters for Model Access"""
    api_key: SecretStr
    base_url: str
    model_name: Optional[str] = None
    api_type: str
    api_version: str


class ModelDetail(BaseModel):
    """Language Model Details"""
    model_id: str
    title: str
    api_type: Literal["azure", "openai"] = "openai"
    api_config: APIConfig
    icon: Optional[str] = None


class ModelRegistry:
    """Registry for Managing Models"""

    def __init__(self):
        self.models: Dict[str, ModelDetail] = {}

    def register_model(self,
                       model_id: str,
                       parameters: APIConfig,
                       title: str,
                       api_type: str,
                       **kwargs,
                       ):
        self.models[model_id] = ModelDetail(
            model_id=model_id,
            api_config=parameters,
            title=title,
            api_type=api_type,
            **kwargs,
        )

    def get_model_config(self, model_id: str):
        return self.models[model_id]

    def get_model_dict(self) -> Dict[str, ModelDetail]:
        return self.models


class ModelRegistrar:
    """Handles model registration logic."""

    @staticmethod
    def register_models(registry: ModelRegistry, models: list):
        for model in models:
            registry.register_model(
                model_id=model["id"],
                parameters=APIConfig(
                    api_key=SecretStr(os.getenv(model["env_keys"].get("api_key", "DEFAULT_API_KEY"), "YOUR_API_KEY")),
                    base_url=os.getenv(model["env_keys"].get("base_url", "DEFAULT_BASE_URL"), "YOUR_BASE_URL"),
                    model_name=os.getenv(model["env_keys"].get("model_name", "DEFAULT_MODEL_NAME"), None),
                    api_type=os.getenv("OPENAI_API_TYPE", "azure"),
                    api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
                ),
                title=model["title"],
                api_type=model["api_type"] or "openai",
                icon=model["icon"] or "",
            )


class ModelManager:
    """Streamlit Application Configuration"""

    def __init__(self):
        self.model_registry = ModelRegistry()
        models_data = self._load_models_from_file("models_config.json")
        ModelRegistrar.register_models(self.model_registry, models_data)

    @staticmethod
    def _load_models_from_file(file_path: str) -> list:
        with open(file_path, "r") as file:
            return json.load(file)

    def get_model_details(self, model_id: str) -> ModelDetail:
        if model_id not in self.model_registry.get_model_dict():
            available_models = self.get_available_model_ids()
            raise ValueError(
                f"Model with ID '{model_id}' not found. Available model IDs: {available_models}"
            )
        return self.model_registry.get_model_config(model_id)

    def get_available_model_ids(self):
        """Returns a list of available model IDs."""
        return list(self.model_registry.get_model_dict().keys())

    def get_model_id_by_name(self, model_name: str):
        """  """
        for id, model_detail in self.model_registry.get_model_dict().items():
            if model_name == model_detail.title:
                return id
        raise ValueError(f"No match ID with name: {model_name}.")

    def health_check_all(self):
        """Performs a health check on all registered models"""
        for model_id in self.get_available_model_ids():
            if not ModelHealthChecker.check(self.get_model_details(model_id).base_url):
                raise RuntimeError(f"Health check failed for model {model_id}")
