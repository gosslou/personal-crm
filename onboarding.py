"""
onboarding.py - Systeme d'onboarding pour les nouveaux utilisateurs du CRM.

Ce module gere le flux d'onboarding en 3 etapes :
1. Enrichissement du profil (nom, LinkedIn, recherche web)
2. Questions personnalisees (formation, hobbies, preferences)
3. Validation et creation du profil master dans la DB
"""

import re
import urllib.request
import urllib.parse
import urllib.error
from html import unescape

from flask import (
    Blueprint, request, redirect, url_for,
    render_template, session, flash, jsonify
)
from database import create_contact, get_connection, get_contact


onboarding_bp = Blueprint(
    'onboarding', __name__,
    template_folder='templates',
    url_prefix='/onboarding'
)


# --- Helpers ---


def is_first_time_user():
    """Verifie si un profil master existe deja dans la DB."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM contacts WHERE informations LIKE '%\"type\": \"profil_master\"%'"
    )
    row = cursor.fetchone()
    conn.close()
    return row is None


def get_master_profile():
    """Recupere le profil master depuis la DB."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM contacts WHERE informations LIKE '%\"type\": \"profil_master\"%'"
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    return get_contact(row["id"])


def _sanitize(text):
    """Nettoie un input texte."""
    if not text:
        return ""
    return text.strip()


def _validate_linkedin_url(url):
    """Valide qu'une URL ressemble a un profil LinkedIn."""
    if not url:
        return False
    pattern = r'^https?://(www\.)?linkedin\.com/in/[\w\-]+/?$'
    return bool(re.match(pattern, url))


