# tests/test_smoke.py – tests smoke API GOVAIAPP
from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "nom": "Acme Corp",
    "secteur": "Finance",
    "maturite_donnees": "intermediaire",
    "principes_directeurs": ["Transparence", "Responsabilité"],
    "contraintes": "Conformité RGPD obligatoire.",
}


def test_health() -> None:
    """GET /health doit retourner 200 avec status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"].startswith("application/json")


def test_generate_policy_stub() -> None:
    """POST /generate-policy avec payload valide doit retourner 200 en mode stub."""
    response = client.post("/generate-policy", json=VALID_PAYLOAD)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert data["policy_markdown"]
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    assert "title" in data["sources"][0]
    assert "excerpt" in data["sources"][0]
    assert VALID_PAYLOAD["nom"] in data["policy_markdown"]


def test_generate_policy_invalid_missing_fields() -> None:
    """POST /generate-policy avec champs requis manquants doit retourner 422."""
    response = client.post("/generate-policy", json={"nom": "X"})  # manque secteur + maturite_donnees
    assert response.status_code == 422


def test_generate_policy_invalid_empty_nom() -> None:
    """POST /generate-policy avec nom vide doit retourner 422 (min_length=1)."""
    response = client.post("/generate-policy", json={**VALID_PAYLOAD, "nom": ""})
    assert response.status_code == 422


def test_generate_policy_no_principes() -> None:
    """POST /generate-policy sans principes_directeurs doit retourner 200 avec fallback."""
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "principes_directeurs"}
    response = client.post("/generate-policy", json=payload)
    assert response.status_code == 200
    assert "_Aucun principe renseigné._" in response.json()["policy_markdown"]

