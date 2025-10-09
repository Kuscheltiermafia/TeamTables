import asyncpg
import asyncio


async def setup_databases():
    #Connect to the PostgreSQL server
    setup_db_conn = await asyncpg.connect(host='localhost', port=5432)

    #Create 'users' database
    exists = await setup_db_conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", 'users'
    )
    if not exists:
        await setup_db_conn.execute("CREATE DATABASE users")

    #Create 'data' database
    exists = await setup_db_conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", 'data'
    )
    if not exists:
        await setup_db_conn.execute("CREATE DATABASE data")

    #Close connection to the PostgreSQL server
    await setup_db_conn.close()

    #Connect to the 'users' database
    conn = await asyncpg.connect(host='localhost', port=5432, database='users')

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
    await conn.execute('''
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'team_role') THEN
                            CREATE TYPE team_role AS ENUM ('admin', 'moderator', 'member');
                        END IF;
                    END$$;
                ''')

    # Create 'team_members' table
    #Etvl. Perms weiter ausarbeiten / ändern
    await conn.execute("""CREATE TABLE IF NOT EXISTS team_members(
                        user_id INT REFERENCES users (userID) ON DELETE CASCADE,
                        team_id INT REFERENCES teams (team_id) ON DELETE CASCADE,
                        role team_role NOT NULL DEFAULT 'member',
                        PRIMARY KEY (user_id, team_id)
                        )""")

    #Close the connection to the 'users' database
    await conn.close()

    #Insert data Database setup here

    #Projekt Perms irgendwo hier speichern, idk wie genau ich das machen werd

#Test Method
if __name__ == '__main__':
    asyncio.run(setup_databases())