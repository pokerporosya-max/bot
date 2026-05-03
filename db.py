import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        name TEXT,
        balance BIGINT DEFAULT 0,
        games INT DEFAULT 0,
        wins INT DEFAULT 0,
        loses INT DEFAULT 0,
        bonus_time BIGINT DEFAULT 0
    )
    """)

def get_user(user_id, name=None):
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()

    if not user:
        cur.execute(
            "INSERT INTO users (user_id, name) VALUES (%s, %s)",
            (user_id, name)
        )
        return get_user(user_id, name)

    return user

def update_balance(user_id, amount):
    cur.execute(
        "UPDATE users SET balance = balance + %s WHERE user_id=%s",
        (amount, user_id)
    )

def update_game(user_id, win=False):
    cur.execute("UPDATE users SET games = games + 1 WHERE user_id=%s", (user_id,))
    if win:
        cur.execute("UPDATE users SET wins = wins + 1 WHERE user_id=%s", (user_id,))
    else:
        cur.execute("UPDATE users SET loses = loses + 1 WHERE user_id=%s", (user_id,))

def set_bonus_time(user_id, t):
    cur.execute("UPDATE users SET bonus_time=%s WHERE user_id=%s", (t, user_id))

def reset_db():
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY")
