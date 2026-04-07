"""Orchestrateur -- generation de politique via stub ou Foundry."""

import logging
from pathlib import Path

from app.api.schemas import CompanyContext

logger = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).parent.parent.parent / "data" / "policy_template.md"


def generate_policy(request: CompanyContext, sources: list[dict[str, str]]) -> str:
    """Genere une politique de gouvernance IA (mode stub).

    Remplace les variables du template par les donnees du contexte entreprise.

    Args:
        request: Contexte entreprise.
        sources: Passages RAG recuperes.

    Returns:
        Texte de la politique en markdown.
    """
    logger.info("Generation stub pour %s", request.nom)

    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        logger.warning("policy_template.md introuvable, utilisation du template par defaut")
        template = (
            "# Politique de gouvernance IA \u2014 {{nom}}\n\n"
            "**Secteur :** {{secteur}}\n"
            "**Maturit\u00e9 donn\u00e9es :** {{maturite_donnees}}\n\n"
            "---\n\n"
            "## Principes directeurs\n\n{{principes_directeurs}}\n\n"
            "## Contraintes identifi\u00e9es\n\n{{contraintes}}\n\n"
            "---\n\n"
            "## Recommandations issues de la veille r\u00e9glementaire\n\n{{sources}}\n"
        )

    principes = "\n".join(f"- {p}" for p in request.principes_directeurs) or "_Aucun principe renseign\u00e9._"
    sources_md = "\n".join(f"**{s['title']}** : {s['excerpt']}" for s in sources)

    return (
        template
        .replace("{{nom}}", request.nom)
        .replace("{{secteur}}", request.secteur)
        .replace("{{maturite_donnees}}", request.maturite_donnees)
        .replace("{{principes_directeurs}}", principes)
        .replace("{{contraintes}}", request.contraintes or "_Aucune contrainte renseign\u00e9e._")
        .replace("{{sources}}", sources_md)
    )


def _build_foundry_prompt(request: CompanyContext) -> str:
    """Construit un prompt structure pour l'agent Foundry a partir du contexte."""
    principes = ", ".join(request.principes_directeurs) if request.principes_directeurs else "non specifies"
    return (
        f"G\u00e9n\u00e8re une politique de gouvernance IA en markdown pour l'entreprise suivante.\n\n"
        f"- Nom : {request.nom}\n"
        f"- Secteur : {request.secteur}\n"
        f"- Maturit\u00e9 donn\u00e9es : {request.maturite_donnees}\n"
        f"- Principes directeurs : {principes}\n"
        f"- Contraintes : {request.contraintes or 'aucune'}\n\n"
        f"Inclus des recommandations concr\u00e8tes et cite tes sources si disponibles."
    )


def generate_policy_foundry(request: CompanyContext) -> tuple[str, list[dict[str, str]]]:
    """Genere une politique via l'agent Foundry (AgentProducteur).

    Args:
        request: Contexte entreprise.

    Returns:
        Tuple (policy_markdown, sources).

    Raises:
        RuntimeError: Si Foundry echoue.
    """
    from app.foundry.client import call_foundry_agent

    prompt = _build_foundry_prompt(request)
    logger.info("Appel Foundry pour %s (%s)", request.nom, request.secteur)

    policy_md = call_foundry_agent(prompt)

    sources = [
        {
            "title": "Azure AI Foundry AgentProducteur",
            "excerpt": f"Politique g\u00e9n\u00e9r\u00e9e par l'agent Foundry pour {request.nom} ({request.secteur}).",
        }
    ]

    return policy_md, sources