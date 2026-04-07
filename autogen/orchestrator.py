"""Orchestrateur AutoGen -- pipeline sequentiel des agents metier GOVAIAPP.

Pipeline : VeilleExterne -> RagInterne -> ProducteurPolitique
Chaque agent appelle son homologue Azure AI Foundry.
"""

from __future__ import annotations

import asyncio
import logging

from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from autogen.agents.veille_externe_agent import VeilleExterneAgent
from autogen.agents.rag_interne_agent import RagInterneAgent
from autogen.agents.producteur_politique_agent import ProducteurPolitiqueAgent

logger = logging.getLogger(__name__)


async def run_policy_pipeline(company_context: str) -> list[dict[str, str]]:
    """Execute le pipeline sequentiel des agents metier.

    Ordre : VeilleExterne -> RagInterne -> ProducteurPolitique.
    Chaque agent recoit la sortie du precedent.

    Args:
        company_context: Description du contexte entreprise (texte libre).

    Returns:
        Liste des messages echanges [{role, content}, ...].
    """
    veille = VeilleExterneAgent()
    rag = RagInterneAgent()
    producteur = ProducteurPolitiqueAgent()

    # max_messages=4 : user + veille + rag + producteur
    team = RoundRobinGroupChat(
        participants=[veille, rag, producteur],
        termination_condition=MaxMessageTermination(max_messages=4),
    )

    logger.info("Lancement du pipeline AutoGen pour: %s", company_context[:80])
    result = await team.run(task=company_context)

    messages: list[dict[str, str]] = []
    for msg in result.messages:
        messages.append({
            "role": getattr(msg, "source", "system"),
            "content": msg.content,
        })

    logger.info("Pipeline termine: %d messages", len(messages))
    return messages


def run_policy_pipeline_sync(company_context: str) -> list[dict[str, str]]:
    """Version synchrone du pipeline (pour appels depuis scripts ou FastAPI)."""
    return asyncio.run(run_policy_pipeline(company_context))


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s %(levelname)s %(message)s",
    )
    results = run_policy_pipeline_sync(
        "PME du secteur sante, maturite intermediaire, "
        "principes: transparence et responsabilite"
    )
    for msg in results:
        role = msg["role"]
        content = msg["content"][:150]
        print(f"[{role}] {content}")