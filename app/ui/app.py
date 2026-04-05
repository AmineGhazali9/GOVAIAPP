"""app/ui/app.py — Interface Streamlit GOVAIAPP (1 page, pédagogique)."""

import os
from typing import Any

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

_MATURITE_LABELS: dict[str, str] = {
    "debutant": "🟡 Débutant",
    "intermediaire": "🟠 Intermédiaire",
    "avance": "🟢 Avancé",
}


def parse_principes(text: str) -> list[str]:
    """Convertit un texte multiligne en liste de principes non vides."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def call_generate_policy(
    payload: dict[str, Any],
    base_url: str = API_URL,
) -> dict[str, Any]:
    """Appelle POST /generate-policy et retourne le JSON ou lève une exception."""
    url = f"{base_url}/generate-policy"
    response = httpx.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="GOVAIAPP — Gouvernance IA", page_icon="🤖", layout="centered")
st.title("🤖 GOVAIAPP — Générateur de politique IA")
st.caption("Renseignez le contexte de votre entreprise, puis cliquez sur **Générer la politique**.")

# ── Formulaire ────────────────────────────────────────────────────────────────
with st.form("policy_form"):
    nom = st.text_input("Nom de l'entreprise *", placeholder="Ex : Acme Corp")
    secteur = st.text_input("Secteur d'activité *", placeholder="Ex : Finance, Santé, Industrie…")
    maturite_donnees = st.selectbox(
        "Maturité données *",
        options=list(_MATURITE_LABELS.keys()),
        format_func=_MATURITE_LABELS.__getitem__,
    )
    principes_raw = st.text_area(
        "Principes directeurs (un par ligne)",
        placeholder="Transparence\nResponsabilité\nÉquité",
        height=120,
    )
    contraintes = st.text_area(
        "Contraintes spécifiques",
        placeholder="Ex : Conformité RGPD obligatoire, pas de LLM cloud…",
        height=80,
    )
    submitted = st.form_submit_button("⚙️ Générer la politique", use_container_width=True)

# ── Résultat ──────────────────────────────────────────────────────────────────
if submitted:
    if not nom.strip() or not secteur.strip():
        st.warning("⚠️ Le nom et le secteur sont obligatoires.")
    else:
        payload = {
            "nom": nom.strip(),
            "secteur": secteur.strip(),
            "maturite_donnees": maturite_donnees,
            "principes_directeurs": parse_principes(principes_raw),
            "contraintes": contraintes.strip(),
        }

        with st.spinner("Génération en cours…"):
            try:
                data = call_generate_policy(payload)
            except httpx.ConnectError:
                st.error("❌ Impossible de joindre l'API. Vérifiez que `uvicorn app.api.main:app --reload` est lancé.")
                data = None
            except httpx.TimeoutException:
                st.error("⏱️ L'API n'a pas répondu dans les 30 secondes. Réessayez.")
                data = None
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 422:
                    st.error(f"⚠️ Données invalides (422) : {exc.response.text}")
                else:
                    st.error(f"❌ Erreur API ({exc.response.status_code}) : {exc.response.text}")
                data = None
            except httpx.RequestError as exc:
                st.error(f"❌ Erreur réseau inattendue : {exc!r}")
                data = None

        if data:
            st.success("✅ Politique générée avec succès !")
            st.divider()
            policy_md = data.get("policy_markdown", "")
            if policy_md:
                st.markdown(policy_md)
            else:
                st.warning("⚠️ La réponse ne contient pas de politique.")

            sources = data.get("sources", [])
            if sources:
                with st.expander(f"📚 Sources RAG ({len(sources)})", expanded=False):
                    for src in sources:
                        st.markdown(f"**{src['title']}**")
                        st.caption(src["excerpt"])
                        st.divider()

