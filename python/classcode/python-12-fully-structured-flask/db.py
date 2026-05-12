"""
PDBC (Python Database Connectivity) Layer
Manages database connections
"""
import sqlite3
from typing import ContextManager
from contextlib import contextmanager


def get_connection() -> sqlite3.Connection:
    """Get a database connection"""
    conn = sqlite3.connect('jolt.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


@contextmanager
def get_connection_context() -> ContextManager[sqlite3.Connection]:
    """Context manager for database connections (auto-closes)"""
    conn = sqlite3.connect('jolt.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
