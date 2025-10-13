import asyncpg
import asyncio
import pytest
import os
from dotenv import load_dotenv

@pytest.mark.test_db
@pytest.mark.asyncio
async def test_projects():
    await db_connect()

async def db_connect():

    if os.getenv('CI') is None:
        load_dotenv('.env.test')

    host = os.getenv('TEST_DB_HOST')
    port = os.getenv('TEST_DB_PORT')
    database = os.getenv('TEST_DB_NAME')
    user = os.getenv('TEST_DB_USER')
    password = os.getenv('TEST_DB_PASSWORD')

    con = await asyncpg.connect(host=host, port=port, database=database, user=user, password=password)
    #await con.execute('DROP TABLE IF EXISTS testdb')

    await con.execute('CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name TEXT, age INT)')

    await con.execute('INSERT INTO test_table (name, age) VALUES ($1, $2)', "Alice", 22)
    await con.execute('INSERT INTO test_table (name, age) VALUES ($1, $2)', "Bob", 72)
    await con.execute('INSERT INTO test_table (name, age) VALUES ($1, $2)', "Deez", 69)

    types = await con.fetch('SELECT * FROM test_table')

    print(types)

    assert types[0]['name'] == "Alice"
    assert types[0]['age'] == 22
    assert types[1]['name'] == "Bob"
    assert types[1]['age'] == 72
    assert types[2]['name'] == "Deez"
    assert types[2]['age'] == 69

    await con.close()