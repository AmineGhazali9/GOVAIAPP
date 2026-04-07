# tests/test_rag_smoke.py – smoke tests fallback RAG GOVAIAPP
"""Vérifie le comportement de retrieve() sans dépendance Azure live."""

import os

import pytest


def _clear_azure_env() -> None:
    """Supprime les variables Azure AI Search de l'environnement courant."""
    for key in ("AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_API_KEY", "AZURE_SEARCH_INDEX_NAME"):
        os.environ.pop(key, None)


@pytest.fixture(autouse=True)
def reset_azure_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Garantit qu'aucune variable Azure n'est définie pendant les tests."""
    monkeypatch.delenv("AZURE_SEARCH_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_SEARCH_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_SEARCH_INDEX_NAME", raising=False)


def test_retrieve_no_azure_returns_stub_list() -> None:
    """Sans vars Azure, retrieve() retourne le stub (liste non vide)."""
    # Réimporte après nettoyage env pour forcer réévaluation is_configured()
    from app.rag.retriever import retrieve

    results = retrieve("gouvernance IA")

    assert isinstance(results, list)
    assert len(results) > 0


def test_retrieve_stub_items_have_title_and_excerpt() -> None:
    """Chaque item du stub contient les clés 'title' et 'excerpt'."""
    from app.rag.retriever import retrieve

    results = retrieve("transparence")

    for item in results:
        assert "title" in item, f"Clé 'title' manquante dans {item}"
        assert "excerpt" in item, f"Clé 'excerpt' manquante dans {item}"
        assert item["title"], "title ne doit pas être vide"
        assert item["excerpt"], "excerpt ne doit pas être vide"


def test_retrieve_partial_azure_config_uses_stub() -> None:
    """Config Azure incomplète (endpoint seul) → fallback stub sans exception."""
    os.environ["AZURE_SEARCH_ENDPOINT"] = "https://fake.search.windows.net"
    # AZURE_SEARCH_API_KEY et AZURE_SEARCH_INDEX_NAME absents

    try:
        from app.rag.retriever import retrieve
        results = retrieve("test")
        assert isinstance(results, list)
        assert len(results) > 0
    finally:
        os.environ.pop("AZURE_SEARCH_ENDPOINT", None)


def test_azure_client_not_configured_returns_empty() -> None:
    """is_configured() retourne False et search() retourne [] sans vars Azure."""
    from app.rag._azure_client import is_configured, search

    assert not is_configured()
    assert search("test") == []
