import sqlite3
import os

# Absolute path to the directory where database.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "command_center.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        company TEXT,
        url TEXT,
        date_applied TEXT,
        status TEXT,
        followup_date TEXT,
        priority TEXT,
        resume_version TEXT,
        cover_letter_version TEXT,
        notes TEXT,
        contact_id INTEGER,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)
    );
    """)

    # Contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        department TEXT,
        role TEXT,
        linkedin TEXT,
        created_at TEXT
    );
    """)

    # Interaction logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id INTEGER,
        date TEXT,
        type TEXT,
        summary TEXT,
        next_action TEXT,
        next_action_date TEXT,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)
    );
    """)

    # Follow-ups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER,
        due_date TEXT,
        completed INTEGER,
        notes TEXT,
        FOREIGN KEY(application_id) REFERENCES applications(id)
    );
    """)

    # Agent state table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_run TEXT,
        status TEXT,
        missing_fields TEXT,
        overdue_items TEXT
    );
    """)

    conn.commit()
    conn.close()
