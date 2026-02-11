# Integration Claude API

## Configuration

### 1. Obtenir une cle API

1. Allez sur [console.anthropic.com](https://console.anthropic.com/)
2. Creez un compte ou connectez-vous
3. Allez dans **API Keys**
4. Creez une nouvelle cle (commence par `sk-ant-`)

### 2. Configurer dans le CRM

**Option A : Via l'interface** (recommande)
1. Cliquez sur **Parametres** dans l'en-tete du CRM
2. Collez votre cle API
3. Cliquez sur **Tester la connexion**
4. Cliquez sur **Enregistrer**

**Option B : Via variable d'environnement**
```bash
export CLAUDE_API_KEY="sk-ant-api03-..."
```

Ou dans `.env` :
```
CLAUDE_API_KEY=sk-ant-api03-...
```

### 3. Variables d'environnement

| Variable | Description | Defaut |
|----------|-------------|--------|
| `CLAUDE_API_KEY` | Cle API Anthropic | (vide) |
| `CLAUDE_MODEL` | Modele Claude | `claude-sonnet-4-5-20250929` |
| `CLAUDE_MAX_TOKENS` | Tokens max par reponse | `1024` |
| `ENABLE_AI_FEATURES` | Activer les fonctionnalites IA | `True` |

---

## Fonctionnalites

### Briefings intelligents

Genere un resume contextuel avant un meeting avec un contact.

- **Acces** : Bouton "Briefing IA" dans le detail d'un contact
- **Contenu** : Resume, points cles, suivis en attente, suggestions
- **API** : `GET /api/claude/briefing/<contact_id>`

### Assistant conversationnel

Chat avec l'IA pour des questions sur vos contacts.

- **Acces** : Lien "Assistant" dans l'en-tete
- **Capacites** : Conseils relationnels, aide a la redaction, suggestions d'actions
- **API** : `POST /api/claude/assistant` avec `{"question": "..."}`

### Suggestions dashboard

Suggestions proactives affichees sur la page d'accueil.

- **Acces** : Widget automatique sur le dashboard
- **Types** : follow_up, anniversaire, networking, relance
- **API** : `GET /api/claude/suggestions`

---

## Routes API

| Route | Methode | Description |
|-------|---------|-------------|
| `/api/claude/test` | GET | Teste la connexion API |
| `/api/claude/settings` | POST | Met a jour les parametres |
| `/api/claude/briefing/<id>` | GET | Genere un briefing IA |
| `/api/claude/assistant` | POST | Assistant conversationnel |
| `/api/claude/suggestions` | GET | Suggestions dashboard |
| `/settings` | GET | Page de parametres |
| `/assistant` | GET | Page de l'assistant |

---

## Modeles disponibles

| Modele | Usage | Vitesse | Cout |
|--------|-------|---------|------|
| Claude Sonnet 4.5 | Recommande pour usage quotidien | Rapide | Moyen |
| Claude Haiku 4.5 | Reponses rapides, suggestions | Tres rapide | Faible |
| Claude Opus 4.6 | Analyses approfondies | Lent | Eleve |

---

## Securite

- La cle API est stockee en memoire (session serveur), pas en base de donnees
- Elle peut aussi etre configuree via variable d'environnement (recommande en production)
- Les requetes a l'API Claude sont faites cote serveur uniquement
- Aucune donnee n'est envoyee a des tiers autres qu'Anthropic
