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

### Em planejamento
- Provisioning dos recursos Azure (Foundry Hub, AI Vision, Doc Intel, Search, Storage)
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
