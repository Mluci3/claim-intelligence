# Claim Intelligence

> **Plataforma multi-agent enterprise para análise automatizada de sinistros automotivos.**
> Construída com Azure AI Foundry, demonstra padrões de produção em agentic AI.

[![Azure AI Foundry](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)](https://learn.microsoft.com/azure/ai-foundry/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## 📋 Sobre o Projeto

**Claim Intelligence** é uma plataforma que automatiza o processo de análise de sinistros automotivos usando agentes inteligentes do Azure AI Foundry. O sistema processa fotos do veículo danificado, documentos do segurado (CNH) e Boletim de Ocorrência, gerando parecer automatizado com classificação de gravidade, estimativa de custo e recomendação de aprovação.

### Motivação

Companhias de seguros processam milhares de sinistros diariamente. A análise manual leva dias, gera inconsistências entre peritos e atrasa indenizações. Este projeto demonstra como pipelines agentic podem reduzir tempo de análise de dias para minutos, mantendo auditabilidade e responsabilização humana.

---

## 🎯 Capacidades

### 🚗 Análise de Imagens de Sinistro
- Detecção automática de peças danificadas
- Classificação de severidade (leve, média, severa, perda total)
- Estimativa de custo de reparo

### 📄 Extração de Documentos
- Leitura de CNH (validação de identidade)
- Parsing de Boletim de Ocorrência
- Identificação de inconsistências

### 🔍 Busca em Base de Conhecimento
- Consulta semântica em políticas de cobertura
- Verificação de exclusões contratuais
- Cálculo de franquia aplicável

### 🤖 Decisão Inteligente
- Parecer fundamentado em documentos da apólice
- Recomendação: aprovar / análise manual / negar
- Trilha de auditoria completa

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                  CLAIM INTELLIGENCE                     │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │           AZURE AI FOUNDRY                        │  │
│  │                                                   │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │      Agent: claim-processor                 │  │  │
│  │  │                                             │  │  │
│  │  │  Tools:                                     │  │  │
│  │  │  • analyze_damage_image  (AI Vision)        │  │  │
│  │  │  • extract_bo_data       (Doc Intel)        │  │  │
│  │  │  • extract_cnh_data      (Doc Intel)        │  │  │
│  │  │  • search_policies       (AI Search RAG)    │  │  │
│  │  │  • calculate_repair_cost (custom function)  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Foundry Components:                                    │
│  • Connections (Vision, Doc Intel, Search, Storage)     │
│  • Evaluations (groundedness, relevance, safety)        │
│  • Observability (traces, metrics, logs)                │
└─────────────────────────────────────────────────────────┘
```

Detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🛠️ Stack Técnico

### Azure AI Services
- **Azure AI Foundry** — plataforma de agents
- **Foundry Agent Service** — runtime gerenciado
- **Azure AI Vision** — análise de imagens
- **Document Intelligence** — extração de PDFs/imagens
- **Azure AI Search** — busca vetorial híbrida
- **Azure Blob Storage** — armazenamento de mídia

### Python Stack
- `azure-ai-projects` — Foundry SDK
- `azure-ai-inference` — model inference
- `azure-ai-agents` — agent runtime
- `azure-ai-vision` — Computer Vision
- `azure-ai-documentintelligence` — document AI
- `azure-search-documents` — AI Search
- `azure-identity` — Managed Identity auth
- `python-dotenv` — configuration management

### Padrões de Engenharia
- **SOLID principles**
- **Clean Code**
- **Dependency Injection**
- **ADR (Architecture Decision Records)**
- **Fail fast configuration**
- **Structured logging**

---

## 📊 Cobertura AI-103

Este projeto é desenhado para cobrir ~85% dos tópicos da certificação **Microsoft Azure AI App and Agent Developer Associate (AI-103)**:

| Domínio AI-103 | Peso | Cobertura |
|----------------|------|-----------|
| Plan and manage AI solution | 25-30% | ✅ Foundry, RBAC, networking, cost |
| Generative AI & agentic solutions | 30-35% | ✅ Agent design, tools, multi-agent, RAG |
| Computer vision | 10-15% | ✅ Image analysis, Custom Vision |
| Text analysis | 10-15% | ✅ NER, PII, summarization |
| Information extraction | 10-15% | ✅ Document Intelligence |

---

## 🚀 Quick Start

> ⚠️ **Em desenvolvimento.** Instruções completas estarão disponíveis ao final do projeto.

### Pré-requisitos

- Python 3.11+
- Azure Subscription com créditos disponíveis
- Conta Kaggle (para download dos datasets)
- Azure CLI instalado

### Instalação (preview)

```bash
# Clone o repositório
git clone https://github.com/Mluci3/claim-intelligence.git
cd claim-intelligence

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais Azure
```

### Provisioning Azure (preview)

```bash
# Login no Azure
az login

# Criar resource group
az group create --name rg-claim-intelligence --location eastus2

# (Demais comandos serão documentados em DEPLOYMENT.md)
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [CONTEXT.md](CONTEXT.md) | Estado atual do projeto (continuidade entre sessões) |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Decisões arquiteturais e diagramas |
| [CHANGELOG.md](docs/CHANGELOG.md) | Histórico de mudanças versionadas |
| [DATASETS.md](docs/DATASETS.md) | Origem e tratamento dos dados |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deploy e operação |
| [decisions/](docs/decisions/) | Architecture Decision Records (ADRs) |

---

## 🔐 Segurança & Compliance

- **Sem dados pessoais reais** — todo dataset é sintético ou público
- **Managed Identity** para autenticação Azure (sem keys hardcoded)
- **Content Safety** ativo em todas as interações
- **PII Detection** em pipelines de processamento
- **Audit trail** completo via Foundry Observability
- **LGPD compliant by design**

---

## 📈 Status do Desenvolvimento

| Fase | Status |
|------|--------|
| 📋 Planejamento | ✅ Concluído |
| 🏗️ Setup Azure Foundry | ⏳ Em breve |
| 🤖 Agent Implementation | ⏳ Em breve |
| 🧪 Evaluations | ⏳ Em breve |
| 📊 Observability | ⏳ Em breve |
| 🚀 Deploy | ⏳ Em breve |

Acompanhe progresso em [CONTEXT.md](CONTEXT.md).

---

## 🎓 Sobre o Projeto

Este projeto integra estudos para a certificação **Microsoft Azure AI App and Agent Developer Associate (AI-103)** e foi construído com metodologia de aprendizado por projeto guiado, alinhada a padrões enterprise de mercado.

### Autora

**Maria Lucia** — AI Engineer
- 💼 [LinkedIn](#)
- 🐙 [GitHub](https://github.com/Mluci3)
- 🌐 Portfolio: paligeri, IARAA, Datathon Fase 05

---

## 📄 Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Reconhecimentos

- **Microsoft Azure AI** pela plataforma Foundry
- **Kaggle** pelos datasets públicos
- **Comunidade Azure AI Brasil** pelas discussões técnicas

---

> 💡 *"Da prototipagem à produção: agents que funcionam em escala."*
