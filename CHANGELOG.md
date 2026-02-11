# Changelog

Toutes les modifications notables de ce projet seront documentees dans ce fichier.

Le format est base sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [1.2.0] - 2026-02-11

### Ajoute
- Integration de l'API Claude (Anthropic) pour fonctionnalites IA
- Briefings intelligents generes par IA pour chaque contact
- Assistant conversationnel IA (page /assistant)
- Suggestions proactives sur le dashboard
- Page de parametres (/settings) pour configurer la cle API
- Choix du modele Claude (Sonnet 4.5, Haiku 4.5, Opus 4.6)
- Bouton "Briefing IA" dans le detail de chaque contact
- Liens navigation vers Assistant et Parametres dans l'en-tete
- Documentation de l'integration Claude (docs/CLAUDE_INTEGRATION.md)

### Technique
- Nouveau module `claude_integration.py` avec classe ClaudeIntegration
- 5 nouvelles routes API pour /api/claude/*
- 2 nouvelles pages (settings, assistant)
- Dependance `anthropic>=0.39.0` ajoutee
- Script de test scripts/test_claude_integration.py

## [1.1.0] - 2026-02-11

### Ajoute
- Systeme de mise a jour automatique integre
- Interface web d'administration des mises a jour (/admin/updates)
- Verification automatique des nouvelles versions depuis GitHub
- Mise a jour en un clic avec git pull
- Sauvegardes automatiques de la base de donnees avant chaque mise a jour
- Conservation des 5 dernieres sauvegardes
- Creation de sauvegardes manuelles
- Affichage du changelog dans l'interface
- Notification de mise a jour (badge vert) dans l'en-tete du CRM
- Documentation du systeme de mise a jour (docs/UPDATE_SYSTEM.md)

### Technique
- Nouveau module `update.py` avec classe UpdateManager
- 6 nouvelles routes Flask pour /admin/updates/* et /admin/backups
- Dependance `requests` ajoutee pour l'API GitHub
- Script de test scripts/test_update_system.py

## [1.0.0] - 2026-02-11

### Ajoute
- Systeme d'onboarding guide en 3 etapes
- Gestion complete des contacts (CRUD)
- Notes chronologiques par contact
- Profil master utilisateur
- Briefings pre-meeting avec extraction des promesses
- Recherche de contacts par nom et categorie
- Enrichissement web via DuckDuckGo (onboarding)
- Documentation complete (README, INSTALL, FAQ)
- Support deploiement Replit et Railway
- Script de validation pre-deploiement

### Securite
- Gitignore pour fichiers sensibles (.env, *.db, .secret_key)
- Variables d'environnement pour la configuration
- Cle secrete Flask auto-generee
