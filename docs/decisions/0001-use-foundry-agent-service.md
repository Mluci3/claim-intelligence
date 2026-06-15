# ADR-0001: Usar Foundry Agent Service como runtime de agents

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucia (tutoria via Claude)

---

## Contexto

O projeto claim-intelligence requer execução de agents inteligentes que combinam múltiplas ferramentas (análise de imagem, extração de documentos, busca semântica). Existem duas abordagens principais para implementar isso no Azure:

1. **Implementação manual** com Azure OpenAI direto + código Python customizado
2. **Foundry Agent Service** — runtime gerenciado pela Microsoft

A escolha impacta diretamente:
- Quantidade de código a manter
- Capacidade de evolução para multi-agent
- Alinhamento com a certificação AI-103
- Padrões enterprise de mercado

---

## Decisão

**Adotar Foundry Agent Service como runtime padrão de agents.**

Toda lógica de orquestração de agents será delegada ao serviço gerenciado da Microsoft, reservando código customizado apenas para tools de negócio específicas.

---

## Consequências

### Positivas

- ✅ **Redução de código** — sem necessidade de implementar manualmente state management, retries, function calling logic
- ✅ **Observability built-in** — traces, metrics, logs nativos sem código adicional
- ✅ **Evaluations built-in** — groundedness, relevance, safety sem implementação manual
- ✅ **Alinhamento AI-103** — Foundry Agent Service é o padrão central da certificação
- ✅ **Threads gerenciadas** — memória de conversa sem código customizado
- ✅ **Tools nativos** — `azure_ai_search`, `code_interpreter`, `bing_grounding`, `openapi` sem implementação
- ✅ **Escalabilidade** — gerenciado pela Microsoft, sem provisionamento manual
- ✅ **Portfolio enterprise** — padrão usado por empresas em produção

### Negativas

- ⚠️ **Lock-in Azure** — código não é portável para outras clouds
- ⚠️ **Dependência de feature releases** — novas capacidades dependem da Microsoft
- ⚠️ **Custo** — serviço gerenciado tem premium sobre implementação self-hosted
- ⚠️ **Beta features** — algumas funcionalidades ainda em preview

### Mitigações

- A camada de tools (lógica de negócio) será desacoplada do Foundry para facilitar migração futura
- Custo será monitorado via Azure Cost Management com budget alerts
- Apenas features GA serão usadas em código de produção; features preview ficam isoladas em ramo experimental

---

## Alternativas Consideradas

### Alternativa 1: Azure OpenAI direto + LangChain

**Prós:**
- Mais portável (LangChain funciona com qualquer LLM)
- Maior controle sobre cada step
- Sem lock-in

**Contras:**
- Muito código boilerplate
- Sem observability nativa
- Não cobre o tópico central do AI-103
- Não é padrão enterprise Azure

**Decisão:** Rejeitada — o projeto é especificamente para AI-103, certificação que cobra Foundry Agent Service.

### Alternativa 2: Semantic Kernel

**Prós:**
- Framework Microsoft oficial
- Bom para multi-agent

**Contras:**
- Complementar ao Foundry, não substituto
- Mais código que Foundry Agent Service
- Documentação ainda em evolução

**Decisão:** Pode ser explorada em fase futura como complemento, não como substituto.

### Alternativa 3: LangGraph

**Prós:**
- Excelente para fluxos complexos
- Maturidade do ecossistema LangChain

**Contras:**
- Não é nativo Azure
- Sem alinhamento com AI-103
- Sem observability Azure nativa

**Decisão:** Rejeitada por não alinhar com objetivo de certificação.

---

## Referências

- [Azure AI Foundry Agent Service Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [AI-103 Study Guide — Microsoft Learn](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects)
