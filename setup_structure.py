#!/usr/bin/env python
"""Setup GOVAIAPP directory structure."""

import os
import sys

base_path = os.path.dirname(os.path.abspath(__file__))

# Define directory structure
directories = [
    "app",
    "app\\api",
    "app\\ui",
    "app\\agents",
    "app\\rag",
    "app\\core",
    "tests",
    "data",
    "data\\watch"
]

# Create all directories
print("Creating directories:")
for dir_path in directories:
    full_path = os.path.join(base_path, dir_path)
    os.makedirs(full_path, exist_ok=True)
    print(f"  ✓ {dir_path}")

# Define files with content
files = {
    "app\\__init__.py": "",
    "app\\api\\__init__.py": "",
    "app\\api\\main.py": "# app/api/main.py – point d'entrée FastAPI (à remplir phase 3)\n",
    "app\\api\\schemas.py": "# app/api/schemas.py – schémas Pydantic (à remplir phase 3)\n",
    "app\\api\\routes.py": "# app/api/routes.py – routes FastAPI (à remplir phase 3)\n",
    "app\\ui\\__init__.py": "",
    "app\\ui\\app.py": "# app/ui/app.py – interface Streamlit (à remplir phase 4)\n",
    "app\\agents\\__init__.py": "",
    "app\\agents\\orchestrator.py": "# app/agents/orchestrator.py – orchestrateur AutoGen (à remplir phase 5)\n",
    "app\\rag\\__init__.py": "",
    "app\\rag\\retriever.py": "# app/rag/retriever.py – connecteur RAG (à remplir phase 5)\n",
    "app\\core\\__init__.py": "",
    "app\\core\\policy_template.md": "# Politique de gouvernance IA – {{nom}}\n\n**Secteur :** {{secteur}}\n**Maturité données :** {{maturite_donnees}}\n\n---\n\n## Principes directeurs\n\n{{principes_directeurs}}\n\n## Contraintes identifiées\n\n{{contraintes}}\n\n---\n\n## Recommandations issues de la veille réglementaire\n\n{{sources}}\n\n---\n\n> *Politique générée en mode stub – connecter Azure AI Foundry pour une analyse personnalisée approfondie.*\n",
    "tests\\__init__.py": "",
    "tests\\test_smoke.py": "# tests/test_smoke.py – tests smoke (à remplir phase 6)\n",
    "data\\watch\\veille_cache.md": "# Veille cache – passages fictifs (à remplir phase 5)\n"
}

# Create all files
print("\nCreating files:")
for file_rel_path, content in files.items():
    full_path = os.path.join(base_path, file_rel_path)
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        file_size = len(content)
        status = "✓"
        if file_size == 0:
            print(f"  {status} {file_rel_path} (empty)")
        else:
            print(f"  {status} {file_rel_path} ({file_size} bytes)")
    except Exception as e:
        print(f"  ✗ {file_rel_path} - ERROR: {e}")
        sys.exit(1)

print("\n✓ Directory structure created successfully!")
