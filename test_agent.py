"""
Smoke test: envia uma mensagem simples para o agent claim-processor
e imprime a resposta, para confirmar que o agent está funcional.

Rodar com: python test_agent.py
"""

from src.claim_intelligence.config import get_model_deployment_name, get_project_client

AGENT_NAME = "claim-processor"


def main() -> None:
    project_client = get_project_client()

    with project_client.get_openai_client() as openai_client:
        response = openai_client.responses.create(
            model=get_model_deployment_name(),
            input="Em uma frase, qual é o seu papel neste projeto?",
            extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
        )
        print("Resposta do agent:")
        print(response.output_text)


if __name__ == "__main__":
    main()
