import sqlite3
from datetime import datetime

DB_NAME = "registrations.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            preferred_language TEXT,
            sport_interest TEXT,
            organisation_name TEXT,
            contact_role TEXT,
            seminar_interest TEXT,
            source TEXT,
            notes TEXT,
            consent INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_missing_columns():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(registrations)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    new_columns = {
        "organisation_name": "TEXT",
        "contact_role": "TEXT",
        "seminar_interest": "TEXT",
        "source": "TEXT",
        "notes": "TEXT",
        "consent": "INTEGER DEFAULT 0"
    }

    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE registrations ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()


def save_registration(
    full_name,
    email,
    phone="",
    preferred_language="",
    sport_interest="",
    organisation_name="",
    contact_role="",
    seminar_interest="",
    source="",
    notes="",
    consent=False
):
    create_table()
    add_missing_columns()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registrations (
            full_name,
            email,
            phone,
            preferred_language,
            sport_interest,
            organisation_name,
            contact_role,
            seminar_interest,
            source,
            notes,
            consent,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name,
        email,
        phone,
        preferred_language,
        sport_interest,
        organisation_name,
        contact_role,
        seminar_interest,
        source,
        notes,
        1 if consent else 0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_registrations():
    create_table()
    add_missing_columns()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            preferred_language,
            sport_interest,
            organisation_name,
            contact_role,
            seminar_interest,
            source,
            notes,
            consent,
            created_at
        FROM registrations
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_registration(
    full_name,
    email,
    phone="",
    preferred_language="",
    sport_interest="",
    organisation_name="",
    contact_role="",
    seminar_interest="",
    source="Website",
    notes="",
    consent=False
):
    save_registration(
        full_name,
        email,
        phone,
        preferred_language,
        sport_interest,
        organisation_name,
        contact_role,
        seminar_interest,
        source,
        notes,
        consent
    )