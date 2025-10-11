import asyncpg
from dotenv import load_dotenv
import os

load_dotenv('.env.deployment.data')

data_pool = None

async def init_data_pool():

    host = os.getenv('DATA_DB_HOST')
    port = os.getenv('DATA_DB_PORT')
    database = os.getenv('DATA_DB_NAME')
    user = os.getenv('DATA_DB_USER')
    password = os.getenv('DATA_DB_PASSWORD')

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
