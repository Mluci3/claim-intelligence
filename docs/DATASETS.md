# Datasets

> **Documentação dos dados utilizados no projeto claim-intelligence.**
> Origem, licenças, tratamento e compliance.

---

## 📋 Visão Geral

Este projeto utiliza **exclusivamente dados públicos ou sintéticos** — nenhum dado pessoal real é processado em nenhum momento. Esta é uma decisão arquitetural fundamental documentada em [ADR-0003](decisions/0003-synthetic-data-for-pii-documents.md).

---

## 🚗 Dataset 1: Car Damage Severity

### Origem
- **Plataforma:** Kaggle
- **Autor:** Prajwal Bhamere
- **URL:** https://www.kaggle.com/datasets/prajwalbhamere/car-damage-severity-dataset
- **Licença:** CC0 - Public Domain

### Conteúdo
- ~1.500 imagens de veículos danificados
- Classificadas em 3 categorias de severidade:
  - `minor` (dano leve)
  - `moderate` (dano moderado)
  - `severe` (dano severo)

### Uso no Projeto
- **Treinamento** de Custom Vision para classificação de severidade
- **Teste** do tool `analyze_damage_image`
- **Demo** de pipeline end-to-end

### Localização Local
```
data/
└── car_damage_severity/
    ├── train/
    │   ├── minor/
    │   ├── moderate/
    │   └── severe/
    └── test/
        ├── minor/
        ├── moderate/
        └── severe/
```

### Compliance
- ✅ Dataset público sem restrições
- ✅ Sem PII (placas borradas/genéricas)
- ✅ Uso comercial permitido

---

## 🪪 Dataset 2: IDNet (Synthetic Driver Licenses)

