from asyncpg import Connection
import uuid


async def create_project(user_connection:Connection, data_connection:Connection, project_name: str, owner_id: int, team_id: int):
    project_id = str(uuid.uuid4())

    await data_connection.execute(f'CREATE SCHEMA "{project_id}"')
    await user_connection.execute('INSERT INTO projects (project_id, project_name, owner_id) VALUES ($1, $2, $3)', project_id, project_name, owner_id)
    return str(project_id)


async def get_project_name(user_connection:Connection, project_id: str) -> str | None:

    result = await user_connection.fetchrow('SELECT project_name FROM projects WHERE project_id = $1', project_id)
    if result:
        return result['project_name']
    else:
        return None