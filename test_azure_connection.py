"""
Teste de conexao com Azure AI Foundry.

Antes de rodar:
1. No portal do Azure AI Foundry (ai.azure.com), abra seu projeto e copie o
   "Project endpoint" (algo como https://<recurso>.services.ai.azure.com/api/projects/<projeto>).
2. Defina a variavel de ambiente PROJECT_ENDPOINT com esse valor
   (no .env ou export PROJECT_ENDPOINT="...").
3. Autentique com `az login` (usa DefaultAzureCredential) ou configure
   AZURE_CLIENT_ID / AZURE_TENANT_ID / AZURE_CLIENT_SECRET para uma service principal.

Rodar com: python test_azure_connection.py
"""

import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    if not endpoint:
        print("Erro: defina a variavel de ambiente PROJECT_ENDPOINT.")
        sys.exit(1)

    print(f"Conectando ao projeto: {endpoint}")

    client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    print("\nConexoes configuradas no projeto:")
    for connection in client.connections.list():
        print(f"  - {connection.name} ({connection.type})")

    print("\nConexao com Azure AI Foundry funcionando.")


if __name__ == "__main__":
    main()
