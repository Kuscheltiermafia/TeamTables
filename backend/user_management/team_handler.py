import asyncpg
from backend.user_management.pool_handler import user_pool

async def create_team(team_name: str) -> int:

    async with user_pool.acquire() as conn:
        team_id = await conn.fetchval(
            'INSERT INTO teams (team_name) VALUES ($1) RETURNING team_id',
            team_name
        )
    return team_id

async def get_team_by_id(team_id: int):
    async with user_pool.acquire() as conn:
        team = await conn.fetchrow(
            'SELECT * FROM teams WHERE team_id = $1',
            team_id
        )
    return team

async def get_team_by_name(team_name: str):
    async with user_pool.acquire() as conn:
        team = await conn.fetchrow(
            'SELECT * FROM teams WHERE team_name = $1',
            team_name
        )
    return team

async def delete_team(team_id: int):
    async with user_pool.acquire() as conn:
        await conn.execute(
            'DELETE FROM teams WHERE team_id = $1',
            team_id
        )