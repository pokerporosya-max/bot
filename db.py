import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()


# ---------------- INIT DB ----------------
def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        name TEXT DEFAULT 'Игрок',
        balance BIGINT DEFAULT 0,
        games INT DEFAULT 0,
        wins INT DEFAULT 0,
        loses INT DEFAULT 0,
        bonus_time BIGINT DEFAULT 0
    )
    """)


# ---------------- GET USER ----------------
def get_user(user_id, name=None):
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()

    # если нет пользователя → создаём
    if not user:
        cur.execute("""
            INSERT INTO users (user_id, name, balance, games, wins, loses, bonus_time)
            VALUES (%s, %s, 0, 0, 0, 0, 0)
        """, (user_id, name or "Игрок"))

        return get_user(user_id, name)

    # обновляем имя если оно пришло
    if name:
        cur.execute("""
            UPDATE users
            SET name=%s
            WHERE user_id=%s
        """, (name, user_id))

    return user


# ---------------- BALANCE ----------------
def update_balance(user_id, amount):
    cur.execute("""
        UPDATE users
        SET balance = balance + %s
        WHERE user_id=%s
    """, (amount, user_id))


# ---------------- GAME STATS ----------------
def update_game(user_id, win=False):
    cur.execute("""
        UPDATE users
        SET games = games + 1
        WHERE user_id=%s
    """, (user_id,))

    if win:
        cur.execute("""
            UPDATE users
            SET wins = wins + 1
            WHERE user_id=%s
        """, (user_id,))
    else:
        cur.execute("""
            UPDATE users
            SET loses = loses + 1
            WHERE user_id=%s
        """, (user_id,))


# ---------------- BONUS TIME ----------------
def set_bonus_time(user_id, t):
    cur.execute("""
        UPDATE users
        SET bonus_time=%s
        WHERE user_id=%s
    """, (t, user_id))


# ---------------- RESET DB ----------------
def reset_db():
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY")


# ---------------- TOP ----------------
def get_top(limit=10):
    cur.execute("""
        SELECT user_id, name, balance
        FROM users
        ORDER BY balance DESC
        LIMIT %s
    """, (limit,))
    return cur.fetchall()


# ---------------- RANK ----------------
def get_user_rank(user_id):
    cur.execute("""
        SELECT balance FROM users WHERE user_id=%s
    """, (user_id,))
    user = cur.fetchone()

    if not user:
        return 1

    cur.execute("""
        SELECT COUNT(*) + 1
        FROM users
        WHERE balance > %s
    """, (user[0],))

    return cur.fetchone()[0]
