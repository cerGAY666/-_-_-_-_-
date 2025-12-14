"""
Database connection pool and query execution.
"""
import psycopg2
from psycopg2 import pool
from typing import List, Tuple, Any
from src.core.config import config

class DatabaseConnection:
    """Manages database connections."""
    
    def __init__(self, min_connections: int = 1, max_connections: int = 10):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            min_connections,
            max_connections,
            config.DB_URI
        )
    
    def execute_query(self, query: str, params: tuple = None) -> List[Tuple[Any, ...]]:
        """Execute a query and return results."""
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                if query.strip().lower().startswith("select"):
                    return cur.fetchall()
                conn.commit()
                return []
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.connection_pool.putconn(conn)
    
    def close_all(self):
        """Close all connections in the pool."""
        self.connection_pool.closeall()
