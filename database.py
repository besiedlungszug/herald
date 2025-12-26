import mysql.connector
import os

try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="herald",
        pool_size=os.getenv('HERALD_POOL_SIZE', 5),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 3306),
        database=os.getenv('DB_NAME', ''),
        user=os.getenv('DB_USER', ''),
        password=os.getenv('DB_PASSWORD', ''),
    )
except mysql.connector.Error as err:
    print(f"Error creating pool: {err}")

def connection():
    """Fetch a connection from the pool."""
    return pool.get_connection()
