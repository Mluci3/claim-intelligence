# Architecture

> **Documentação arquitetural do projeto claim-intelligence.**
> Decisões de design, diagramas e justificativas técnicas.

---

## 📐 Visão Geral

`claim-intelligence` é um sistema baseado em **agents inteligentes** que automatiza a análise de sinistros automotivos. A arquitetura segue padrões cloud-native modernos, com forte foco em:

- **Agentic AI** como paradigma central (não service-oriented)
- **Foundry-first** — recursos gerenciados sempre que possível
- **Security by design** — Managed Identity, sem keys em código
- **Observability nativa** — traces, metrics, evaluations built-in
- **Synthetic data** — compliance com LGPD desde a concepção

---

## 🏗️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: PRESENTATION                                  │
│  (futuro: API REST / Streamlit / Power Apps)            │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: AGENT ORCHESTRATION                           │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Foundry Agent Service                            │  │
│  │  • Thread management (memória)                    │  │
│  │  • Run execution                                  │  │
│  │  • Tool calling automation                        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: TOOLS (capacidades do agent)                  │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │ analyze_damage  │  │ extract_bo_data │               │
│  │ (function)      │  │ (function)      │               │
│  └─────────────────┘  └─────────────────┘               │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │ extract_cnh     │  │ search_policies │               │
│  │ (function)      │  │ (azure_ai_search)│              │
│  └─────────────────┘  └─────────────────┘               │
│  ┌─────────────────┐                                    │
│  │ calculate_cost  │                                    │
│  │ (function)      │                                    │
│  └─────────────────┘                                    │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: AZURE AI SERVICES                             │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ AI Vision    │  │ Doc Intel    │  │ AI Search    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ OpenAI       │  │ Content      │                     │
│  │ (GPT-4o)     │  │ Safety       │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│  LAYER 5: STORAGE & DATA                                │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ Blob Storage │  │ AI Search    │                     │
│  │ (imagens,    │  │ (índice de   │                     │
│  │  documentos) │  │  políticas)  │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│  LAYER 6: CROSS-CUTTING CONCERNS                        │
│                                                         │
│  • Authentication: Managed Identity                     │
│  • Observability: Foundry traces + Application Insights │
│  • Evaluations: Foundry built-in evaluators             │
│  • Cost monitoring: Azure Cost Management               │
└─────────────────────────────────────────────────────────┘
```

---

## 🌐 Topologia de Recursos Azure

```
Subscription: Azure subscription 1
│
└── Resource Group: rg-claim-intelligence (East US 2)
    │
    ├── Foundry Hub: hub-claim-intelligence
    │   ├── Project: claim-analyzer
    │   │   ├── Agent: claim-processor
    │   │   ├── Model Deployment: gpt-4o-claim
    │   │   ├── Model Deployment: text-embedding-ada-002
    │   │   └── Connections (ver abaixo)
    │   │
    │   └── (Project: claim-evaluator — futuro)
    │
    ├── Azure AI Vision: vision-claim-intelligence
    │   └── Custom Vision Project: damage-severity-classifier
    │
    ├── Document Intelligence: docintel-claim-intelligence
    │   ├── prebuilt-idDocument (CNH)
    │   └── prebuilt-layout (BO)
    │
    ├── Azure AI Search: search-claim-intelligence
    │   └── Index: policies-knowledge-base
    │
    ├── Azure Blob Storage: stclaimintelligence
    │   ├── Container: damage-images
    │   ├── Container: documents
    │   └── Container: synthetic-data
    │
    └── Application Insights: appi-claim-intelligence
        └── (telemetria do agent)
```

---

## 🔄 Fluxo de Dados (E2E)

```
1. INPUT
   Usuário envia ao agent:
   - 📸 5 fotos do veículo danificado
   - 📄 PDF do Boletim de Ocorrência
   - 🪪 Foto da CNH do segurado
   - 📝 Número da apólice

2. AGENT THREAD CREATION
   • Foundry cria thread única para esta análise
   • Thread mantém contexto durante toda a sessão

