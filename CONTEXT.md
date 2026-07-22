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
- **Última atualização:** 20/07/2026

---

## 🎯 Objetivo

Construir uma plataforma multi-agent enterprise-grade que automatiza análise de sinistros automotivos, cobrindo ~85% dos tópicos da certificação AI-103 em um único projeto de portfolio.

---

## 👤 Perfil da Desenvolvedora

- **Nome:** Maria Lucilene
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
rg-claim-intelligence
├── Foundry Hub: hub-claim-intelligence (East US 2)
│   └── Foundry Project: claim-analyzer (East US 2)
│       ├── Agent: claim-processor
│       └── Connections: Vision ✅, Doc Intel ✅, Search ✅, Storage ⏳
├── Azure AI Vision: vision-claim-intelligence (East US 2)
├── Document Intelligence: docintel-claim-intelligence (East US 2)
├── Azure AI Search: search-claim-intelligence (East US — ver nota de região abaixo)
└── Azure Blob Storage: stclaimintelligence (East US 2 — Entra ID only, rede restrita)
```

> **Nota de segurança — Storage:** provisionado com `allowSharedKeyAccess=false` (sem key estática, só Microsoft Entra ID/RBAC) e `networkRuleSet.defaultAction=Deny` com IP da Maria liberado + `bypass=AzureServices`. Padrão mais rígido que os outros 3 recursos (que ainda usam "Chave da API"); decisão de progressivamente aplicar least-privilege conforme a certificação cobra.

> **Nota de região — Azure AI Search:** provisionado em **East US**, não East US 2 como o resto do stack. Motivo: tentativa de criação em East US 2 falhou com `InsufficientResourcesAvailable` (capacidade do tier Free esgotada na região no momento). Decisão consciente: manter Free (custo R$ 0) em vez de pagar S1 (~US$ 250/mês fixo) só para manter consistência de região — não se justifica para o volume de uso do projeto (poucos documentos, baixo volume de queries). Latência extra entre East US e East US 2 é desprezível para esse caso de uso.

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
✅ Car Damage Severity (Kaggle, 1.631 imagens) — baixado e extraído em data/car_damage_severity/
❌ IDNet (Kaggle, CNHs sintéticas) — download corrompido (zip de 20GB sem rodapé válido, precisa refazer)
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

- Planejamento estratégico do projeto e documentação arquitetural (6 ADRs, README, ARCHITECTURE, CHANGELOG, DATASETS)
- Configuração do Git local no Mac (branch `main` como padrão) e primeiro push para o GitHub (Mluci3/claim-intelligence)
- Criação manual via Azure Portal do Resource Group `rg-claim-intelligence`
- Provisionamento do Foundry Hub `hub-claim-intelligence`
- Provisionamento do Foundry Project `claim-analyzer`
- Setup do ambiente de desenvolvimento local Python (`.env`, `requirements.txt` com `azure-ai-projects`, `azure-identity`, `python-dotenv`)
- `.env.example` corrigido para o padrão do SDK 2.x (`PROJECT_ENDPOINT` em vez de connection string)
- Azure CLI instalado + `az login` configurado (autenticação local via `DefaultAzureCredential`)
- Script `test_azure_connection.py` criado e validado — autentica e lista connections do Project
- Recurso **Azure AI services** `vision-claim-intelligence` (East US 2) provisionado e conectado ao Foundry Project (`claim-analyzer`) via connection tipo "Chave da API"
- Recurso **Document Intelligence** `docintel-claim-intelligence` (East US 2, kind `FormRecognizer`) provisionado e conectado ao Foundry Project via "Chave da API"
- Recurso **Azure AI Search** `search-claim-intelligence` provisionado (Free tier, região **East US** — ver nota de região acima) e conectado ao Foundry Project
- Recurso **Azure Blob Storage** `stclaimintelligence` (East US 2, Standard LRS) provisionado com hardening: Entra ID only (sem key), rede restrita ao IP da Maria + trusted Azure services
- Criado `docs/AI-103-STUDY-GUIDE.md` — manual de estudos hands-on, atualizado a cada sessão

### 🔄 Em andamento

- Conectar o Storage ao Foundry Project (provavelmente via Entra ID, não "Chave da API" — key access está desabilitada)

### ⏭️ Próximos passos (ordem)

1. Conectar `stclaimintelligence` ao Foundry Project via Microsoft Entra ID
2. Refazer o download do IDNet (zip anterior de 20GB corrompido — ver nota abaixo)
3. Criar o agente `claim-processor` 100% via código Python (SDK)
4. Implementar a primeira tool (single-agent) — provavelmente Vision, já que a connection está pronta e o dataset Car Damage Severity já está pronto

---

## 🚧 Bloqueios Ativos

Nenhum bloqueio ativo no momento (senha do Kaggle recuperada em 21/07/2026).

---

## 🧠 Contexto Importante para Próxima Sessão

### O que foi discutido

- Pivot estratégico de AI-102 para AI-103 (AI-102 retira em 30/06/2026)
- Pesquisa de datasets confirmou viabilidade do domínio (seguros)
- Decisão por dados sintéticos para CNH e BO (questão de LGPD)
- Padrão ADR (Architecture Decision Record) adotado para documentação
- Metodologia de continuidade entre chats definida (CONTEXT.md + Git)
- **20/07/2026:** primeira sessão hands-on completa de provisionamento — Vision criado e conectado ao Foundry Project. Erros reais documentados em `docs/AI-103-STUDY-GUIDE.md` (soft-delete, categoria de connection errada gerando 400, mismatch de kind de recurso, arquivos "dataless" do iCloud travando leitura local). Maria pediu explicitamente aprender "onde clicar" no portal — próximas sessões devem manter esse formato de walkthrough manual, não automatizar via CLI/Bicep ainda
- **21/07/2026:** Document Intelligence e AI Search provisionados e conectados sem erros novos (lições da sessão anterior já aplicadas). AI Search precisou mudar de região (East US 2 → East US) por falta de capacidade do tier Free — decisão consciente de manter Free em vez de pagar S1 (~US$250/mês) por consistência de região, sem justificativa de custo pro volume de uso do projeto. Storage provisionado já com hardening de segurança (Entra ID only, rede restrita por IP) — os outros 3 recursos ainda estão no padrão mais simples ("Chave da API", rede aberta); planejar hardening deles depois. **Pendência real para a próxima sessão:** conectar o Storage ao Foundry Project — ainda não foi feito, e como a key está desabilitada, provavelmente vai exigir um fluxo de connection via Microsoft Entra ID diferente dos outros 3 (que usaram "Chave da API"). Todos os 6 componentes de infra do stack planejado (Hub, Project, Vision, Doc Intel, Search, Storage) já existem no Azure.
- **Preferência registrada:** sempre tentar Free tier primeiro em qualquer recurso novo; quando não for possível, estimar o custo fixo real (mesmo sem uso) antes de decidir — não pagar por conveniência/consistência sem justificativa de uso real.
- **21/07/2026:** conferido `data/` — Car Damage Severity está completo e extraído (1.631 imagens, 3 classes). IDNet só tem o `.zip` de 20GB, e ele está corrompido (sem rodapé válido de ZIP — download foi interrompido, apesar do arquivo parecer ter o tamanho esperado). Bloqueio de senha do Kaggle já foi resolvido, então o próximo passo é só refazer o download do IDNet.

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

1. Abrir nova sessão de AI pair programming
2. Colar o conteúdo deste arquivo
3. Dizer: *"Sou Maria. Estamos no projeto claim-intelligence para AI-103. Continue de onde paramos baseado neste CONTEXT.md."*
4. O agente lerá o contexto e retomará a sessão
