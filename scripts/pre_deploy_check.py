#!/usr/bin/env python3
"""
Script de validation avant deploiement.
Verifie que tout est pret pour la distribution.
"""

import os
import sys
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'


def check(condition, message):
    if condition:
        print(f"{Colors.GREEN}  {Colors.RESET} {message}")
        return True
    else:
        print(f"{Colors.RED}  {Colors.RESET} {message}")
        return False


def warn(message):
    print(f"{Colors.YELLOW}  {Colors.RESET} {message}")


def main():
    print("Verification pre-deploiement...\n")

    errors = 0
    warnings = 0

    # 1. Fichiers essentiels
    print("Fichiers essentiels")
    errors += not check(Path("README.md").exists(), "README.md existe")
    errors += not check(Path("requirements.txt").exists(), "requirements.txt existe")
    errors += not check(Path("app.py").exists(), "app.py existe")
    errors += not check(Path("config.py").exists(), "config.py existe")
    errors += not check(Path(".gitignore").exists(), ".gitignore existe")
    errors += not check(Path("LICENSE").exists(), "LICENSE existe")
    print()

    # 2. Configuration Replit
    print("Configuration Replit")
    errors += not check(Path(".replit").exists(), ".replit existe")
    errors += not check(Path("replit.nix").exists(), "replit.nix existe")
    print()

    # 3. Configuration Railway
    print("Configuration Railway")
    errors += not check(Path("Procfile").exists(), "Procfile existe")
    errors += not check(Path("runtime.txt").exists(), "runtime.txt existe")
    errors += not check(Path("railway.json").exists(), "railway.json existe")
    print()

    # 4. Structure des dossiers
    print("Structure")
    errors += not check(Path("static").is_dir(), "Dossier static/ existe")
    errors += not check(Path("static/index.html").exists(), "static/index.html existe")
    errors += not check(Path("templates").is_dir(), "Dossier templates/ existe")
    errors += not check(Path("templates/onboarding").is_dir(), "Dossier templates/onboarding/ existe")
    errors += not check(Path("data/.gitkeep").exists(), "data/.gitkeep existe")
    print()

    # 5. Fichiers sensibles NON commites
    print("Securite")
    if Path(".env").exists():
        warn(".env existe (ne doit PAS etre commite)")
        warnings += 1
    else:
        check(True, ".env n'existe pas (bon)")

    if Path("data/crm.db").exists():
        warn("crm.db existe (ne doit PAS etre commite)")
        warnings += 1
    else:
        check(True, "crm.db n'existe pas dans le repo (bon)")

    if Path(".secret_key").exists():
        warn(".secret_key existe (ne doit PAS etre commite)")
        warnings += 1
    else:
        check(True, ".secret_key n'existe pas (bon)")
    print()

    # 6. Contenu README
    print("README.md")
    with open("README.md", "r") as f:
        readme = f.read()
        errors += not check("Run on Replit" in readme, "Badge Replit present")
        errors += not check("Railway" in readme, "Mention Railway presente")
        errors += not check("Installation" in readme or "installation" in readme, "Section Installation presente")
        errors += not check("FAQ" in readme or "Support" in readme, "Section Support/FAQ presente")
    print()

    # 7. requirements.txt
    print("Dependances")
    with open("requirements.txt", "r") as f:
        reqs = f.read()
        errors += not check("Flask" in reqs or "flask" in reqs, "Flask dans requirements.txt")
        errors += not check("gunicorn" in reqs, "gunicorn dans requirements.txt")
    print()

    # 8. .gitignore
    print(".gitignore")
    with open(".gitignore", "r") as f:
        gitignore = f.read()
        errors += not check("*.db" in gitignore, "*.db dans .gitignore")
        errors += not check(".env" in gitignore, ".env dans .gitignore")
        errors += not check("data/" in gitignore or "data/*" in gitignore, "data/ dans .gitignore")
    print()

    # 9. Test d'import Python
    print("Import Python")
    try:
        import flask
        check(True, f"Flask importable (v{flask.__version__})")
    except ImportError:
        errors += not check(False, "Flask non importable - pip install -r requirements.txt")
    print()

    # Resume
    print("=" * 50)
    if errors == 0 and warnings == 0:
        print(f"{Colors.GREEN}Tout est OK ! Pret pour le deploiement.{Colors.RESET}")
        return 0
    elif errors == 0:
        print(f"{Colors.YELLOW}{warnings} warning(s) - Verifiez avant de deployer{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{errors} erreur(s) - Corrigez avant de deployer{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
