# Modele de gouvernance IA -- Regles metier

## Objectif

GOVAIAPP genere des politiques de gouvernance IA personnalisees
a partir du contexte d'une entreprise. Ce document decrit les regles
metier et fonctionnelles implementees.

---

## 1. Modele de donnees -- Contexte entreprise

Le formulaire capture 5 informations :

| Champ                 | Type                              | Obligatoire | Validation               |
|-----------------------|-----------------------------------|-------------|--------------------------|
| `nom`                 | string                            | Oui         | min 1 caractere          |
| `secteur`             | string                            | Oui         | min 1 caractere          |
| `maturite_donnees`    | enum                              | Oui         | debutant/intermediaire/avance |
| `principes_directeurs`| liste de strings                  | Non         | texte libre, 1 par ligne |
| `contraintes`         | string                            | Non         | texte libre              |

### Niveaux de maturite

| Niveau          | Signification                                    |
|-----------------|--------------------------------------------------|
| `debutant`      | Donnees peu structurees, pas de gouvernance       |
| `intermediaire` | Processus en cours, gouvernance partielle         |
| `avance`        | Donnees maitrisees, gouvernance etablie           |

---

## 2. Regles de generation de politique

### R1 -- Choix du mode de generation

```
SI FOUNDRY_ENABLED = true
   ET FOUNDRY_PROJECT_ENDPOINT est defini
   ET FOUNDRY_AGENT_PRODUCTEUR_ID est defini
ALORS -> Mode Foundry (agent Azure AI)
SINON -> Mode Stub (template local)
```

### R2 -- Fallback automatique

```
SI Mode Foundry actif
   ET l'appel Foundry echoue (erreur reseau, auth, agent)
ALORS -> Bascule silencieuse vers Mode Stub
   ET -> Log warning avec detail de l'erreur
```

### R3 -- Enrichissement RAG (mode stub)

```
SI Azure AI Search est configure (3 env vars)
ALORS -> Recherche de sources dans l'index Azure
   SI aucun resultat -> fallback stub local
SINON -> Lecture des sources depuis data/watch/veille_cache.md
```

### R4 -- Structure de la politique generee (mode stub)

La politique suit le template `data/policy_template.md` :

1. Titre avec nom de l'entreprise
2. Metadata : secteur, maturite donnees
3. Section principes directeurs (liste a puces)
4. Section contraintes identifiees
5. Section recommandations issues de la veille reglementaire (sources RAG)
6. Note de mode (stub vs Foundry)

### R5 -- Structure de la politique generee (mode Foundry)

Le prompt envoye a l'agent contient :
- Nom, secteur, maturite donnees
- Principes directeurs (liste)
- Contraintes specifiques
- Instruction : generer en markdown avec recommandations concretes

L'agent Foundry produit une politique libre en markdown.

---

## 3. Pipeline AutoGen -- Regles d'orchestration

### R6 -- Ordre sequentiel obligatoire

```
1. VeilleExterneAgent  -- collecte les signaux reglementaires
2. RagInterneAgent     -- enrichit avec les documents internes
3. ProducteurPolitiqueAgent -- synthetise la politique finale
```

Chaque agent recoit la sortie du precedent (chainage).

### R7 -- Resilience par agent

```
POUR CHAQUE agent du pipeline :
   SI Foundry configure pour cet agent
      ESSAYER appel Foundry
      SI echec -> message [FALLBACK NomAgent] + contexte original
   SINON -> message [STUB NomAgent] + contexte original
```

Le pipeline ne s'arrete jamais sur une erreur d'un agent individuel.

### R8 -- Terminaison du pipeline

Le pipeline se termine apres exactement 4 messages :
1. Message utilisateur (contexte entreprise)
2. Reponse VeilleExterneAgent
3. Reponse RagInterneAgent
4. Reponse ProducteurPolitiqueAgent

---

## 4. Sources de veille reglementaire (mode stub)

Le fichier `data/watch/veille_cache.md` contient les references suivantes :

| Source                                  | Theme                          |
|-----------------------------------------|--------------------------------|
| Referentiel IA de confiance -- UE       | AI Act, conformite             |
| Charte ethique IA -- OCDE              | Explicabilite, recours humain  |
| Guide CNIL -- IA et RGPD              | AIPD, DPO, donnees perso      |
| Framework de gouvernance IA -- Microsoft| Comite pluridisciplinaire      |

---

## 5. Agents Azure AI Foundry deployes

| Nom             | ID                              | Modele      | Outils          |
|-----------------|---------------------------------|-------------|-----------------|
| AgentExterne    | FOUNDRY_AGENT_VEILLE_EXTERNE_ID | gpt-5-nano  | --              |
| AgentRAG        | FOUNDRY_AGENT_RAG_ID            | gpt-5-chat  | Azure AI Search |
| AgentProducteur | FOUNDRY_AGENT_PRODUCTEUR_ID     | gpt-5-chat  | Files           |

Authentification : `DefaultAzureCredential` (Microsoft Entra ID).
Prerequis : role RBAC `Azure AI User` sur le projet Foundry.

---

## 6. Regles de validation (API)

| Regle                              | Implementation              | Erreur     |
|------------------------------------|-----------------------------|------------|
| nom obligatoire et non vide        | Pydantic `min_length=1`     | 422        |
| secteur obligatoire et non vide    | Pydantic `min_length=1`     | 422        |
| maturite parmi 3 valeurs           | Pydantic `Literal`          | 422        |
| erreur interne de generation       | try/except dans route       | 500        |
| Foundry indisponible               | fallback silencieux         | 200 (stub) |