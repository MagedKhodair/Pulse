import asyncpg
from typing import Optional
import ssl

def pg_connection():
    return dict(
        user="app_api",
        password="api_123",
        host="pulse-psql.postgres.database.azure.com",
        port=5432,
        database="postgres",
        server_settings={'search_path': 'app_schema'},
        ssl=ssl.create_default_context()
        
    )

# Connection pool functions
connection_pool: Optional[asyncpg.Pool] = None

async def init_db():
    """Initialize database connection pool"""
    global connection_pool
    connection_pool = await asyncpg.create_pool(
        **pg_connection(),
        min_size=5,        
        max_size=20,    
        command_timeout=60
    )
    print("Database connection pool created")

async def close_db():
    """Close database connection pool"""
    global connection_pool
    if connection_pool:
        await connection_pool.close()
        print("Database connection pool closed")

async def get_db():
    """Get database connection from pool"""
    if not connection_pool:
        raise Exception("Database pool not initialized")
    return await connection_pool.acquire()

async def release_db(connection):
    """Release connection back to pool"""
    await connection_pool.release(connection)

# Database utility functions
async def execute_query(query: str, *args):
    """Execute a query and return results"""
    conn = await get_db()
    try:
        result = await conn.fetch(query, *args)
        return result
    finally:
        await release_db(conn)

async def execute_command(query: str, *args):
    """Execute a command (INSERT/UPDATE/DELETE)"""
    conn = await get_db()
    try:
        result = await conn.execute(query, *args)
        return result
    finally:
        await release_db(conn)

