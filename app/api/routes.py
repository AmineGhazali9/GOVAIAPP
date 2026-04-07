"""Routes API GOVAIAPP -- /health + /generate-policy."""

import logging

from fastapi import APIRouter, HTTPException

from app.api.schemas import CompanyContext, PolicyDraftResponse, HealthResponse, Source
from app.foundry.client import is_foundry_enabled
from app.rag.retriever import retrieve
from app.agents.orchestrator import (
    generate_policy as orchestrate_stub,
    generate_policy_foundry,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["monitoring"])
def health() -> HealthResponse:
    """V\u00e9rifie que l'API est op\u00e9rationnelle."""
    return HealthResponse(status="ok")


@router.post("/generate-policy", response_model=PolicyDraftResponse, tags=["gouvernance"])
def generate_policy(request: CompanyContext) -> PolicyDraftResponse:
    """G\u00e9n\u00e8re une politique de gouvernance IA.

    Si FOUNDRY_ENABLED=true et les env vars sont presentes, utilise l'agent Foundry.
    Sinon (ou en cas d'echec Foundry), utilise le mode stub local.
    """
    logger.info("G\u00e9n\u00e9ration demand\u00e9e pour %s (%s)", request.nom, request.secteur)

    # --- Mode Foundry ---
    if is_foundry_enabled():
        try:
            policy_md, sources_raw = generate_policy_foundry(request)
            sources = [Source(title=s["title"], excerpt=s["excerpt"]) for s in sources_raw]
            logger.info("Politique g\u00e9n\u00e9r\u00e9e via Foundry pour %s", request.nom)
            return PolicyDraftResponse(policy_markdown=policy_md, sources=sources)
        except Exception as exc:
            logger.warning(
                "Foundry indisponible, fallback stub: %s", exc,
            )

    # --- Mode stub (fallback) ---
    try:
        query = f"{request.secteur} {request.maturite_donnees}"
        sources_raw = retrieve(query)
        policy_md = orchestrate_stub(request, sources_raw)
        sources = [Source(title=s["title"], excerpt=s["excerpt"]) for s in sources_raw]
    except Exception as exc:
        logger.exception("Erreur lors de la g\u00e9n\u00e9ration de politique (stub)")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur") from exc

    return PolicyDraftResponse(policy_markdown=policy_md, sources=sources)