def enrich_profile_from_web(first_name, last_name, company=None):
    """
    Tente d'enrichir un profil via une recherche web basique.
    Utilise DuckDuckGo HTML pour extraire des infos publiques.
    """
    profile = {
        "prenom": first_name,
        "nom": last_name,
        "entreprise": company or "",
        "poste": "",
        "secteur": "",
        "source": "recherche_web"
    }

    query_parts = [first_name, last_name]
    if company:
        query_parts.append(company)
    query_parts.append("LinkedIn")
    query = " ".join(query_parts)

    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; CRM-Onboarding/1.0)"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")

        snippets = re.findall(
            r'<a class="result__snippet"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )

        for snippet in snippets[:5]:
            clean = re.sub(r'<[^>]+>', '', snippet)
            clean = unescape(clean)

            poste_match = re.search(
                r'(?:^|\s|-|\u2013)\s*([A-Z][^.\u00b7\-]+?)(?:\s+(?:at|@|chez|[-\u2013])\s+)',
                clean
            )
            if poste_match and not profile["poste"]:
                profile["poste"] = poste_match.group(1).strip()

            if not profile["entreprise"]:
                ent_match = re.search(
                    r'(?:at|@|chez|[-\u2013])\s+([A-Z][^\.\-]+)',
                    clean
                )
                if ent_match:
                    profile["entreprise"] = ent_match.group(1).strip()

    except (urllib.error.URLError, TimeoutError, OSError):
        profile["source"] = "saisie_manuelle"

    return profile


def enrich_profile_from_linkedin_url(linkedin_url):
    """
    Tente d'extraire des infos depuis une URL LinkedIn publique
    via une recherche web.
    """
    profile = {
        "linkedin": linkedin_url,
        "prenom": "",
        "nom": "",
        "entreprise": "",
        "poste": "",
        "secteur": "",
        "source": "linkedin_url"
    }

    try:
        encoded_url = urllib.parse.quote_plus(linkedin_url)
        url = f"https://html.duckduckgo.com/html/?q={encoded_url}"

        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; CRM-Onboarding/1.0)"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")

        title_match = re.search(
            r'<a class="result__a"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1))
            title = unescape(title)
            parts = re.split(r'\s*[-\u2013|]\s*', title)
            if len(parts) >= 1:
                name_parts = parts[0].strip().split()
                if len(name_parts) >= 2:
                    profile["prenom"] = name_parts[0]
                    profile["nom"] = " ".join(name_parts[1:])
                elif len(name_parts) == 1:
                    profile["nom"] = name_parts[0]
            if len(parts) >= 2:
                profile["poste"] = parts[1].strip()
            if len(parts) >= 3:
                entreprise = parts[2].strip()
                if "LinkedIn" not in entreprise:
                    profile["entreprise"] = entreprise

    except (urllib.error.URLError, TimeoutError, OSError):
        slug_match = re.search(r'linkedin\.com/in/([\w\-]+)', linkedin_url)
        if slug_match:
            slug = slug_match.group(1).replace('-', ' ').title()
            parts = slug.split()
            if len(parts) >= 2:
                profile["prenom"] = parts[0]
                profile["nom"] = " ".join(parts[1:])

    return profile


def create_master_profile(profile_data):
    """Cree le contact profil master dans la DB."""
    informations = {
        "type": "profil_master",
        "poste": profile_data.get("poste", ""),
        "societe": profile_data.get("entreprise", ""),
        "secteur": profile_data.get("secteur", ""),
        "linkedin": profile_data.get("linkedin", ""),
        "formation": profile_data.get("formation", ""),
        "hobbies": profile_data.get("hobbies", []),
        "sport_details": profile_data.get("sport_details", ""),
        "style_communication": profile_data.get("style_communication", ""),
        "objectifs_crm": profile_data.get("objectifs_crm", []),
        "source_enrichissement": profile_data.get("source", "manuel"),
    }

    contact = create_contact(
        nom=profile_data.get("nom", ""),
        prenom=profile_data.get("prenom", ""),
        categorie="autre",
        informations=informations
    )

    return contact


# --- Routes ---


@onboarding_bp.route('/')
def welcome():
    """Page d'accueil de l'onboarding."""
    if not is_first_time_user():
        return redirect('/')
    return render_template('onboarding/welcome.html')


@onboarding_bp.route('/step1', methods=['GET', 'POST'])
def step1():
    """Etape 1 : Enrichissement automatique du profil."""
    if not is_first_time_user():
        return redirect('/')

    if request.method == 'POST':
        linkedin_url = _sanitize(request.form.get('linkedin_url', ''))
        first_name = _sanitize(request.form.get('first_name', ''))
        last_name = _sanitize(request.form.get('last_name', ''))
        company = _sanitize(request.form.get('company', ''))

        if linkedin_url:
            if not _validate_linkedin_url(linkedin_url):
                flash("URL LinkedIn invalide. Utilisez le format : https://linkedin.com/in/votre-profil")
                return render_template('onboarding/step1.html')
            profile_data = enrich_profile_from_linkedin_url(linkedin_url)
        elif first_name and last_name:
            profile_data = enrich_profile_from_web(first_name, last_name, company)
        else:
            flash("Veuillez remplir au moins votre prenom et nom, ou fournir votre URL LinkedIn.")
            return render_template('onboarding/step1.html')

        session['temp_profile'] = profile_data
        return redirect(url_for('onboarding.step2'))

    return render_template('onboarding/step1.html')


@onboarding_bp.route('/step2', methods=['GET', 'POST'])
def step2():
    """Etape 2 : Questions personnalisees."""
    if not is_first_time_user():
        return redirect('/')

    profile = session.get('temp_profile')
    if not profile:
        return redirect(url_for('onboarding.step1'))

    if request.method == 'POST':
        profile['formation'] = _sanitize(request.form.get('formation', ''))
        profile['hobbies'] = request.form.getlist('hobbies')
        profile['sport_details'] = _sanitize(request.form.get('sport_details', ''))
        profile['style_communication'] = _sanitize(request.form.get('style_communication', ''))
        profile['objectifs_crm'] = request.form.getlist('objectifs_crm')

        session['temp_profile'] = profile
        return redirect(url_for('onboarding.step3'))

    return render_template('onboarding/step2.html', profile=profile)


@onboarding_bp.route('/step3', methods=['GET', 'POST'])
def step3():
    """Etape 3 : Validation et creation du profil."""
    if not is_first_time_user():
        return redirect('/')

    profile = session.get('temp_profile')
    if not profile:
        return redirect(url_for('onboarding.step1'))

    if request.method == 'POST':
        contact = create_master_profile(profile)
        session.pop('temp_profile', None)
        flash(f"Bienvenue {profile.get('prenom', '')} ! Votre profil est cree.")
        return redirect('/?first_time=true')

    return render_template('onboarding/step3.html', profile=profile)


@onboarding_bp.route('/skip')
def skip():
    """Permet de passer l'onboarding (lien 'Plus tard')."""
    session['skip_onboarding'] = True
    return redirect('/')
