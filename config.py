"""
config.py - Configuration centralisee pour le CRM Personnel.

Gere les variables d'environnement et les parametres de l'application
pour tous les environnements (dev, production, Replit, Railway).
"""

import os
from datetime import timedelta


class Config:
    """Configuration de base."""

    # Cle secrete Flask (generee automatiquement si absente)
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

    # Base de donnees
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join('data', 'crm.db')

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

    # Application
    APP_NAME = "CRM Personnel"
    APP_VERSION = "1.0.0"

    # GitHub (pour systeme de mise a jour)
    GITHUB_REPO = "gosslou/personal-crm"
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"

    # Onboarding
    ENABLE_WEB_ENRICHMENT = os.environ.get('ENABLE_WEB_ENRICHMENT', 'True').lower() == 'true'

    @staticmethod
    def init_app(app):
        """Initialise l'application avec la config."""
        db_dir = os.path.dirname(Config.DATABASE_PATH)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)


class DevelopmentConfig(Config):
    """Config developpement."""
    DEBUG = True


class ProductionConfig(Config):
    """Config production."""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
