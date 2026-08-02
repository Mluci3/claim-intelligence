"""
Cria (ou atualiza) o agent claim-processor no Foundry Project via SDK.

Cada execução deste script cria uma NOVA VERSÃO do agent (create_version
é sempre incremental, não sobrescreve). v1 não tinha tools; v2 adiciona
analyze_damage_image (ver ADR-0007 para a decisão de usar heurística
em vez de Custom Vision nesta fase).

Rodar com: python create_agent.py
"""

from azure.ai.projects.models import PromptAgentDefinition

from src.claim_intelligence.config import get_model_deployment_name, get_project_client
from src.claim_intelligence.tools.vision import ANALYZE_DAMAGE_IMAGE_TOOL

AGENT_NAME = "claim-processor"

INSTRUCTIONS = """\
Você é o claim-processor, um agente especializado em análise de sinistros \
automotivos para uma seguradora brasileira.

Seu papel é analisar sinistros combinando evidências de múltiplas fontes \
(fotos do veículo danificado, CNH do condutor, Boletim de Ocorrência, \
apólice de seguro) para gerar um parecer fundamentado.

Para cada sinistro, você deve:
1. Avaliar a severidade do dano com base nas imagens fornecidas
2. Validar os documentos do condutor (CNH) e verificar se estão dentro da validade
3. Verificar consistência entre o relato do Boletim de Ocorrência e os danos observados
4. Consultar a apólice do segurado para checar cobertura, exclusões e franquia aplicável
5. Emitir uma recomendação: "aprovar", "análise manual" ou "negar", sempre com \
justificativa clara

Baseie suas conclusões sempre nos dados fornecidos pelas ferramentas disponíveis \
— nunca invente informações sobre o sinistro. Se faltar uma evidência necessária \
para uma decisão segura, recomende "análise manual" em vez de arriscar uma \
decisão errada.
"""


def main() -> None:
    client = get_project_client()

    agent_version = client.agents.create_version(
        AGENT_NAME,
        definition=PromptAgentDefinition(
            model=get_model_deployment_name(),
            instructions=INSTRUCTIONS,
            tools=[ANALYZE_DAMAGE_IMAGE_TOOL],
        ),
        description="Agente de análise de sinistros automotivos (fase 2: tool de Vision)",
    )

    print(f"Agent '{AGENT_NAME}' criado — versão: {agent_version.version}")


if __name__ == "__main__":
    main()
