import sqlite3

def init_db():
    conn = sqlite3.connect("support_pilot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_user(full_name, email, department, password):
    try:
        conn = sqlite3.connect("support_pilot.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, department, password) VALUES (?, ?, ?, ?)",
            (full_name, email, department, password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(email, password):
    conn = sqlite3.connect("support_pilot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, email FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user