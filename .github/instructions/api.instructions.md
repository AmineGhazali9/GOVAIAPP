---
applyTo:
  - "app/api/**"
---

## Standards API
- Endpoints REST simples.
- Schémas Pydantic centralisés dans `schemas.py`.
- Gestion d’erreur cohérente (HTTPException) et logs.
- Une route `/health` obligatoire.
- Ajoute un test smoke minimal.