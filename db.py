import sqlite3
from datetime import datetime
import csv
from auth import init_user_db

DB_FILE = "history.db"

def init_all_databases():
    init_db()
    init_user_db()
    init_guest_tracking_db()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content_type TEXT,
            tone TEXT,
            input_text TEXT,
            output_text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_db(username, content_type, tone, input_text, output_text):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (username, content_type, tone, input_text, output_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, content_type, tone, input_text, output_text, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def get_last_n_entries(username, n=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT content_type, tone, input_text, output_text, created_at
        FROM history WHERE username = ? ORDER BY id DESC LIMIT ?
    ''', (username, n))
    rows = c.fetchall()
    conn.close()
    return rows


def get_total_count(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM history where username=?", (username,))
    count = c.fetchone()[0]
    conn.close()
    return count

def delete_old_guest_entries(hours=1):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        DELETE FROM history
        WHERE username = 'guest'
        AND datetime(created_at) <= datetime('now', ?)
    ''', (f'-{hours} hours',))
    conn.commit()
    conn.close()

def init_guest_tracking_db():
    conn = sqlite3.connect("guests.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS guest_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id TEXT,
            converted INTEGER DEFAULT 0,  -- 0 = no, 1 = yes
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_guest_conversion_stats():
    conn = sqlite3.connect("guests.db")
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM guest_sessions')
    total_guests = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM guest_sessions WHERE converted = 1')
    converted_guests = c.fetchone()[0]

    conn.close()
    return total_guests, converted_guests
