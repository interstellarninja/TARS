import os
from dotenv import load_dotenv
import argparse

class Config:
    def __init__(self, use_args=True, api=None, model=None):
        load_dotenv()

        # Optionally parse command-line arguments
        if use_args:
            parser = argparse.ArgumentParser(description='Run TARS with selected API and model')
            parser.add_argument('--api', choices=['azure', 'ollama'], default='ollama', help='Choose the API to use (default: ollama)')
            parser.add_argument('--model', type=str, help='Specify the model to use. If not provided, defaults will be used based on the API.')
            args = parser.parse_args()
            api = args.api
            model = args.model

        # AI Provider configuration
        self.AI_PROVIDER = api or 'ollama'

        if self.AI_PROVIDER == 'azure':
            self.AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
            self.AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
            self.AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
            self.AZURE_OPENAI_DEPLOYMENT = model if model else os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini')
        elif self.AI_PROVIDER == 'ollama':
            self.OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
            self.OLLAMA_MODEL = model if model else os.getenv('OLLAMA_MODEL', 'llama2')
        else:
            raise ValueError(f"Unknown AI provider: {self.AI_PROVIDER}")

        # Discord configuration
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

        # GitHub configuration
        self.GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
        self.REPO_NAME = os.getenv('GITHUB_REPO')

        # Logging configuration
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    def __str__(self):
        return f"""TARS Configuration:
        AI Provider: {self.AI_PROVIDER}
        Model: {self.AZURE_OPENAI_DEPLOYMENT if self.AI_PROVIDER == 'azure' else self.OLLAMA_MODEL}
        GitHub Repo: {self.REPO_NAME}
        Log Level: {self.LOG_LEVEL}
        """

def load_config(use_args=True, api=None, model=None):
    return Config(use_args=use_args, api=api, model=model)
