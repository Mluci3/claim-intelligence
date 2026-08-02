"""
Testa o loop completo de tool calling do agent claim-processor.

Isso NÃO é uma chamada só. É o padrão agentic real:

1. Enviamos a pergunta pro agent (responses.create)
2. O modelo decide chamar analyze_damage_image e devolve um item tipo
   "function_call" (nome + argumentos em JSON) — ele NÃO executa nada
3. Nosso código executa a função de verdade (aqui, de fato chama o
   Azure AI Vision)
4. Devolvemos o resultado da função pro modelo (segunda chamada a
   responses.create, com o resultado anexado)
5. Só agora o modelo gera a resposta final incorporando esse resultado

Rodar com: python test_agent_with_tool.py
"""

import json

from src.claim_intelligence.config import get_model_deployment_name, get_project_client
from src.claim_intelligence.tools.vision import analyze_damage_image

AGENT_NAME = "claim-processor"
SAMPLE_IMAGE = "data/car_damage_severity/data3a/validation/02-moderate/0042.JPEG"


def main() -> None:
    project_client = get_project_client()

    with project_client.get_openai_client() as openai_client:
        # 1. Primeira chamada — pedimos pro agent avaliar a imagem.
        response = openai_client.responses.create(
            model=get_model_deployment_name(),
            input=(
                f"Analise a severidade do dano na imagem em '{SAMPLE_IMAGE}' "
                "e me dê um parecer curto."
            ),
            extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
        )

        # 2. Procuramos por um item do tipo function_call na resposta.
        function_calls = [item for item in response.output if item.type == "function_call"]

        if not function_calls:
            print("O agent respondeu sem chamar nenhuma tool:")
            print(response.output_text)
            return

        call = function_calls[0]
        print(f"Agent pediu para chamar: {call.name}({call.arguments})")

        # 3. Executamos a função de verdade.
        args = json.loads(call.arguments)
        tool_result = analyze_damage_image(**args)
        print(f"Resultado real da tool: {tool_result}")

        # 4. Devolvemos o resultado pro modelo continuar o raciocínio.
        final_response = openai_client.responses.create(
            model=get_model_deployment_name(),
            input=[
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(tool_result),
                }
            ],
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
        )

        # 5. Resposta final, já incorporando o resultado da tool.
        print("\nParecer final do agent:")
        print(final_response.output_text)


if __name__ == "__main__":
    main()
