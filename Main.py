from backend.data_management.pool_handler import init_data_pool
from backend.user_management.pool_handler import init_user_pool

async def main():
    await init_data_pool()
    await init_user_pool()

if __name__ == '__main__':
    main()