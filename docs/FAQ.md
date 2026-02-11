# FAQ - Questions frequentes

## General

### Qu'est-ce que ce CRM ?
Un CRM personnel pour gerer vos contacts professionnels et personnels, avec enrichissement automatique et briefings pre-meeting.

### Pourquoi ce CRM plutot qu'un autre ?
- **Vos donnees chez vous** : Pas de big tech qui possede vos contacts
- **Gratuit ou pas cher** : Replit gratuit ou ~$5/mois
- **Simple** : Interface epuree, pas de bloat
- **Personnalisable** : Code ouvert, modifiable a volonte

### Est-ce securise ?
Oui. Vos donnees restent sur votre instance (Replit/Railway/serveur personnel). Elles ne sont jamais partagees avec des tiers.

---

## Installation

### Quelle option choisir ?

| Critere | Replit | Railway | Local |
|---------|--------|---------|-------|
| **Facilite** | Tres facile | Facile | Moyen |
| **Gratuit** | Oui (limite) | ~$5/mois | Oui |
| **Uptime 24/7** | Non (upgrade $7) | Oui | Depend de vous |
| **Personnalisation** | Moyenne | Bonne | Totale |

**Recommandation** : Commencez avec Replit gratuit. Si ca vous plait, upgradez.

---

## Utilisation

### Comment ajouter un contact ?
1. Bouton "+ Nouveau contact"
2. Remplir : Nom, Prenom, Categorie
3. Champs optionnels : Societe, Telephone, Email, Ville, Anniversaire
4. Informations supplementaires en JSON pour les champs libres
5. Sauvegarder

### Comment rechercher un contact ?
- Barre de recherche en haut
- Recherche dans : Nom, Prenom, Informations
- Filtre par categorie

### Comment exporter mes donnees ?
Telechargez le fichier `data/crm.db` :
- Replit : Files > `data/crm.db` > Download
- Railway : Via CLI Railway
- Local : Copier `data/crm.db`

---

## Donnees & Confidentialite

### Ou sont stockees mes donnees ?
- Replit : Serveurs Replit (USA)
- Railway : Cloud providers
- Local : Sur votre machine

### Qui a acces a mes donnees ?
Uniquement vous.

### Puis-je migrer vers une autre plateforme ?
Oui. Exportez votre `crm.db` et importez-le dans une nouvelle instance.

---

## Problemes courants

### L'app Replit met du temps a se reveiller
Plan gratuit : mise en veille apres 1h d'inactivite. Upgrade vers Hacker ($7/mois) pour always-on.

### La recherche web dans l'onboarding ne fonctionne pas
Restriction reseau ou rate limit. Remplissez manuellement, la recherche web est optionnelle.

### Mes notes ne s'enregistrent pas
1. Verifier les logs
2. Verifier que `data/` est accessible en ecriture
3. Redemarrer l'app

---

## Personnalisation

### Puis-je changer les couleurs ?
Oui. Modifiez `static/css/onboarding.css` pour l'onboarding, ou le CSS inline dans `static/index.html`.

### Puis-je ajouter des champs personnalises ?
Oui. Le champ "Informations" accepte n'importe quel JSON.

### Claude Code peut-il m'aider a personnaliser ?
Oui. Decrivez ce que vous voulez a Claude Code et il modifiera le code pour vous.
