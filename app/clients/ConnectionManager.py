import mysql.connector
import os
from mysql.connector import pooling
from dotenv import load_dotenv
load_dotenv()
class ConnectionManager:
    def __init__(self):
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }

        # Create a connection pool
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **self.db_config
        )

    # Get a connection
    def get_connection(self):
        return self.pool.get_connection()

    # Close the connection
    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()
