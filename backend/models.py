"""
EcoSphere - models.py
Lightweight data-access layer. Supports both SQLite (default) and PostgreSQL.
No ORM is used so the schema.sql file remains the single source of truth.
"""

import os
import sqlite3
import re
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "ecosphere.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "database", "seed.sql")

DATABASE_URL = os.environ.get("DATABASE_URL", "")

IS_POSTGRES = DATABASE_URL.startswith("postgres")

if IS_POSTGRES:
    import psycopg2
    from psycopg2.extras import DictCursor


def get_db():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


def _adapt_sql(sql):
    """Adapt SQLite ? placeholders to PostgreSQL %s placeholders if needed."""
    if IS_POSTGRES:
        return sql.replace("?", "%s")
    return sql


def _get_cursor(conn):
    if IS_POSTGRES:
        return conn.cursor(cursor_factory=DictCursor)
    return conn.cursor()


def init_db(force=False):
    """Create the database from schema.sql (+ seed.sql) if it doesn't exist yet."""
    if IS_POSTGRES:
        logger.info("Skipping init_db for PostgreSQL (assume managed via migrations).")
        return

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
    sql = _adapt_sql(sql)
    conn = get_db()
    cur = _get_cursor(conn)
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    if one:
        return result[0] if result else None
    return result


def execute(sql, params=()):
    sql = _adapt_sql(sql)
    conn = get_db()
    cur = _get_cursor(conn)
    cur.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def executemany(sql, seq_of_params):
    sql = _adapt_sql(sql)
    conn = get_db()
    cur = _get_cursor(conn)
    cur.executemany(sql, seq_of_params)
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
    
    sql = _adapt_sql(sql)
    conn = get_db()
    cur = _get_cursor(conn)
    cur.execute(sql, tuple(data.values()))
    conn.commit()
    
    # Postgres doesn't easily return lastrowid without RETURNING, 
    # but for compatibility we'll try or return 0 for now
    last_id = 0
    if not IS_POSTGRES:
        last_id = cur.lastrowid
    
    conn.close()
    return last_id


def update_row(table, row_id, data: dict):
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    execute(sql, tuple(data.values()) + (row_id,))


def delete_row(table, row_id):
    execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
