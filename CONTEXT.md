# CONTEXT.md — Estado Atual do Projeto

> **Arquivo de continuidade entre sessões.**
> Este documento é a fonte da verdade sobre o estado atual do projeto.
> Atualizado ao final de cada sessão de desenvolvimento.
> Em caso de novo chat, cole este arquivo e diga "continue de onde paramos".

---

## 📋 Identificação

- **Projeto:** claim-intelligence
- **Domínio:** Análise inteligente de sinistros automotivos
- **Certificação alvo:** AI-103 (Azure AI App and Agent Developer Associate)
- **Data prevista da prova:** 15-31/07/2026
- **Início do projeto:** 08/06/2026
- **Última atualização:** 08/06/2026

---

## 🎯 Objetivo

Construir uma plataforma multi-agent enterprise-grade que automatiza análise de sinistros automotivos, cobrindo ~85% dos tópicos da certificação AI-103 em um único projeto de portfolio.

---

## 👤 Perfil da Desenvolvedora

- **Nome:** Maria Lucia
- **Cargo:** AI Engineer @ Minsait (GOLLabs squad)
- **Stack atual:** Python, LangChain, Azure AI, Copilot Studio, Power Automate
- **Projetos relevantes:** Datathon Fase 05 (MLOps), paligeri (RAG clínico), IARAA (RAG agroecologia), FlightOps (Copilot Studio em produção)
- **Localização:** Brasil (São Paulo)
- **Idiomas:** Português (nativo), Inglês (em estudo)

---

## 🏗️ Decisões Arquiteturais (já tomadas)

| # | Decisão | Status | ADR |
|---|---------|--------|-----|
| 1 | Foundry Agent Service como runtime de agents | ✅ Confirmada | ADR-0001 |
| 2 | Single-agent na fase 1 → multi-agent na fase 3 | ✅ Confirmada | ADR-0002 |
| 3 | Dados sintéticos para PII (CNH, BO) | ✅ Confirmada | ADR-0003 |
| 4 | Híbrido EN/PT (código EN, comentários PT) | ✅ Confirmada | ADR-0004 |
| 5 | Resource Group isolado (sem conflito com paligeri) | ✅ Confirmada | ADR-0005 |
| 6 | CONTEXT.md + Git + Memory para continuidade entre chats | ✅ Confirmada | ADR-0006 |

---

## 🔧 Stack Técnico

### Azure Resources (a provisionar)

```
rg-claim-intelligence (East US 2)
├── Foundry Hub: hub-claim-intelligence
│   └── Foundry Project: claim-analyzer
│       ├── Agent: claim-processor
│       └── Connections: Vision, Doc Intel, Search, Storage
├── Azure AI Vision: vision-claim-intelligence
├── Document Intelligence: docintel-claim-intelligence
├── Azure AI Search: search-claim-intelligence
└── Azure Blob Storage: stclaimintelligence
```

### SDKs Python

```
azure-ai-projects     → gerenciar projetos Foundry
azure-ai-inference    → consumir modelos
azure-ai-agents       → criar e executar agents
azure-ai-vision       → análise de imagens
azure-ai-documentintelligence → extração de docs
azure-search-documents → Azure AI Search
azure-identity        → Managed Identity
azure-storage-blob    → armazenamento de imagens
python-dotenv         → configuração via .env
```

### Datasets

```
✅ Car Damage Severity (Kaggle, ~1.500 imagens)
✅ IDNet (Kaggle, CNHs sintéticas)
🛠️ BOs sintéticos (gerar com templates públicos)
🛠️ Apólices fictícias (criar 10-15 em MD/PDF)
```

---

## 📅 Cronograma

| Semana | Período | Fase | Foco |
|--------|---------|------|------|
| 1 | 09-15/06 | Foundation Reset | Setup Foundry + estrutura inicial |
| 2 | 16-22/06 | Agents Fundamentos | Single-agent + tool calling |
| 3 | 23-29/06 | RAG + Multi-agent | Azure AI Search + orchestration |
| 4 | 30/06-06/07 | Planning & Ops | Security, RBAC, Evaluations |
| 5 | 07-13/07 | Vision + Text + Extract | Domínios específicos |
| 6 | 14-20/07 | Simulados + revisão | Preparação final |
| - | 21-31/07 | **PROVA** | Janela de execução |

---

## 📊 Estado Atual

### ✅ Concluído

- Planejamento estratégico do projeto
- Pesquisa de viabilidade de dados (datasets identificados)
- Decisões arquiteturais iniciais (6 ADRs)
- Estrutura de documentação criada

### 🔄 Em andamento

- (nada ainda — projeto na fase de planejamento)

### ⏭️ Próximos passos (ordem)

1. **Maria recupera senha Kaggle** ⏳ (bloqueio)
2. Setup do ambiente local (estrutura de pastas)
3. Criar Resource Group `rg-claim-intelligence`
4. Provisionar Foundry Hub + Project
5. Provisionar AI Vision + Document Intelligence + Storage
6. Download dos datasets
7. Estrutura inicial do código Python
8. Primeiro agent funcional (single-agent)

---

## 🚧 Bloqueios Ativos

| Bloqueio | Responsável | Desde |
|----------|-------------|-------|
| Recuperação de senha Kaggle (necessário para baixar datasets) | Maria | 08/06/2026 |

---

## 🧠 Contexto Importante para Próxima Sessão

### O que foi discutido

- Pivot estratégico de AI-102 para AI-103 (AI-102 retira em 30/06/2026)
- Pesquisa de datasets confirmou viabilidade do domínio (seguros)
- Decisão por dados sintéticos para CNH e BO (questão de LGPD)
- Padrão ADR (Architecture Decision Record) adotado para documentação
- Metodologia de continuidade entre chats definida (CONTEXT.md + Git)

### Padrão de operação acordado

1. **Tutor explica conceito** com profundidade
2. **Hands-on** no projeto (onde clicar, porquês)
3. **Exercícios** de fixação estilo AI-103
4. **Documenta decisões** em ADRs e CHANGELOG

### Tom da relação

- Maria é AI Engineer sênior — não precisa de explicação básica
- Comentários técnicos diretos
- Foco em padrões enterprise (SOLID, clean code, segurança)
- Justificativas técnicas antes de qualquer código

---

## 🔗 Recursos Externos

### Datasets

- [Car Damage Severity](https://www.kaggle.com/datasets/prajwalbhamere/car-damage-severity-dataset)
- [IDNet](https://www.kaggle.com/datasets/chitreshkr/idnet-identity-document-analysis)
- [VehiDE (backup)](https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection)

### Documentação oficial AI-103

- [Microsoft Learn AI-103 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103)
- [Azure AI Foundry Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Projects SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects)

---

## 📝 Como atualizar este arquivo

Ao final de cada sessão, atualizar:

1. **Última atualização** (topo do arquivo)
2. **Estado Atual** (✅ Concluído / 🔄 Em andamento / ⏭️ Próximos passos)
3. **Bloqueios Ativos** (adicionar/remover)
4. **Contexto Importante para Próxima Sessão** (resumir decisões)
5. **Cronograma** (marcar progresso da semana)

---

## 🔄 Como retomar em novo chat

1. Abrir novo chat com Claude
2. Colar o conteúdo deste arquivo
3. Dizer: *"Sou Maria. Estamos no projeto claim-intelligence para AI-103. Continue de onde paramos baseado neste CONTEXT.md."*
4. Claude lerá o contexto e retomará a sessão
