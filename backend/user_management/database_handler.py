import asyncpg
import asyncio

async def create_table():
    #Connect to the PostgreSQL database
    conn = await asyncpg.connect(host='localhost', port=5432, database='users')
