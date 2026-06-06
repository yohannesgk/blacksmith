from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import json
import sys
from typing import Optional, Dict, Any

class ConfigManager:
    """Manages configuration loading and validation for BlacksmithAI."""
    
    DEFAULT_CONFIG_PATH = "./config.json"
    
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
        self.validate_env()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            print(f"[bold red]Error:[/bold red] Configuration file '{self.config_path}' not found.")
            print("Please create a config.json file based on the provided example.")
            sys.exit(1)
            
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[bold red]Error:[/bold red] Failed to parse '{self.config_path}': {e}")
            sys.exit(1)

    def validate_env(self):
        load_dotenv()
        provider = self.get_default_provider()
        key_name = f"{provider.upper()}_API_KEY"
        if not os.getenv(key_name):
            print(f"[bold yellow]Warning:[/bold yellow] {key_name} is not set in environment variables.")

    def get_default_provider(self) -> str:
        return self.config.get("defaults", {}).get("provider", "openrouter")

    def get_provider_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        provider = provider or self.get_default_provider()
        return self.config.get("provider", {}).get(provider, {})

    def get_api_key(self, provider: Optional[str] = None) -> str:
        provider = provider or self.get_default_provider()
        return os.getenv(f"{provider.upper()}_API_KEY", "")

# Initialize global config manager
config_manager = ConfigManager()

# Select provider and model
default_provider = config_manager.get_default_provider()
provider_config = config_manager.get_provider_config(default_provider)

base_url = provider_config.get("base_url", "https://openrouter.ai/api/v1")
default_model = provider_config.get("default_model", "mistralai/devstral-2512")
model_config = provider_config.get("default_model_config", {})

context_size = model_config.get("context_size", 200000)
max_retries = model_config.get("max_retries", 3)
stream_usage = model_config.get("stream_usage", True)
max_tokens = model_config.get("max_tokens")
embedding_model = provider_config.get("default_embedding_model", "openai/text-embedding-3-small")

api_key = config_manager.get_api_key(default_provider)

class init_model:
    def __init__(self, reasoning_effort=None, temperature=0):
        self.model = ChatOpenAI(
            model=default_model,
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
            stream_usage=stream_usage,
            profile={"max_input_tokens": context_size},
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )

    def get_model(self):
        return self.model
    
class init_embedding_model():
    def __init__(self):
        self.model = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
        )

    def get_model(self):
        return self.model
