from asyncpg import Connection
import uuid


async def create_project(connection:Connection, project_name: str, owner_id: int, team_id: int):
    session_id = uuid.uuid4()

    await connection.execute(f'CREATE SCHEMA "{session_id}"')


    await connection.execute('INSERT INTO projects (project_id, project_name, owner_id, team_id) VALUES ($1, $2, $3, $4)', project_name, project_name, owner_id, team_id)


async def get_project_name(connection:Connection, project_id: str) -> str | None:

    result = await connection.fetchrow('SELECT project_name FROM projects WHERE project_id = $1', project_id)
    if result:
        return result['project_name']
    else:
        return None

async def get_team_projects(connection:Connection, team_id: int):
    results = await connection.fetch('SELECT project_id, project_name FROM projects WHERE team_id = $1', team_id)
    return results