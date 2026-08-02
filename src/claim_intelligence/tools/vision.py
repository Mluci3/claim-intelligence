"""
Tool `analyze_damage_image` — Function Tool client-side.

Azure AI Vision (Image Analysis) não é uma tool "hospedada" pelo Foundry
Agent Service (diferente de AzureAISearchTool, por exemplo). Por isso a
integração é sempre via Function Tool: o Foundry só descreve o contrato
pro modelo; quem chama a API de verdade é este código.

LIMITAÇÃO CONHECIDA (documentada por decisão, não por descuido):
Image Analysis devolve tags genéricas de visão computacional (objetos,
cenas, legendas), não foi treinado para diferenciar severidade de dano
automotivo. A classificação abaixo é uma heurística baseada em palavras-
chave nas tags — um placeholder que destrava o pipeline agora, não um
classificador confiável. Ver ADR-0007 para a decisão e o plano de evoluir
para um modelo Custom Vision treinado no dataset local (car_damage_severity).
"""

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from src.claim_intelligence.config import get_project_client

VISION_CONNECTION_NAME = "vision-claim-intelligence"

# Palavras-chave que orientam a heurística. Case-insensitive, comparadas
# contra as tags devolvidas pelo Image Analysis.
_SEVERE_KEYWORDS = {"wreck", "wreckage", "totaled", "crushed", "destroyed", "overturned", "rollover", "fire"}
_MODERATE_KEYWORDS = {"damage", "damaged", "broken", "crash", "collision", "crumpled", "bumper"}
_MINOR_KEYWORDS = {"scratch", "scrape", "dent", "chip"}


def _get_vision_client() -> ImageAnalysisClient:
    """Constrói o client do Vision usando a connection do Foundry.

    Deliberadamente NÃO lemos endpoint/key de variáveis de ambiente
    próprias do Vision — isso duplicaria a credencial em dois lugares
    (o .env e a connection já registrada no Foundry Project). Buscamos
    a credencial pela connection, que é a peça que já provisionamos e
    conectamos nas sessões anteriores.
    """
    project_client = get_project_client()
    connection = project_client.connections.get(VISION_CONNECTION_NAME, include_credentials=True)

    return ImageAnalysisClient(
        endpoint=connection.target,
        credential=AzureKeyCredential(connection.credentials.api_key),
    )


def analyze_damage_image(image_path: str) -> dict:
    """Analisa uma imagem de veículo danificado e estima a severidade.

    :param image_path: Caminho local do arquivo de imagem.
    :return: dict com caption, tags detectadas e uma estimativa heurística
        de severidade (minor/moderate/severe/indeterminado).
    """
    client = _get_vision_client()

    with open(image_path, "rb") as f:
        image_data = f.read()

    # CAPTION não está disponível em todas as regiões (ex: East US 2, onde
    # o vision-claim-intelligence está provisionado) — feature parity
    # regional é uma limitação real do serviço, não um erro de código.
    # TAGS tem disponibilidade ampla, então é o que sustenta a heurística.
    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.TAGS],
    )

    tag_names = {tag.name.lower() for tag in result.tags.list} if result.tags else set()

    if tag_names & _SEVERE_KEYWORDS:
        severity = "severe"
    elif tag_names & _MODERATE_KEYWORDS:
        severity = "moderate"
    elif tag_names & _MINOR_KEYWORDS:
        severity = "minor"
    else:
        severity = "indeterminado"

    return {
        "tags": [{"name": tag.name, "confidence": tag.confidence} for tag in result.tags.list] if result.tags else [],
        "heuristic_severity": severity,
        "note": (
            "Classificação heurística baseada em tags genéricas do Image Analysis, "
            "não um classificador treinado para severidade de dano automotivo."
        ),
    }


# Schema descrevendo a tool pro modelo (usado em PromptAgentDefinition.tools).
# "strict": True exige additionalProperties=False e todos os campos em
# "required" — regra da OpenAI Responses API para tool calling confiável.
ANALYZE_DAMAGE_IMAGE_TOOL = {
    "type": "function",
    "name": "analyze_damage_image",
    "description": (
        "Analisa uma imagem de veículo danificado e retorna observações visuais "
        "(legenda, tags) e uma estimativa heurística de severidade do dano. "
        "A estimativa é aproximada — se a resposta vier como 'indeterminado' ou a "
        "confiança parecer baixa, prefira recomendar análise manual."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "image_path": {
                "type": "string",
                "description": "Caminho local do arquivo de imagem a ser analisado.",
            }
        },
        "required": ["image_path"],
        "additionalProperties": False,
    },
    "strict": True,
}
