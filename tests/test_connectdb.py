import asyncpg
import asyncio
import pytest
import os
from dotenv import load_dotenv

@pytest.mark.test_db
def test_db():
    asyncio.run(db_connect())

async def db_connect():
    #conDB = await asyncpg.connect(host='localhost', port=5432)
    #await conDB.execute("CREATE DATABASE testdb")

    #await conDB.close()

    if os.getenv('CI') is None:
        load_dotenv('.env.test')

    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    con = await asyncpg.connect(host=host, port=port, database=database, user=user, password=password)
    #await con.execute("DROP TABLE IF EXISTS testdb")

    await con.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name TEXT, age INT)")

    await con.execute("INSERT INTO test_table (name, age) VALUES ('Alice', 22)")
    await con.execute("INSERT INTO test_table (name, age) VALUES ('Bob', 72)")
    await con.execute("INSERT INTO test_table (name, age) VALUES ('Deez', 69)")

    types = await con.fetch("SELECT * FROM test_table")

    assert types[0]['name'] == 'Alice'
    assert types[0]['age'] == 22
    assert types[1]['name'] == 'Bob'
    assert types[1]['age'] == 72
    assert types[2]['name'] == 'Deez'
    assert types[2]['age'] == 69

    print(types)

    await con.close()