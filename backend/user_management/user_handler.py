import asyncpg
import asyncio
import bcrypt

from backend.user_management.pool_handler import user_pool


async def create_user(userName: str, email: str, password: str, lastName: str, firstName: str):
    async with user_pool.acquire() as conn:
        #Correct Input
        if not all([userName, email, password]):
            raise ValueError("Username, email, and password cannot be empty.")

        #Unique username and email
        existing_user = await conn.fetchrow('SELECT * FROM users WHERE userName = $1 OR email = $2', userName, email)
        if existing_user:
            raise ValueError("Username or email already exists.")

        #hash password
        hashed_pw = hash_password(password)

        #Insert user into database
        user_id = await conn.fetchval(
            'INSERT INTO users (userName, email, password, lastName, firstName) VALUES ($1, $2, $3, $4, $5) RETURNING userID',
            userName, email, hashed_pw, lastName, firstName
        )
        return user_id

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def valid_password(userKey: str, password: str) -> bool:
    async with user_pool.acquire() as conn:
        if userKey is None or password is None:
            return False

        #Check if userKey is an email or username
        if "@" in userKey:
            user = await conn.fetchrow('SELECT * FROM users WHERE email = $1', userKey)
        else:
            user = await conn.fetchrow('SELECT * FROM users WHERE userName = $1', userKey)

        #Verify password
        if user and verify_password(password, user['password']):
            return True
        return False