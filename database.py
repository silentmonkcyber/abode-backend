import sqlite3
from contextlib import contextmanager

DB_PATH = "abode_renovators.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            phone       TEXT,
            service     TEXT,
            message     TEXT,
            status      TEXT    NOT NULL DEFAULT 'pending',
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS testimonials (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT    NOT NULL,
            location    TEXT,
            rating      INTEGER NOT NULL DEFAULT 5,
            review      TEXT    NOT NULL,
            is_visible  INTEGER NOT NULL DEFAULT 1,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS portfolio (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            location    TEXT,
            category    TEXT,
            description TEXT,
            image_url   TEXT,
            is_featured INTEGER NOT NULL DEFAULT 0,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """)
    print("Database ready.")
