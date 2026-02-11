"""
database.py - Gestion de la base de donnees SQLite pour le CRM personnel.

Ce fichier contient toutes les fonctions pour interagir avec la base de donnees :
- Creation des tables
- Ajout, modification, suppression de contacts
- Recherche de contacts
- Gestion des notes
"""

import sqlite3
import json
import os
from datetime import datetime


def _get_db_path():
    """Retourne le chemin de la base de donnees depuis la config ou le defaut."""
    return os.environ.get('DATABASE_PATH', os.path.join('data', 'crm.db'))


def get_connection():
    """Cree et retourne une connexion a la base de donnees SQLite."""
    db_path = _get_db_path()
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialise la base de donnees en creant la table 'contacts'."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT DEFAULT '',
            categorie TEXT DEFAULT 'autre',
            informations TEXT DEFAULT '{}',
            notes TEXT DEFAULT '[]',
            date_creation TEXT NOT NULL,
            date_modification TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_contacts_nom
        ON contacts(nom)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_contacts_categorie
        ON contacts(categorie)
    """)

    conn.commit()
    conn.close()
    print(f"[DB] Base de donnees initialisee : {_get_db_path()}")


def create_contact(nom, prenom="", categorie="autre", informations=None):
    """Cree un nouveau contact dans la base de donnees."""
    if informations is None:
        informations = {}

    maintenant = datetime.now().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacts (nom, prenom, categorie, informations, notes,
                              date_creation, date_modification)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nom,
        prenom,
        categorie.lower(),
        json.dumps(informations, ensure_ascii=False),
        json.dumps([]),
        maintenant,
        maintenant
    ))

    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"[DB] Contact cree : {prenom} {nom} (ID: {contact_id})")
    return get_contact(contact_id)


def get_contact(contact_id):
    """Recupere un contact par son ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return _row_to_dict(row)


def update_contact(contact_id, **kwargs):
    """Met a jour un contact existant."""
    contact = get_contact(contact_id)
    if contact is None:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    champs_autorises = ["nom", "prenom", "categorie", "informations"]
    updates = []
    values = []

    for champ, valeur in kwargs.items():
        if champ in champs_autorises:
            if champ == "informations":
                infos_existantes = contact["informations"]
                if isinstance(valeur, dict):
                    infos_existantes.update(valeur)
                    valeur = json.dumps(infos_existantes, ensure_ascii=False)
                else:
                    valeur = json.dumps(valeur, ensure_ascii=False)
            elif champ == "categorie":
                valeur = valeur.lower()
            updates.append(f"{champ} = ?")
            values.append(valeur)

    if not updates:
        conn.close()
        return contact

    updates.append("date_modification = ?")
    values.append(datetime.now().isoformat())

    values.append(contact_id)

    query = f"UPDATE contacts SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    print(f"[DB] Contact mis a jour (ID: {contact_id})")
    return get_contact(contact_id)


def delete_contact(contact_id):
    """Supprime un contact par son ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    supprime = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if supprime:
        print(f"[DB] Contact supprime (ID: {contact_id})")
    return supprime


def search_contacts(query=None, categorie=None):
    """Recherche des contacts par nom/prenom et/ou categorie."""
    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    values = []

    if query:
        conditions.append(
            "(nom LIKE ? OR prenom LIKE ? OR informations LIKE ?)"
        )
        motif = f"%{query}%"
        values.extend([motif, motif, motif])

    if categorie:
        conditions.append("categorie = ?")
        values.append(categorie.lower())

    sql = "SELECT * FROM contacts"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY nom, prenom"

    cursor.execute(sql, values)
    rows = cursor.fetchall()
    conn.close()

    return [_row_to_dict(row) for row in rows]


def get_all_contacts():
    """Recupere tous les contacts, tries par nom puis prenom."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts ORDER BY nom, prenom")
    rows = cursor.fetchall()
    conn.close()

    return [_row_to_dict(row) for row in rows]


def add_note(contact_id, contenu):
    """Ajoute une note chronologique a un contact."""
    contact = get_contact(contact_id)
    if contact is None:
        return None

    notes = contact["notes"]
    notes.append({
        "date": datetime.now().isoformat(),
        "contenu": contenu
    })

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE contacts
        SET notes = ?, date_modification = ?
        WHERE id = ?
    """, (
        json.dumps(notes, ensure_ascii=False),
        datetime.now().isoformat(),
        contact_id
    ))

    conn.commit()
    conn.close()

    print(f"[DB] Note ajoutee au contact (ID: {contact_id})")
    return get_contact(contact_id)


def _row_to_dict(row):
    """Convertit une ligne SQLite en dictionnaire Python."""
    return {
        "id": row["id"],
        "nom": row["nom"],
        "prenom": row["prenom"],
        "categorie": row["categorie"],
        "informations": json.loads(row["informations"]),
        "notes": json.loads(row["notes"]),
        "date_creation": row["date_creation"],
        "date_modification": row["date_modification"]
    }


if __name__ == "__main__":
    init_db()
    print("[DB] Base de donnees prete !")
