"""app/ui/app.py -- Interface Streamlit GOVAIAPP (1 page, pedagogique)."""

import os
from typing import Any

from dotenv import load_dotenv
import httpx
import streamlit as st

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

_MATURITE_LABELS: dict[str, str] = {
    "debutant": "\U0001f7e1 Debutant",
    "intermediaire": "\U0001f7e0 Intermediaire",
    "avance": "\U0001f7e2 Avance",
}


def parse_principes(text: str) -> list[str]:
    """Convertit un texte multiligne en liste de principes non vides."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def call_generate_policy(
    payload: dict[str, Any],
    base_url: str = API_URL,
) -> dict[str, Any]:
    """Appelle POST /generate-policy et retourne le JSON ou leve une exception."""
    url = f"{base_url}/generate-policy"
    response = httpx.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


# -- Page config --
st.set_page_config(page_title="GOVAIAPP - Gouvernance IA", page_icon="\U0001f916", layout="centered")
st.title("\U0001f916 GOVAIAPP \u2014 Generateur de politique IA")
st.caption("Renseignez le contexte de votre entreprise, puis cliquez sur **Generer la politique**.")

# -- Indicateur de mode --
_foundry_on = os.getenv("FOUNDRY_ENABLED", "false").lower() == "true"
if _foundry_on:
    st.info("\U0001f680 Mode **Azure AI Foundry** actif")
else:
    st.info("\U0001f9ea Mode **Stub local** (FOUNDRY_ENABLED=false)")


# -- Formulaire --
with st.form("policy_form"):
    nom = st.text_input("Nom de l'entreprise *", placeholder="Ex : Acme Corp")
    secteur = st.text_input("Secteur d'activite *", placeholder="Ex : Finance, Sante, Industrie...")
    maturite_donnees = st.selectbox(
        "Maturite donnees *",
        options=list(_MATURITE_LABELS.keys()),
        format_func=_MATURITE_LABELS.__getitem__,
    )
    principes_raw = st.text_area(
        "Principes directeurs (un par ligne)",
        placeholder="Transparence\nResponsabilite\nEquite",
        height=120,
    )
    contraintes = st.text_area(
        "Contraintes specifiques",
        placeholder="Ex : Conformite RGPD obligatoire, pas de LLM cloud...",
        height=80,
    )
    submitted = st.form_submit_button("\u2699\ufe0f Generer la politique", use_container_width=True)

# -- Resultat --
if submitted:
    if not nom.strip() or not secteur.strip():
        st.warning("\u26a0\ufe0f Le nom et le secteur sont obligatoires.")
    else:
        payload = {
            "nom": nom.strip(),
            "secteur": secteur.strip(),
            "maturite_donnees": maturite_donnees,
            "principes_directeurs": parse_principes(principes_raw),
            "contraintes": contraintes.strip(),
        }

        with st.spinner("Generation en cours..."):
            try:
                data = call_generate_policy(payload)
            except httpx.ConnectError:
                st.error("\u274c Impossible de joindre l'API. Verifiez que `uvicorn app.api.main:app --reload` est lance.")
                data = None
            except httpx.TimeoutException:
                st.error("\u23f1\ufe0f L'API n'a pas repondu dans les 60 secondes. Reessayez.")
                data = None
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 422:
                    st.error(f"\u26a0\ufe0f Donnees invalides (422) : {exc.response.text}")
                else:
                    st.error(f"\u274c Erreur API ({exc.response.status_code}) : {exc.response.text}")
                data = None
            except httpx.RequestError as exc:
                st.error(f"\u274c Erreur reseau inattendue : {exc!r}")
                data = None

        if data:
            st.success("\u2705 Politique generee avec succes !")
            st.divider()
            policy_md = data.get("policy_markdown", "")
            if policy_md:
                st.markdown(policy_md)
            else:
                st.warning("\u26a0\ufe0f La reponse ne contient pas de politique.")

            sources = data.get("sources", [])
            if sources:
                with st.expander(f"\U0001f4da Sources RAG ({len(sources)})", expanded=False):
                    for src in sources:
                        st.markdown(f"**{src['title']}**")
                        st.caption(src["excerpt"])
                        st.divider()