"""
claude_integration.py - Integration de l'API Claude (Anthropic) dans le CRM.

Fournit des fonctionnalites IA :
- Test de connexion API
- Generation de briefings contextuels
- Assistant conversationnel
- Suggestions intelligentes pour le dashboard
"""

import json
from config import Config

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ClaudeIntegration:
    """Classe principale pour l'integration Claude API."""

    def __init__(self, api_key=None):
        self.api_key = api_key or Config.CLAUDE_API_KEY
        self.model = Config.CLAUDE_MODEL
        self.max_tokens = Config.CLAUDE_MAX_TOKENS
        self.client = None
        if self.api_key and ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def is_configured(self):
        """Verifie si l'API est configuree et disponible."""
        return bool(self.api_key and self.client)

    def update_api_key(self, new_key):
        """Met a jour la cle API dynamiquement."""
        self.api_key = new_key
        if new_key and ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=new_key)
        else:
            self.client = None

    def test_connection(self):
        """Teste la connexion a l'API Claude."""
        if not ANTHROPIC_AVAILABLE:
            return {
                "success": False,
                "message": "Le module 'anthropic' n'est pas installe. Executez: pip install anthropic"
            }

        if not self.api_key:
            return {
                "success": False,
                "message": "Cle API non configuree. Ajoutez-la dans les parametres."
            }

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{"role": "user", "content": "Reponds uniquement 'OK' pour confirmer la connexion."}]
            )
            return {
                "success": True,
                "message": "Connexion reussie !",
                "model": self.model
            }
        except anthropic.AuthenticationError:
            return {
                "success": False,
                "message": "Cle API invalide. Verifiez votre cle sur console.anthropic.com"
            }
        except anthropic.RateLimitError:
            return {
                "success": False,
                "message": "Limite de requetes atteinte. Reessayez dans quelques instants."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur de connexion: {str(e)}"
            }

    def generate_briefing(self, contact, master_profile=None):
        """Genere un briefing intelligent pour un contact."""
        if not self.is_configured():
            return {"success": False, "message": "API Claude non configuree"}

        # Construire le contexte du contact
        infos = contact.get("informations", {}) or {}
        notes = contact.get("notes", []) or []

        notes_text = ""
        if notes:
            recent_notes = notes[-10:]  # 10 dernieres notes
            notes_text = "\n".join(
                f"- [{n.get('date', 'N/A')}] {n.get('contenu', '')}"
                for n in recent_notes
            )

        master_context = ""
        if master_profile:
            master_infos = master_profile.get("informations", {}) or {}
            master_context = f"""
Profil de l'utilisateur (vous) :
- Nom: {master_profile.get('prenom', '')} {master_profile.get('nom', '')}
- Informations: {json.dumps(master_infos, ensure_ascii=False)}
"""

        prompt = f"""Tu es un assistant CRM personnel. Genere un briefing concis et utile pour preparer une rencontre avec ce contact.

{master_context}

Contact :
- Nom: {contact.get('prenom', '')} {contact.get('nom', '')}
- Categorie: {contact.get('categorie', 'autre')}
- Informations: {json.dumps(infos, ensure_ascii=False)}

Notes recentes :
{notes_text if notes_text else "Aucune note enregistree."}

Genere un briefing structure avec :
1. **Resume du contact** (qui est cette personne, relation)
2. **Points cles a aborder** (sujets de conversation pertinents)
3. **Promesses ou suivis en attente** (extraits des notes)
4. **Suggestions** (comment renforcer la relation)

Sois concis, pratique et bienveillant. Reponds en francais."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                "success": True,
                "briefing": response.content[0].text,
                "model": self.model
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur: {str(e)}"}

    def ask_assistant(self, question, contacts_context=None, master_profile=None):
        """Assistant conversationnel pour questions sur les contacts."""
        if not self.is_configured():
            return {"success": False, "message": "API Claude non configuree"}

        system_prompt = """Tu es un assistant CRM personnel intelligent. Tu aides l'utilisateur a gerer ses contacts et relations.
Tu peux :
- Repondre aux questions sur les contacts
- Donner des conseils relationnels
- Suggerer des actions (appeler, envoyer un message, planifier un meeting)
- Aider a rediger des messages

Sois concis, pratique et bienveillant. Reponds en francais."""

        context_parts = []
        if master_profile:
            master_infos = master_profile.get("informations", {}) or {}
            context_parts.append(
                f"Profil utilisateur: {master_profile.get('prenom', '')} {master_profile.get('nom', '')} - {json.dumps(master_infos, ensure_ascii=False)}"
            )

        if contacts_context:
            context_parts.append(f"Contexte contacts:\n{contacts_context}")

        user_message = question
        if context_parts:
            user_message = "\n\n".join(context_parts) + f"\n\nQuestion: {question}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return {
                "success": True,
                "response": response.content[0].text,
                "model": self.model
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur: {str(e)}"}

    def generate_dashboard_suggestions(self, contacts, master_profile=None):
        """Genere des suggestions proactives pour le dashboard."""
        if not self.is_configured():
            return {"success": False, "message": "API Claude non configuree"}

        if not contacts:
            return {"success": True, "suggestions": []}

        # Resumer les contacts pour le contexte (max 20)
        contacts_summary = []
        for c in contacts[:20]:
            infos = c.get("informations", {}) or {}
            notes = c.get("notes", []) or []
            last_note = notes[-1] if notes else None
            contacts_summary.append({
                "nom": f"{c.get('prenom', '')} {c.get('nom', '')}",
                "categorie": c.get("categorie", "autre"),
                "nb_notes": len(notes),
                "derniere_note": last_note.get("date", "") if last_note else "jamais",
                "infos_cles": {k: v for k, v in infos.items() if k in ["societe", "ville", "anniversaire"]}
            })

        prompt = f"""Analyse ces contacts CRM et genere 3-5 suggestions d'actions concretes.

Contacts :
{json.dumps(contacts_summary, ensure_ascii=False, indent=2)}

Pour chaque suggestion, donne :
- Un titre court (max 60 caracteres)
- Une description (1-2 phrases)
- Le type: "follow_up", "anniversaire", "networking", "relance"

Reponds UNIQUEMENT avec un JSON valide (array d'objets avec titre, description, type).
Pas de markdown, pas de texte avant ou apres le JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text.strip()
            # Extraire le JSON meme s'il est entoure de texte
            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                suggestions = json.loads(text[start:end])
            else:
                suggestions = []

            return {
                "success": True,
                "suggestions": suggestions
            }
        except json.JSONDecodeError:
            return {"success": True, "suggestions": []}
        except Exception as e:
            return {"success": False, "message": f"Erreur: {str(e)}"}
