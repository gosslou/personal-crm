# CRM Personnel - Gestion intelligente de contacts

Un CRM personnel avec onboarding guide pour gerer efficacement vos contacts professionnels et personnels.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Fonctionnalites

- **Gestion complete des contacts** : Ajout, modification, recherche, categories
- **Notes chronologiques** : Historique des interactions avec chaque contact
- **Briefings intelligents** : Resume pre-meeting avec promesses en attente
- **Onboarding guide** : Configuration en 5 minutes avec enrichissement web
- **Vos donnees chez vous** : Hebergement personnel, aucun tiers
- **Responsive** : Fonctionne sur mobile, tablette et desktop

---

## Installation rapide (2 minutes)

### Option 1 : Replit (Recommande - Zero config)

**Parfait pour : Utilisateurs non-techniques, test rapide**

1. Cliquez sur ce bouton :

   [![Run on Replit](https://replit.com/badge/github/YOUR-USERNAME/personal-crm)](https://replit.com/new/github/YOUR-USERNAME/personal-crm)

2. Creez un compte Replit gratuit (si vous n'en avez pas)
3. Le projet se clone automatiquement
4. Cliquez sur **"Run"**
5. Votre CRM demarre ! Cliquez sur l'URL generee
6. Suivez l'onboarding guide (5 minutes)

**C'est tout !**

### Option 2 : Railway (~$5/mois)

**Parfait pour : Usage professionnel, uptime 24/7**

1. Cliquez sur ce bouton :

   [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR-TEMPLATE-ID)

2. Creez un compte Railway
3. Les variables d'environnement se configurent automatiquement
4. Deploiement automatique en ~2 min
5. Accedez a votre URL Railway

### Option 3 : Installation locale (Developpeurs)

```bash
# 1. Cloner le repo
git clone https://github.com/YOUR-USERNAME/personal-crm.git
cd personal-crm

# 2. Creer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dependances
pip install -r requirements.txt

# 4. Creer le fichier .env
cp .env.example .env
# Editer .env avec vos valeurs

# 5. Lancer l'application
python app.py

# 6. Ouvrir http://localhost:5000
```

---

## Premier lancement

Au premier lancement, l'onboarding vous guide pour :

1. **Enrichir votre profil** via LinkedIn ou recherche web
2. **Repondre a quelques questions** (formation, hobbies, style de communication)
3. **Valider votre profil** et commencer a utiliser le CRM

**Duree : 5 minutes**

---

## Configuration avancee

### Variables d'environnement

| Variable | Description | Defaut | Requis |
|----------|-------------|--------|--------|
| `SECRET_KEY` | Cle secrete Flask | Auto-genere | Non |
| `DATABASE_PATH` | Chemin de la DB | `data/crm.db` | Non |
| `PORT` | Port d'ecoute | `5000` | Non |
| `FLASK_ENV` | Environnement | `development` | Non |
| `ENABLE_WEB_ENRICHMENT` | Enrichissement web | `True` | Non |

### Configuration Replit

Les secrets se configurent dans l'onglet **"Secrets"** (icone cadenas) du menu gauche Replit.

### Configuration Railway

Les variables se configurent dans **Settings > Variables** du dashboard Railway.

---

## Utilisation

### Gerer vos contacts

- **Ajouter** : Bouton "+ Nouveau contact" en haut
- **Modifier** : Cliquez sur un contact > "Modifier"
- **Supprimer** : Cliquez sur un contact > "Supprimer"
- **Rechercher** : Barre de recherche + filtre par categorie

### Categories

- **Famille** : Contacts familiaux
- **Amis** : Contacts personnels
- **Pro** : Contacts professionnels
- **Autre** : Tout le reste

### Notes chronologiques

1. Ouvrez un contact
2. Section "Notes" en bas
3. Tapez votre note et cliquez "Ajouter"
4. Horodatage automatique

### Briefings

Accedez au briefing d'un contact via `/briefing/<id>` pour un resume complet avant un meeting.

---

## FAQ

**Mes donnees sont-elles securisees ?**
Oui. Vos donnees restent sur votre instance personnelle. Personne d'autre n'y a acces.

**Puis-je exporter mes donnees ?**
Oui. La base SQLite est dans `data/crm.db`. Telechargez-la depuis Replit/Railway.

**Combien ca coute ?**
- Replit : Gratuit (avec limitations) ou $7/mois (Hacker plan)
- Railway : ~$5/mois
- Local : Gratuit

**L'app Replit "dort" ?**
Plan gratuit : mise en veille apres 1h d'inactivite. Upgrade vers Hacker ($7/mois) pour always-on.

---

## Support

- [Guide d'installation detaille](./INSTALL.md)
- [FAQ complete](./docs/FAQ.md)
- [Issues GitHub](https://github.com/YOUR-USERNAME/personal-crm/issues)

---

## License

MIT License - voir [LICENSE](LICENSE)

---

## Roadmap

- [ ] Export contacts en CSV/Excel
- [ ] Import depuis LinkedIn/Google Contacts
- [ ] Rappels automatiques (anniversaires, follow-ups)
- [ ] Tags personnalises
- [ ] Recherche avancee avec filtres
- [ ] Integration calendrier
