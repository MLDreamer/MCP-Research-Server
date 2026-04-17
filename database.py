import sqlite3
from pathlib import Path

def init_db(db_path: Path):
    """Initialize SQLite with FTS5 for ranked retrieval."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT NOT NULL,
            content   TEXT NOT NULL,
            tags      TEXT DEFAULT '',
            created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts 
        USING fts5(title, content, tags, content='notes', content_rowid='id')
    """)
    conn.commit()
    conn.close()
