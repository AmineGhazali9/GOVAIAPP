---
name: rag-azure-ai-search
description: >
  Utilise ce skill pour implémenter une couche RAG simple via Azure AI Search (index) avec fallback stub local.
---

# RAG Azure AI Search (minimal et fiable)

Objectif
- Fournir une fonction `retrieve(query)` qui renvoie des passages + métadonnées.
- Utiliser des variables d’environnement.
- Si non configuré: retourner un stub déterministe à partir d’un fichier local.

Règles
- Pas de secrets dans le code.
- Ajouter une section README "Configuration Azure AI Search" listant les variables requises.
- Ajouter un test smoke sans dépendance Azure.