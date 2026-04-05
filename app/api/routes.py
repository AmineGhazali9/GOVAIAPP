import logging

from fastapi import APIRouter, HTTPException

from app.api.schemas import CompanyContext, PolicyDraftResponse, HealthResponse, Source
from app.rag.retriever import retrieve
from app.agents.orchestrator import generate_policy as orchestrate_policy

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["monitoring"])
def health() -> HealthResponse:
    """Vérifie que l'API est opérationnelle."""
    return HealthResponse(status="ok")


@router.post("/generate-policy", response_model=PolicyDraftResponse, tags=["gouvernance"])
def generate_policy(request: CompanyContext) -> PolicyDraftResponse:
    """Génère une politique de gouvernance IA à partir du contexte entreprise.

    Mode stub (sans Azure) : sources lues depuis data/watch/veille_cache.md,
    policy_markdown générée via data/policy_template.md.
    """
    logger.info("Génération demandée pour %s (%s)", request.nom, request.secteur)

    try:
        query = f"{request.secteur} {request.maturite_donnees}"
        sources_raw = retrieve(query)
        policy_md = orchestrate_policy(request, sources_raw)
        sources = [Source(title=s["title"], excerpt=s["excerpt"]) for s in sources_raw]

    except Exception as exc:
        logger.exception("Erreur lors de la génération de politique")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur") from exc

    return PolicyDraftResponse(policy_markdown=policy_md, sources=sources)
