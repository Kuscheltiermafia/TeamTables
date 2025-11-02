import pytest

from conftest import user_db_transaction
from backend.user_management.team_handler import create_team
from backend.data_management.project_handler import create_project, get_project_name, get_team_projects
from backend.user_management.user_handler import create_user


@pytest.mark.data_db
@pytest.mark.asyncio
async def test_setup_project(user_db_transaction, data_db_transaction):

    project_name = "Test Project"

    user_id = await create_user(
        user_connection=user_db_transaction,
        userName="project_tester",
        email="project@tester.com",
        password="securepassword",
        lastName="Tester",
        firstName="Project"
    )

    team_id = await create_team(user_connection=user_db_transaction, team_name= "Project Testers")

    project_id = await create_project(user_connection=user_db_transaction, data_connection=data_db_transaction, project_name=project_name, owner_id=user_id, team_id=team_id)
    print(f"Created project with ID: {project_id}")
    db_project_name = await get_project_name(user_connection=user_db_transaction, project_id=project_id)
    assert db_project_name == project_name
    assert await get_team_projects(user_connection=user_db_transaction ,team_id=team_id) == [(project_id, project_name)]