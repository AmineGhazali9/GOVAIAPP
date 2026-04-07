# GOVAIAPP

Application de demonstration agentique de **gouvernance IA**, construite
avec GitHub Copilot en mode human-in-the-loop.

Genere des politiques de gouvernance IA personnalisees a partir du contexte
d'une entreprise, en s'appuyant sur des agents Azure AI Foundry ou un mode
stub local.

---

## Technologies et frameworks

| Couche           | Technologie                | Version   | Role                              |
|------------------|----------------------------|-----------|-----------------------------------|
| **Langage**      | Python                     | 3.10+     | Langage principal                 |
| **API**          | FastAPI                    | >= 0.111  | Endpoints REST                    |
| **Serveur**      | Uvicorn                    | >= 0.29   | Serveur ASGI                      |
| **Schemas**      | Pydantic                   | >= 2.7    | Validation et serialisation       |
| **UI**           | Streamlit                  | >= 1.35   | Interface web                     |
| **Agents**       | AutoGen AG2 (agentchat)    | >= 0.7    | Orchestration multi-agents        |
| **Agents**       | AutoGen AG2 (core)         | >= 0.7    | Infrastructure agents             |
| **IA Cloud**     | Azure AI Foundry Agents    | >= 1.1    | Agents IA en production           |
| **Auth**         | Azure Identity             | >= 1.16   | DefaultAzureCredential (Entra ID) |
| **RAG**          | Azure AI Search            | >= 11.4   | Recherche documentaire            |
| **HTTP client**  | httpx                      | >= 0.27   | Appels API depuis UI et tests     |
| **Config**       | python-dotenv              | >= 1.0    | Chargement `.env`                 |
| **Tests**        | pytest                     | >= 8.2    | Tests unitaires et integration    |

---

## Architecture

```
GOVAIAPP/
+-- app/
|   +-- api/          # FastAPI (main, routes, schemas)
|   +-- agents/       # Orchestrator stub + Foundry
|   +-- foundry/      # Client Azure AI Foundry (AgentsClient)
|   +-- rag/          # RAG (Azure AI Search ou stub local)
|   +-- ui/           # Streamlit (interface utilisateur)
+-- autogen/
|   +-- agents/       # 3 agents metier AG2 (veille, RAG, producteur)
|   +-- config/       # Configuration centralisee Foundry
|   +-- orchestrator.py  # Pipeline RoundRobin
+-- data/
|   +-- policy_template.md    # Template de politique (mode stub)
|   +-- watch/veille_cache.md # Sources de veille (mode stub)
+-- tests/            # 23 tests (unitaires, API, integration, AutoGen)
+-- docs/             # Documentation (architecture, regles, sessions)
+-- .github/
|   +-- agents/       # 4 agents GitHub Copilot (Dev, QA, Doc, Validator)
|   +-- instructions/ # Instructions Copilot par domaine
|   +-- Skills/       # Skills Copilot (logging, delivery, RAG)
```

Documentation detaillee : [`docs/architecture.md`](docs/architecture.md)

---

## Prerequis

- **Python 3.10+** (teste avec 3.13)
- **Windows PowerShell** (ou tout terminal compatible)
- **Azure CLI** avec `az login` effectue (pour le mode Foundry)
  - Role RBAC `Azure AI User` sur le projet Azure AI Foundry

---

## Installation

```powershell
# 1. Cloner le depot
git clone <url-du-repo>
cd GOVAIAPP

# 2. Creer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# 3. Installer les dependances
pip install -r requirements.txt
```

---

## Configuration

Copier `.env.example` en `.env` et renseigner les valeurs :

```powershell
Copy-Item .env.example .env
```

### Variables d'environnement

