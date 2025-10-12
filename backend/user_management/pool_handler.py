import asyncpg
from dotenv import load_dotenv
import os

if os.getenv('CI') is None:
    load_dotenv('.env.deployment')

user_pool : asyncpg.Pool = None

async def init_user_pool():

    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('USER_DB_NAME')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    global user_pool
    if user_pool is None:
        async with asyncpg.create_pool(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        ) as pool:
            user_pool = pool

async def close_user_pool():
    global user_pool
    if user_pool is not None:
        await user_pool.close()
        user_pool = None