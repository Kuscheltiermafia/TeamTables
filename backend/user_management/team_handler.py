import asyncpg
from asyncpg import Connection

async def create_team(connection:Connection, team_name: str) -> int:


    team_id = await connection.fetchval(
        'INSERT INTO teams (team_name) VALUES ($1) RETURNING team_id',
        team_name
    )
    return team_id

async def get_team_by_id(connection:Connection, team_id: int):

    team = await connection.fetchrow(
        'SELECT * FROM teams WHERE team_id = $1',
        team_id
    )
    return team

async def get_team_by_name(connection:Connection, team_name: str):

    team = await connection.fetchrow(
        'SELECT * FROM teams WHERE team_name = $1',
        team_name
    )
    return team

async def delete_team(connection:Connection, team_id: int):

    await connection.execute(
        'DELETE FROM teams WHERE team_id = $1',
        team_id
    )