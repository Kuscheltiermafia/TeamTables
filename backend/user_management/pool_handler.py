import asyncpg
from dotenv import load_dotenv
import os
from typing import Optional

if os.getenv('CI') is None:
    load_dotenv('.env.deployment')

user_pool: Optional[asyncpg.Pool] = None

async def init_user_pool():
    print("Initializing user database pool...")

    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('USER_DB_NAME')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    global user_pool
    if user_pool is None:
        try:
            user_pool = await asyncpg.create_pool(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
            )
        except Exception as e:
            print(f"ERROR: Failed to initialize user database pool: {e}")
            raise
        
    print("User database pool initialized.")

def get_user_pool() -> asyncpg.Pool:
    if user_pool is None:
        raise RuntimeError("User database pool has not been initialized. Ensure init_user_pool() was called on startup.")
    return user_pool

async def close_user_pool():
    global user_pool
    if user_pool is not None:
        await user_pool.close()
        user_pool = None
        print("User database pool closed.")