import asyncpg
from dotenv import load_dotenv
import os

load_dotenv('.env.deployment.data')

user_pool = None

async def init_user_pool():

    host = os.getenv('DATA_DB_HOST')
    port = os.getenv('DATA_DB_PORT')
    database = os.getenv('DATA_DB_NAME')
    user = os.getenv('DATA_DB_USER')
    password = os.getenv('DATA_DB_PASSWORD')

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
