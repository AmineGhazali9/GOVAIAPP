# AutoGen -- Orchestration des agents metier GOVAIAPP

## Architecture

```
autogen/
  config/
    foundry_config.py              # Config centralisee + appel Foundry generique
  agents/
    veille_externe_agent.py        # Agent de veille reglementaire externe
    rag_interne_agent.py           # Agent RAG sur documents internes
    producteur_politique_agent.py  # Agent producteur de politique
  orchestrator.py                  # Pipeline sequentiel (RoundRobinGroupChat)
```

## Separation des responsabilites

| Couche | Responsabilite | Technologie |
|--------|---------------|-------------|
| **Azure AI Foundry** | Execution des agents metier (LLM, RAG, tools) | AgentsClient SDK |
| **AutoGen (AG2 0.7)** | Orchestration du pipeline multi-agents | autogen-agentchat |
| **FastAPI / Streamlit** | API REST + UI utilisateur | app/ |
| **Custom Agents Copilot** | Personas ingenierie (Dev, QA, Doc, Validator) | .github/agents/ |

### Ce qui est dans AutoGen

- Orchestration sequentielle : Veille externe -> RAG interne -> Producteur
- Transmission des sorties entre agents (message passing)
- Mode stub si Foundry n'est pas configure

### Ce qui reste dans Azure AI Foundry

- Les 3 agents metier (veille externe, RAG interne, producteur)
- Le modele LLM, les outils, le knowledge store
- La configuration des agents (system prompt, tools, files)

### Ce qui n'est PAS dans AutoGen

- Les personas Copilot (Dev, QA, Doc, Validator) -> .github/agents/
- La logique API / UI -> app/
- Aucune cle secrete (variables d'environnement uniquement)

## Variables d'environnement requises

| Variable | Description |
|----------|-------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Endpoint du projet Azure AI Foundry |
| `FOUNDRY_AGENT_EXTERNE_ID` | ID de l'agent de veille externe |
| `FOUNDRY_AGENT_RAG_ID` | ID de l'agent RAG interne |
| `FOUNDRY_AGENT_PRODUCTEUR_ID` | ID de l'agent producteur de politique |

## Utilisation

```bash
# Mode stub (sans Foundry configure)
python -m autogen.orchestrator

# Mode Foundry (variables d'environnement requises)
python -m autogen.orchestrator
```

## Vers Microsoft Agent Framework (MAF)

La structure actuelle (agents + orchestrator) est directement transposable
vers Azure AI Agent Service (MAF). La migration consiste a :

1. Remplacer `BaseChatAgent` par l'interface MAF equivalente
2. Remplacer `RoundRobinGroupChat` par le workflow MAF
3. Conserver `foundry_config.py` pour les appels Foundry inchanges