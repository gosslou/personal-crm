# Systeme de mise a jour

## Pour les utilisateurs

### Verifier les mises a jour

1. Cliquez sur "Mises a jour" dans l'en-tete du CRM
2. Le systeme verifie automatiquement les nouvelles versions sur GitHub
3. Si une mise a jour est disponible, un bouton vert apparait

Un point vert sur le lien "Mises a jour" indique qu'une nouvelle version est disponible.

### Appliquer une mise a jour

1. Cliquer sur "Mettre a jour maintenant"
2. Confirmer dans la boite de dialogue
3. Attendre la fin (30-60 secondes)
4. Redemarrer l'application

**Important :** Une sauvegarde automatique de la base de donnees est creee avant chaque mise a jour.

### Sauvegardes

- Les 5 dernieres sauvegardes sont conservees automatiquement dans `data/backups/`
- Vous pouvez creer une sauvegarde manuelle depuis la page "Mises a jour"

Pour restaurer une sauvegarde manuellement :
```bash
cp data/backups/crm_backup_YYYYMMDD_HHMMSS.db data/crm.db
```

---

## Pour les developpeurs

### Publier une nouvelle version

1. **Developper la fonctionnalite**

2. **Mettre a jour CHANGELOG.md**
   ```markdown
   ## [1.1.0] - 2026-XX-XX

   ### Ajoute
   - Nouvelle fonctionnalite X

   ### Corrige
   - Bug Y
   ```

3. **Mettre a jour la version dans config.py**
   ```python
   APP_VERSION = "1.1.0"
   ```

4. **Commit, tag et push**
   ```bash
   git add .
   git commit -m "feat: Add feature X - v1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

5. **Creer une release sur GitHub** (optionnel)
   - GitHub > Releases > "Draft a new release"
   - Tag: v1.1.0
   - Copier le contenu du CHANGELOG pour cette version

### Architecture

```
update.py
  UpdateManager
    check_for_updates()     # Verifie GitHub (releases puis commits)
    backup_database()       # Copie crm.db dans data/backups/
    update_from_github()    # git stash + git pull origin main
    get_changelog()         # Lit CHANGELOG.md
    list_backups()          # Liste les fichiers de backup
```

### Flow de mise a jour

```
1. User clique "Mettre a jour"
2. Backup de crm.db
3. git stash (modifications locales)
4. git pull origin main
5. pip install -r requirements.txt (si modifie)
6. Redemarrage requis
```

### Routes API

| Route | Methode | Description |
|-------|---------|-------------|
| `/admin/updates` | GET | Page d'administration |
| `/admin/updates/check` | GET | Verifie les mises a jour (JSON) |
| `/admin/updates/apply` | POST | Applique la mise a jour |
| `/admin/updates/changelog` | GET | Retourne le changelog |
| `/admin/backups` | GET | Liste les backups |
| `/admin/backups/create` | POST | Cree un backup manuel |
