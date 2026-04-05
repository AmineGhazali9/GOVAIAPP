# GOVAIAPP

Application de démonstration agentique de **gouvernance IA**, construite avec GitHub Copilot en mode human-in-the-loop.

Démontre une démarche outillée : Dev → QA → Doc → Validator, avec RAG via Azure AI Search.

---

## Architecture

```
GOVAIAPP/
├── app/
│   ├── api/          # FastAPI – endpoints REST
│   ├── ui/           # Streamlit – interface utilisateur
│   ├── agents/       # AutoGen – orchestration agents IA
│   └── rag/          # Connecteur RAG (Azure AI Search ou stub local)
├── data/
│   └── watch/        # Cache de veille (stub local RAG)
├── tests/            # Tests smoke pytest
└── docs/             # Documentation et journal de démo
```

---

## Prérequis

- Python 3.10+
- Windows PowerShell

---

## Installation

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Lancer l'application

**API (FastAPI) :**
```powershell
uvicorn app.api.main:app --reload
```
Disponible sur : http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

**Interface (Streamlit) :**
```powershell
streamlit run app/ui/app.py
```
Disponible sur : http://localhost:8501

---

## Tests

```powershell
pytest -q
```

---

## Configuration Azure AI Search

Copier `.env.example` en `.env` et renseigner les variables :

| Variable | Description |
|---|---|
| `AZURE_SEARCH_ENDPOINT` | URL du service Azure AI Search |
| `AZURE_SEARCH_API_KEY` | Clé API Azure AI Search |
| `AZURE_SEARCH_INDEX_NAME` | Nom de l'index |
| `AZURE_OPENAI_ENDPOINT` | URL Azure OpenAI / AI Foundry |
| `AZURE_OPENAI_API_KEY` | Clé API Azure OpenAI |
| `AZURE_OPENAI_DEPLOYMENT` | Nom du déploiement LLM |

> Si ces variables ne sont pas définies, l'application utilise automatiquement un **mode stub** local (`data/watch/veille_cache.md`).

---

## Agents GitHub Copilot

| Agent | Rôle |
|---|---|
| **Dev** | Développe l'application (FastAPI + Streamlit + AutoGen) |
| **QA** | Tests bout en bout, identification de bugs |
| **Doc** | Documentation architecture et décisions |
| **Validator** | Prépare PR et déclenche revue Copilot |

---

## Journal de démo

Voir [`docs/demo_log.md`](docs/demo_log.md) pour le journal chronologique des actions agents.
