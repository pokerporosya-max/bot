import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 500,
    bottles INTEGER DEFAULT 5,
    cactus INTEGER DEFAULT 0,
    fap INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    record INTEGER DEFAULT 0,
    last_bonus INTEGER DEFAULT 0,
    last_water INTEGER DEFAULT 0
)
""")

conn.commit()


def get_user(uid):
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    return cur.fetchone()


def create_user(uid):
    if not get_user(uid):
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (uid,))
        conn.commit()


def update(uid, field, value):
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, uid))
    conn.commit()


def add(uid, field, value):
    cur.execute(f"UPDATE users SET {field} = {field} + ? WHERE user_id=?", (value, uid))
    conn.commit()
