# ADR-0003: Dados sintéticos para documentos PII (CNH, BO, Apólices)

**Status:** ✅ Accepted
**Data:** 2026-06-08
**Decisor:** Maria Lucia (tutoria via Claude)

---

## Contexto

O projeto claim-intelligence processa documentos sensíveis típicos do domínio de seguros:

- **CNH** — documento de identidade com dados pessoais
- **BO (Boletim de Ocorrência)** — registro policial com PII de envolvidos
- **Apólices** — contratos com dados do segurado

Para desenvolvimento e demonstração, é necessário ter exemplos desses documentos. No entanto:

- ❌ **Dados reais** violam LGPD/GDPR (impossível obter consentimento de envolvidos em sinistros aleatórios)
- ❌ **Datasets públicos de CNH/BO brasileiros reais** não existem (e não deveriam existir)
- ❌ **Captura própria** geraria documentos de pessoas reais (sem autorização)

---

## Decisão

**Utilizar exclusivamente dados sintéticos para todos os documentos contendo PII no projeto.**

Origens autorizadas:
1. **Datasets públicos sintéticos** (ex: IDNet para driver licenses americanas)
2. **Geração própria** baseada em templates públicos (BOs, CNHs brasileiras, apólices)
3. **Dados fictícios** (nomes, CPFs, placas em formato válido mas conteúdo falso)

---

## Consequências

### Positivas

- ✅ **LGPD compliant by design** — zero risco de violação
- ✅ **Sem necessidade de DPO** — não há processamento de dados reais
- ✅ **Portfolio público** — projeto pode ser open-source sem restrições
- ✅ **Reprodutibilidade** — qualquer pessoa pode replicar os experimentos
- ✅ **Controle total** — sabemos exatamente o que esperar nos dados
- ✅ **Casos extremos** — podemos criar edge cases artificialmente (ex: CNH vencida, BO com inconsistências)
- ✅ **Alinhamento AI-103** — Responsible AI cobra essa prática (Privacy by design)

### Negativas

- ⚠️ **Trabalho de geração** — BOs, CNHs BR e apólices precisam ser criados manualmente
- ⚠️ **Realismo limitado** — dados sintéticos podem ser menos variados que dados reais
- ⚠️ **Validação restrita** — sem benchmarks contra dados reais de produção

### Mitigações

- Templates baseados em modelos públicos oficiais (Polícia Civil SP/RJ, SENATRAN)
- Geração programática via script Python para escalar quando necessário
- Adoção de IDNet (597k imagens sintéticas) para volume em testes
- Marcação visual clara em todos os documentos: "EXEMPLO SINTÉTICO - NÃO É REAL"

---

## Princípios de Geração de Dados Sintéticos

### CNH Brasileira Sintética

- Layout baseado em modelo oficial SENATRAN (público)
- Foto: imagem placeholder (silhueta genérica)
- Nome: nomes fictícios (não correspondentes a pessoas reais)
- CPF: gerado com algoritmo de validação, mas sem correspondência real
- Número CNH: 11 dígitos aleatórios
- Categorias: B, AB, D (variações)
- Estados emissores: variados
- Validades: vigentes e vencidas (para teste)
- **Marcação obrigatória:** watermark "AMOSTRA SINTÉTICA"

### Boletim de Ocorrência Sintético

- Template baseado em modelo Polícia Civil SP (público)
- Número BO: formato XXXX/YYYY (fictício)
- Data: datas fictícias
- Local: endereços fictícios
- Envolvidos: nomes fictícios
- Veículos: modelos reais com placas fictícias
- Narrativa: cenários típicos de sinistros (gerados manualmente)
- **Marcação obrigatória:** cabeçalho "DOCUMENTO DE EXEMPLO - NÃO É REAL"

### Apólice Sintética

- Estrutura baseada em padrões SUSEP (públicos)
- Seguradora: fictícia (ex: "SeguroFlow Brasil")
- Segurado: dados fictícios
- Veículo: modelo real com placa fictícia
- Coberturas: variadas (básica, intermediária, premium)
- Exclusões: padrão de mercado
- Valores: realistas mas não vinculados a apólices reais
- **Marcação obrigatória:** rodapé "APÓLICE FICTÍCIA PARA DEMONSTRAÇÃO"

---

## Datasets Aprovados

### Datasets Públicos Sintéticos

| Dataset | Origem | Uso |
|---------|--------|-----|
| Car Damage Severity | Kaggle (público) | Imagens de dano (sem PII) |
| IDNet | Kaggle (sintético) | Driver licenses sintéticas |

### Datasets de Geração Própria

| Dataset | Quantidade | Status |
|---------|-----------|--------|
| BOs sintéticos | 10-15 | A gerar |
| CNHs BR sintéticas | 5-10 | A gerar |
| Apólices fictícias | 10-15 | A gerar |

---

## Alternativas Consideradas

### Alternativa 1: Obter dados reais via parceria

**Prós:**
- Dados realistas de produção

**Contras:**
- Requer parceria formal com seguradora
- LGPD: necessário consentimento explícito de cada segurado
- Inviável para projeto de portfolio individual

**Decisão:** Rejeitada — não viável legalmente.

### Alternativa 2: Anonimização de dados reais

**Prós:**
- Mais realista que totalmente sintético

**Contras:**
- Risco residual de reidentificação
- Complexidade de processo de anonimização (k-anonimato, etc)
- Custo de DPO/jurídico

**Decisão:** Rejeitada — overhead injustificado para projeto de aprendizado.

### Alternativa 3: Dados sintéticos gerados por LLM

**Prós:**
- Rápido de gerar
- Variedade ilimitada

**Contras:**
- Risco de gerar dados que coincidam com pessoas reais
- LLMs podem produzir documentos visualmente inconsistentes
- Necessária validação humana de cada saída

**Decisão:** Parcialmente adotada — usaremos LLM para gerar **conteúdo textual** de BOs (narrativas), mas não para gerar dados estruturados (CPFs, números de documento).

---

## Implementação

### Script de Geração

Um script `scripts/generate_synthetic_data.py` será desenvolvido com:

```python
class SyntheticDataGenerator:
    """
    Gera documentos sintéticos para o projeto.

    Princípios:
    - Nomes via biblioteca Faker (locale pt_BR)
    - CPFs gerados com algoritmo de validação
    - Placas em formato válido (ABC-1234 ou ABC1D23 Mercosul)
    - Datas em range coerente
    - Marcação visual obrigatória
    """

    def generate_cnh(self) -> dict: ...
    def generate_bo(self) -> dict: ...
    def generate_policy(self) -> dict: ...
```

### Validação

Cada documento gerado deve:
1. ✅ Ter marcação visual de "exemplo sintético"
2. ✅ Não corresponder a nenhuma pessoa real conhecida
3. ✅ Manter formato válido para teste de extração
4. ✅ Ser armazenado em diretório claramente identificado como sintético

---

## Referências

- [LGPD - Lei Geral de Proteção de Dados](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [GDPR - General Data Protection Regulation](https://gdpr.eu/)
- [Microsoft Responsible AI Standard](https://www.microsoft.com/ai/responsible-ai)
- [IDNet Paper - Synthetic Identity Documents](https://arxiv.org/html/2408.01690v1)
- [SUSEP - Modelos de Apólices](https://www.gov.br/susep/)
