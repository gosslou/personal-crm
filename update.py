"""
update.py - Gestion des mises a jour de l'application.

Verifie les nouvelles versions sur GitHub, cree des backups
de la base de donnees, et applique les mises a jour via git pull.
"""

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

import requests

from config import Config


class UpdateManager:
    """Gere les mises a jour de l'application."""

    def __init__(self):
        self.current_version = Config.APP_VERSION
        self.github_api = Config.GITHUB_API_URL
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self):
        """
        Verifie si une mise a jour est disponible sur GitHub.

        Essaie d'abord les releases GitHub, puis les commits en fallback.
        """
        try:
            response = requests.get(
                f"{self.github_api}/releases/latest",
                timeout=10
            )

            if response.status_code == 404:
                return self._check_commits()

            if response.status_code != 200:
                return self._check_commits()

            release = response.json()
            latest_version = release['tag_name'].lstrip('v')

            return {
                'update_available': self._compare_versions(latest_version, self.current_version),
                'latest_version': latest_version,
                'current_version': self.current_version,
                'release_notes': release.get('body', 'Aucune note de version'),
                'published_at': release.get('published_at', '')
            }

        except Exception as e:
            return {
                'error': True,
                'message': f"Erreur lors de la verification : {str(e)}",
                'current_version': self.current_version
            }

    def _check_commits(self):
        """Fallback : verifie les commits si pas de releases."""
        try:
            response = requests.get(
                f"{self.github_api}/commits/main",
                timeout=10
            )

            if response.status_code != 200:
                return {
                    'error': True,
                    'message': 'Impossible de verifier les mises a jour',
                    'current_version': self.current_version
                }

            commit = response.json()

            try:
                local_commit = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout.strip()

                update_available = commit['sha'] != local_commit
            except (subprocess.CalledProcessError, FileNotFoundError):
                update_available = False

            return {
                'update_available': update_available,
                'latest_version': commit['sha'][:7],
                'current_version': self.current_version,
                'release_notes': commit['commit']['message'],
                'published_at': commit['commit']['author']['date']
            }

        except Exception as e:
            return {
                'error': True,
                'message': str(e),
                'current_version': self.current_version
            }

    def _compare_versions(self, v1, v2):
        """Compare deux versions semver. Retourne True si v1 > v2."""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            return v1_parts > v2_parts
        except (ValueError, AttributeError):
            return v1 != v2

    def backup_database(self):
        """Cree une sauvegarde de la base de donnees."""
        try:
            db_path = Path(Config.DATABASE_PATH)

            if not db_path.exists():
                return {
                    'success': False,
                    'message': 'Base de donnees introuvable'
                }

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"crm_backup_{timestamp}.db"

            shutil.copy2(db_path, backup_path)

            self._cleanup_old_backups(keep=5)

            return {
                'success': True,
                'backup_path': str(backup_path),
                'message': f'Backup cree : {backup_path.name}'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur backup : {str(e)}'
            }

    def _cleanup_old_backups(self, keep=5):
        """Supprime les anciens backups, garde les N plus recents."""
        backups = sorted(
            self.backup_dir.glob("crm_backup_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        for old_backup in backups[keep:]:
            old_backup.unlink()

    def update_from_github(self):
        """Execute la mise a jour depuis GitHub via git pull."""
        try:
            # 1. Backup de la DB
            backup_result = self.backup_database()
            if not backup_result['success']:
                return {
                    'success': False,
                    'message': 'Echec du backup, mise a jour annulee',
                    'output': backup_result['message']
                }

            # 2. Verifier que c'est un repo Git
            if not Path('.git').exists():
                return {
                    'success': False,
                    'message': 'Pas un depot Git. Impossible de mettre a jour.',
                    'output': ''
                }

            # 3. Stash les modifications locales
            subprocess.run(
                ['git', 'stash'],
                capture_output=True,
                timeout=10
            )

            # 4. Pull depuis GitHub
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                return {
                    'success': False,
                    'message': 'Echec de la mise a jour',
                    'output': result.stderr
                }

            # 5. Installer les nouvelles dependances si besoin
            if 'requirements.txt' in result.stdout:
                pip_result = subprocess.run(
                    ['pip', 'install', '-r', 'requirements.txt'],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if pip_result.returncode != 0:
                    return {
                        'success': True,
                        'message': 'Mise a jour reussie. Redemarrage requis pour les nouvelles dependances.',
                        'output': result.stdout
                    }

            return {
                'success': True,
                'message': 'Mise a jour reussie ! Redemarrez l\'application.',
                'output': result.stdout
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'message': 'Timeout lors de la mise a jour',
                'output': ''
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur inattendue : {str(e)}',
                'output': ''
            }

    def get_changelog(self):
        """Lit le fichier CHANGELOG.md."""
        try:
            changelog_path = Path('CHANGELOG.md')
            if changelog_path.exists():
                return changelog_path.read_text(encoding='utf-8')
            return "Aucun changelog disponible."
        except Exception as e:
            return f"Erreur lecture changelog : {str(e)}"

    def list_backups(self):
        """Liste les backups disponibles."""
        if not self.backup_dir.exists():
            return []

        backups = []
        for backup in sorted(self.backup_dir.glob('crm_backup_*.db'), reverse=True):
            stat = backup.stat()
            backups.append({
                'name': backup.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

        return backups
