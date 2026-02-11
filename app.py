"""
app.py - API REST Flask pour le CRM personnel.

Ce fichier cree un serveur web (API) qui permet de gerer les contacts
via des requetes HTTP. C'est le point d'entree principal du backend.

Routes disponibles :
- GET    /api/contacts          -> Liste tous les contacts
- POST   /api/contacts          -> Cree un nouveau contact
- GET    /api/contacts/<id>     -> Recupere un contact par ID
- PUT    /api/contacts/<id>     -> Met a jour un contact
- DELETE /api/contacts/<id>     -> Supprime un contact
- POST   /api/contacts/<id>/notes -> Ajoute une note a un contact
- GET    /api/search?q=...&categorie=... -> Recherche des contacts
"""

import os

from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, flash
from flask_cors import CORS
from config import config as app_config
from database import (
    init_db,
    create_contact,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_all_contacts,
    add_note,
)
from models import valider_contact, valider_note, ValidationError
from crm_briefing import get_contact_briefing, format_briefing_text
from onboarding import onboarding_bp, is_first_time_user, get_master_profile

# Creation de l'application Flask
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Charger la config
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(app_config.get(env, app_config['default']))
app_config.get(env, app_config['default']).init_app(app)

# Cle secrete pour les sessions
app.secret_key = app.config['SECRET_KEY']

# CORS : permet a l'interface web d'appeler l'API depuis un navigateur
CORS(app)

# Enregistrement du blueprint onboarding
app.register_blueprint(onboarding_bp)


@app.before_request
def check_onboarding():
    """
    Redirige vers l'onboarding si aucun profil master n'existe.
    Exclut les routes API, onboarding, static, et briefing.
    """
    path = request.path
    if (path.startswith('/onboarding') or
        path.startswith('/api/') or
        path.startswith('/static/') or
        path.startswith('/briefing')):
        return None
    from flask import session
    if session.get('skip_onboarding'):
        return None
    if is_first_time_user():
        return redirect('/onboarding/')


# --- Routes de l'API ---


@app.route("/api/contacts", methods=["GET"])
def route_get_all_contacts():
    """Liste tous les contacts."""
    contacts = get_all_contacts()
    return jsonify({"contacts": contacts, "total": len(contacts)})


@app.route("/api/contacts", methods=["POST"])
def route_create_contact():
    """Cree un nouveau contact."""
    data = request.get_json()

    if not data:
        return jsonify({"erreur": "Donnees JSON requises"}), 400

    try:
        valide = valider_contact(
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            categorie=data.get("categorie", "autre"),
            informations=data.get("informations")
        )

        contact = create_contact(
            nom=valide["nom"],
            prenom=valide["prenom"],
            categorie=valide["categorie"],
            informations=valide["informations"]
        )

        return jsonify({"contact": contact, "message": "Contact cree"}), 201

    except ValidationError as e:
        return jsonify({"erreur": str(e)}), 400


@app.route('/')
def index():
    """Sert la page principale du frontend."""
    return send_from_directory('static', 'index.html')


@app.route('/api/master-profile')
def api_master_profile():
    """Retourne le profil master de l'utilisateur."""
    profile = get_master_profile()
    if profile is None:
        return jsonify({"erreur": "Aucun profil master"}), 404
    return jsonify({"profile": profile})


# --- Routes Briefing ---


@app.route('/briefing/<int:contact_id>')
def route_briefing(contact_id):
    """Affiche le briefing HTML pour un contact."""
    contact = get_contact(contact_id)
    if contact is None:
        return jsonify({"erreur": f"Contact {contact_id} non trouve"}), 404
    briefing = get_contact_briefing(contact)
    return render_template('briefing.html', briefing=briefing)


@app.route('/api/briefing/<int:contact_id>')
def route_api_briefing(contact_id):
    """API JSON pour le briefing d'un contact."""
    contact = get_contact(contact_id)
    if contact is None:
        return jsonify({"erreur": f"Contact {contact_id} non trouve"}), 404
    briefing = get_contact_briefing(contact)
    return jsonify(briefing)


@app.route('/briefing-text/<int:contact_id>')
def route_briefing_text(contact_id):
    """Version texte brut du briefing."""
    contact = get_contact(contact_id)
    if contact is None:
        return f"Contact {contact_id} non trouve", 404
    briefing = get_contact_briefing(contact)
    return format_briefing_text(briefing), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/<path:path>')
def serve_static(path):
    """Sert les fichiers statiques du frontend."""
    if path.startswith(('onboarding', 'api/', 'briefing', 'static/')):
        return jsonify({"erreur": "Non trouve"}), 404
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')


@app.route("/api/contacts/<int:contact_id>", methods=["GET"])
def route_get_contact(contact_id):
    """Recupere un contact par son ID."""
    contact = get_contact(contact_id)
    if contact is None:
        return jsonify({"erreur": f"Contact {contact_id} non trouve"}), 404
    return jsonify({"contact": contact})


@app.route("/api/contacts/<int:contact_id>", methods=["PUT"])
def route_update_contact(contact_id):
    """Met a jour un contact existant."""
    data = request.get_json()

    if not data:
        return jsonify({"erreur": "Donnees JSON requises"}), 400

    existing = get_contact(contact_id)
    if existing is None:
        return jsonify({"erreur": f"Contact {contact_id} non trouve"}), 404

    try:
        valide = valider_contact(
            nom=data.get("nom", existing["nom"]),
            prenom=data.get("prenom", existing["prenom"]),
            categorie=data.get("categorie", existing["categorie"]),
            informations=data.get("informations", existing["informations"])
        )

        contact = update_contact(contact_id, **valide)
        return jsonify({"contact": contact, "message": "Contact mis a jour"})

    except ValidationError as e:
        return jsonify({"erreur": str(e)}), 400


@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def route_delete_contact(contact_id):
    """Supprime un contact."""
    if delete_contact(contact_id):
        return jsonify({"message": f"Contact {contact_id} supprime"})
    else:
        return jsonify({"erreur": f"Contact {contact_id} non trouve"}), 404


@app.route("/api/contacts/<int:contact_id>/notes", methods=["POST"])
def route_add_note(contact_id):
    """Ajoute une note a un contact."""
    data = request.get_json()

    if not data:
        return jsonify({"erreur": "Donnees JSON requises"}), 400

    try:
        contenu = valider_note(data.get("contenu", ""))
        contact = add_note(contact_id, contenu)

        if contact is None:
            return jsonify(
                {"erreur": f"Contact {contact_id} non trouve"}
            ), 404

        return jsonify({"contact": contact, "message": "Note ajoutee"}), 201

    except ValidationError as e:
        return jsonify({"erreur": str(e)}), 400


@app.route("/api/search", methods=["GET"])
def route_search_contacts():
    """Recherche des contacts."""
    query = request.args.get("q")
    categorie = request.args.get("categorie")
    contacts = search_contacts(query=query, categorie=categorie)
    return jsonify({"contacts": contacts, "total": len(contacts)})


@app.route("/api/health", methods=["GET"])
def health_check():
    """Verifie que le serveur fonctionne."""
    return jsonify({"status": "ok", "message": "CRM Personnel operationnel"})


# --- Demarrage du serveur ---

if __name__ == "__main__":
    init_db()

    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)

    print("=" * 50)
    print("  CRM Personnel - Backend Flask")
    print(f"  API disponible sur http://{host}:{port}")
    print("=" * 50)

    app.run(host=host, port=port, debug=debug)
