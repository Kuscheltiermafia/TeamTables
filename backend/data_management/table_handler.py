from data_management.pool_handler import data_pool


async def create_table(table_name: str, schema: str):
    async with data_pool.acquire() as connection:
        existing_tables = await connection.fetch(f'''
            SELECT tablename FROM pg_tables WHERE schemaname = $1 AND tablename = $2
        ''', schema, table_name)
        if existing_tables:
            raise ValueError(f"Table {table_name} already exists in schema {schema}")

    async with data_pool.acquire() as connection:
        await connection.fetch(f'''
            SELECT schema_name FROM information_schema.schemata WHERE schema_name = $1
        ''', schema)
        if not existing_tables:
            raise ValueError(f"Schema {schema} does not exist")

    async with data_pool.acquire() as connection:
        await connection.execute(f'CREATE TABLE "{schema}".{table_name} (id SERIAL PRIMARY KEY)')