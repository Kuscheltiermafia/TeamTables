import pytest
import asyncpg
import os

import pytest_asyncio
from dotenv import load_dotenv


@pytest_asyncio.fixture
async def data_db_pool():

    if os.getenv('CI') is None:
        load_dotenv('.env.deployment')

    pool = await asyncpg.create_pool(
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('DATA_DB_NAME'),
    )

    yield pool

    await pool.close()

@pytest_asyncio.fixture
async def data_db_transaction(data_db_pool):
    async with data_db_pool.acquire() as connection:
        async with connection.transaction():
            yield connection



@pytest_asyncio.fixture
async def user_db_pool():
    if os.getenv('CI') is None:
        load_dotenv('.env.deployment')

    pool = await asyncpg.create_pool(
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('USER_DB_NAME'),
    )

    yield pool

    await pool.close()

@pytest_asyncio.fixture
async def user_db_transaction(user_db_pool):
    async with user_db_pool.acquire() as connection:
        async with connection.transaction():
            yield connection