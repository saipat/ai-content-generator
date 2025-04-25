import sqlite3
from datetime import datetime
import csv


DB_FILE = "history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_type TEXT,
        tone TEXT,
        input_text TEXT,
        output_text TEXT,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

def save_to_db(content_type, tone, input_text, output_text):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (content_type, tone, input_text, output_text, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (content_type, tone, input_text, output_text, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_last_n_entries(n=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT content_type, tone, input_text, output_text, created_at
        FROM history ORDER BY id DESC LIMIT ?
    ''', (n,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_total_count():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM history")
    count = c.fetchone()[0]
    conn.close()
    return count

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()
    conn.close()

def export_history_csv(file_path="exported_history.csv"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    headers = ["id", "content_type", "tone", "input_text", "output_text", "created_at"]
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return file_path