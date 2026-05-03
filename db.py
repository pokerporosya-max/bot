import asyncpg
from config import DATABASE_URL

pool = None

# ---------------------------
# ИНИЦИАЛИЗАЦИЯ БД
# ---------------------------
async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,

            balance INT DEFAULT 1000,
            cactus INT DEFAULT 0,

            games INT DEFAULT 0,
            wins INT DEFAULT 0,
            loses INT DEFAULT 0
        )
        """)

# ---------------------------
# ПОЛЬЗОВАТЕЛЬ
# ---------------------------
async def add_user(user_id, username):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO users (user_id, username)
        VALUES ($1, $2)
        ON CONFLICT (user_id) DO NOTHING
        """, user_id, username)

async def get_user(user_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow("""
        SELECT * FROM users WHERE user_id=$1
        """, user_id)

# ---------------------------
# БАЛАНС
# ---------------------------
async def update_balance(user_id, amount):
    async with pool.acquire() as conn:
        await conn.execute("""
        UPDATE users
        SET balance = balance + $1
        WHERE user_id=$2
        """, amount, user_id)

# ---------------------------
# ИГРЫ
# ---------------------------
async def update_game(user_id, win: bool):
    async with pool.acquire() as conn:
        if win:
            await conn.execute("""
            UPDATE users
            SET wins = wins + 1,
                games = games + 1
            WHERE user_id=$1
            """, user_id)
        else:
            await conn.execute("""
            UPDATE users
            SET loses = loses + 1,
                games = games + 1
            WHERE user_id=$1
            """, user_id)

# ---------------------------
# КАКТУС
# ---------------------------
async def update_cactus(user_id, grow):
    async with pool.acquire() as conn:
        await conn.execute("""
        UPDATE users
        SET cactus = cactus + $1
        WHERE user_id=$2
        """, grow, user_id)
# ---------------------------
# ТОПЫ
# ---------------------------

async def top_balance():
    async with pool.acquire() as conn:
        return await conn.fetch("""
        SELECT username, balance
        FROM users
        ORDER BY balance DESC
        LIMIT 10
        """)

async def top_games():
    async with pool.acquire() as conn:
        return await conn.fetch("""
        SELECT username, games
        FROM users
        ORDER BY games DESC
        LIMIT 10
        """)

async def top_cactus():
    async with pool.acquire() as conn:
        return await conn.fetch("""
        SELECT username, cactus
        FROM users
        ORDER BY cactus DESC
        LIMIT 10
        """)
