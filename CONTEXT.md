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
- **Data prevista da prova:** 15-30/08/2026
- **Início do projeto:** 08/06/2026
- **Última atualização:** 29/07/2026

---

## 🎯 Objetivo

Construir uma plataforma multi-agent enterprise-grade que automatiza análise de sinistros automotivos, cobrindo ~85% dos tópicos da certificação AI-103 em um único projeto de portfolio.

---

## 👤 Perfil da Desenvolvedora

- **Nome:** Maria Lucilene
- **Cargo:** AI Engineer @ Minsait (GOLLabs squad)
- **Stack atual:** Python, LangChain, Azure AI, Copilot Studio, Power Automate
- **Projetos relevantes:** Datathon Fase 05 (MLOps), Paligeri (RAG clínico), IARAA (RAG agroecologia), FlightOps (Copilot Studio em produção)
- **Localização:** Brasil (São Paulo)
- **Idiomas:** Português (nativo), Inglês (B1)

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

### Azure Resources (provisionados ✅ — infra completa)

```
rg-claim-intelligence
├── Foundry Hub: hub-claim-intelligence (East US 2)
│   └── Foundry Project: claim-analyzer (East US 2)
│       ├── Model deployment: gpt-5.4-nano (Global Standard) ✅
│       ├── Agent: claim-processor ✅ (v2 — tool analyze_damage_image ativa)
│       └── Connections: Vision ✅, Doc Intel ✅, Search ✅, Storage ✅
├── Azure AI Vision: vision-claim-intelligence (East US 2)
├── Document Intelligence: docintel-claim-intelligence (East US 2)
├── Azure AI Search: search-claim-intelligence (East US — ver nota de região abaixo)
└── Azure Blob Storage: stclaimintelligence (East US 2 — Entra ID only, rede restrita)
```

> **Nota de segurança — Storage:** provisionado com `allowSharedKeyAccess=false` (sem key estática, só Microsoft Entra ID/RBAC) e `networkRuleSet.defaultAction=Deny` com IP da Maria liberado + `bypass=AzureServices`. Padrão mais rígido que os outros 3 recursos (que ainda usam "Chave da API"); decisão de progressivamente aplicar least-privilege conforme a certificação cobra. RBAC da Managed Identity do Foundry Project escopado por container (`damage-images`, `documents`) com role `Storage Blob Data Contributor`, não na conta inteira — role assignment não tem custo, então dá pra ser rigoroso sem afetar o orçamento zero do projeto.

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
✅ Synthetic EU Driver's Licences (Kaggle, amostra de 30 imagens) — substitui o IDNet, ver docs/DATASETS.md
🛠️ BOs sintéticos (gerar com templates públicos)
🛠️ Apólices fictícias (criar 10-15 em MD/PDF)
```

---

## 📅 Cronograma

> ⚠️ **Reconstruído em 29/07/2026.** O plano original (6 semanas, prova 21-31/07) previa 1 semana para provisionamento — na prática levou de 08/06 a 29/07 (~7 semanas), então a prova foi remarcada para 15-30/08. Cronograma abaixo reflete o estado real do projeto, não o plano original.

| Período | Fase | Foco | Status |
|---------|------|------|--------|
| 08/06 – 29/07 | Foundation Reset | Planejamento, ADRs, provisionamento dos 6 recursos Azure, 4 connections, hardening inicial do Storage | ✅ Concluído |
| 29/07 – 04/08 | Agent Implementation | Criar `claim-processor` via SDK, primeira tool (Vision — `analyze_damage_image`) | 🔄 Próximo |
| 05/08 – 11/08 | Extract + RAG | Tools `extract_cnh_data` (Doc Intelligence) e `extract_bo_data`; indexar apólices fictícias no AI Search; tool `search_policies` | ⏳ |
| 12/08 – 14/08 | Planning & Ops | Evaluations (groundedness, relevance, safety); hardening de segurança nos 3 recursos restantes (Entra ID); Observability básica | ⏳ |
| 15/08 – 25/08 | Simulados + revisão | Questões estilo AI-103 por domínio, revisão dos pontos fracos | ⏳ |
| 15/08 – 30/08 | **PROVA** | Janela de execução — agendar depois de fechar os simulados | ⏳ |

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
- Deployment de modelo `gpt-5.4-nano` (Global Standard, pay-as-you-go) criado no Foundry Project
- Agent `claim-processor` (v1) criado 100% via SDK (`create_agent.py`, `PromptAgentDefinition`), sem tools ainda — testado com sucesso via `test_agent.py` (Responses API + `agent_reference`)
- Estrutura `src/claim_intelligence/` criada (`config.py` com factory do client, reutilizável pelos próximos scripts)
- Venv movido para `~/.venvs/claim-intelligence` (fora da pasta Documents sincronizada pelo iCloud) — resolve de vez o bug recorrente de arquivos "dataless"
- Tool `analyze_damage_image` implementada como Function Tool (`src/claim_intelligence/tools/vision.py`) — busca credencial via connection do Foundry (não duplica key no `.env`), classificação de severidade por heurística sobre tags do Image Analysis (ver ADR-0007)
- Agent `claim-processor` v2 criado com a tool anexada; loop completo de tool calling testado e validado ponta a ponta (`test_agent_with_tool.py`) — agent corretamente recomendou "análise manual" quando a heurística voltou `indeterminado`

### 🔄 Em andamento

- Nenhuma tarefa de infraestrutura em andamento — primeira tool completa e validada, próximo passo é a segunda tool

### ⏭️ Próximos passos (ordem)

1. Implementar `extract_cnh_data` (Document Intelligence) e testar com a amostra de carteiras EU
2. Implementar `extract_bo_data` e `search_policies` (RAG via AI Search)
3. Gerar datasets sintéticos restantes (BOs, apólices) e indexar apólices no AI Search
4. (Futuro) Treinar Custom Vision pra substituir a heurística de severidade (ADR-0007)
5. (Futuro) Aplicar o mesmo padrão de hardening do Storage (Entra ID only, RBAC granular) em Vision/Doc Intel/Search

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
- **29/07/2026:** Storage conectado ao Foundry Project via Microsoft Entra ID. RBAC da Managed Identity do Project (`22c5dcd0-...`, distinta da identity do Hub) escopado por container (`damage-images`, `documents`) com `Storage Blob Data Contributor`, sem permissão ampla na conta — reforça o princípio de least-privilege sem custo, já que role assignment é sempre gratuito. Os 4 recursos auxiliares estão provisionados E conectados; próxima infraestrutura pendente é só o hardening dos outros 3 (Vision/Doc Intel/Search), que fica pra depois.
- **29/07/2026:** IDNet descartado definitivamente — dataset é um pacote monolítico de 49GB (não 20GB como parecia), sem suporte a download parcial via API do Kaggle, e volume muito maior do que o projeto precisa. Substituído por `felipebandeiraramos/synthetic-eu-drivers-licences` (arquivos individuais, baixamos só 30 amostras via `kaggle datasets download -f`). Categorias de habilitação do padrão EU (A/B/C) são estruturalmente mais próximas da CNH brasileira do que o padrão americano — Maria identificou corretamente que passaporte (outra opção considerada) não serviria, porque o projeto precisa de campos específicos de habilitação (categoria, validade) pra lógica de decisão de sinistro. Detalhes completos em `docs/DATASETS.md`.

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
- [Synthetic EU Driver's Licences](https://www.kaggle.com/datasets/felipebandeiraramos/synthetic-eu-drivers-licences)
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
