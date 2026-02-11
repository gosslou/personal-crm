#!/usr/bin/env python3
"""Test du systeme de mise a jour."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from update import UpdateManager


def test_update_system():
    print("Test du systeme de mise a jour\n")

    manager = UpdateManager()

    # Test 1: Version
    print("1. Test verification de version...")
    result = manager.check_for_updates()

    if result.get('error'):
        print(f"   Erreur: {result.get('message', 'Inconnue')}")
    else:
        print(f"   Version actuelle: {result['current_version']}")
        if result['update_available']:
            print(f"   Mise a jour disponible: {result['latest_version']}")
        else:
            print("   A jour")

    # Test 2: Backup
    print("\n2. Test backup de la base de donnees...")
    backup_result = manager.backup_database()

    if backup_result['success']:
        print(f"   OK: {backup_result['message']}")
    else:
        print(f"   Info: {backup_result['message']}")

    # Test 3: Changelog
    print("\n3. Test lecture du changelog...")
    changelog = manager.get_changelog()
    print(f"   Changelog charge ({len(changelog)} caracteres)")

    # Test 4: List backups
    print("\n4. Test liste des backups...")
    backups = manager.list_backups()
    print(f"   {len(backups)} backup(s) trouve(s)")

    # Test 5: Compare versions
    print("\n5. Test comparaison de versions...")
    assert manager._compare_versions("1.1.0", "1.0.0") is True
    assert manager._compare_versions("1.0.0", "1.0.0") is False
    assert manager._compare_versions("0.9.0", "1.0.0") is False
    assert manager._compare_versions("2.0.0", "1.9.9") is True
    print("   Toutes les comparaisons OK")

    print("\nTests termines !")


if __name__ == "__main__":
    test_update_system()
