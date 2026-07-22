# ADR-0005: Resource Group isolado do projeto paligeri

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucilene

---

## Contexto

Existem 2 estratégias para provisionar recursos Azure:

1. **Reaproveitar recursos do paligeri** (Foundry project existente, AI Search criado)
2. **Criar tudo do zero** em novo Resource Group isolado

---

## Decisão

**Criar todos os recursos do claim-intelligence em Resource Group isolado:**

```
rg-claim-intelligence (East US 2)
├── hub-claim-intelligence (Foundry Hub)
├── vision-claim-intelligence (AI Vision)
├── docintel-claim-intelligence (Document Intelligence)
├── search-claim-intelligence (AI Search)
└── stclaimintelligence (Blob Storage)
```

Projeto paligeri (`rg-ai-certifications-study`) permanece intocado.

---

## Consequências

### Positivas
- ✅ **Isolamento de custos** — fácil rastrear gasto por projeto
- ✅ **Sem risco cruzado** — alteração em um projeto não afeta o outro
- ✅ **Limpeza simples** — `az group delete` remove tudo de uma vez
- ✅ **Tags por projeto** — `Environment=Study`, `Project=ClaimIntelligence`
- ✅ **Padrão enterprise** — cada produto/projeto tem seu RG
- ✅ **RBAC granular** — controle de acesso por projeto

### Negativas
- ⚠️ **Mais recursos provisionados** — consome mais crédito (mas ainda dentro do orçamento)
- ⚠️ **Tempo de setup** — provisioning de novos recursos (~30 min)

### Mitigações
- Budget alerts específicos por RG monitoram custos
- Recursos serão deletados ao final do projeto (ou após prova)
- Free tiers utilizados onde possível (AI Search Free, AI Vision F0)

---

## Naming Convention

Padrão Microsoft Cloud Adoption Framework:

```
{resource-type}-{project-name}[-{environment}]
```

Exemplos:
- `rg-claim-intelligence` (Resource Group)
- `hub-claim-intelligence` (Foundry Hub)
- `vision-claim-intelligence` (AI Vision)
- `stclaimintelligence` (Storage — sem hífens)

Tags obrigatórias:
- `Environment=Study`
- `Project=ClaimIntelligence`
- `Owner=Maria`
- `Certification=AI-103`
