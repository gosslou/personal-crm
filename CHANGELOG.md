# Changelog

Toutes les modifications notables de ce projet seront documentees dans ce fichier.

Le format est base sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

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
- Systeme de mise a jour automatique avec backups
- Interface d'administration des mises a jour
- Script de validation pre-deploiement

### Securite
- Gitignore pour fichiers sensibles (.env, *.db, .secret_key)
- Variables d'environnement pour la configuration
- Cle secrete Flask auto-generee
