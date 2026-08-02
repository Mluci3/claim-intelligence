import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def get_project_client() -> AIProjectClient:
    endpoint = os.environ["PROJECT_ENDPOINT"]
    return AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())


def get_model_deployment_name() -> str:
    return os.environ["AZURE_OPENAI_DEPLOYMENT_GPT"]
