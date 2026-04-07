# .github/copilot-instructions.md

## Contexte du projet
Tu travailles sur GOVAIAPP, une application de démonstration agentique de gouvernance IA.
Objectif: démontrer une démarche outillée avec GitHub Copilot (dev, tests, doc, validation).

## Contraintes non négociables
- Code simple, lisible, pédagogique. Évite les patterns “trop magiques”.
- Séparation stricte UI (Streamlit), API (FastAPI), agents (AutoGen), RAG (Azure AI Search).
- Ne jamais inclure de secrets dans le code. Utiliser des variables d’environnement.
- Chaque fonctionnalité doit avoir au moins un test smoke ou une commande de vérification.

## Conventions techniques
- Python 3.10+.
- Type hints sur toutes les fonctions publiques.
- Pydantic pour les schémas API.
- Logs structurés et messages d’erreurs explicites.

## Commandes attendues (Windows PowerShell)
- Installer: `python -m venv .venv` puis `.venv\Scripts\activate` puis `pip install -r requirements.txt`
- Lancer API: `uvicorn app.api.main:app --reload`
- Lancer UI: `streamlit run app/ui/app.py`
- Tests: `pytest -q`

## RAG
- L’intégration RAG passe par Azure AI Search (index) et un client LLM via Azure AI Foundry.
- Si la config Azure n’est pas disponible, fournir un mode "stub" qui renvoie des passages fictifs depuis `data/watch/veille_cache.md`.