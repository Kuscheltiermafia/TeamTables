import asyncpg
import asyncio
import bcrypt
from asyncpg import Connection

from backend.user_management.pool_handler import user_pool

# help functions

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# async functions

async def create_user(connection:Connection,  userName: str, email: str, password: str, lastName: str, firstName: str) -> int:
        
    if not all([userName, email, password]):
        raise ValueError("Username, email, and password cannot be empty.")

    existing_user = await connection.fetchrow('SELECT * FROM users WHERE userName = $1 OR email = $2', userName, email)
    if existing_user:
        raise ValueError("Username or email already exists.")

    hashed_pw = hash_password(password)

    user_id = await connection.fetchval(
        'INSERT INTO users (userName, email, password, lastName, firstName) VALUES ($1, $2, $3, $4, $5) RETURNING userID',
        userName, email, hashed_pw, lastName, firstName
    )
    return user_id

async def valid_password(connection:Connection, userKey: str, password: str) -> bool:

    if userKey is None or password is None:
        return False

    if "@" in userKey:
        user = await connection.fetchrow('SELECT * FROM users WHERE email = $1', userKey)
    else:
        user = await connection.fetchrow('SELECT * FROM users WHERE userName = $1', userKey)

    if user and verify_password(password, user['password']):
        return True
    return False