"""
Module de briefing pour le CRM Personnel.
Genere des briefings avant meetings avec extraction des infos cles.
"""

import json
from datetime import datetime
from typing import Dict, List


def get_contact_briefing(contact: Dict) -> Dict:
    """Genere un briefing complet pour un contact."""
    info = contact.get('informations', {})
    if isinstance(info, str):
        info = json.loads(info)

    notes = contact.get('notes', [])
    if isinstance(notes, str):
        notes = json.loads(notes)

    briefing = {
        'contact': {
            'id': contact.get('id'),
            'nom_complet': f"{contact.get('prenom', '')} {contact.get('nom', '')}".strip(),
            'prenom': contact.get('prenom', ''),
            'nom': contact.get('nom', ''),
            'categorie': contact.get('categorie', ''),
        },
        'contexte_pro': {
            'societe': info.get('societe', ''),
            'poste': info.get('poste', ''),
            'secteur': info.get('secteur', ''),
            'specialite': info.get('specialite', ''),
            'email': info.get('email', ''),
            'telephone': info.get('telephone', ''),
            'linkedin': info.get('linkedin', ''),
            'ville': info.get('ville', ''),
        },
        'vie_perso': info.get('vie_perso', {}),
        'sujets_conversation': info.get('sujets_conversation', []),
        'dernier_contact': info.get('dernier_contact', {}),
        'promesses_en_attente': _extract_promesses(notes),
        'a_suivre': info.get('dernier_contact', {}).get('a_suivre', []),
        'notes_recentes': _format_recent_notes(notes[-5:][::-1] if notes else []),
        'info_complementaire': info.get('info_complementaire', ''),
        'parcours': info.get('parcours', ''),
    }

    return briefing


def _extract_promesses(notes: List[Dict]) -> List[Dict]:
    """Extrait les promesses non tenues des notes."""
    promesses = []
    keywords = ['je devais', 'je dois', 'promis', 'a faire', 'todo', 'rappel',
                'je lui ai promis', 'je vais lui', "je m'engage"]

    for note in reversed(notes):
        contenu = note.get('contenu', '').lower()
        for keyword in keywords:
            if keyword in contenu:
                promesses.append({
                    'date': _format_date(note.get('date', '')),
                    'contenu': note.get('contenu', ''),
                })
                break

    return promesses[:5]


def _format_recent_notes(notes: List[Dict]) -> List[Dict]:
    """Formate les notes recentes pour affichage."""
    formatted = []
    for note in notes:
        formatted.append({
            'date': _format_date(note.get('date', '')),
            'contenu': note.get('contenu', ''),
        })
    return formatted


def _format_date(date_str: str) -> str:
    """Convertit une date ISO en format lisible DD/MM/YYYY."""
    if not date_str:
        return ''
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return date_str


def format_briefing_text(briefing: Dict) -> str:
    """Genere une version texte du briefing (pour terminal/API)."""
    lines = []
    c = briefing['contact']
    lines.append(f"=== BRIEFING : {c['nom_complet']} ===")
    lines.append(f"Categorie : {c['categorie']}")
    lines.append("")

    pro = briefing['contexte_pro']
    if any(pro.values()):
        lines.append("--- CONTEXTE PRO ---")
        if pro['societe']:
            lines.append(f"Societe : {pro['societe']}")
        if pro['poste']:
            lines.append(f"Poste : {pro['poste']}")
        if pro['ville']:
            lines.append(f"Ville : {pro['ville']}")
        if pro['telephone']:
            lines.append(f"Tel : {pro['telephone']}")
        if pro['email']:
            lines.append(f"Email : {pro['email']}")
        lines.append("")

    vie = briefing['vie_perso']
    if vie:
        lines.append("--- VIE PERSO ---")
        for k, v in vie.items():
            lines.append(f"  {k} : {v}")
        lines.append("")

    sujets = briefing['sujets_conversation']
    if sujets:
        lines.append("--- SUJETS DE CONVERSATION ---")
        for s in sujets:
            lines.append(f"  * {s}")
        lines.append("")

    dernier = briefing['dernier_contact']
    if dernier:
        lines.append("--- DERNIER CONTACT ---")
        for k, v in dernier.items():
            lines.append(f"  {k} : {v}")
        lines.append("")

    promesses = briefing['promesses_en_attente']
    if promesses:
        lines.append("--- PROMESSES EN ATTENTE ---")
        for p in promesses:
            lines.append(f"  [{p['date']}] {p['contenu']}")
        lines.append("")

    notes = briefing['notes_recentes']
    if notes:
        lines.append("--- NOTES RECENTES ---")
        for n in notes:
            lines.append(f"  [{n['date']}] {n['contenu']}")

    return "\n".join(lines)
