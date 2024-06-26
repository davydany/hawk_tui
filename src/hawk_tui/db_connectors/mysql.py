import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Union, Tuple

from hawk_tui.db_connectors.base import BaseConnection

class MySQLConnection(BaseConnection):
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        super().__init__(host, port, username, password, database)

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database
        )

    def is_connected(self) -> bool:
        return self.connection.is_connected() if self.connection else False

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def execute_command(self, command: str, params: tuple = None) -> int:
        cursor = self.connection.cursor()
        try:
            cursor.execute(command, params)
            self.connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    # Create
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute_command(query, tuple(data.values()))

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
        query = "SHOW TABLES"
        return [list(row.values())[0] for row in self.execute_query(query)]

    def describe_table(self, table: str) -> List[Dict[str, Any]]:
        query = f"DESCRIBE {table}"
        return self.execute_query(query)

    def execute_transaction(self, commands: List[Tuple[str, tuple]]) -> bool:
        try:
            self.connection.start_transaction()
            cursor = self.connection.cursor()
            for command, params in commands:
                cursor.execute(command, params)
            self.connection.commit()
            return True
        except Error:
            self.connection.rollback()
            return False
        finally:
            cursor.close()