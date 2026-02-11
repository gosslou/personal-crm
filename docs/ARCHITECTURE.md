# Architecture du CRM Personnel

## Vue d'ensemble

```
personal-crm/
├── app.py              # Point d'entree Flask, routes API
├── config.py           # Configuration centralisee (env vars)
├── database.py         # Couche d'acces SQLite
├── models.py           # Validation des donnees
├── onboarding.py       # Blueprint d'onboarding (3 etapes)
├── crm_briefing.py     # Generation de briefings
├── static/             # Frontend (HTML/CSS/JS)
│   ├── index.html      # Application SPA
│   └── css/
│       └── onboarding.css
├── templates/          # Templates Jinja2
│   ├── briefing.html
│   └── onboarding/
│       ├── welcome.html
│       ├── step1.html
│       ├── step2.html
│       └── step3.html
└── data/               # Donnees (gitignored)
    └── crm.db          # Base SQLite
```

## Base de donnees

Table unique `contacts` avec champs JSON flexibles :

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT DEFAULT '',
    categorie TEXT DEFAULT 'autre',
    informations TEXT DEFAULT '{}',    -- JSON dict
    notes TEXT DEFAULT '[]',           -- JSON array
    date_creation TEXT NOT NULL,
    date_modification TEXT NOT NULL
);
```

- `informations` : Dict JSON flexible (societe, poste, email, telephone, etc.)
- `notes` : Array JSON de `{date, contenu}`
- Profil master identifie par `"type": "profil_master"` dans informations

## API REST

| Methode | Route | Description |
|---------|-------|-------------|
| GET | `/api/contacts` | Liste tous les contacts |
| POST | `/api/contacts` | Cree un contact |
| GET | `/api/contacts/<id>` | Recupere un contact |
| PUT | `/api/contacts/<id>` | Met a jour un contact |
| DELETE | `/api/contacts/<id>` | Supprime un contact |
| POST | `/api/contacts/<id>/notes` | Ajoute une note |
| GET | `/api/search?q=...&categorie=...` | Recherche |
| GET | `/api/health` | Health check |
| GET | `/api/master-profile` | Profil master |
| GET | `/briefing/<id>` | Briefing HTML |
| GET | `/api/briefing/<id>` | Briefing JSON |

## Onboarding

Flux en 3 etapes avec Blueprint Flask :
1. Enrichissement profil (LinkedIn ou recherche DuckDuckGo)
2. Questions personnalisees (formation, hobbies, style)
3. Validation et creation du profil master

Le `@before_request` redirige vers l'onboarding si aucun profil master n'existe.
