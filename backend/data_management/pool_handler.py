import asyncpg
from dotenv import load_dotenv
import os

if os.getenv('CI') is None:
    load_dotenv('.env.deployment')

data_pool : asyncpg.Pool = None

async def init_data_pool():

    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('DATA_DB_NAME')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    global data_pool
    if data_pool is None:
        async with asyncpg.create_pool(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        ) as pool:
            data_pool = pool

async def close_data_pool():
    global data_pool
    if data_pool is not None:
        await data_pool.close()
        data_pool = None