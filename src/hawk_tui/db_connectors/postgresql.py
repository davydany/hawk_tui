import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Union, Tuple

from hawk_tui.db_connectors.base import BaseConnection

class PostgreSQLConnection(BaseConnection):
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        super().__init__(host, port, username, password, database)

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database
        )

    def is_connected(self) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except psycopg2.Error:
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_command(self, command: str, params: tuple = None) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(command, params)
            self.connection.commit()
            return cursor.rowcount

    # Create
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['%s'] * len(data))
        
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(placeholders)
        )
        
        return self.execute_command(query.as_string(self.connection), tuple(values))

    # Read
    def select(self, table: str, columns: List[str] = None, where: Dict[str, Any] = None, 
               order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        columns_str = "*" if columns is None else ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table}"
        
        params = []
        if where:
            conditions = []
            for key, value in where.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            query += " WHERE " + " AND ".join(conditions)
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query, tuple(params))

    # Update
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        set_items = [f"{key} = %s" for key in data.keys()]
        where_items = [f"{key} = %s" for key in where.keys()]
        
        query = f"UPDATE {table} SET {', '.join(set_items)} WHERE {' AND '.join(where_items)}"
        params = list(data.values()) + list(where.values())
        
        return self.execute_command(query, tuple(params))

    # Delete
    def delete(self, table: str, where: Dict[str, Any]) -> int:
        where_items = [f"{key} = %s" for key in where.keys()]
        query = f"DELETE FROM {table} WHERE {' AND '.join(where_items)}"
        
        return self.execute_command(query, tuple(where.values()))

    # Additional useful methods
    def list_tables(self) -> List[str]:
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        return [row['table_name'] for row in self.execute_query(query)]

    def describe_table(self, table: str) -> List[Dict[str, Any]]:
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
        """
        return self.execute_query(query, (table,))

    def execute_transaction(self, commands: List[Tuple[str, tuple]]) -> bool:
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    for command, params in commands:
                        cursor.execute(command, params)
            return True
        except psycopg2.Error:
            return False