# Persistent SQLite-backed conversation memory
# - Uses sqlite3 (stdlib, no new deps)
# - Schema: sessions(id INTEGER PK, session_id TEXT, query TEXT, answer TEXT, timestamp TEXT)

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "conversations.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            query TEXT,
            answer TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_turn(session_id, query, answer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO sessions (session_id, query, answer, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (str(session_id), str(query), str(answer), timestamp))
    conn.commit()
    conn.close()

def get_history(session_id, last_n=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT query, answer FROM sessions
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (session_id, last_n))
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse to get chronological order
    history = [{"query": row[0], "answer": row[1]} for row in reversed(rows)]
    return history

def clear_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM sessions WHERE session_id = ?
    ''', (session_id,))
    conn.commit()
    conn.close()

# init_db() called on import
init_db()
