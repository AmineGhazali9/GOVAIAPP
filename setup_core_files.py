#!/usr/bin/env python3
import os
import sys

# Define paths
base_path = r"C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP"
core_dir = os.path.join(base_path, "app", "core")

try:
    # Create directory
    os.makedirs(core_dir, exist_ok=True)
    print(f"✓ Directory {core_dir} created successfully")
    
    # Create empty __init__.py
    init_file = os.path.join(core_dir, "__init__.py")
    open(init_file, 'w').close()
    print(f"✓ File {init_file} created successfully")
    
    # Create policy_template.md
    template_content = """# Politique de gouvernance IA – {{nom}}

**Secteur :** {{secteur}}
**Maturité données :** {{maturite_donnees}}

---

## Principes directeurs

{{principes_directeurs}}

## Contraintes identifiées

{{contraintes}}

---

## Recommandations issues de la veille réglementaire

{{sources}}

---

> *Politique générée en mode stub – connecter Azure AI Foundry pour une analyse personnalisée approfondie.*
"""
    
    template_file = os.path.join(core_dir, "policy_template.md")
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    print(f"✓ File {template_file} created successfully")
    
    print("\nAll files created successfully!")
    sys.exit(0)
    
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
