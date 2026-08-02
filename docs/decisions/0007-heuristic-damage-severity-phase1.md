# ADR-0007: Classificação heurística de severidade na fase 1 (Custom Vision adiado)

**Status:** ✅ Accepted
**Data:** 2026-08-02
**Decisor:** Maria Lucilene

---

## Contexto

A tool `analyze_damage_image` do agent `claim-processor` precisa estimar a severidade de dano de um veículo a partir de uma foto. O README original previa "Treinamento de Custom Vision para classificação de severidade", mas isso exige provisionar recursos novos (Custom Vision Training + Prediction), rotular o dataset (1.631 imagens já baixadas em `data/car_damage_severity/`) e treinar um modelo — trabalho real antes de qualquer tool funcionar ponta a ponta.

Duas alternativas avaliadas:

1. **Heurística sobre Azure AI Vision (Image Analysis)** — usa o recurso já provisionado e conectado (`vision-claim-intelligence`), aplica regras simples sobre as tags genéricas retornadas (caption, tags, confidence) para estimar minor/moderate/severe.
2. **Treinar Custom Vision primeiro** — mais fiel à visão original do projeto, mas adia a entrega do agent funcional.

---

## Decisão

**Implementar a heurística agora (fase 1), documentar a limitação explicitamente, e tratar Custom Vision como evolução futura.**

Justificativa: o objetivo imediato é destravar o loop completo de tool calling do agent (arquitetura, integração com a connection do Foundry, parsing da resposta) — que é o que a AI-103 avalia no domínio de Computer Vision. A precisão da classificação em si é secundária nesta fase e será resolvida separadamente.

---

## Consequências

### Positivas
- ✅ Agent funcional ponta a ponta ainda hoje, sem depender de mais provisionamento
- ✅ Sem custo adicional — reaproveita a connection do Vision já existente
- ✅ Ensina o padrão de Function Tool completo (schema, loop de tool calling, parsing de resposta)

### Negativas
- ⚠️ Classificação de severidade é frágil — tags genéricas do Image Analysis não foram treinadas para diferenciar dano automotivo por gravidade
- ⚠️ Pode gerar `"indeterminado"` com frequência em imagens sem palavras-chave reconhecíveis

### Mitigações
- Tool retorna explicitamente um campo `note` avisando que é heurística, não classificador treinado
- Instructions do agent (ADR já embutido no `create_agent.py`) já orientam recomendar "análise manual" quando a evidência for insuficiente — a resposta heurística fraca deve empurrar nessa direção, não forçar uma decisão

---

## Alternativas Consideradas

### Alternativa 1: Custom Vision Training + Prediction desde já

**Prós:**
- Classificação real, treinada no dataset do projeto
- Custom Vision tem tier Free (F0) — não geraria custo direto para o volume do projeto

**Contras:**
- Mais dois recursos Azure para provisionar, conectar e documentar
- Exige rotular/subir o dataset na ferramenta do Custom Vision antes de qualquer resultado
- Atrasa a validação do pipeline do agent como um todo

**Decisão:** Adiada, não rejeitada — vira próximo passo natural depois que o agent estiver completo com todas as tools básicas.

---

## Referências

- [Azure AI Vision — Image Analysis](https://learn.microsoft.com/azure/ai-services/computer-vision/overview-image-analysis)
- [Azure AI Custom Vision](https://learn.microsoft.com/azure/ai-services/custom-vision-service/overview)
- `src/claim_intelligence/tools/vision.py`
