from typing import Literal

from pydantic import BaseModel, Field

MaturiteDonnees = Literal["debutant", "intermediaire", "avance"]


class CompanyContext(BaseModel):
    """Contexte entreprise pour générer une politique de gouvernance IA."""

    nom: str = Field(..., min_length=1, description="Nom de l'entreprise")
    secteur: str = Field(..., min_length=1, description="Secteur d'activité")
    principes_directeurs: list[str] = Field(
        default_factory=list,
        description="Principes directeurs de l'entreprise en matière d'IA",
    )
    maturite_donnees: MaturiteDonnees = Field(
        ...,
        description="Niveau de maturité données : debutant | intermediaire | avance",
    )
    contraintes: str = Field(
        default="",
        description="Contraintes spécifiques (réglementaires, techniques, etc.)",
    )


class Source(BaseModel):
    """Source RAG retournée avec la politique."""

    title: str = Field(..., min_length=1)
    excerpt: str = Field(..., min_length=1)


class PolicyDraftResponse(BaseModel):
    """Résultat de la génération de politique de gouvernance IA."""

    policy_markdown: str = Field(
        ..., description="Politique de gouvernance IA générée en Markdown"
    )
    sources: list[Source] = Field(
        default_factory=list, description="Sources utilisées"
    )


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""

    status: Literal["ok"]

