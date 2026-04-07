"""Configuration centralisee Azure AI Foundry -- agents metier GOVAIAPP."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

AGENT_ENV_VARS: dict[str, str] = {
    "veille_externe": "FOUNDRY_AGENT_VEILLE_EXTERNE_ID",
    "rag_interne": "FOUNDRY_AGENT_RAG_ID",
    "producteur_politique": "FOUNDRY_AGENT_PRODUCTEUR_ID",
}


def get_foundry_endpoint() -> str:
    """Retourne l endpoint du projet Azure AI Foundry."""
    return os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")


def get_agent_id(agent_name: str) -> str:
    """Retourne l ID Foundry d un agent metier par son nom logique."""
    env_var = AGENT_ENV_VARS.get(agent_name)
    if env_var is None:
        valid = list(AGENT_ENV_VARS.keys())
        raise ValueError(f"Agent inconnu: {agent_name}. Valides: {valid}")
    return os.getenv(env_var, "")


def is_foundry_configured(agent_name: str) -> bool:
    """Verifie si un agent Foundry est configure (endpoint + agent ID)."""
    return bool(get_foundry_endpoint()) and bool(get_agent_id(agent_name))


def call_foundry_generic(agent_name: str, prompt: str) -> str:
    """Appelle un agent Azure AI Foundry par son nom logique."""
    try:
        from azure.identity import DefaultAzureCredential
        from azure.ai.agents import AgentsClient
        from azure.ai.agents.models import ListSortOrder
    except ImportError as exc:
        raise RuntimeError(
            "azure-ai-agents et azure-identity requis. "
            "pip install azure-ai-agents azure-identity"
        ) from exc

    endpoint = get_foundry_endpoint()
    agent_id = get_agent_id(agent_name)

    if not endpoint or not agent_id:
        env_var = AGENT_ENV_VARS[agent_name]
        raise RuntimeError(
            f"Agent Foundry '{agent_name}' non configure "
            f"(FOUNDRY_PROJECT_ENDPOINT ou {env_var} manquant)"
        )

    logger.info("Appel Foundry agent=%s (id=%s)", agent_name, agent_id)

    try:
        client = AgentsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )
        agent = client.get_agent(agent_id)
        thread = client.threads.create()
        client.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

        if run.status == "failed":
            raise RuntimeError(f"Run echoue: {run.last_error}")

        msgs = client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        last_text = ""
        for msg in msgs:
            if msg.text_messages:
                last_text = msg.text_messages[-1].text.value

        if not last_text:
            raise RuntimeError(f"Aucune reponse de l agent '{agent_name}'")

        logger.info("Reponse Foundry agent=%s (%d car.)", agent_name, len(last_text))
        return last_text

    except Exception as exc:
        logger.error("Erreur Foundry agent=%s: %s", agent_name, exc)
        raise RuntimeError(f"Echec appel Foundry '{agent_name}': {exc}") from exc