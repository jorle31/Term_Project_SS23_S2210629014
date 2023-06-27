"""
File that contains the database connector class.
"""
import sqlite3
from typing import List, Tuple


class DatabaseConnector():

    def __init__(self, dbname: str) -> None:
        self.dbname = dbname
        self.conn = None
        self.c = None

    def open(self) -> None:
        self.conn = sqlite3.connect(f"db/{self.dbname}")
        self.c = self.conn.cursor()

    def close(self) -> None:
        if self.c:
            self.c.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
        self.c = None
        self.conn = None

    def create_table(self, tablename: str, columns: List[Tuple[str, str]]) -> None:
        column_str = ", ".join([f"{col[0]} {col[1]}" for col in columns])
        self.c.execute(f"CREATE TABLE {tablename} ({column_str})")
