# Architecture Decision Records (ADRs)

> **Decisões arquiteturais documentadas seguindo o padrão ADR.**
> Cada decisão importante do projeto é registrada em arquivo numerado para futura referência.

---

## 📋 O que é um ADR?

Um Architecture Decision Record (ADR) é um documento que captura uma decisão arquitetural importante junto com seu contexto e consequências.

**Por que ADRs?**
- 📜 **Histórico** — futuras pessoas (incluindo você daqui 6 meses) entendem o "porquê" das decisões
- 🔍 **Transparência** — alternativas consideradas estão documentadas
- 🔄 **Evolução** — decisões podem ser revisadas e marcadas como "superseded"
- 🏢 **Padrão enterprise** — adotado por Microsoft, Spotify, Netflix, etc.

---

## 📚 Índice de Decisões

| # | Título | Status | Data |
|---|--------|--------|------|
| [0001](0001-use-foundry-agent-service.md) | Foundry Agent Service como runtime de agents | ✅ Accepted | 2026-06-08 |
| [0002](0002-single-agent-first-multi-later.md) | Single-agent na fase 1, multi-agent na fase 3 | ✅ Accepted | 2026-06-08 |
| [0003](0003-synthetic-data-for-pii-documents.md) | Dados sintéticos para documentos PII | ✅ Accepted | 2026-06-08 |
| [0004](0004-hybrid-en-pt-language.md) | Híbrido EN/PT — código EN, comentários PT | ✅ Accepted | 2026-06-08 |
| [0005](0005-isolated-resource-group.md) | Resource Group isolado do projeto paligeri | ✅ Accepted | 2026-06-08 |
| [0006](0006-context-md-strategy.md) | Estratégia CONTEXT.md + Git para continuidade | ✅ Accepted | 2026-06-08 |

---

## 🎯 Status dos ADRs

- ✅ **Accepted** — decisão atualmente em vigor
- 🔄 **Proposed** — em discussão, ainda não aprovada
- ❌ **Rejected** — analisada e descartada
- 🗑️ **Superseded** — substituída por outra decisão (link para a nova)
- 📜 **Deprecated** — não mais aplicável

---

## ✍️ Como criar um novo ADR

### 1. Determinar o número

Próximo número sequencial. Não reutilize números, mesmo de ADRs rejeitados.

### 2. Criar arquivo

```bash
touch docs/decisions/000X-titulo-curto-em-kebab-case.md
```

### 3. Usar template

```markdown
# ADR-000X: Título da Decisão

**Status:** 🔄 Proposed
**Data:** YYYY-MM-DD
**Decisor:** Nome

---

## Contexto

Descreva o problema ou situação que motiva a decisão.

---

## Decisão

Declare claramente a decisão tomada.

---

## Consequências

### Positivas
- Benefícios esperados

### Negativas
- Trade-offs aceitos

### Mitigações
- Como compensar as negativas

---

## Alternativas Consideradas

### Alternativa 1: Nome

**Prós:** ...
**Contras:** ...
**Decisão:** Rejeitada porque...

---

## Referências

- Links úteis
```

### 4. Atualizar este índice

Adicione linha na tabela acima.

### 5. Commitar

```bash
git add docs/decisions/
git commit -m "docs(adr): adiciona ADR-000X sobre [tema]"
```

---

## 🔗 Referências

- [Architecture Decision Records (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [adr.github.io](https://adr.github.io/) — coleção de templates e ferramentas
- [Microsoft Azure Architecture Decision Records](https://docs.microsoft.com/azure/architecture/guide/design-principles/)
