"""Script unique : crée app/core/ + fichiers manquants sans écraser l'existant."""
import os
from pathlib import Path

ROOT = Path(__file__).parent

# 1. Créer le répertoire app/core
core_dir = ROOT / "app" / "core"
core_dir.mkdir(parents=True, exist_ok=True)
print(f"✓ {core_dir.relative_to(ROOT)}")

# 2. __init__.py (vide) – seulement si absent
init_file = core_dir / "__init__.py"
if not init_file.exists():
    init_file.write_text("", encoding="utf-8")
    print(f"✓ {init_file.relative_to(ROOT)} (créé)")
else:
    print(f"  {init_file.relative_to(ROOT)} (déjà présent)")

# 3. policy_template.md – seulement si absent
template_file = core_dir / "policy_template.md"
if not template_file.exists():
    template_file.write_text(
        "# Politique de gouvernance IA \u2013 {{nom}}\n\n"
        "**Secteur :** {{secteur}}\n"
        "**Maturit\u00e9 donn\u00e9es :** {{maturite_donnees}}\n\n"
        "---\n\n"
        "## Principes directeurs\n\n"
        "{{principes_directeurs}}\n\n"
        "## Contraintes identifi\u00e9es\n\n"
        "{{contraintes}}\n\n"
        "---\n\n"
        "## Recommandations issues de la veille r\u00e9glementaire\n\n"
        "{{sources}}\n\n"
        "---\n\n"
        "> *Politique g\u00e9n\u00e9r\u00e9e en mode stub \u2013 connecter Azure AI Foundry pour une analyse personnalis\u00e9e approfondie.*\n",
        encoding="utf-8",
    )
    print(f"✓ {template_file.relative_to(ROOT)} (créé)")
else:
    print(f"  {template_file.relative_to(ROOT)} (déjà présent)")

print("\nTerminé.")
