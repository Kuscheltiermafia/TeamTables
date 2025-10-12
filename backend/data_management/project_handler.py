from data_management.pool_handler import data_pool
from user_management.pool_handler import user_pool
import uuid


async def create_project(project_name: str, owner_id: int, team_id: int):
    session_id = uuid.uuid4()
    async with data_pool.acquire() as connection:
        await connection.execute("CREATE SCHEMA $1", session_id)

    async with user_pool.acquire() as connection:
        await connection.execute("INSERT INTO projects (project_id, project_name, owner_id, team_id) VALUES ($1, $2, $3, $4)", project_name, project_name, owner_id, team_id)


async def get_project_name(project_id: str) -> str | None:
    async with user_pool.acquire() as connection:
        result = await connection.fetchrow("SELECT project_name FROM projects WHERE project_id = $1", project_id)
        if result:
            return result['project_name']
        else:
            return None

async def get_team_projects(team_id: int):
    async with user_pool.acquire() as connection:
        results = await connection.fetch("SELECT project_id, project_name FROM projects WHERE team_id = $1", team_id)
        return results