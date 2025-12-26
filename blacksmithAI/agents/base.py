from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import json

load_dotenv()

#load configuration
config = json.load(open("./config.json", "r"))

# select provider and model
default_provider = config['defaults']['provider']

base_url = config['provider'][f'{default_provider}']['base_url'] or 'https://openrouter.ai/api/v1' # default openrouter
default_model = config['provider'][f'{default_provider}']['default_model'] or "mistralai/devstral-2512"
context_size = config['provider'][f'{default_provider}']['default_model_config']['context_size'] or 200000
max_retries = config['provider'][f'{default_provider}']['default_model_config']['max_retries'] or 3
stream_usage = config['provider'][f'{default_provider}']['default_model_config']['stream_usage'] or True
max_tokens = config['provider'][f'{default_provider}']['default_model_config']['max_tokens'] or None
embedding_model = config['provider'][f'{default_provider}']['default_embedding_model'] or "openai/text-embedding-3-small"

# api key
key = f'{default_provider.upper()}_API_KEY'
api_key = os.getenv(key, "") # get key from env

class init_model():
    
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
    
    
