@echo off
cd /d "C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP"
mkdir app\core 2>nul
if exist app\core (
    echo ✓ Directory app\core created successfully
) else (
    echo ✗ Failed to create directory app\core
    exit /b 1
)

REM Create empty __init__.py
type nul > app\core\__init__.py
if exist app\core\__init__.py (
    echo ✓ File app\core\__init__.py created successfully
) else (
    echo ✗ Failed to create app\core\__init__.py
    exit /b 1
)

REM Create policy_template.md with exact content
(
echo # Politique de gouvernance IA -- {{nom}}
echo.
echo **Secteur :** {{secteur}}
echo **Maturite donnees :** {{maturite_donnees}}
echo.
echo ---
echo.
echo ## Principes directeurs
echo.
echo {{principes_directeurs}}
echo.
echo ## Contraintes identifiees
echo.
echo {{contraintes}}
echo.
echo ---
echo.
echo ## Recommandations issues de la veille reglementaire
echo.
echo {{sources}}
echo.
echo ---
echo.
echo ^> *Politique generee en mode stub -- connecter Azure AI Foundry pour une analyse personnalisee approfondie.*
) > app\core\policy_template.md
if exist app\core\policy_template.md (
    echo ✓ File app\core\policy_template.md created successfully
) else (
    echo ✗ Failed to create app\core\policy_template.md
    exit /b 1
)

echo.
echo All files created successfully!
