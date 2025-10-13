import os

import asyncpg
import asyncio

from dotenv import load_dotenv


async def setup_databases():
    #Load environment variables from .env.deployment file if not in CI environment
    if os.getenv('CI') is None:
        load_dotenv('.env.deployment')

    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    user_db_name = os.getenv('USER_DB_NAME')
    data_db_name = os.getenv('DATA_DB_NAME')
    #Connect to the PostgreSQL server
    setup_db_conn = await asyncpg.connect(host=host, port=port, user=user, password=password)

    #Create 'users' database
    exists = await setup_db_conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", user_db_name
    )
    if not exists:
        await setup_db_conn.execute(f'CREATE DATABASE "{user_db_name}"')

    #Create 'data' database
    exists = await setup_db_conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", data_db_name
    )
    if not exists:
        await setup_db_conn.execute(f'CREATE DATABASE "{data_db_name}"')

    #Close connection to the PostgreSQL server
    await setup_db_conn.close()

    await asyncio.sleep(1)  #Wait a moment to ensure the database is created before connecting

    #Connect to the 'users' database
    conn = await asyncpg.connect(host=host, port=port, database=user_db_name, user=user, password=password)

    #Create 'users' table
    await conn.execute("""CREATE TABLE IF NOT EXISTS users (
        userID    SERIAL NOT NULL PRIMARY KEY,
        userName  VARCHAR(25) NOT NULL UNIQUE,
        email     VARCHAR(50) NOT NULL,
        password  VARCHAR(100) NOT NULL UNIQUE,
        lastName  VARCHAR(50),
        firstName VARCHAR(50)
        )""")

    #Create 'teams' table
    await conn.execute("""CREATE TABLE IF NOT EXISTS teams (
        team_id SERIAL PRIMARY KEY,
        team_name VARCHAR(50) NOT NULL UNIQUE,
        token TEXT)""")

    # Creating 'team_role'
    await conn.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'team_role') THEN
                            CREATE TYPE team_role AS ENUM ('admin', 'moderator', 'member');
                        END IF;
                    END$$;
                """)

    # Create 'team_members' table
    #Etvl. Perms weiter ausarbeiten / ändern
    await conn.execute("""CREATE TABLE IF NOT EXISTS team_members(
        user_id INT REFERENCES users (userID) ON DELETE CASCADE,
        team_id INT REFERENCES teams (team_id) ON DELETE CASCADE,
        role team_role NOT NULL DEFAULT 'member',
        PRIMARY KEY (user_id, team_id)
        )""")

    #Create 'projects' table
    await conn.execute("""CREATE TABLE IF NOT EXISTS projects (
        project_id VARCHAR(36) PRIMARY KEY,
        project_name VARCHAR(50) NOT NULL,
        owner_id INT REFERENCES users (userID) ON DELETE SET NULL,
        team_id INT REFERENCES teams (team_id) ON DELETE SET NULL
        )""")

    #Close the connection to the 'users' database
    await conn.close()

    #Insert data Database setup here

    #Projekt Perms irgendwo hier speichern, idk wie genau ich dies machen werd

#Test Method
if __name__ == '__main__':
    asyncio.run(setup_databases())