### Origem
- **Plataforma:** Kaggle
- **Autor:** IDNet research team
- **URL:** https://www.kaggle.com/datasets/chitreshkr/idnet-identity-document-analysis
- **Licença:** Research use
- **Paper:** [arXiv 2408.01690](https://arxiv.org/html/2408.01690v1)

### Conteúdo
- 597.900 imagens **sintéticas** de driver licenses
- 10 estados americanos
- Inclui versões legítimas e forjadas (para detecção de fraude)
- **Totalmente gerado por AI** — nenhuma pessoa real

### Uso no Projeto
- **Teste** do tool `extract_cnh_data` (adaptado para contexto US/BR)
- **Demonstração** de Document Intelligence prebuilt-idDocument
- **Detecção de adulteração** (extensão futura)

### Localização Local
```
data/
└── idnet_sample/
    ├── california/
    ├── texas/
    └── new_york/
```

### Compliance
- ✅ Dataset 100% sintético
- ✅ Nenhuma pessoa real envolvida
- ✅ Uso para pesquisa permitido

### ⚠️ Limitação Conhecida
IDNet contém CNHs americanas. Para demonstração de contexto brasileiro, complementaremos com CNHs sintéticas brasileiras geradas manualmente (ver Dataset 4).

---

## 📄 Dataset 3: BOs Sintéticos (Boletins de Ocorrência)

### Origem
- **Geração própria** baseada em templates públicos
- **Referências:**
  - Modelo público Polícia Civil SP: https://www.policiacivil.sp.gov.br/
  - Modelo público Polícia Civil RJ
  - Formato padronizado SINESP

### Conteúdo (a gerar)
- 10-15 Boletins de Ocorrência fictícios
- Casos variados:
  - Colisão entre 2 veículos
  - Atropelamento
  - Furto/roubo de veículo
  - Acidente com vítima
  - Acidente sem vítima
- Dados 100% fictícios

### Estrutura Padrão de um BO
```
BOLETIM DE OCORRÊNCIA Nº [XXXX/2026]
DATA: [data fictícia]
LOCAL: [endereço fictício]

ENVOLVIDOS:
- Condutor 1: [nome fictício], CNH [fictícia]
- Condutor 2: [nome fictício], CNH [fictícia]

VEÍCULOS:
- Veículo 1: [modelo, placa fictícia]
- Veículo 2: [modelo, placa fictícia]

DESCRIÇÃO DOS FATOS:
[Narrativa fictícia do acidente]

DANOS REGISTRADOS:
[Descrição dos danos]
```

### Uso no Projeto
- **Teste** do tool `extract_bo_data`
- **Demo** de Document Intelligence Layout
- **Validação** de cross-checking de informações (BO ↔ apólice)

### Localização Local
```
data/
└── bo_synthetic/
    ├── bo_001_colisao.pdf
    ├── bo_002_atropelamento.pdf
    ├── bo_003_furto.pdf
    └── ...
```

### Compliance
- ✅ Dados 100% fictícios
- ✅ Templates baseados em modelos públicos
- ✅ Nomes, CPFs, placas inventados (formato válido, conteúdo falso)
- ⚠️ Marcado claramente como "EXEMPLO SINTÉTICO" em cada documento

---

## 📋 Dataset 4: CNHs Brasileiras Sintéticas

### Origem
- **Geração própria**
- Layout baseado em CNH brasileira padrão (Detran/SENATRAN)
- Layout público disponível

### Conteúdo (a gerar)
- 5-10 CNHs brasileiras fictícias
- Variações:
  - Categorias diferentes (B, AB, D)
  - Estados emissores diferentes
  - Validades diferentes (vigentes e vencidas)

### Uso no Projeto
- **Teste** do tool `extract_cnh_data` em contexto BR
- **Demo** de adaptação cultural do Document Intelligence

### Localização Local
```
data/
└── cnh_synthetic_br/
    ├── cnh_001_categoria_b.jpg
    ├── cnh_002_categoria_ab.jpg
    └── ...
```

### Compliance
- ✅ Dados 100% fictícios
- ✅ Marcado como "AMOSTRA - NÃO É CNH REAL"
- ✅ Layout baseado em modelo público SENATRAN

---

## 📑 Dataset 5: Apólices de Seguro Fictícias

### Origem
- **Criação própria** baseada em estruturas de apólices reais públicas
- Referências: SUSEP, sites de seguradoras (estruturas públicas)

### Conteúdo (a gerar)
- 10-15 apólices fictícias em formato Markdown e PDF
- Variações de cobertura:
  - Apólice básica (RCF apenas)
  - Apólice intermediária (RCF + colisão)
  - Apólice premium (compreensiva)

### Estrutura Padrão
```markdown
# APÓLICE DE SEGURO AUTOMOTIVO Nº [XXXX]

## SEGURADO
- Nome: [fictício]
- CPF: [fictício]
- CNH: [fictícia]

## VEÍCULO
- Marca/Modelo: [modelo real, placa fictícia]
- Ano: YYYY

## COBERTURAS
- [lista de coberturas]

## EXCLUSÕES
- [lista de exclusões]

## FRANQUIA
- Valor: R$ X.XXX,XX
- Percentual: X%

## VIGÊNCIA
- Início: DD/MM/YYYY
- Fim: DD/MM/YYYY
```

### Uso no Projeto
- **Indexação** no Azure AI Search (índice `policies-knowledge-base`)
- **Base de RAG** para consulta de coberturas
- **Teste** do tool `search_policies`

### Localização Local
```
data/
└── policies_synthetic/
    ├── apolice_001_basica.md
    ├── apolice_002_intermediaria.md
    └── ...
```

### Compliance
- ✅ Dados 100% fictícios
- ✅ Baseado em estruturas públicas de mercado
- ✅ Sem nenhum dado de pessoa real

---

## 🛡️ Princípios de Compliance

### LGPD by Design

1. **Nenhum dado real** — todos os datasets são públicos ou sintéticos
2. **Sem coleta de PII** — o sistema nunca processará dados reais durante o desenvolvimento
3. **Audit trail** — todo processamento é rastreável
4. **Anonimização** — datasets sintéticos não permitem reidentificação
5. **Direito ao esquecimento** — todos os dados podem ser removidos a qualquer momento

### Boas Práticas Aplicadas

- ✅ Datasets versionados (sem dados versionados — paths em `.gitignore`)
- ✅ Marcação visual em todos os documentos sintéticos
- ✅ Documentação clara da origem
- ✅ Licenças respeitadas
- ✅ Citação dos autores quando aplicável

---

## 📥 Como Baixar os Datasets

### Pré-requisitos
- Conta Kaggle ativa
- Kaggle CLI instalado: `pip install kaggle`
- Token API Kaggle configurado

### Comandos

```bash
# Car Damage Severity
kaggle datasets download -d prajwalbhamere/car-damage-severity-dataset -p data/car_damage_severity --unzip

# IDNet (sample, dataset completo é muito grande)
kaggle datasets download -d chitreshkr/idnet-identity-document-analysis -p data/idnet_sample --unzip
```

### Datasets Sintéticos (a gerar)

Os BOs, CNHs brasileiras e apólices serão gerados via:
- Script Python `scripts/generate_synthetic_data.py` (a desenvolver)
- Templates em `templates/`
- Dados fictícios em `data/templates/fake_data.yaml`

---

## 📊 Resumo

| Dataset | Tipo | Fonte | Compliance | Status |
|---------|------|-------|------------|--------|
| Car Damage Severity | Imagens | Kaggle público | ✅ | A baixar |
| IDNet | Imagens sintéticas | Kaggle (sintético) | ✅ | A baixar |
| BOs Sintéticos | PDFs | Geração própria | ✅ | A gerar |
| CNHs BR Sintéticas | Imagens | Geração própria | ✅ | A gerar |
| Apólices Fictícias | Markdown/PDF | Criação própria | ✅ | A gerar |
