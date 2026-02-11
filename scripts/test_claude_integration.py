#!/usr/bin/env python3
"""Test de l'integration Claude API."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeIntegration, ANTHROPIC_AVAILABLE


def test_claude_integration():
    print("Test de l'integration Claude API\n")

    # Test 1: Module anthropic
    print("1. Verification du module anthropic...")
    if ANTHROPIC_AVAILABLE:
        print("   OK: Module anthropic installe")
    else:
        print("   ATTENTION: Module anthropic non installe (pip install anthropic)")

    # Test 2: Instanciation
    print("\n2. Test instanciation ClaudeIntegration...")
    claude = ClaudeIntegration()
    print(f"   OK: Instance creee")
    print(f"   Configuree: {claude.is_configured()}")
    print(f"   Modele: {claude.model}")
    print(f"   Max tokens: {claude.max_tokens}")

    # Test 3: Test sans cle API
    print("\n3. Test connexion sans cle API...")
    result = claude.test_connection()
    assert not result['success'], "Devrait echouer sans cle API"
    print(f"   OK: {result['message']}")

    # Test 4: Test update_api_key
    print("\n4. Test update_api_key...")
    claude.update_api_key("sk-fake-key")
    assert claude.api_key == "sk-fake-key"
    claude.update_api_key("")
    assert not claude.is_configured()
    print("   OK: Mise a jour de la cle fonctionne")

    # Test 5: Briefing sans cle
    print("\n5. Test generate_briefing sans cle...")
    contact = {"nom": "Test", "prenom": "Contact", "categorie": "pro", "informations": {}, "notes": []}
    result = claude.generate_briefing(contact)
    assert not result['success']
    print(f"   OK: {result['message']}")

    # Test 6: Assistant sans cle
    print("\n6. Test ask_assistant sans cle...")
    result = claude.ask_assistant("Test question")
    assert not result['success']
    print(f"   OK: {result['message']}")

    # Test 7: Suggestions sans cle
    print("\n7. Test generate_dashboard_suggestions sans cle...")
    result = claude.generate_dashboard_suggestions([contact])
    assert not result['success']
    print(f"   OK: {result['message']}")

    # Test 8: Avec cle API reelle (si disponible)
    api_key = os.environ.get('CLAUDE_API_KEY', '')
    if api_key:
        print("\n8. Test avec cle API reelle...")
        claude_real = ClaudeIntegration(api_key=api_key)
        result = claude_real.test_connection()
        print(f"   Resultat: {'OK' if result['success'] else result['message']}")
    else:
        print("\n8. Test avec cle API reelle... IGNORE (CLAUDE_API_KEY non defini)")

    print("\nTests termines !")


if __name__ == "__main__":
    test_claude_integration()
