from asyncpg import Connection

async def create_table(data_connection:Connection, table_name: str, schema: str):

    existing_tables = await data_connection.fetch(f'''
        SELECT tablename FROM pg_tables WHERE schemaname = $1 AND tablename = $2
    ''', schema, table_name)
    if existing_tables:
        raise ValueError(f"Table {table_name} already exists in schema {schema}")


    await data_connection.fetch(f'''
        SELECT schema_name FROM information_schema.schemata WHERE schema_name = $1
    ''', schema)
    if not existing_tables:
        raise ValueError(f"Schema {schema} does not exist")


    await data_connection.execute(f'CREATE TABLE "{schema}".{table_name} (id SERIAL PRIMARY KEY)')