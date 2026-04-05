"""Stub RAG local – lit data/watch/veille_cache.md."""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

CACHE_PATH = Path(__file__).parent.parent.parent / "data" / "watch" / "veille_cache.md"


def retrieve(query: str) -> list[dict[str, str]]:
    """Retourne des passages depuis data/watch/veille_cache.md.

    Mode stub : le paramètre query est ignoré, tous les passages sont retournés.
    Fallback vers une source par défaut si le fichier est absent ou vide.
    """
    logger.debug("stub retrieve – query ignorée : %r", query)

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

