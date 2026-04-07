# Architecture GOVAIAPP

## Vue d'ensemble

GOVAIAPP est une application de demonstration de gouvernance IA composee
de 4 couches independantes qui communiquent via HTTP et appels de fonctions.

```
+---------------------+        +---------------------+
|   UI (Streamlit)    | ---->  |   API (FastAPI)      |
|   :8501             | HTTP   |   :8000              |
+---------------------+        +----------+----------+
                                           |
                      +--------------------+--------------------+
                      |                    |                    |
              +-------v------+    +--------v-------+   +-------v--------+
              | Orchestrator |    | RAG Retriever   |   | Foundry Client |
              | (app/agents) |    | (app/rag)       |   | (app/foundry)  |
              +--------------+    +--------+--------+   +-------+--------+
                                           |                    |
                                  +--------v--------+   +------v---------+
                                  | Azure AI Search |   | Azure AI       |
                                  | (ou stub local) |   | Foundry Agents |
                                  +-----------------+   +----------------+
```

## Pipeline AutoGen (module autogen/)

Pipeline autonome d'orchestration multi-agents metier,
independant de l'API. Executable en CLI ou integrable dans d'autres systemes.

```
Contexte entreprise (texte)
        |
        v
+---------------------+
| VeilleExterneAgent  |  --> Foundry AgentExterne (gpt-5-nano)
+---------------------+       ou stub local
        |
        v
+---------------------+
| RagInterneAgent     |  --> Foundry AgentRAG (gpt-5-chat + Azure AI Search)
+---------------------+       ou stub local
        |
        v
+-------------------------+
| ProducteurPolitiqueAgent|  --> Foundry AgentProducteur (gpt-5-chat + Files)
+-------------------------+       ou stub local
        |
        v
Politique de gouvernance IA (markdown)
```

Orchestration : `RoundRobinGroupChat` (AG2 0.7), terminaison apres 4 messages
(user + 3 agents).

---

## Composants

### 1. UI -- Streamlit (`app/ui/app.py`)

- Page unique, formulaire avec 5 champs
- Appelle l'API via HTTP POST `/generate-policy`
- Affiche un indicateur de mode (Foundry / Stub)
- Gestion d'erreurs : ConnectError, Timeout, HTTP 4xx/5xx

### 2. API -- FastAPI (`app/api/`)

| Endpoint           | Methode | Description                          |
|---------------------|---------|--------------------------------------|
| `/health`           | GET     | Health check (`{"status": "ok"}`)    |
| `/generate-policy`  | POST    | Genere une politique de gouvernance  |

Logique de `/generate-policy` :
1. Si `FOUNDRY_ENABLED=true` et env vars presentes -> appel Foundry
2. Si Foundry echoue -> fallback automatique vers stub
3. Mode stub : RAG retriever + template markdown

Schemas Pydantic :
- `CompanyContext` : entree (nom, secteur, maturite, principes, contraintes)
- `PolicyDraftResponse` : sortie (policy_markdown, sources[])

### 3. Orchestrator -- Stub + Foundry (`app/agents/orchestrator.py`)

- `generate_policy()` : mode stub, remplace les variables du template
  `data/policy_template.md` avec les donnees du contexte
- `generate_policy_foundry()` : construit un prompt structure, appelle
  `AgentProducteur` via le client Foundry

### 4. RAG (`app/rag/`)

- `retriever.py` : point d'entree unique `retrieve(query)`
  - Azure AI Search si configure (3 env vars)
  - Sinon stub local : parse `data/watch/veille_cache.md`
- `_azure_client.py` : client Azure AI Search avec `SearchClient`

### 5. Client Foundry (`app/foundry/client.py`)

- `is_foundry_enabled()` : verifie `FOUNDRY_ENABLED`, endpoint et agent ID
- `call_foundry_agent()` : workflow AgentsClient
  `get_agent -> create thread -> create message -> run -> list messages`
- Authentification : `DefaultAzureCredential` (Entra ID, pas de cle API)

### 6. AutoGen Pipeline (`autogen/`)

Module autonome d'orchestration multi-agents :

| Fichier                              | Role                                |
|--------------------------------------|-------------------------------------|
| `orchestrator.py`                    | Pipeline RoundRobin (async + sync)  |
| `config/foundry_config.py`          | Config centralisee, client generique|
| `agents/veille_externe_agent.py`    | Veille reglementaire externe        |
| `agents/rag_interne_agent.py`       | Enrichissement RAG interne          |
| `agents/producteur_politique_agent.py`| Production de la politique finale  |

Chaque agent :
- Herite de `BaseChatAgent` (AG2 0.7)
- Appelle son homologue Foundry si configure
- Fallback avec message `[FALLBACK ...]` si Foundry echoue
- Stub avec message `[STUB ...]` si non configure

### 7. Agents Copilot (`.github/agents/`)

4 agents GitHub Copilot pour le workflow de developpement :

| Agent      | Fichier                      | Role                        |
|------------|------------------------------|-----------------------------|
| Dev        | `01-dev.agent.md`            | Developpe le code           |
| QA         | `02-qa.agent.md`             | Tests et detection de bugs  |
| Doc        | `03-doc.agent.md`            | Documentation               |
| Validator  | `04-Validator.agent.md`      | Revue et validation PR      |

---

## Modes de fonctionnement

| Mode               | Condition                                    | Comportement                |
|--------------------|----------------------------------------------|-----------------------------|
| Foundry            | `FOUNDRY_ENABLED=true` + env vars presentes  | Appel agents Azure AI Foundry|
| Stub local         | Foundry absent ou `FOUNDRY_ENABLED=false`    | Template + RAG stub local   |
| Fallback auto      | Foundry configure mais en erreur             | Bascule silencieuse vers stub|

---

## Flux de donnees -- generation de politique

```
1. Utilisateur remplit le formulaire (UI Streamlit)
2. UI envoie POST /generate-policy { CompanyContext }
3. API verifie is_foundry_enabled()
   |
   +-- true --> Appel Foundry AgentProducteur
   |            |-- succes --> retourne PolicyDraftResponse
   |            +-- echec  --> fallback vers stub (etape 4)
   |
   +-- false --> (etape 4)
   
4. Mode stub :
   a. RAG retriever recherche des sources (Azure AI Search ou veille_cache.md)
   b. Orchestrator remplace les variables du template
   c. Retourne PolicyDraftResponse { policy_markdown, sources[] }

5. UI affiche la politique en Markdown + sources en expandeur
```

---

## Securite

- Aucun secret dans le code : variables d'environnement uniquement
- `.env` exclu du depot (`.gitignore`)
- Authentification Azure : `DefaultAzureCredential` (Entra ID)
- Validation des entrees : Pydantic avec contraintes `min_length`
- Erreurs explicites : pas de stack traces exposees au client