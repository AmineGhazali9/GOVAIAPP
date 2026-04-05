---
name: agent-logging
description: >
  Journalise chaque action des agents (Dev, QA, Doc, Validator) dans docs/demo_log.md.
  Use when: un agent termine une action, un incrément, un test, une PR, ou une validation.
  Produit un tableau Markdown chronologique avec date, agent, action et résultat.
---

# Journalisation des actions agents

## Quand utiliser
- Après chaque action significative d'un agent (création de fichier, test, PR, documentation).
- Lors d'un handoff entre agents.
- En fin d'incrément dans le workflow progressive-delivery.

## Procédure

### 1. Vérifier l'existence du journal
- Si `docs/demo_log.md` n'existe pas, le créer avec le template ci-dessous.

### 2. Ajouter une entrée
Ajouter une ligne au tableau dans `docs/demo_log.md` avec les colonnes suivantes :

| Colonne  | Description                                      |
|----------|--------------------------------------------------|
| Date     | Date et heure au format `YYYY-MM-DD HH:MM`       |
| Agent    | Nom de l'agent (Dev, QA, Doc, Validator)          |
| Action   | Description courte de l'action effectuée          |
| Résultat | ✅ Succès, ⚠️ Partiel, ❌ Échec                   |

### 3. Format d'une entrée

```markdown
| 2026-04-05 14:30 | Dev | Scaffold FastAPI + Streamlit | ✅ Succès |
```

### 4. Template initial

Si le fichier `docs/demo_log.md` n'existe pas, le créer avec ce contenu :

```markdown
# Journal des actions agents – GOVAIAPP

| Date | Agent | Action | Résultat |
|------|-------|--------|----------|
```

### 5. Règles
- Une ligne par action atomique (pas de regroupement).
- Ne jamais supprimer d'entrées existantes (append only).
- Lors d'un handoff, l'agent sortant ajoute une entrée "Handoff vers [Agent]".
- En cas d'échec, préciser brièvement la raison dans la colonne Action.

## Exemple complet

```markdown
# Journal des actions agents – GOVAIAPP

| Date | Agent | Action | Résultat |
|------|-------|--------|----------|
| 2026-04-05 10:00 | Dev | Scaffold initial FastAPI + Streamlit | ✅ Succès |
| 2026-04-05 10:15 | Dev | Ajout endpoint /health | ✅ Succès |
| 2026-04-05 10:20 | Dev | Handoff vers QA | ✅ Succès |
| 2026-04-05 10:25 | QA | Tests smoke /health | ✅ Succès |
| 2026-04-05 10:30 | QA | Test endpoint /evaluate – timeout | ❌ Échec |
| 2026-04-05 10:35 | QA | Handoff vers Dev avec rapport de bug | ✅ Succès |
| 2026-04-05 11:00 | Dev | Fix timeout /evaluate | ✅ Succès |
| 2026-04-05 11:05 | Doc | Mise à jour docs/architecture.md | ✅ Succès |
| 2026-04-05 11:10 | Validator | Création branche + PR #1 | ✅ Succès |
| 2026-04-05 11:15 | Validator | Revue Copilot déclenchée | ✅ Succès |
```
