import asyncpg
import asyncio

def test_db():
    asyncio.run(db_connect())

async def db_connect():
    #conDB = await asyncpg.connect(host='localhost', port=5432)
    #await conDB.execute("CREATE DATABASE testdb")

    #await conDB.close()

    con = await asyncpg.connect(host='localhost', port=5432, database='testdb')
    #await con.execute("DROP TABLE IF EXISTS testdb")

    await con.execute("""CREATE TABLE IF NOT EXISTS testdb (id SERIAL PRIMARY KEY, name TEXT, age INT)""")

    await con.execute("""INSERT INTO testdb (name, age) VALUES ('Alice', 22)""")
    await con.execute("""INSERT INTO testdb (name, age) VALUES ('Bob', 72)""")
    await con.execute("""INSERT INTO testdb (name, age) VALUES ('Deez', 69)""")

    types = await con.fetch('SELECT * FROM testdb')

    print(types)

    await con.close()