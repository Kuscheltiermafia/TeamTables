import pytest
from backend.user_management.user_handler import create_user

@pytest.mark.user_creation
@pytest.mark.asyncio
async def test_setup_user(user_db_transaction):


    user_id = await create_user(user_connection=user_db_transaction, userName="testuser", email="test.test@test.test", password="Test1234!", lastName="Test", firstName="User")
    assert user_id is not None