import asyncpg
from dotenv import load_dotenv
import os

if os.getenv('CI') is None:
    load_dotenv('.env.deployment')

# noinspection PyTypeChecker
user_pool : asyncpg.Pool = None

async def init_user_pool():

    print("Initializing user database pool...")

    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('USER_DB_NAME')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    global user_pool
    if user_pool is None:
        # noinspection PyUnresolvedReferences
        user_pool = await asyncpg.create_pool(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

    print("User database pool initialized.")

async def close_user_pool():
    global user_pool
    if user_pool is not None:
        await user_pool.close()
        user_pool = None