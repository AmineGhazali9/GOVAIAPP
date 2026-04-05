"""Stub orchestrateur – génère policy_markdown depuis data/policy_template.md."""

import logging
from pathlib import Path

from app.api.schemas import CompanyContext

logger = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).parent.parent.parent / "data" / "policy_template.md"


def generate_policy(request: CompanyContext, sources: list[dict[str, str]]) -> str:
    """Génère une politique de gouvernance IA (mode stub).

    Remplace les variables du template par les données du contexte entreprise.
    Chemin template : data/policy_template.md
    (prévu dans app/core/policy_template.md – déplacé dans data/ faute de pwsh).

    Args:
        request: Contexte entreprise.
        sources: Passages RAG récupérés.

    Returns:
        Texte de la politique en markdown.
    """
    logger.info("Génération stub pour %s", request.nom)

    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        logger.warning("policy_template.md introuvable, utilisation du template par défaut")
        template = (
            "# Politique de gouvernance IA – {{nom}}\n\n"
            "**Secteur :** {{secteur}}\n"
            "**Maturité données :** {{maturite_donnees}}\n\n"
            "---\n\n"
            "## Principes directeurs\n\n{{principes_directeurs}}\n\n"
            "## Contraintes identifiées\n\n{{contraintes}}\n\n"
            "---\n\n"
            "## Recommandations issues de la veille réglementaire\n\n{{sources}}\n"
        )

    principes = "\n".join(f"- {p}" for p in request.principes_directeurs) or "_Aucun principe renseigné._"
    sources_md = "\n".join(f"**{s['title']}** : {s['excerpt']}" for s in sources)

    return (
        template
        .replace("{{nom}}", request.nom)
        .replace("{{secteur}}", request.secteur)
        .replace("{{maturite_donnees}}", request.maturite_donnees)
        .replace("{{principes_directeurs}}", principes)
        .replace("{{contraintes}}", request.contraintes or "_Aucune contrainte renseignée._")
        .replace("{{sources}}", sources_md)
    )

