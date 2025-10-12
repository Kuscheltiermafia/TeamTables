import asyncio

import pytest

import backend.data_management.pool_handler
import backend.user_management.pool_handler
import backend.data_management.project_handler
from data_management.project_handler import create_project, get_project_name, get_team_projects

@pytest.mark.data_db
def test_projects():
    asyncio.run(setup_project())

async def setup_project():

    project_name = "Test Project"
    team_id = 1

    await backend.data_management.pool_handler.init_data_pool()
    await backend.user_management.pool_handler.init_user_pool()

    project_id = await create_project(project_name=project_name, owner_id=1, team_id=team_id)
    db_project_name = await get_project_name(project_id)
    assert db_project_name == project_name
    assert get_team_projects(team_id) == [(project_id, project_name)]