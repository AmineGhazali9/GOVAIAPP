---
name: progressive-delivery
description: >
  Utilise ce skill pour construire GOVAIAPP étape par étape. Toujours: plan -> petit incrément -> tests -> résumé -> mise à jour demo_log -> validation humaine.
---

# Procédure Progressive Delivery (obligatoire)

À chaque demande de développement:
1) Produire un plan en 3 à 7 étapes maximum.
2) Exécuter uniquement l’étape 1.
3) Lancer les commandes de vérification/tests pertinentes.
4) Résumer ce qui a changé et quels fichiers ont été modifiés.
5) Mettre à jour `docs/demo_log.md` avec:
   - l’étape, le prompt, les fichiers modifiés, les commandes, le résultat attendu.
6) S’arrêter et demander: "Puis-je passer à l’étape suivante ?"
Contraintes
- Human-in-the-loop: ne jamais activer de mode qui bypass l’approbation.
- Si une dépendance (Azure/RAG) manque: fallback stub obligatoire.