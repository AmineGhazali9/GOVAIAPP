"""Retriever RAG – Azure AI Search quand configuré, stub local sinon."""

import logging
import re
from pathlib import Path

from app.rag._azure_client import is_configured
from app.rag._azure_client import search as azure_search

logger = logging.getLogger(__name__)

CACHE_PATH = Path(__file__).parent.parent.parent / "data" / "watch" / "veille_cache.md"


def retrieve(query: str) -> list[dict[str, str]]:
    """Retourne des passages RAG pertinents pour la requête.

    Stratégie :
    1. Si Azure AI Search est configuré (variables ``AZURE_SEARCH_ENDPOINT``,
       ``AZURE_SEARCH_API_KEY``, ``AZURE_SEARCH_INDEX_NAME`` toutes définies),
       délègue à ``_azure_client.search()``.
    2. En cas d'absence de config ou d'échec Azure, bascule sur le stub local
       (``data/watch/veille_cache.md``).

    Args:
        query: La requête de recherche (utilisée uniquement en mode Azure).

    Returns:
        Liste de dicts avec les clés ``title`` et ``excerpt``.
    """
    if is_configured():
        results = azure_search(query)
        if results:
            return results
        logger.info("Azure AI Search n'a retourné aucun résultat, fallback stub")

    return _stub_retrieve(query)


def _stub_retrieve(query: str) -> list[dict[str, str]]:
    """Lit data/watch/veille_cache.md et retourne tous les passages."""
    logger.debug("stub retrieve – query : %r", query)

    if not CACHE_PATH.exists():
        logger.warning("veille_cache.md introuvable, utilisation du fallback")
        return [{"title": "Fallback", "excerpt": "Aucune source disponible."}]

    content = CACHE_PATH.read_text(encoding="utf-8")
    sources: list[dict[str, str]] = []

    for block in re.split(r"\n## SOURCE:", content):
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        lines = block.splitlines()
        title = lines[0].strip(" –-")
        excerpt = " ".join(line.strip() for line in lines[1:] if line.strip())
        if title and excerpt:
            sources.append({"title": title, "excerpt": excerpt})

    if not sources:
        logger.warning("Aucune source parsée dans veille_cache.md, fallback")
        return [{"title": "Fallback", "excerpt": "Aucune source disponible."}]

    return sources

