"""Client Azure AI Search – utilisé par retriever.py quand la config est présente."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_REQUIRED_VARS = ("AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_API_KEY", "AZURE_SEARCH_INDEX_NAME")


def is_configured() -> bool:
    """Retourne True si les 3 variables Azure AI Search sont définies et non vides."""
    return all(os.getenv(v, "") for v in _REQUIRED_VARS)


def search(query: str, top: int = 5) -> list[dict[str, str]]:
    """Interroge Azure AI Search et retourne une liste de {title, excerpt}.

    Retourne une liste vide ([]]) si la config est absente ou en cas d'erreur réseau/HTTP,
    permettant à l'appelant de basculer sur le stub local.

    Args:
        query: La requête de recherche.
        top: Nombre maximum de résultats à retourner.

    Returns:
        Liste de dicts avec les clés ``title`` et ``excerpt``.
    """
    if not is_configured():
        logger.debug("Azure AI Search non configuré, retour []")
        return []

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    key = os.getenv("AZURE_SEARCH_API_KEY", "")
    index = os.getenv("AZURE_SEARCH_INDEX_NAME", "")

    try:
        from azure.core.exceptions import AzureError
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential

        client = SearchClient(
            endpoint=endpoint,
            index_name=index,
            credential=AzureKeyCredential(key),
        )

        results = client.search(search_text=query, top=top)
        sources: list[dict[str, str]] = []
        for doc in results:
            title = str(doc.get("title") or doc.get("id") or "Sans titre")
            excerpt = str(doc.get("content") or doc.get("excerpt") or doc.get("text") or "")
            if excerpt:
                sources.append({"title": title, "excerpt": excerpt})

        logger.info("Azure AI Search : %d résultat(s) pour la requête %r", len(sources), query)
        return sources

    except ImportError:
        logger.error(
            "azure-search-documents n'est pas installé. "
            "Exécutez : pip install azure-search-documents"
        )
        return []
    except Exception as exc:  # AzureError, réseau, auth…
        logger.warning(
            "Azure AI Search indisponible (%s: %s), fallback stub",
            type(exc).__name__,
            exc,
        )
        return []
