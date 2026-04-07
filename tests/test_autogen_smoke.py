"""Tests smoke AutoGen pipeline (mode stub -- sans Foundry)."""

from __future__ import annotations

import asyncio
import os
from unittest.mock import patch

import pytest


# Force stub mode: no Foundry env vars
@pytest.fixture(autouse=True)
def _no_foundry(monkeypatch):
    monkeypatch.delenv("FOUNDRY_PROJECT_ENDPOINT", raising=False)
    monkeypatch.delenv("FOUNDRY_AGENT_VEILLE_EXTERNE_ID", raising=False)
    monkeypatch.delenv("FOUNDRY_AGENT_RAG_ID", raising=False)
    monkeypatch.delenv("FOUNDRY_AGENT_PRODUCTEUR_ID", raising=False)
    monkeypatch.delenv("FOUNDRY_ENABLED", raising=False)


def test_pipeline_returns_4_messages():
    """Le pipeline stub retourne exactement 4 messages (user + 3 agents)."""
    from autogen.orchestrator import run_policy_pipeline_sync

    msgs = run_policy_pipeline_sync("Entreprise test, secteur bancaire")
    assert len(msgs) == 4


def test_pipeline_message_order():
    """Les messages sont dans l'ordre: user, VeilleExterne, RagInterne, Producteur."""
    from autogen.orchestrator import run_policy_pipeline_sync

    msgs = run_policy_pipeline_sync("Test secteur sante")
    roles = [m["role"] for m in msgs]
    assert roles == ["user", "VeilleExterneAgent", "RagInterneAgent", "ProducteurPolitiqueAgent"]


def test_pipeline_stub_markers():
    """En mode stub, chaque agent produit un marqueur [STUB ...]."""
    from autogen.orchestrator import run_policy_pipeline_sync

    msgs = run_policy_pipeline_sync("Demo stub")
    assert "[STUB VeilleExterne]" in msgs[1]["content"]
    assert "[STUB RagInterne]" in msgs[2]["content"]
    assert "[STUB ProducteurPolitique]" in msgs[3]["content"]


def test_pipeline_propagates_context():
    """Le contexte utilisateur est propage aux agents."""
    from autogen.orchestrator import run_policy_pipeline_sync

    context = "Mon entreprise est dans la finance"
    msgs = run_policy_pipeline_sync(context)
    # User message contains original context
    assert context in msgs[0]["content"]