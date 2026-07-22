# AI-103 — Manual de Estudos (Hands-on)

> **Registro vivo de aprendizado prático.**
> Cada sessão hands-on no projeto vira uma entrada aqui: o que foi feito, onde clicar, erros encontrados e o porquê. Serve como material de revisão pré-prova, complementar ao `CONTEXT.md` (que foca em estado do projeto, não em conceitos).

---

## Índice

1. [Fundamentos: Subscription → Resource Group → Recursos](#1-fundamentos-subscription--resource-group--recursos)
2. [Azure AI Foundry: Hub vs Project vs Connection](#2-azure-ai-foundry-hub-vs-project-vs-connection)
3. [Criando um recurso no Portal](#3-criando-um-recurso-no-portal)
4. [Soft-delete e purge](#4-soft-delete-e-purge)
5. [Conectando um recurso ao Foundry Project](#5-conectando-um-recurso-ao-foundry-project)
6. [Autenticação: DefaultAzureCredential na prática](#6-autenticação-defaultazurecredential-na-prática)
7. [Armadilhas encontradas (erros reais)](#7-armadilhas-encontradas-erros-reais)
8. [Free tier: disponibilidade varia por região](#8-free-tier-disponibilidade-varia-por-região)

---

## 1. Fundamentos: Subscription → Resource Group → Recursos

Hierarquia de organização no Azure, do mais amplo ao mais específico:

```
Tenant (Microsoft Entra ID)
└── Subscription (unidade de billing)
    └── Resource Group (agrupamento lógico, sem custo próprio)
        └── Recursos (Foundry Hub, Cognitive Services, Storage, etc.)
```

- **Subscription**: unidade de cobrança e de limites de quota. No projeto, usamos "Azure subscription 1".
- **Resource Group (RG)**: contêiner lógico — não tem custo, existe só para agrupar/isolar recursos que têm o mesmo ciclo de vida (criar e deletar juntos). Decisão do projeto (ADR-0005): RG isolado `rg-claim-intelligence`, separado de outros projetos pessoais (ex: `paligeri`), para não misturar billing nem correr risco de deletar recurso errado.
- **Region**: onde o recurso fisicamente roda. Recursos que vão se comunicar (Hub, Vision, Storage) devem estar na **mesma region** sempre que possível — evita latência extra e é pré-requisito de algumas features (ex: managed network isolation).

**Ponto de prova:** deletar um Resource Group deleta *tudo* dentro dele — é a forma mais comum de "limpar" um ambiente de estudo/lab inteiro de uma vez.

---

## 2. Azure AI Foundry: Hub vs Project vs Connection

Três conceitos que a prova adora confundir:

| Conceito | O que é | Escopo |
|---|---|---|
| **Hub** | Camada de infraestrutura compartilhada: rede, segurança, managed identity, billing. Tipo de recurso ARM: `Foundry` | Pode conter múltiplos Projects |
| **Project** | Onde você de fato trabalha: cria agents, roda experimentos, conecta recursos. Tipo ARM: `Foundry project` | Pertence a um único Hub |
| **Connection** | Referência gerenciada (endpoint + credencial) a um serviço externo (Vision, Storage, Search, OpenAI...). O agent nunca guarda a credencial diretamente, só o nome da connection | Pode ser **Hub-level** (compartilhada entre todos os Projects do hub) ou **Project-level** (isolada a um Project) |

**Por que Connection existe (não é burocracia):**
- Rotação de credencial sem redeploy do agent
- RBAC granular (Managed Identity só acessa o que tem connection registrada)
- Portabilidade entre ambientes (dev/prod trocam só a connection, código do agent não muda)

**Erro comum:** ter o recurso provisionado no Azure **não é suficiente**. Sem virar uma Connection dentro do Project, ele é invisível para agents e para o SDK (`client.connections.list()` não retorna nada).

No projeto: Hub = `hub-claim-intelligence`, Project = `claim-analyzer`, ambos em `rg-claim-intelligence` / `eastus2`.

---

## 3. Criando um recurso no Portal

Passo a passo genérico (usado para o Azure AI services / Vision):

1. [portal.azure.com](https://portal.azure.com) → **"Create a resource"**
2. Buscar o tipo de serviço (ex: **"Azure AI services"** — multi-serviço, cobre Vision/Language/Doc Intelligence num único recurso)
3. Preencher:
   - **Subscription**: a mesma do resto do projeto
   - **Resource group**: `rg-claim-intelligence` (nunca criar um novo RG por recurso)
   - **Region**: igual ao Hub (`East US 2` no projeto)
   - **Name**: convenção `<serviço>-claim-intelligence` (ex: `vision-claim-intelligence`)
   - **Pricing tier**: recursos multi-serviço geralmente só oferecem **S0** (pay-as-you-go); tiers F0 (free) costumam existir só em recursos single-service
4. Aceitar o "Responsible AI Notice" (obrigatório em qualquer serviço cognitivo)
5. **Review + Create**

**Nota sobre tipos de recurso — atenção redobrada aqui:**
- **"Computer Vision"** (single-service, kind `ComputerVision`) ≠ **"Azure AI services"** (multi-service, kind `CognitiveServices`). O segundo é o que integra melhor com o Foundry.
- O Hub em si roda sobre um recurso kind `AIServices` — um terceiro kind, reservado para a infraestrutura do próprio Foundry, criado automaticamente quando você provisiona o Hub.

---

## 4. Soft-delete e purge

Recursos Cognitive Services (Vision, Doc Intelligence, Language, OpenAI, etc.) têm **soft-delete**: ao deletar, o nome fica "reservado"/protegido por um período de retenção — você não consegue recriar outro recurso com o mesmo nome até:

- **Esperar o período de retenção expirar**, ou
- **Purgar manualmente**:
  ```
  az cognitiveservices account purge \
    --location <region> \
    --resource-group <rg> \
    --name <nome-do-recurso>
  ```

Para ver o que está "preso" em soft-delete:
```
az cognitiveservices account list-deleted -o table
```

**Ponto de prova:** essa é uma proteção contra exclusão acidental (parecido com soft-delete de Key Vault). Em ambiente de estudo/lab, você vai esbarrar nisso toda vez que recriar um recurso com o mesmo nome rapidamente.

---

## 5. Conectando um recurso ao Foundry Project

No Foundry Portal ([ai.azure.com](https://ai.azure.com)) → abrir o Project → **Management Center** → **Connected resources** → **+ New connection**.

O modal tem duas abas:

- **"Procurar" (Browse)**: só lista recursos que o Foundry reconhece nativamente por categoria — Azure AI Search, Azure OpenAI, Storage Account, Cosmos DB, Application Insights, Bing Grounding, etc. Cada categoria tem seu próprio card na tela "Escolher uma conexão".
- **"Conectar Manualmente" / categoria "Chave da API" (Personalizado)**: para qualquer recurso Cognitive Services que **não** tem card dedicado (ex: Computer Vision, Document Intelligence standalone) — você fornece **endpoint** e **key** manualmente.

**Regra prática:** se o recurso não aparece na busca automática, não é erro — é porque ele se conecta pela categoria genérica **"Chave da API"**, não por uma categoria específica.

Pegar endpoint e key:
- Portal → recurso → **"Keys and Endpoint"** (menu lateral), ou via CLI:
  ```
  az cognitiveservices account show --name <nome> --resource-group <rg> --query "properties.endpoint" -o tsv
  az cognitiveservices account keys list --name <nome> --resource-group <rg>
  ```

---

## 6. Autenticação: DefaultAzureCredential na prática

O SDK `azure-ai-projects` (v2.x) usa `AIProjectClient(endpoint=..., credential=...)`. Na prática local usamos `DefaultAzureCredential()`, que tenta métodos de autenticação em cascata, nesta ordem (resumida):

1. Variáveis de ambiente (service principal via `AZURE_CLIENT_ID`/`AZURE_TENANT_ID`/`AZURE_CLIENT_SECRET`)
2. Managed Identity (se rodando dentro do Azure)
3. **Azure CLI** (`az login`) ← o que usamos em dev local
4. Outras (VS Code, PowerShell, etc.)

Por isso `az login` resolve tudo: ele grava um token em `~/.azure` que qualquer processo do seu usuário consegue reaproveitar, em qualquer pasta — não tem relação com o diretório do projeto.

**Nota de versão do SDK:** `azure-ai-projects` 1.x usava `AIProjectClient.from_connection_string(...)`. A partir da 2.x isso foi descontinuado em favor do endpoint direto do Project (`https://<hub>.services.ai.azure.com/api/projects/<project>`, visível em Project → Overview → "Project endpoint"). Manter o `.env` alinhado com a versão do SDK instalada evita erro de variável errada.

Script de smoke test do projeto: `test_azure_connection.py` (raiz do repo) — autentica e lista `client.connections.list()`.

---

## 7. Armadilhas encontradas (erros reais)

Registro de erros reais batidos durante o desenvolvimento — cada um é matéria de prova disfarçada de bug.

| Sintoma | Causa raiz | Lição |
|---|---|---|
| `ModuleNotFoundError: No module named 'azure'` | Script rodando com o Python do sistema/pyenv, não o `.venv` do projeto | Sempre confirmar `which python` aponta pro `.venv/bin/python` antes de rodar |
| `zsh: command not found: az` | Azure CLI não instalado | `brew install azure-cli`; é pré-requisito separado do SDK Python |
| Criar recurso e nome "já existe" mesmo após deletar | Soft-delete prendendo o nome | `az cognitiveservices account purge` |
| **Erro 400 ao criar connection no Foundry** | Categoria de connection errada — estava tentando conectar um recurso Cognitive Services pela categoria "Fábrica de IA do Azure" (que espera outro Hub), não pela categoria "Chave da API" | Recurso sem card dedicado na aba "Procurar" → sempre cai em "Chave da API" (conexão manual) |
| `client.connections.list()` retorna vazio | Recurso existe no Azure mas nunca foi registrado como Connection no Project | Provisionar recurso ≠ conectar recurso; são dois passos manuais separados |
| Leitura de arquivos do projeto trava com "Operation timed out" | Arquivos "dataless" — placeholders do iCloud Drive (Desktop & Documents sync) evictados do disco local | Reboot ou "Baixar Agora" no Finder materializa o conteúdo de volta |
| `Deployment ... failed` / `InsufficientResourcesAvailable` ao criar Azure AI Search Free | Região sem capacidade disponível para novos serviços Free naquele momento — não é erro de configuração | Trocar de região resolve (ex: East US 2 → East US); antes de migrar para tier pago só por causa disso, calcular custo fixo real (S1 ≈ US$ 250/mês) contra o volume de uso real do projeto |

---

## 8. Free tier: disponibilidade varia por região

Nem toda região do Azure tem capacidade de Free tier disponível o tempo todo — principalmente em serviços com pegada mais pesada como Azure AI Search. Isso **não é erro de configuração**, é limitação real de capacidade da Microsoft naquele momento/região.

**Princípio adotado no projeto:** sempre tentar Free tier primeiro; se a região planejada não tiver capacidade, trocar de região mantendo Free em vez de migrar para tier pago por conveniência. Antes de aceitar um custo fixo recorrente, sempre estimar o valor real (ex: AI Search S1 ≈ US$ 250/mês, cobrado mesmo sem uso) e comparar com o volume de uso real do projeto — em projetos de estudo/portfolio, quase nunca se justifica.

Caso real: `search-claim-intelligence` ficou em **East US** em vez de **East US 2** (região do resto do stack) por esse motivo — latência extra entre regiões próximas é desprezível para o volume de uso do projeto, então a economia venceu a consistência de região.

---

## Como manter este manual atualizado

Ao final de cada sessão hands-on, adicionar:
1. Uma entrada na seção relevante (ou nova seção, se for conceito novo)
2. Qualquer erro novo na tabela da seção 7, no formato Sintoma / Causa raiz / Lição
3. Data da sessão, se for uma decisão ou comportamento que pode mudar (versão de SDK, preview features)
