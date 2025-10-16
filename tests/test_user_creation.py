import pytest

import backend.user_management.pool_handler

@pytest.mark.user_creation
@pytest.mark.asyncio
async def test_user_creation():
    await setup_user()

async def setup_user():

    await backend.user_management.pool_handler.init_user_pool()

    from backend.user_management.user_handler import create_user

    user_id = await create_user(userName="testuser", email="test.test@test.test", password="Test1234!", lastName="Test", firstName="User")
    assert user_id is not None