| Variable                         | Obligatoire | Description                                    |
|----------------------------------|-------------|------------------------------------------------|
| `FOUNDRY_ENABLED`                | Non         | `true` pour activer le mode Foundry            |
| `FOUNDRY_PROJECT_ENDPOINT`       | Si Foundry  | Endpoint du projet Azure AI Foundry            |
| `FOUNDRY_AGENT_PRODUCTEUR_ID`    | Si Foundry  | ID de l'agent producteur de politique          |
| `FOUNDRY_AGENT_VEILLE_EXTERNE_ID`| Si AutoGen  | ID de l'agent de veille externe                |
| `FOUNDRY_AGENT_RAG_ID`           | Si AutoGen  | ID de l'agent RAG interne                      |
| `AZURE_SEARCH_ENDPOINT`          | Non         | Endpoint Azure AI Search (mode RAG complet)    |
| `AZURE_SEARCH_API_KEY`           | Non         | Cle API Azure AI Search                        |
| `AZURE_SEARCH_INDEX_NAME`        | Non         | Nom de l'index Azure AI Search                 |
| `AZURE_TENANT_ID`                | Non         | Tenant Azure AD (multi-tenant)                 |

> **Sans aucune variable**, l'application fonctionne en mode stub local.

---

## Lancer l'application

### 1. Demarrer l'API (FastAPI)

```powershell
uvicorn app.api.main:app --reload --port 8000
```

- API : http://localhost:8000
- Swagger : http://localhost:8000/docs

### 2. Demarrer l'interface (Streamlit)

```powershell
streamlit run app/ui/app.py --server.port 8501
```

- UI : http://localhost:8501

### 3. Utilisation

1. Ouvrir http://localhost:8501
2. Remplir le formulaire (nom, secteur, maturite, principes, contraintes)
3. Cliquer sur "Generer la politique"
4. La politique s'affiche en Markdown, les sources RAG dans un expandeur

---

## Pipeline AutoGen (CLI)

Le module `autogen/` est un pipeline autonome qui enchaine 3 agents metier :

```powershell
.venv\Scripts\python -m autogen.orchestrator
```

Sortie : 4 messages (user + VeilleExterne + RagInterne + ProducteurPolitique).

---

## Tests

### Lancer tous les tests

```powershell
pytest -q
```

### Lancer avec details

```powershell
pytest --tb=short -v
```

### Suite de tests

| Fichier                    | Type        | Nb  | Couverture                          |
|----------------------------|-------------|-----|-------------------------------------|
| `test_smoke.py`            | API         | 7   | Health, stub, validation, fallback  |
| `test_rag_smoke.py`        | Unitaire    | 4   | RAG retriever, stub, parsing        |
| `test_ui_smoke.py`         | Integration | 8   | Import UI, parsing, appels API mock |
| `test_autogen_smoke.py`    | Integration | 4   | Pipeline AutoGen stub complet       |
| **Total**                  |             |**23**|                                    |

---

## Modes de fonctionnement

| Mode            | Activation                                     | Comportement                    |
|-----------------|-------------------------------------------------|---------------------------------|
| **Stub local**  | Par defaut (aucune config)                      | Template + sources veille_cache |
| **Foundry**     | `FOUNDRY_ENABLED=true` + endpoint + agent IDs   | Agent Azure AI Foundry          |
| **Fallback**    | Foundry active mais en erreur                   | Bascule automatique vers stub   |

---

## Agents GitHub Copilot

4 agents configurent le workflow de developpement dans VS Code :

| Agent      | Fichier                            | Role                        |
|------------|------------------------------------|-----------------------------|
| Dev        | `.github/agents/01-dev.agent.md`   | Developpe le code           |
| QA         | `.github/agents/02-qa.agent.md`    | Tests et detection de bugs  |
| Doc        | `.github/agents/03-doc.agent.md`   | Documentation               |
| Validator  | `.github/agents/04-Validator.agent.md` | Revue et validation PR  |

---

## Documentation

| Document                                              | Contenu                         |
|-------------------------------------------------------|---------------------------------|
| [`docs/architecture.md`](docs/architecture.md)        | Composants, flux, schemas ASCII |
| [`docs/governance_model.md`](docs/governance_model.md)| Regles metier et fonctionnelles |
| [`docs/demo_log.md`](docs/demo_log.md)                | Journal chronologique de demo   |

---

## Licence

Voir [LICENSE](LICENSE).