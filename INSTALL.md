# Guide d'installation detaille

Ce guide couvre tous les scenarios d'installation possibles.

## Table des matieres

1. [Replit](#replit)
2. [Railway](#railway)
3. [Installation locale](#installation-locale)
4. [Troubleshooting](#troubleshooting)

---

## Replit

### Prerequis
- Compte Replit (gratuit)
- Navigateur web

### Etapes

1. **Fork/Import le projet**
   - Methode 1 : Cliquer sur le badge "Run on Replit" dans le README
   - Methode 2 : Sur Replit.com > "Create" > "Import from GitHub" > `YOUR-USERNAME/personal-crm`

2. **Configuration automatique**
   - Replit detecte automatiquement le fichier `.replit`
   - Les dependances s'installent automatiquement

3. **Lancer l'app**
   - Cliquez sur "Run"
   - Attendez ~30 secondes
   - L'URL s'affiche en haut (ex: `https://personal-crm-YOUR-USERNAME.replit.app`)

4. **Configurer les secrets (optionnel)**
   - Menu gauche > Icone cadenas > "Secrets"
   - Ajouter `SECRET_KEY` : Genere auto ou creez-en un via :
     ```
     python -c "import secrets; print(secrets.token_hex(32))"
     ```

5. **Acceder a l'app**
   - Cliquez sur l'URL generee
   - L'onboarding demarre automatiquement

### Limitations plan gratuit Replit

- L'app "dort" apres 1h d'inactivite (se reveille au premier acces)
- 1 GB de stockage
- CPU et RAM limites

### Upgrade vers Hacker ($7/mois)

- Uptime 24/7 (always-on)
- Plus de ressources
- Domaine custom possible

---

## Railway

### Prerequis
- Compte Railway
- Compte GitHub (pour lier le repo)

### Etapes

1. **Deployer depuis GitHub**
   - Allez sur railway.app/new
   - "Deploy from GitHub repo"
   - Selectionnez `YOUR-USERNAME/personal-crm`
   - Railway detecte automatiquement Procfile et requirements.txt

2. **Configuration des variables**
   - Railway genere automatiquement `PORT`
   - Ajoutez manuellement :
     - `SECRET_KEY` : Generer via `python -c "import secrets; print(secrets.token_hex(32))"`
     - `FLASK_ENV` : `production`

3. **Deploiement**
   - Automatique apres configuration
   - Duree : ~2 minutes
   - URL generee : `https://your-app.railway.app`

4. **Domaine custom (optionnel)**
   - Settings > Networking > Custom Domain

### Couts Railway

- $5 de credit gratuit/mois
- Pay-as-you-go apres
- ~$5-10/mois pour usage normal

---

## Installation locale

### Prerequis
- Python 3.10+ installe
- Git installe
- Terminal/Command Prompt

### Etapes completes

1. **Cloner le repo**
   ```bash
   git clone https://github.com/YOUR-USERNAME/personal-crm.git
   cd personal-crm
   ```

2. **Creer l'environnement virtuel**
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installer les dependances**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configuration**
   ```bash
   cp .env.example .env
   # Editer .env avec votre editeur
   # Generer une SECRET_KEY :
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Lancer l'application**
   ```bash
   python app.py
   ```

6. **Acceder a l'app**
   - Ouvrir http://localhost:5000
   - L'onboarding demarre automatiquement

### Lancer en production
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

---

## Troubleshooting

### Erreur : "ModuleNotFoundError: No module named 'flask'"
```bash
# Verifier que l'environnement virtuel est active
which python  # Doit pointer vers venv/bin/python
# Reinstaller les dependances
pip install -r requirements.txt
```

### Erreur : "Address already in use"
```bash
# Changer le port
export PORT=5001
python app.py
```

### L'app Replit ne demarre pas
1. Verifier que `.replit` existe
2. Cliquer sur "Shell" et lancer manuellement : `python app.py`
3. Regarder les logs d'erreur

### Railway : Deploiement echoue
1. Verifier les logs : Settings > Deployment Logs
2. Verifier que `Procfile` existe
3. Verifier que `gunicorn` est dans `requirements.txt`
