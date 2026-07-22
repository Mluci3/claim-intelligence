# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adota [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Não Lançado]

### Adicionado
- Estrutura inicial de documentação (README, CONTEXT, CHANGELOG, ARCHITECTURE)
- Architecture Decision Records (ADRs) iniciais
- Estratégia de continuidade entre chats via CONTEXT.md
- Definição da arquitetura macro do projeto
- Identificação de datasets viáveis (Car Damage Severity, IDNet)
- Decisão por dados sintéticos para CNH e BO (compliance LGPD)
- Provisionamento do Foundry Hub (`hub-claim-intelligence`) e Foundry Project (`claim-analyzer`) em `rg-claim-intelligence` (East US 2)
- Script `test_azure_connection.py` para smoke test de autenticação/conectividade via `azure-ai-projects` + `DefaultAzureCredential`
- Recurso **Azure AI services** `vision-claim-intelligence` (East US 2) provisionado e conectado ao Foundry Project (connection tipo "Chave da API")
- Recurso **Document Intelligence** `docintel-claim-intelligence` (East US 2) provisionado e conectado ao Foundry Project (connection tipo "Chave da API")
- Recurso **Azure AI Search** `search-claim-intelligence` provisionado (Free tier, East US) e conectado ao Foundry Project
- Recurso **Azure Blob Storage** `stclaimintelligence` (East US 2, Standard LRS) provisionado com Microsoft Entra ID only (`allowSharedKeyAccess=false`) e rede restrita por IP (`defaultAction=Deny` + `bypass=AzureServices`)
- `docs/AI-103-STUDY-GUIDE.md` — manual de estudos hands-on para revisão pré-prova

### Modificado
- `.env.example` atualizado de `AZURE_AI_PROJECT_CONNECTION_STRING` (padrão `azure-ai-projects` 1.x) para `PROJECT_ENDPOINT` (padrão 2.x, instalado no projeto)
- `requirements.txt` passa a listar `azure-ai-projects`, `azure-identity` e `python-dotenv`

### Decisões técnicas
- **Azure AI Search em East US, não East US 2:** tentativa de criação no Free tier em East US 2 falhou com `InsufficientResourcesAvailable` (falta de capacidade da região no momento). Decisão: manter Free em outra região em vez de pagar S1 (~US$ 250/mês fixo) só por consistência de região — sem justificativa de custo para o volume de uso do projeto. Detalhes em `docs/AI-103-STUDY-GUIDE.md`.
- **Storage provisionado direto com hardening de segurança** (Entra ID only + rede restrita), diferente dos outros 3 recursos (ainda em "Chave da API" com rede aberta) — início de uma passada progressiva de least-privilege pelo projeto, alinhada a tópicos de segurança da AI-103.

### Todos os recursos auxiliares provisionados
- Foundry Hub, Foundry Project, Vision, Document Intelligence, AI Search e Storage — os 6 componentes de infraestrutura do stack planejado estão criados

### Em planejamento
- Conectar Storage ao Foundry Project via Microsoft Entra ID
- Hardening de segurança dos demais recursos (Vision, Doc Intel, Search) para o mesmo padrão do Storage
- Implementação do primeiro agent single-tool
- Pipeline de ingestão de imagens
- Pipeline de extração de documentos

---

## [0.1.0] — 2026-06-08

### Adicionado
- 🎉 Início do projeto **claim-intelligence**
- Definição do domínio: análise inteligente de sinistros automotivos
- Pesquisa de viabilidade técnica e disponibilidade de dados
- Plano de cobertura AI-103 (~85% dos tópicos)
- Cronograma de 6 semanas com meta de prova em 15-31/07/2026

### Decisões arquiteturais
- **ADR-0001:** Foundry Agent Service como runtime de agents
- **ADR-0002:** Single-agent na fase inicial, evolução para multi-agent
- **ADR-0003:** Dados sintéticos para documentos PII (CNH, BO)
- **ADR-0004:** Híbrido EN/PT (código em inglês, comentários em português)
- **ADR-0005:** Resource Group isolado do projeto paligeri
- **ADR-0006:** Estratégia CONTEXT.md + Git para continuidade

---

## Convenções

### Tipos de mudança

- **Adicionado** — para novas funcionalidades
- **Modificado** — para mudanças em funcionalidades existentes
- **Depreciado** — para funcionalidades que serão removidas
- **Removido** — para funcionalidades removidas
- **Corrigido** — para correções de bugs
- **Segurança** — para mudanças relacionadas a vulnerabilidades

### Versionamento

- **MAJOR.MINOR.PATCH**
- **MAJOR** — mudanças incompatíveis na API
- **MINOR** — novas funcionalidades compatíveis
- **PATCH** — correções compatíveis

### Estrutura de entry

```markdown
## [versão] — YYYY-MM-DD

### Adicionado
- Funcionalidade X
- Funcionalidade Y

### Modificado
- Comportamento Z

### Corrigido
- Bug #123
```
