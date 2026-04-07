"""Client Azure AI Foundry Agents -- utilise AgentsClient (azure.ai.agents)."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


def is_foundry_enabled() -> bool:
    """Retourne True si le mode Foundry est active et configure."""
    return (
        os.getenv("FOUNDRY_ENABLED", "false").lower() == "true"
        and bool(os.getenv("FOUNDRY_PROJECT_ENDPOINT", ""))
        and bool(os.getenv("FOUNDRY_AGENT_PRODUCTEUR_ID", ""))
    )


def call_foundry_agent(prompt: str) -> str:
    """Envoie un prompt a l'agent Foundry et retourne la reponse texte.

    Utilise AgentsClient (azure.ai.agents) avec DefaultAzureCredential.
    Workflow: get_agent -> create thread -> create message -> run -> list messages.

    Args:
        prompt: Le prompt utilisateur a envoyer a l'agent.

    Returns:
        Le texte de la derniere reponse de l'agent.

    Raises:
        RuntimeError: Si la communication avec Foundry echoue.
    """
    try:
        from azure.identity import DefaultAzureCredential
        from azure.ai.agents import AgentsClient
        from azure.ai.agents.models import ListSortOrder
    except ImportError as exc:
        raise RuntimeError(
            "azure-ai-agents et azure-identity sont requis. "
            "Installez: pip install azure-ai-agents azure-identity"
        ) from exc

    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
    agent_id = os.getenv("FOUNDRY_AGENT_PRODUCTEUR_ID", "")

    logger.info("Appel Foundry AgentProducteur (id=%s) sur %s", agent_id, endpoint)

    try:
        client = AgentsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )

        agent = client.get_agent(agent_id)
        thread = client.threads.create()
        client.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt,
        )

        run = client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id,
        )

        if run.status == "failed":
            raise RuntimeError(f"Run echoue: {run.last_error}")

        messages = client.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING,
        )

        last_text = ""
        for msg in messages:
            if msg.text_messages:
                last_text = msg.text_messages[-1].text.value

        if not last_text:
            raise RuntimeError("Aucune reponse texte de l'agent Foundry")

        logger.info("Reponse Foundry recue (%d caracteres)", len(last_text))
        return last_text

    except Exception as exc:
        logger.error("Erreur Foundry: %s", exc)
        raise RuntimeError(f"Echec appel Foundry Agent: {exc}") from exc