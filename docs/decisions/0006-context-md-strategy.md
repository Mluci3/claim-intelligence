# ADR-0006: Context Engineering Strategy — CONTEXT.md + Git para continuidade entre sessões de AI pair programming

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucilene

---

## Contexto

Sessões de **AI pair programming** têm **limite de contexto** (tokens). Em projetos longos como claim-intelligence (6 semanas, múltiplas sessões), é necessária estratégia de *context engineering* para manter continuidade sem perder decisões e estado.

Alternativas avaliadas:

1. **Memória nativa paga da ferramenta de IA** — memória persistente, mas com custo recorrente e lock-in
2. **Apenas memória automática gratuita** — pode falhar em conversas muito longas
3. **CONTEXT.md + Git** — fonte da verdade externa
4. **Híbrido CONTEXT.md + Memory + Git** — máxima resiliência

---

## Decisão

**Adotar estratégia híbrida com 3 camadas de continuidade:**

### Camada 1: Git como fonte da verdade
- Todo código e documentação versionados
- CHANGELOG.md registra cada mudança
- ADRs documentam decisões arquiteturais
- Branches por feature/fase

### Camada 2: CONTEXT.md como ponte entre sessões
- Arquivo único com estado atual do projeto
- Atualizado ao final de cada sessão de desenvolvimento
- Em novo chat: cole o conteúdo + diga "continue de onde paramos"

### Camada 3: Memória automática do agente de codificação (gratuita)
- Captura contexto recente automaticamente
- Backup de informações entre sessões próximas

---

## Estrutura do CONTEXT.md

```markdown
# CONTEXT.md

## 📋 Identificação
- Projeto, certificação, datas

## 🎯 Objetivo
- Visão de alto nível

## 👤 Perfil
- Quem é a desenvolvedora

## 🏗️ Decisões (link para ADRs)

## 🔧 Stack Técnico
- Resources Azure
- SDKs Python
- Datasets

## 📅 Cronograma

## 📊 Estado Atual
- ✅ Concluído
- 🔄 Em andamento
- ⏭️ Próximos passos

## 🚧 Bloqueios Ativos

## 🧠 Contexto Importante para Próxima Sessão
- Decisões recentes
- Padrão de operação acordado
- Tom da relação

## 🔄 Como retomar em novo chat
- Instruções claras
```

---

## Consequências

### Positivas
- ✅ **Resiliência** — 3 camadas garantem continuidade
- ✅ **Gratuito** — não requer plano pago de nenhuma ferramenta
- ✅ **Auditável** — histórico no Git mostra evolução
- ✅ **Portabilidade** — funciona com qualquer LLM/agente de codificação (CLI, IDE plugin, etc.)
- ✅ **Documentação viva** — projeto se documenta sozinho
- ✅ **Onboarding rápido** — qualquer pessoa entende em 5 min
- ✅ **Audit trail** — útil para portfolio (recrutadores veem evolução)

### Negativas
- ⚠️ **Disciplina necessária** — CONTEXT.md precisa ser atualizado ao final de cada sessão
- ⚠️ **Overhead** — alguns minutos por sessão para atualizar

### Mitigações
- Atualização do CONTEXT.md é parte do "ritual de fim de sessão"
- Lembrete de atualizar ao final de cada bloco de trabalho
- Template padronizado facilita atualização rápida

---

## Protocolo de Atualização

### Ao final de cada sessão de desenvolvimento

1. **Editar CONTEXT.md**:
   - Atualizar "Última atualização" (data)
   - Mover items de "🔄 Em andamento" para "✅ Concluído"
   - Atualizar "⏭️ Próximos passos"
   - Adicionar/remover "🚧 Bloqueios Ativos"
   - Resumir em "🧠 Contexto Importante para Próxima Sessão"

2. **Commitar no Git**:
   ```bash
   git add CONTEXT.md
   git commit -m "docs(context): atualiza estado pós-sessão YYYY-MM-DD"
   git push
   ```

3. **Se sessão produziu decisão importante**:
   - Criar novo ADR em `docs/decisions/`
   - Adicionar entry no CHANGELOG.md

### Ao iniciar nova sessão (mesma sessão de AI pair programming)

- CONTEXT.md é consultado no início para retomar contexto

### Ao iniciar nova sessão de AI pair programming

1. Maria abre uma nova sessão
2. Cola conteúdo do CONTEXT.md
3. Diz: *"Sou Maria. Estamos no projeto claim-intelligence para AI-103. Continue de onde paramos baseado neste CONTEXT.md."*
4. O agente lê o contexto e retoma

---

## Alternativas Consideradas

### Alternativa 1: Apenas memória nativa paga da ferramenta de IA

**Prós:**
- Memória persistente nativa
- Sem necessidade de manter CONTEXT.md

**Contras:**
- Requer plano pago (custo recorrente)
- Lock-in na plataforma específica
- Sem versionamento de decisões

**Decisão:** Rejeitada — solução gratuita é igualmente eficaz com disciplina.

### Alternativa 2: Apenas Memory (gratuito)

**Prós:**
- Zero overhead manual

**Contras:**
- Memory pode falhar em conversas muito longas
- Sem versionamento
- Sem auditoria de decisões

**Decisão:** Adotada como camada complementar, não como única estratégia.

### Alternativa 3: Notion/Confluence externo

**Prós:**
- Interface rica para documentação

**Contras:**
- Fora do repositório de código
- Risco de divergência entre código e docs
- Custo adicional

**Decisão:** Rejeitada — documentação fica junto ao código (princípio "docs as code").

---

## Referências

- [The C4 Model — Communication of Software Architecture](https://c4model.com/)
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)
- [ADR GitHub Organization](https://adr.github.io/)
