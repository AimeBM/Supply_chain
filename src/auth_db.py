import os
import sqlite3
import bcrypt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('patron', 'manager')),
            first_login INTEGER NOT NULL DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# SECURITY
# -----------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

# -----------------------------
# AUTH
# -----------------------------
def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, first_name, last_name, username, email, password_hash, role, first_login
        FROM users WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row[5]):
        return {
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "username": row[3],
            "email": row[4],
            "role": row[6],
            "first_login": row[7]
        }
    return None

# -----------------------------
# USER MANAGEMENT
# -----------------------------
def create_user(first, last, username, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (first_name, last_name, username, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        first, last, username, email,
        hash_password(password), role
    ))
    conn.commit()
    conn.close()

def update_credentials(user_id, new_username, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET username = ?, password_hash = ?, first_login = 0
        WHERE id = ?
    """, (
        new_username,
        hash_password(new_password),
        user_id
    ))
    conn.commit()
    conn.close()

def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, first_name, last_name, username, email, role, first_login
        FROM users
        WHERE id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "username": row[3],
            "email": row[4],
            "role": row[5],
            "first_login": row[6]
        }
    return None
