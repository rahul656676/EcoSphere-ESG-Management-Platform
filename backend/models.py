"""
EcoSphere - models.py
Lightweight data-access layer over SQLite (mirrors database/schema.sql).
No ORM is used so the schema.sql file remains the single source of truth.
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "ecosphere.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "database", "seed.sql")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(force=False):
    """Create the database from schema.sql (+ seed.sql) if it doesn't exist yet."""
    fresh = force or (not os.path.exists(DB_PATH))
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_db()
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()

    if fresh:
        with open(SEED_PATH, "r") as f:
            conn.executescript(f.read())
        conn.commit()

    conn.close()


def query(sql, params=(), one=False):
    conn = get_db()
    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    if one:
        return result[0] if result else None
    return result


def execute(sql, params=()):
    conn = get_db()
    cur = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def executemany(sql, seq_of_params):
    conn = get_db()
    conn.executemany(sql, seq_of_params)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Generic helpers used across controllers/routes
# ---------------------------------------------------------------------------

def table_all(table, order_by="id"):
    return query(f"SELECT * FROM {table} ORDER BY {order_by}")


def get_by_id(table, row_id):
    return query(f"SELECT * FROM {table} WHERE id = ?", (row_id,), one=True)


def insert_row(table, data: dict):
    cols = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    return execute(sql, tuple(data.values()))


def update_row(table, row_id, data: dict):
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    execute(sql, tuple(data.values()) + (row_id,))


def delete_row(table, row_id):
    execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
