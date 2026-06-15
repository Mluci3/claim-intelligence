# ADR-0004: Híbrido EN/PT — código em inglês, comentários em português

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucia

---

## Contexto

O projeto será publicado como portfolio público. Existem três abordagens para idioma:

1. Tudo em português (natural para Maria)
2. Tudo em inglês (padrão internacional)
3. Híbrido (código EN, comentários PT)

---

## Decisão

**Adotar padrão híbrido: nomes técnicos em inglês, comentários explicativos em português.**

### Regras

- ✅ **Inglês:** nomes de classes, funções, variáveis, arquivos, branches Git
- ✅ **Inglês:** documentação técnica formal (README, ARCHITECTURE)
- ✅ **Português:** comentários no código explicando lógica de negócio
- ✅ **Português:** docstrings com explicações detalhadas (após resumo em inglês)
- ✅ **Português:** ADRs e CHANGELOG (audience: Maria + tutoria)

### Exemplo

```python
def analyze_damage_image(image_url: str) -> DamageAnalysis:
    """
    Analyze vehicle damage in an image.

    Esta função consome o Azure AI Vision para detectar e
    classificar danos em fotos de veículos sinistrados.
    Retorna severidade, peças afetadas e confiança.

    Args:
        image_url: URL pública da imagem (Blob Storage SAS)

    Returns:
        DamageAnalysis com severidade, peças e confidence score
    """
    # Verifica se a URL é acessível antes de chamar a API
    # (evita custos com chamadas que falhariam)
    ...
```

---

## Consequências

### Positivas
- ✅ Código portable para times internacionais
- ✅ Comentários em PT facilitam compreensão durante aprendizado
- ✅ Portfolio acessível para recrutadores BR e internacionais
- ✅ Terminologia técnica em EN ajuda na prova AI-103 (em inglês)

### Negativas
- ⚠️ Inconsistência potencial se outras pessoas contribuírem
- ⚠️ Comentários em PT são "perdidos" para audiência internacional

### Mitigações
- README e docs principais em inglês para máxima alcance
- Glossário PT-EN no docs/ para conceitos chave