3. TOOL CALLING (em paralelo quando possível)
   • analyze_damage_image → AI Vision processa fotos
   • extract_cnh_data → Doc Intel extrai dados da CNH
   • extract_bo_data → Doc Intel extrai dados do BO
   • search_policies → AI Search recupera política do segurado

4. CONSOLIDATION
   • Agent recebe outputs de todas as tools
   • GPT-4o cruza informações:
     - Veículo do BO bate com veículo da apólice?
     - Tipo de dano coberto pela apólice?
     - Valor estimado dentro da franquia?

5. CALCULATION
   • calculate_repair_cost → estima custo de reparo
     baseado em severidade + tabela de peças

6. DECISION
   • Agent gera parecer estruturado:
     - Status: APROVADO / ANÁLISE MANUAL / NEGADO
     - Justificativa fundamentada em documentos
     - Valor recomendado de indenização
     - Citações dos documentos consultados

7. OBSERVABILITY
   • Foundry registra:
     - Cada tool call executada
     - Tempo de cada step
     - Tokens consumidos
     - Trace completo para auditoria
```

---

## 🧩 Padrões de Design Aplicados

### Dependency Injection
Todos os clientes Azure são injetados via construtor, nunca instanciados internamente.

```python
class ClaimAgent:
    def __init__(self, vision: VisionClient, doc_intel: DocIntelClient):
        self._vision = vision
        self._doc_intel = doc_intel
```

### Fail Fast Configuration
Variáveis de ambiente são validadas na inicialização, não em runtime.

```python
@dataclass(frozen=True)
class AzureConfig:
    @classmethod
    def from_env(cls) -> "AzureConfig":
        # Lança EnvironmentError se faltar variável
        ...
```

### Single Responsibility Principle
Cada classe tem uma responsabilidade clara:
- `VisionClient` → apenas análise de imagens
- `DocIntelClient` → apenas extração de documentos
- `SearchClient` → apenas busca em índice
- `ClaimAgent` → apenas orquestração

### Strategy Pattern
Diferentes estratégias de análise podem ser plugadas:
- `DamageAnalyzer` (interface)
  - `AIVisionDamageAnalyzer` (implementação 1)
  - `CustomVisionDamageAnalyzer` (implementação 2)

---

## 🔐 Segurança

### Autenticação
- **Managed Identity** para todos os recursos Azure
- **Sem API keys** em código ou .env de produção
- `.env` apenas em desenvolvimento local (versionado em `.env.example` com placeholders)

### Autorização
- **RBAC** granular por recurso
- Princípio do menor privilégio
- Cada serviço tem role mínimo necessário

### Compliance
- **LGPD by design** — apenas dados sintéticos
- **Audit trail** completo via Foundry Observability
- **PII Detection** ativa em todos os inputs

---

## 📊 Observability

### Traces
Cada execução do agent é rastreável end-to-end:
- Início do thread
- Cada tool call
- Tempo de cada step
- Tokens consumidos
- Erros e retries

### Metrics
- Latência média por tipo de sinistro
- Custo por análise (tokens)
- Taxa de aprovação automática
- Taxa de análise manual necessária

### Evaluations
Foundry executa avaliações contínuas:
- **Groundedness** — resposta baseada nos documentos?
- **Relevance** — resposta relevante à pergunta?
- **Safety** — conteúdo seguro?
- **Custom** — métricas específicas de negócio (acurácia de severidade)

---

## 🚀 Estratégia de Evolução

### Fase 1 — Single Agent (Semana 1-2)
- 1 agent com 5 tools
- Foco em tool calling profundo
- Sem multi-agent ainda

### Fase 2 — Multi-Agent (Semana 3-4)
- Orchestrator + agents especializados
- Image Agent, Document Agent, Decision Agent
- Comunicação entre agents

### Fase 3 — Production-Ready (Futuro)
- API REST com FastAPI
- Deployment via Container Apps
- CI/CD com GitHub Actions
- Frontend Streamlit ou Power Apps

---

## 📚 Referências

- [Microsoft Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects)
- [Foundry Agent Service](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Responsible AI Standard](https://www.microsoft.com/ai/responsible-ai)
- [Architecture Decision Records](https://adr.github.io/)
