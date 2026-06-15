# ADR-0002: Single-agent na fase 1, evolução para multi-agent na fase 3

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucia (tutoria via Claude)

---

## Contexto

A certificação AI-103 cobre tanto **single-agent** quanto **multi-agent orchestration**. O projeto claim-intelligence poderia ser implementado de duas formas:

1. **Multi-agent desde o início** — 4 agents especializados (image, document, policy, decision)
2. **Single-agent inicialmente** — 1 agent com 5 tools, evoluindo para multi-agent

A escolha impacta a curva de aprendizado, robustez do projeto e cobertura da prova.

---

## Decisão

**Implementar single-agent na fase 1 (Semanas 1-2), evoluir para multi-agent na fase 3 (Semanas 3-4).**

Fase 1 foca em dominar fundamentos de agents (tool calling, threads, runs). Fase 3 adiciona complexidade de orquestração após domínio do básico.

---

## Consequências

### Positivas

- ✅ **Curva de aprendizado gradual** — dominar fundamentos antes de complexidade
- ✅ **Reuso de código** — tools desenvolvidos na fase 1 são reutilizados na fase 3
- ✅ **Cobertura dupla da prova** — projeto demonstra ambos os padrões
- ✅ **Iteração rápida** — single-agent mais simples de debugar e refinar
- ✅ **Evolução natural** — multi-agent emerge organicamente quando complexidade justifica
- ✅ **Portfolio evolutivo** — commits mostram progressão técnica clara

### Negativas

- ⚠️ **Refatoração na fase 3** — código single-agent precisa ser adaptado
- ⚠️ **Tempo total maior** — comparado a multi-agent direto bem planejado

### Mitigações

- Tools são desenhados desde o início com interfaces claras (SOLID), facilitando reuso
- Decisão de refatoração é documentada e versionada (CHANGELOG)
- Tempo adicional é absorvido pelo cronograma de 6 semanas com folga

---

## Arquitetura Esperada

### Fase 1: Single-Agent

```
USER
  ↓
┌──────────────────────────────┐
│   Agent: claim-processor     │
│                              │
│   Tools:                     │
│   • analyze_damage_image     │
│   • extract_bo_data          │
│   • extract_cnh_data         │
│   • search_policies          │
│   • calculate_repair_cost    │
└──────────────────────────────┘
  ↓
RESPONSE
```

### Fase 3: Multi-Agent

```
USER
  ↓
┌──────────────────────────────┐
│  Orchestrator Agent          │
└──────────────────────────────┘
  ↓        ↓        ↓        ↓
┌────┐ ┌────┐ ┌────┐ ┌────┐
│Img │ │Doc │ │Pol │ │Dec │
│Agt │ │Agt │ │Agt │ │Agt │
└────┘ └────┘ └────┘ └────┘
  ↓        ↓        ↓        ↓
RESPONSE (consolidada)
```

---

## Alternativas Consideradas

### Alternativa 1: Multi-agent desde o início

**Prós:**
- Cobre o tópico mais cobrado do AI-103 (30-35%) imediatamente
- Padrão mais sofisticado de portfolio

**Contras:**
- Curva muito íngreme para dominar Foundry pela primeira vez
- Alto risco de bugs difíceis de debugar em código mais complexo
- Sem base sólida de fundamentos antes da complexidade

**Decisão:** Rejeitada — pedagogicamente inferior.

### Alternativa 2: Manter single-agent até o fim

**Prós:**
- Simplicidade total
- Menos código para manter

**Contras:**
- Não cobre multi-agent orchestration (tópico pesado do AI-103)
- Portfolio limitado em sofisticação técnica
- Não demonstra capacidade de arquitetar sistemas complexos

**Decisão:** Rejeitada — não atende ao objetivo de certificação.

---

## Referências

- [AI-103 Skills Outline — Generative AI and Agentic Solutions](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
- [Microsoft Agent Framework](https://learn.microsoft.com/azure/ai-foundry/agents/)
- ADR-0001: Foundry Agent Service como runtime
